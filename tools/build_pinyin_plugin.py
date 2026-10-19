"""Rebuild the offline plugin from its vendored, checksum-verified sources."""

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "extensions/pinyin-initials"


def build():
    lock = json.loads((SOURCE / "vendor/manifest.json").read_text(encoding="utf-8"))
    for name, expected in lock["files"].items():
        if hashlib.sha256((SOURCE / "vendor" / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Vendored dependency checksum differs: {name}")
    library = (SOURCE / "vendor/pinyin-pro.js").read_text(encoding="utf-8")
    traditional = json.loads((SOURCE / "vendor/traditional.json").read_text(encoding="utf-8"))
    invocation = (SOURCE / "source.js").read_text(encoding="utf-8")
    data = library + "\npinyinPro.addTraditionalDict(" + json.dumps(traditional, ensure_ascii=False, separators=(",", ":")) + ");\n" + invocation
    (SOURCE / "main.js").write_bytes(data.encode("utf-8"))
    print(f"Built offline pinyin plugin ({len(data.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    build()
