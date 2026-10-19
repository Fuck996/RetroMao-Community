"""Shared authoring checks and deterministic archives for the public repository."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from jsonschema import Draft202012Validator
from PIL import Image

from validate_languages import unique_object

ROOT = Path(__file__).resolve().parents[1]
VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")
IGNORED = {".git", "node_modules", ".venv", "__pycache__", "dist", "reports"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def write_json(path, value):
    Path(path).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def schema_check(value, name):
    validator = Draft202012Validator(read_json(ROOT / "schemas" / f"{name}.schema.json"))
    errors = sorted(validator.iter_errors(value), key=lambda error: str(list(error.path)))
    if errors:
        error = errors[0]
        raise ValueError(f"{name}/{'.'.join(map(str, error.path))}: {error.message}")


def version(value):
    if not isinstance(value, str) or not VERSION.fullmatch(value):
        raise ValueError("Use a three-part numeric version")
    return tuple(map(int, value.split(".")))


def path_in(root, value):
    if not isinstance(value, str) or not value or any(part in ("", ".", "..") for part in value.split("/")) or any(char in value for char in "\\:\0"):
        raise ValueError(f"Invalid package path: {value!r}")
    path = Path(root) / value
    if path.is_symlink() or not path.resolve().is_relative_to(Path(root).resolve()):
        raise ValueError(f"Package path escapes its source: {value}")
    return path


def required_file(root, value, limit):
    path = path_in(root, value)
    if not path.is_file() or not 0 < path.stat().st_size <= limit:
        raise ValueError(f"Missing, empty or oversized package file: {value}")
    return path


def unique_ids(values, label):
    ids = [value["id"] for value in values]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Duplicate {label} ID")


def package_files(source):
    paths = []
    for path in sorted(Path(source).rglob("*")):
        relative = path.relative_to(source)
        if any(part in IGNORED for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Symbolic links are not allowed: {relative}")
        if not path.is_file() or path.name == "retromao-package.json":
            continue
        if path.name.startswith(".env") or path.suffix.lower() in {".jks", ".keystore", ".pem", ".key"}:
            raise ValueError(f"Private configuration must not be packaged: {relative}")
        path_in(source, relative.as_posix())
        paths.append(path)
    return paths


def archive_limits(source, max_files, max_bytes=64 * 1024 * 1024):
    files = package_files(source)
    if len(files) > max_files or sum(path.stat().st_size for path in files) > max_bytes:
        raise ValueError("Package exceeds host archive limits")
    return files


def validate_plugin(source):
    from build_script_plugin import validate_localizations
    manifest = read_json(required_file(source, "plugin.json", 1024 * 1024))
    schema_check(manifest, "plugin")
    validate_localizations(manifest)
    pages, actions, settings = (manifest.get(key, []) for key in ("pages", "actions", "settings"))
    providers = manifest.get("resourceProviders", [])
    minimum = version(manifest["minAppVersion"])
    if not (pages or actions or providers):
        raise ValueError("Declare a page, action or resource provider")
    if actions and not manifest.get("entryPoint"):
        raise ValueError("Actions require entryPoint")
    for values, label in ((pages, "page"), (actions, "action"), (settings, "setting"), (providers, "provider")):
        unique_ids(values, label)
    for key, suffix in (("entryPoint", ".js"), ("icon", None)):
        if key in manifest:
            file = required_file(source, manifest[key], 4 * 1024 * 1024)
            if suffix and file.suffix != suffix:
                raise ValueError(f"{key} requires a {suffix} file")
    for page in pages:
        if required_file(source, page["path"], 4 * 1024 * 1024).suffix != ".html":
            raise ValueError("Pages require HTML files")
        if page.get("kind", "BUSINESS") == "CONFIGURATION":
            if page["id"] != manifest.get("configurationPage") or minimum < (0, 9, 96):
                raise ValueError("Dedicated configuration pages require their entry and host 0.9.96")
    if "configurationPage" in manifest:
        config = next((page for page in pages if page["id"] == manifest["configurationPage"]), None)
        if config is None or minimum < (0, 9, 95):
            raise ValueError("configurationPage requires a declared page and host 0.9.95")
        if minimum >= (0, 9, 96) and config.get("kind") != "CONFIGURATION":
            raise ValueError("Declare a dedicated CONFIGURATION page")
        if config.get("kind") == "CONFIGURATION" and any(page.get("kind", "BUSINESS") == "BUSINESS" and page["path"] == config["path"] for page in pages):
            raise ValueError("Configuration and business pages cannot share an HTML file")
    capabilities = manifest.get("capabilities", [])
    if "NETWORK" in capabilities and not manifest.get("networkHosts"):
        raise ValueError("NETWORK requires networkHosts")
    for setting in settings:
        kind = setting.get("kind", "TEXT")
        default = setting.get("default", "false" if kind == "BOOLEAN" else "")
        options = setting.get("options", [])
        if kind == "CHOICE" and (not options or len({option["value"] for option in options}) != len(options)):
            raise ValueError(f"Invalid choices: {setting['id']}")
        if not default and setting.get("required"):
            continue
        if kind == "BOOLEAN" and default not in ("true", "false"):
            raise ValueError(f"Invalid boolean default: {setting['id']}")
        if kind == "NUMBER" and default:
            import math
            if not math.isfinite(float(default)):
                raise ValueError(f"Invalid numeric default: {setting['id']}")
        if kind == "CHOICE" and default not in {option["value"] for option in options}:
            raise ValueError(f"Invalid choice default: {setting['id']}")
    if providers and (minimum < (0, 9, 98) or "ROM_RESOURCES" not in capabilities or not manifest.get("entryPoint")):
        raise ValueError("Resource providers require entryPoint, ROM_RESOURCES and host 0.9.98")
    known_platforms = {row["id"] for row in read_json(ROOT / "contracts/host.json")["platforms"]}
    known_platforms.update(read_json(path)["platform"]["id"] for path in (ROOT / "extensions").glob("*/platform.json"))
    for provider in providers:
        if provider["platformId"] not in known_platforms:
            raise ValueError(f"Unknown provider platform: {provider['platformId']}; install and validate its platform package")
        if not any(setting["id"] == provider["directorySetting"] and setting.get("kind") == "DIRECTORY" for setting in settings):
            raise ValueError("Resource providers require a DIRECTORY setting")
        for path in provider.get("rootPaths", [""]):
            if path:
                path_in(source, path)
        path_in(source, provider["rootMarker"])
    archive_limits(source, 2048)
    return manifest


def validate_platform(source):
    manifest = read_json(required_file(source, "platform.json", 1024 * 1024))
    schema_check(manifest, "platform")
    platform = manifest["platform"]
    known = read_json(ROOT / "contracts/host.json")["platforms"]
    names = {name.lower() for row in known for name in [row["name"], *row["aliases"]]}
    if platform["id"] in {row["id"] for row in known} or any(name.lower() in names for name in [platform["name"], *platform["aliases"]]):
        raise ValueError("Platform ID, name or alias collides with a built-in platform")
    unique_ids(manifest.get("launchers", []), "launcher")
    for launcher in manifest.get("launchers", []):
        unique_ids(launcher.get("cores", []), "core")
    for value in manifest.get("assets", {}).values():
        path = required_file(source, value, 8 * 1024 * 1024)
        if path.suffix.lower() not in (".png", ".webp"):
            raise ValueError("Platform icons require PNG or WebP")
        with Image.open(path) as image:
            if image.format not in ("PNG", "WEBP") or not all(1 <= size <= 2048 for size in image.size):
                raise ValueError(f"Invalid platform icon: {value}")
            image.verify()
    archive_limits(source, 128)
    return manifest


def write_archive(source, target, files):
    target = Path(target)
    if target.resolve().is_relative_to(Path(source).resolve()):
        raise ValueError("Build output must be outside the package source")
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            entry = ZipInfo(path.relative_to(source).as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes(), compresslevel=9)
    content = target.read_bytes()
    return {"fileName": target.name, "sizeBytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
