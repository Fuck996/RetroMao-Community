"""Build the two introductory community packs and their catalogue."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
TAG = "packs-2026-10-06"


def font(size: int):
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def make_images() -> None:
    art = ROOT / "examples/amber/art"
    art.mkdir(parents=True, exist_ok=True)
    background = Image.new("RGB", (1280, 720))
    pixels = background.load()
    for y in range(720):
        for x in range(1280):
            glow = max(0, 1 - ((x - 1020) ** 2 / 1200000 + (y - 200) ** 2 / 550000))
            pixels[x, y] = (int(23 + 37 * glow), int(18 + 16 * glow), int(15 + 7 * glow))
    draw = ImageDraw.Draw(background)
    for x in range(0, 1280, 64):
        draw.line((x, 0, x, 720), fill="#30241B", width=1)
    for y in range(0, 720, 64):
        draw.line((0, y, 1280, y), fill="#30241B", width=1)
    background.save(art / "library.png", optimize=True)

    preview = background.copy()
    draw = ImageDraw.Draw(preview)
    draw.rectangle((0, 0, 1280, 106), fill="#241B15")
    draw.text((58, 52), "RetroMao", anchor="lm", font=font(47), fill="#F9B64D")
    for x, label in ((452, "LIBRARY"), (700, "RECENT"), (924, "FAVORITES")):
        draw.text((x, 55), label, anchor="lm", font=font(22), fill="#FFF1DB")
    draw.text((72, 176), "AMBER ARCADE", font=font(35), fill="#F9B64D")
    draw.text((72, 240), "Game collection", font=font(20), fill="#C8A785")
    draw.rounded_rectangle((67, 294, 318, 605), radius=15, fill="#281E17", outline="#6A4932", width=3)
    draw.text((92, 328), "SELECTED", font=font(24), fill="#FFF1DB")
    draw.text((92, 384), "A new adventure", font=font(21), fill="#F9B64D")
    draw.text((92, 426), "Artwork preview", font=font(18), fill="#C8A785")
    for index, color in enumerate(("#7C4536", "#415A56", "#6E5A3A", "#364E6E")):
        left = 380 + index * 212
        draw.rounded_rectangle((left, 235, left + 172, 487), radius=12, fill=color, outline="#F9B64D" if index == 0 else "#6A4932", width=4)
        draw.text((left + 86, 346), f"GAME {index + 1}", anchor="mm", font=font(24), fill="#FFF1DB")
        draw.text((left + 86, 516), f"Collection {index + 1}", anchor="mm", font=font(18), fill="#FFF1DB")
    draw.text((70, 665), "Style illustration · 1280 × 720", font=font(17), fill="#C8A785")
    previews = ROOT / "previews"
    previews.mkdir(exist_ok=True)
    preview.save(previews / "amber-arcade.png", optimize=True)


def make_package(name: str, paths: list[str]) -> dict[str, int | str]:
    DIST.mkdir(exist_ok=True)
    target = DIST / name
    with ZipFile(target, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for path in paths:
            archive.write(ROOT / path, Path(*Path(path).parts[2:]).as_posix())
    content = target.read_bytes()
    return {"fileName": name, "sizeBytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}


def main() -> None:
    from retromao import pack
    platform = pack(ROOT / "examples/msx", DIST, "msx-1.1.0")
    theme = make_package("theme-amber-1.0.0.zip", [
        "examples/amber/theme.json", "examples/amber/art/library.png"
    ])
    entries = [
        platform,
        {"kind": "THEME", "id": "amber-arcade", "name": "琥珀街机", "author": "RetroMao Community",
         "description": "暖色网格背景、琥珀色卡片与轻微焦点动效。", "version": "1.0.0",
         "minAppVersion": "0.9.44", "releaseTag": TAG, **theme,
         "previewPath": "previews/amber-arcade.png"},
    ]
    (DIST / "examples.catalog.json").write_text(json.dumps({"schemaVersion": 1, "entries": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
