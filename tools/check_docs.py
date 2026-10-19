"""Check public document coverage, executable examples and local links."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def fenced(text):
    return re.findall(r"```[^\n]*\n(.*?)```", text, re.S)


def check_docs():
    documents = [path for path in ROOT.rglob("*.md") if not any(part in {".git", ".venv", "node_modules", "dist", "reports", "work"} for part in path.relative_to(ROOT).parts)]
    parallel = {"README.md", "README.en.md", "README.ja.md"}
    readmes = [(ROOT / name).read_text(encoding="utf-8") for name in ("README.md", "README.en.md", "README.ja.md")]
    if not all(fenced(text) == fenced(readmes[0]) for text in readmes):
        raise ValueError("README commands differ between Chinese, English and Japanese")
    for path in documents:
        text = path.read_text(encoding="utf-8")
        if path.name not in parallel or path.parent != ROOT:
            sections = re.split(r"^## (?:中文|English|日本語)\s*$", text, flags=re.M)
            if len(sections) != 4:
                raise ValueError(f"Document needs 中文 / English / 日本語 sections: {path.relative_to(ROOT)}")
            if path.name != "CHANGELOG.md" and not all(fenced(section) == fenced(sections[1]) for section in sections[1:]):
                raise ValueError(f"Translated executable examples differ: {path.relative_to(ROOT)}")
        for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text):
            if target.startswith(("https://", "http://", "#", "mailto:")):
                continue
            target_path = target.split("#")[0]
            if target_path and not (path.parent / target_path).resolve().exists():
                raise ValueError(f"Broken document link: {path.relative_to(ROOT)} -> {target}")
        if "python community/" in text or "node --test community/" in text:
            raise ValueError(f"Main-repository command leaked into public guide: {path.relative_to(ROOT)}")
    print(f"Documents: {len(documents)} trilingual files checked")


if __name__ == "__main__":
    check_docs()
