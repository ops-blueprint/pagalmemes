#!/usr/bin/env python3
"""Render meme dicts (from fetch_memes.py) into punchy, centered text cards.

Visually distinct from the facts-project cards: bold centered text, solid
color-blocked background per category instead of a subtle gradient, built for
quick-read humor rather than dense fact text.
"""
import argparse
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
W, H = 1080, 1350

FONT_DIR = Path(__file__).resolve().parent / "fonts"
FONT_BLACK = FONT_DIR / "Anton-Regular.ttf"
FONT_BOLD = FONT_DIR / "Ubuntu-Bold.ttf"
FONT_REGULAR = FONT_DIR / "Ubuntu-Regular.ttf"

BG = (18, 18, 22)


def fit_text(draw, text, font_path, max_width, max_height, start_size=76, min_size=36):
    size = start_size
    while size >= min_size:
        font = ImageFont.truetype(str(font_path), size)
        all_lines = []
        for paragraph in text.split("\n"):
            avg_char_w = font.getlength("n")
            wrap_width = max(6, int(max_width / max(avg_char_w, 1)))
            all_lines.extend(textwrap.wrap(paragraph, width=wrap_width) or [""])
        line_height = font.getbbox("Ag")[3] + 16
        total_height = line_height * len(all_lines)
        if total_height <= max_height:
            return font, all_lines, line_height
        size -= 2
    font = ImageFont.truetype(str(font_path), min_size)
    all_lines = []
    for paragraph in text.split("\n"):
        wrap_width = max(6, int(max_width / max(font.getlength("n"), 1)))
        all_lines.extend(textwrap.wrap(paragraph, width=wrap_width) or [""])
    line_height = font.getbbox("Ag")[3] + 16
    return font, all_lines, line_height


def make_meme_card(meme, out_path, page_handle="@YourPage"):
    accent = tuple(meme["accent"])
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    margin = 80

    # top accent bar
    draw.rectangle([0, 0, W, 16], fill=accent)

    # category badge
    badge_font = ImageFont.truetype(str(FONT_BOLD), 34)
    badge_text = meme["label"]
    bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_w = (bbox[2] - bbox[0]) + 48
    badge_h = (bbox[3] - bbox[1]) + 28
    draw.rounded_rectangle([margin, 90, margin + badge_w, 90 + badge_h], radius=badge_h / 2, fill=accent)
    draw.text((margin + 24, 90 + 14 - bbox[1]), badge_text, font=badge_font, fill=(15, 15, 15))

    # Centered punchy text -- the meme itself
    area_top, area_bottom = 260, H - 180
    body_font, lines, line_height = fit_text(
        draw, meme["text"], FONT_BLACK,
        max_width=W - 2 * margin, max_height=area_bottom - area_top, start_size=84, min_size=40
    )
    block_height = line_height * len(lines)
    y = area_top + max(0, (area_bottom - area_top - block_height) // 2)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        line_w = bbox[2] - bbox[0]
        x = (W - line_w) / 2
        draw.text((x, y), line, font=body_font, fill=(255, 255, 255))
        y += line_height

    # Footer
    footer_font = ImageFont.truetype(str(FONT_BOLD), 34)
    cta_font = ImageFont.truetype(str(FONT_REGULAR), 30)
    draw.rectangle([0, H - 130, W, H], fill=(0, 0, 0))
    draw.text((margin, H - 100), page_handle, font=footer_font, fill=accent)
    draw.text((margin, H - 55), "Follow for daily memes", font=cta_font, fill=(220, 220, 220))

    img.save(out_path, quality=95)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Render meme cards from a memes JSON file")
    parser.add_argument("--memes", default=str(BASE_DIR / "memes_today.json"))
    parser.add_argument("--out-dir", default=str(BASE_DIR / "output"))
    parser.add_argument("--handle", default="@YourPage")
    args = parser.parse_args()

    memes = json.loads(Path(args.memes).read_text())
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, meme in enumerate(memes, start=1):
        out_path = out_dir / f"meme_{i}.png"
        make_meme_card(meme, out_path, page_handle=args.handle)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
