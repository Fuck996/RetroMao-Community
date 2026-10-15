"""Package one script plugin and emit its Release catalog entry without publishing it."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def build(source: Path, output: Path, release_tag: str) -> dict:
    manifest = json.loads((source / "plugin.json").read_text(encoding="utf-8"))
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
    entry = {key: manifest[key] for key in ("id", "name", "author", "description", "version", "minAppVersion")}
    entry.update(kind="SCRIPT", releaseTag=release_tag, fileName=name, sizeBytes=len(content), sha256=hashlib.sha256(content).hexdigest())
    if manifest.get("iconName"):
        entry["iconName"] = manifest["iconName"]
    (output / f"{manifest['id']}.catalog-entry.json").write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return entry


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "dist")
    parser.add_argument("--release-tag", required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.source.resolve(), args.output.resolve(), args.release_tag), ensure_ascii=False, indent=2))
