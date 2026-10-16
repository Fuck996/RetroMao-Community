"""Package one script plugin and emit its Release catalog entry without publishing it."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def validate_localizations(manifest: dict) -> None:
    default = manifest.get("defaultLocale")
    translations = manifest.get("localizations", {})
    tag = re.compile(r"[a-z]{2,3}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}|[0-9]{3}))?")
    if not isinstance(default, str) or not tag.fullmatch(default) or not isinstance(translations, dict):
        raise ValueError("Declare a valid defaultLocale and localizations object")
    if len(translations) > 31 or any(not tag.fullmatch(locale) for locale in translations) or default in translations:
        raise ValueError("Declare at most 31 additional locales; the base fields provide the default language")
    if default != "zh-Hans" and "zh-Hans" not in translations:
        raise ValueError("Published plugins must include Simplified Chinese (zh-Hans)")
    messages = manifest.get("messages", {})
    if not isinstance(messages, dict):
        raise ValueError("messages must be an object")
    minimum = manifest.get("minAppVersion", "")
    if translations or messages:
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", minimum) or tuple(map(int, minimum.split("."))) < (0, 9, 94):
            raise ValueError("Localized plugin metadata and ready.messages require minAppVersion 0.9.94 or later")
    base = {"name": manifest["name"], "description": manifest.get("description", ""),
            "pages": {page["id"]: page["title"] for page in manifest.get("pages", [])},
            "actions": {action["id"]: {"title": action["title"], "description": action.get("description", "")} for action in manifest.get("actions", [])},
            "settings": {setting["id"]: {"label": setting["label"], "options": {choice["value"]: choice["label"] for choice in setting.get("options", [])}} for setting in manifest.get("settings", [])},
            "messages": messages}
    for locale, text in [(default, base), *translations.items()]:
        if not isinstance(text, dict) or not isinstance(text.get("name"), str) or not text["name"].strip() or len(text["name"]) > 80:
            raise ValueError(f"{locale}: invalid plugin name")
        if not isinstance(text.get("description", ""), str) or len(text.get("description", "")) > 240:
            raise ValueError(f"{locale}: store description exceeds 240 characters")
        for field in ("pages", "actions", "settings", "messages"):
            value = text.get(field, {})
            if not isinstance(value, dict) or value.keys() != base[field].keys():
                raise ValueError(f"{locale}: {field} keys differ from the base language")
        if any(not isinstance(title, str) or not title.strip() for title in text.get("pages", {}).values()):
            raise ValueError(f"{locale}: missing page title")
        for action in text.get("actions", {}).values():
            if not isinstance(action.get("title"), str) or not action["title"].strip() or not isinstance(action.get("description", ""), str):
                raise ValueError(f"{locale}: invalid action text")
        for key, setting in text.get("settings", {}).items():
            if not isinstance(setting.get("label"), str) or not setting["label"].strip() or setting.get("options", {}).keys() != base["settings"][key]["options"].keys():
                raise ValueError(f"{locale}: invalid setting text or choice keys")
            if any(not isinstance(label, str) or not label.strip() for label in setting.get("options", {}).values()):
                raise ValueError(f"{locale}: missing choice label")
        values = text.get("messages", {})
        if len(values) > 1000 or any(not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9._-]{0,99}", key) or not isinstance(value, str) or len(value) > 16000 or "\0" in value for key, value in values.items()):
            raise ValueError(f"{locale}: invalid custom messages")
        if len(json.dumps(values, ensure_ascii=False).encode("utf-8")) > 256 * 1024:
            raise ValueError(f"{locale}: custom messages exceed 256 KiB")


def build(source: Path, output: Path, release_tag: str) -> dict:
    manifest = json.loads((source / "plugin.json").read_text(encoding="utf-8"))
    validate_localizations(manifest)
    configuration_page = manifest.get("configurationPage")
    pages = manifest.get("pages", [])
    minimum = tuple(map(int, manifest["minAppVersion"].split(".")))
    if any(page.get("kind", "BUSINESS") not in ("BUSINESS", "CONFIGURATION") for page in pages):
        raise ValueError("Invalid plugin page kind")
    if any(page.get("kind") == "CONFIGURATION" and (page["id"] != configuration_page or minimum < (0, 9, 96)) for page in pages):
        raise ValueError("Configuration pages require their declared entry and minAppVersion 0.9.96 or later")
    if configuration_page is not None:
        if not isinstance(configuration_page, str) or configuration_page not in {page["id"] for page in manifest.get("pages", [])}:
            raise ValueError("configurationPage must reference a declared page")
        if minimum < (0, 9, 95):
            raise ValueError("configurationPage requires minAppVersion 0.9.95 or later")
        config = next(page for page in pages if page["id"] == configuration_page)
        if minimum >= (0, 9, 96) and config.get("kind") != "CONFIGURATION":
            raise ValueError("Declare configurationPage as a dedicated CONFIGURATION page")
        if config.get("kind") == "CONFIGURATION" and any(page.get("kind", "BUSINESS") == "BUSINESS" and page["path"] == config["path"] for page in pages):
            raise ValueError("Configuration and business pages must use different files")
    output.mkdir(parents=True, exist_ok=True)
    name = f"plugin-{manifest['id']}-{manifest['version']}.zip"
    target = output / name
    files = sorted(path for path in source.rglob("*") if path.is_file())
    if any(path.is_symlink() for path in files):
        raise ValueError("Plugin packages must not contain symbolic links")
    with ZipFile(target, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, path.relative_to(source).as_posix())
    content = target.read_bytes()
    entry = {key: manifest[key] for key in ("id", "name", "author", "version", "minAppVersion")}
    entry["description"] = manifest.get("description", "")
    entry.update(kind="SCRIPT", releaseTag=release_tag, fileName=name, sizeBytes=len(content), sha256=hashlib.sha256(content).hexdigest())
    if manifest.get("iconName"):
        entry["iconName"] = manifest["iconName"]
    entry["defaultLocale"] = manifest["defaultLocale"]
    if manifest.get("localizations"):
        entry["localizations"] = {locale: {"name": text["name"], "description": text.get("description", "")} for locale, text in manifest["localizations"].items()}
    (output / f"{manifest['id']}.catalog-entry.json").write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return entry


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "dist")
    parser.add_argument("--release-tag", required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.source.resolve(), args.output.resolve(), args.release_tag), ensure_ascii=True, indent=2))
