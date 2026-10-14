"""Validate standalone community language files without application source."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


LOCALE = re.compile(r"[a-z]{2,3}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}|[0-9]{3}))?")
ARGUMENT = re.compile(r"%%|%([1-9][0-9]*)\$([sd])")
PROTECTED = ("ROM", "WebDAV", "RetroArch", "ScreenScraper", "SAF", "MD5", "SHA-256", "ETag", "Android",
             "3D", "2D", "PPSSPP", "DuckStation", "Dolphin", "Cemu", "Flycast", "Azahar", "Vita3K", "melonDS",
             "DraStic", "NooDS", "Citra MMJ", "OpenGL", "Vulkan", "UMD", "BIOS", "CPS", "PGM", "NAOMI", "HuCard")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    data = path.read_bytes()
    if b"\r" in data:
        raise ValueError(f"Language files must use LF line endings: {path.name}")
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object)


def catalog_hash(messages):
    text = json.dumps(messages, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def arguments(text):
    return Counter((match.group(1), match.group(2)) for match in ARGUMENT.finditer(text) if match.group(1))


def validate(root, require_complete=False, locale=None):
    root = Path(root)
    source = read_json(root / "zh-Hans.json")
    source_messages = source["messages"]
    if not source_messages or any(not isinstance(v, str) or not v.strip() for v in source_messages.values()):
        raise ValueError("Chinese source must contain every non-empty message")
    expected_hash = catalog_hash(source_messages)
    rows = []
    for path in sorted(root.glob("*.json")):
        if path.name == "index.json":
            continue
        pack = read_json(path)
        author = pack.get("author", "")
        credits = pack.get("credits", [])
        if not isinstance(author, str) or len(author) > 160 or not isinstance(credits, list) or len(credits) > 50 or any(not isinstance(credit, str) or not credit.strip() or len(credit) > 160 for credit in credits):
            raise ValueError(f"Invalid author credits: {path.name}")
        if pack.get("status") == "reviewed" and not author.strip():
            raise ValueError(f"Reviewed language needs an author: {path.name}")
        pack_locale = pack.get("locale")
        if not isinstance(pack_locale, str) or not LOCALE.fullmatch(pack_locale) or path.stem != pack_locale:
            raise ValueError(f"Invalid locale or filename: {path.name}")
        if pack.get("schema_version") != 1 or pack.get("catalog_hash") != expected_hash:
            raise ValueError(f"Incompatible catalog: {path.name}")
        if pack.get("catalog_version") != source["catalog_version"]:
            raise ValueError(f"Incompatible catalog version: {path.name}")
        if pack.get("status") not in {"source", "draft", "reviewed"}:
            raise ValueError(f"Invalid review status: {path.name}")
        if (pack_locale == "zh-Hans") != (pack["status"] == "source"):
            raise ValueError(f"Source status belongs to zh-Hans only: {path.name}")
        if not isinstance(pack.get("name"), str) or not pack["name"].strip():
            raise ValueError(f"Missing native language name: {path.name}")
        messages = pack["messages"]
        if set(messages) != set(source_messages):
            raise ValueError(f"Missing or unknown message keys: {path.name}")
        complete = 0
        require_this = require_complete and (locale is None or locale == pack_locale)
        for key, value in messages.items():
            if value is None:
                if pack["status"] != "draft" or require_this:
                    raise ValueError(f"Incomplete language: {path.name}/{key}")
                continue
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Empty or non-text translation: {path.name}/{key}")
            if arguments(value) != arguments(source_messages[key]):
                raise ValueError(f"Placeholder mismatch: {path.name}/{key}")
            for term in PROTECTED:
                pattern = r"(?<![A-Za-z0-9_])" + re.escape(term) + r"(?![A-Za-z0-9_])"
                if re.search(pattern, source_messages[key]) and not re.search(pattern, value):
                    raise ValueError(f"Protected term missing: {path.name}/{key}/{term}")
            complete += 1
        if require_this and pack_locale != "zh-Hans" and pack["status"] != "reviewed":
            raise ValueError(f"Language not reviewed: {path.name}")
        rows.append({"locale": pack_locale, "name": pack["name"], "file": path.name, "author": author,
                     "status": pack["status"], "translated": complete, "total": len(messages),
                     "size_bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    if locale is not None and not any(row["locale"] == locale for row in rows):
        raise ValueError(f"Requested language does not exist: {locale}")
    return {"schema_version": 1, "catalog_version": source["catalog_version"],
            "catalog_hash": expected_hash, "languages": rows}


def check_index(root, expected):
    if read_json(Path(root) / "index.json") != expected:
        raise ValueError("Language index does not match files; run --write-index and commit the updated index")


def write_index(root, index):
    data = (json.dumps(index, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    (Path(root) / "index.json").write_bytes(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--languages", type=Path, default=Path(__file__).resolve().parents[1] / "languages")
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--write-index", action="store_true")
    parser.add_argument("--locale", help="Apply the completion gate to one language")
    args = parser.parse_args()
    index = validate(args.languages, args.require_complete, args.locale)
    if args.write_index:
        write_index(args.languages, index)
    check_index(args.languages, index)
    for row in index["languages"]:
        print(f'{row["locale"]}: {row["translated"]}/{row["total"]} ({row["status"]})')


if __name__ == "__main__":
    main()
