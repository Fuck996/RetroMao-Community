"""RetroMao community CLI; see README.md / README.en.md / README.ja.md."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from extension_tools import ROOT, archive_limits, read_json, schema_check, validate_platform, validate_plugin, version, write_archive, write_json
import validate_languages


def scaffold(args):
    if args.kind == "language":
        if not validate_languages.LOCALE.fullmatch(args.id) or args.id == "zh-Hans":
            raise ValueError("Use a supported BCP 47 locale other than zh-Hans")
        target = ROOT / "languages" / f"{args.id}.json"
        if target.exists():
            raise ValueError(f"Already exists: {target}")
        pack = read_json(ROOT / "languages/zh-Hans.json")
        pack.update(locale=args.id, name=args.name, author=args.author, credits=[], status="draft",
                    messages=dict.fromkeys(pack["messages"]))
        write_json(target, pack)
        validate_languages.write_index(target.parent, validate_languages.validate(target.parent))
    else:
        target = ROOT / "extensions" / args.id
        if target.exists():
            raise ValueError(f"Already exists: {target}")
        if not re.fullmatch(r"[a-z][a-z0-9._-]{1,60}", args.id):
            raise ValueError("Use a lowercase extension ID")
        shutil.copytree(ROOT / "templates" / args.kind, target)
        if args.kind == "plugin":
            manifest = read_json(target / "plugin.json")
            manifest.update(id=args.id, name=args.name, author=args.author)
            write_json(target / "plugin.json", manifest)
        else:
            manifest = read_json(target / "platform.json")
            manifest["platform"].update(id=args.id, name=args.name, aliases=[args.id])
            write_json(target / "platform.json", manifest)
            metadata = read_json(target / "retromao-package.json")
            metadata.update(id=args.id, name=args.name, author=args.author)
            write_json(target / "retromao-package.json", metadata)
    print(target.relative_to(ROOT).as_posix())


def check_source(source):
    source = Path(source).resolve()
    if source.is_file():
        if source.suffix != ".json" or "messages" not in read_json(source):
            raise ValueError("Expected a language JSON file or package directory")
        result = validate_languages.validate(source.parent, locale=source.stem)
        validate_languages.check_index(source.parent, result)
        return "LANGUAGE", read_json(source)
    if (source / "plugin.json").is_file():
        return "SCRIPT", validate_plugin(source)
    if (source / "platform.json").is_file():
        manifest = validate_platform(source)
        metadata = read_json(source / "retromao-package.json")
        schema_check(metadata, "package")
        if metadata["kind"] != "PLATFORM" or metadata["id"] != manifest["platform"]["id"] or metadata["name"] != manifest["platform"]["name"]:
            raise ValueError("Platform package identity differs from its release metadata")
        if manifest.get("launchers") and version(metadata["minAppVersion"]) < (0, 9, 108):
            raise ValueError("Platform launchers require host 0.9.108 or a build containing that feature")
        return "PLATFORM", metadata
    raise ValueError("No plugin.json or platform.json at package root")


def pack(source, output, tag):
    if not re.fullmatch(r"[a-zA-Z0-9._-]{1,80}", tag):
        raise ValueError("Invalid Release tag")
    source, output = Path(source).resolve(), Path(output).resolve()
    kind, manifest = check_source(source)
    if kind == "LANGUAGE":
        validate_languages.validate(source.parent, require_complete=True, locale=source.stem)
        raise ValueError("Languages are published as JSON plus languages/index.json; do not ZIP them")
    if kind == "SCRIPT":
        from build_script_plugin import build
        entry = build(source, output, tag)
    else:
        entry = {key: manifest[key] for key in ("id", "name", "author", "description", "version", "minAppVersion")}
        target = output / f"platform-{entry['id']}-{entry['version']}.zip"
        entry.update(kind=kind, releaseTag=tag, **write_archive(source, target, archive_limits(source, 128)))
        if manifest.get("previewPath"):
            entry["previewPath"] = manifest["previewPath"]
        write_json(output / f"{entry['id']}.catalog-entry.json", entry)
    return entry


def command(*args, cwd=ROOT):
    result = subprocess.run(list(args), cwd=cwd, check=True, stdout=subprocess.PIPE, encoding="utf-8")
    return result.stdout.strip()


def publish(args):
    source = Path(args.source).resolve()
    source.relative_to(ROOT)
    if command("git", "status", "--porcelain"):
        raise ValueError("Commit source, documentation and index changes before publishing")
    head = command("git", "rev-parse", "HEAD")
    branch = command("git", "branch", "--show-current")
    origin = command("git", "remote", "get-url", "origin").removesuffix(".git")
    if origin not in (f"https://github.com/{args.repository}", f"git@github.com:{args.repository}"):
        raise ValueError("--repository must match this checkout's origin")
    remote = command("git", "ls-remote", "origin", f"refs/heads/{branch}").split()
    if not remote or remote[0] != head:
        raise ValueError("Push this exact source commit before publishing")
    entry = pack(source, ROOT / "dist", args.tag)
    index_path = ROOT / ("plugins/index.json" if entry["kind"] == "SCRIPT" else "catalog.json")
    index = read_json(index_path)
    prior = next((row for row in index["entries"] if row["id"] == entry["id"] and row["kind"] == entry["kind"]), None)
    if prior and version(entry["version"]) <= version(prior["version"]):
        raise ValueError("Published extension versions are immutable; increment version")
    archive = ROOT / "dist" / entry["fileName"]
    if not args.notes or not Path(args.notes).is_file():
        raise ValueError("Provide --notes with Chinese, English and Japanese release notes")
    notes = Path(args.notes).read_text(encoding="utf-8")
    if not all(marker in notes for marker in ("## 中文", "## English", "## 日本語")):
        raise ValueError("Release notes require 中文 / English / 日本語 sections")
    command("gh", "release", "create", args.tag, str(archive), "--repo", args.repository,
            "--target", head, "--title", f"{entry['id']} {entry['version']}", "--notes-file", args.notes)
    with tempfile.TemporaryDirectory(prefix="retromao-release-") as directory:
        command("gh", "release", "download", args.tag, "--repo", args.repository,
                "--pattern", entry["fileName"], "--dir", directory)
        import hashlib
        actual = (Path(directory) / entry["fileName"]).read_bytes()
        if len(actual) != entry["sizeBytes"] or hashlib.sha256(actual).hexdigest() != entry["sha256"]:
            raise ValueError("Published asset verification failed; index was not changed")
    index["entries"] = [row for row in index["entries"] if not (row["id"] == entry["id"] and row["kind"] == entry["kind"])] + [entry]
    write_json(index_path, index)
    print(f"Verified Release asset. Commit and push {index_path.relative_to(ROOT)} to expose it in the app.")


def check_repository():
    index = validate_languages.validate(ROOT / "languages")
    validate_languages.check_index(ROOT / "languages", index)
    for schema in (ROOT / "schemas").glob("*.json"):
        from jsonschema import Draft202012Validator
        Draft202012Validator.check_schema(read_json(schema))
    for folder in [ROOT / "templates", ROOT / "extensions"]:
        for manifest in sorted(folder.glob("*/plugin.json")):
            validate_plugin(manifest.parent)
        for manifest in sorted(folder.glob("*/platform.json")):
            check_source(manifest.parent)
    for folder in (ROOT / "examples").iterdir():
        if (folder / "plugin.json").exists() and (folder / read_json(folder / "plugin.json").get("entryPoint", "")).is_file():
            validate_plugin(folder)
        if (folder / "platform.json").exists():
            validate_platform(folder)
    from check_docs import check_docs
    check_docs()
    print(f"OK: {len(index['languages'])} languages, package templates, examples, schemas and trilingual documents")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("kind", choices=("plugin", "platform", "language"))
    init.add_argument("--id", required=True)
    init.add_argument("--name", required=True)
    init.add_argument("--author", required=True)
    check = commands.add_parser("check")
    check.add_argument("source", nargs="?")
    build = commands.add_parser("pack")
    build.add_argument("source")
    build.add_argument("--release-tag", required=True)
    build.add_argument("--output", type=Path, default=ROOT / "dist")
    preview = commands.add_parser("preview")
    preview.add_argument("source")
    preview.add_argument("--port", type=int, default=8765)
    preview.add_argument("--fixtures", type=Path, default=ROOT / "tools/preview/fixtures.json")
    release = commands.add_parser("publish")
    release.add_argument("source")
    release.add_argument("--tag", required=True)
    release.add_argument("--repository", required=True)
    release.add_argument("--notes", required=True)
    args = parser.parse_args()
    if args.command == "init":
        scaffold(args)
    elif args.command == "check":
        print(check_source(args.source)[0] + ": OK") if args.source else check_repository()
    elif args.command == "pack":
        print(json.dumps(pack(args.source, args.output, args.release_tag), ensure_ascii=True, indent=2))
    elif args.command == "preview":
        from preview import serve
        serve(Path(args.source), args.port, args.fixtures)
    elif args.command == "publish":
        publish(args)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
