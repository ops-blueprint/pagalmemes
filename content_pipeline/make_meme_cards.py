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


def draw_checkmark(draw, cx, cy, size, color, width=10):
    p1 = (cx - size * 0.5, cy)
    p2 = (cx - size * 0.15, cy + size * 0.4)
    p3 = (cx + size * 0.55, cy - size * 0.45)
    draw.line([p1, p2], fill=color, width=width)
    draw.line([p2, p3], fill=color, width=width)


def draw_x_mark(draw, cx, cy, size, color, width=10):
    half = size * 0.5
    draw.line([(cx - half, cy - half), (cx + half, cy + half)], fill=color, width=width)
    draw.line([(cx - half, cy + half), (cx + half, cy - half)], fill=color, width=width)


def make_split_card(top_text, bottom_text, out_path, page_handle="@YourPage",
                     top_label="EXPECTATION", bottom_label="REALITY",
                     top_color=(59, 130, 246), bottom_color=(239, 68, 68)):
    """Two-panel split format (e.g. Expectation vs Reality) -- fully original
    layout, drawn shapes only, no copyrighted characters or images."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    margin = 70
    mid_y = H // 2

    draw.rectangle([0, 0, W, mid_y], fill=(22, 26, 36))
    draw.rectangle([0, mid_y, W, H], fill=(30, 20, 22))
    draw.rectangle([0, mid_y - 4, W, mid_y + 4], fill=(10, 10, 12))

    label_font = ImageFont.truetype(str(FONT_BLACK), 52)
    draw.text((margin, 60), top_label, font=label_font, fill=top_color)
    draw.text((margin, mid_y + 60), bottom_label, font=label_font, fill=bottom_color)

    body_font_top, lines_top, lh_top = fit_text(
        draw, top_text, FONT_REGULAR, max_width=W - 2 * margin, max_height=mid_y - 220, start_size=56, min_size=30
    )
    y = 170
    for line in lines_top:
        draw.text((margin, y), line, font=body_font_top, fill=(235, 235, 235))
        y += lh_top

    body_font_bot, lines_bot, lh_bot = fit_text(
        draw, bottom_text, FONT_REGULAR, max_width=W - 2 * margin, max_height=mid_y - 220, start_size=56, min_size=30
    )
    y = mid_y + 170
    for line in lines_bot:
        draw.text((margin, y), line, font=body_font_bot, fill=(235, 235, 235))
        y += lh_bot

    footer_font = ImageFont.truetype(str(FONT_BOLD), 32)
    draw.text((margin, H - 55), page_handle, font=footer_font, fill=(210, 210, 210))

    img.save(out_path, quality=95)
    return out_path


def make_comparison_card(rejected_text, approved_text, out_path, page_handle="@YourPage"):
    """Two-row approve/reject comparison format -- generic checkmark/X icons,
    fully original geometry, no reference to any existing meme character."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    margin = 70
    icon_col_w = 150
    row_h = (H - 220) // 2

    red = (239, 68, 68)
    green = (34, 197, 94)

    # Row 1: rejected
    row1_top = 140
    draw.rounded_rectangle([margin, row1_top, W - margin, row1_top + row_h], radius=24, outline=red, width=5)
    draw_x_mark(draw, margin + icon_col_w // 2, row1_top + row_h // 2, 70, red)
    font1, lines1, lh1 = fit_text(
        draw, rejected_text, FONT_REGULAR,
        max_width=W - 2 * margin - icon_col_w - 40, max_height=row_h - 40, start_size=46, min_size=26
    )
    block_h1 = lh1 * len(lines1)
    y = row1_top + max(0, (row_h - block_h1) // 2)
    for line in lines1:
        draw.text((margin + icon_col_w, y), line, font=font1, fill=(235, 235, 235))
        y += lh1

    # Row 2: approved
    row2_top = row1_top + row_h + 40
    draw.rounded_rectangle([margin, row2_top, W - margin, row2_top + row_h], radius=24, outline=green, width=5)
    draw_checkmark(draw, margin + icon_col_w // 2, row2_top + row_h // 2, 70, green)
    font2, lines2, lh2 = fit_text(
        draw, approved_text, FONT_REGULAR,
        max_width=W - 2 * margin - icon_col_w - 40, max_height=row_h - 40, start_size=46, min_size=26
    )
    block_h2 = lh2 * len(lines2)
    y = row2_top + max(0, (row_h - block_h2) // 2)
    for line in lines2:
        draw.text((margin + icon_col_w, y), line, font=font2, fill=(235, 235, 235))
        y += lh2

    footer_font = ImageFont.truetype(str(FONT_BOLD), 32)
    draw.text((margin, H - 55), page_handle, font=footer_font, fill=(210, 210, 210))

    img.save(out_path, quality=95)
    return out_path


REEL_W, REEL_H = 1080, 1920


def make_meme_card_vertical(meme, out_path, page_handle="@YourPage"):
    """9:16 version for Reels. Keeps text away from where Facebook's own Reels UI
    (caption, follow button, like/comment/share icons) overlays the bottom/right
    edges when actually played back in the app."""
    accent = tuple(meme["accent"])
    img = Image.new("RGB", (REEL_W, REEL_H), BG)
    draw = ImageDraw.Draw(img)

    margin = 90
    safe_right = REEL_W - 160  # keep clear of Reels' right-edge action icons

    draw.rectangle([0, 0, REEL_W, 16], fill=accent)

    badge_font = ImageFont.truetype(str(FONT_BOLD), 38)
    badge_text = meme["label"]
    bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_w = (bbox[2] - bbox[0]) + 52
    badge_h = (bbox[3] - bbox[1]) + 30
    draw.rounded_rectangle([margin, 140, margin + badge_w, 140 + badge_h], radius=badge_h / 2, fill=accent)
    draw.text((margin + 26, 140 + 15 - bbox[1]), badge_text, font=badge_font, fill=(15, 15, 15))

    # Main text centered in the middle band -- clear of top badge and bottom Reels UI
    area_top, area_bottom = 420, 1380
    body_font, lines, line_height = fit_text(
        draw, meme["text"], FONT_BLACK,
        max_width=safe_right - margin, max_height=area_bottom - area_top, start_size=92, min_size=44
    )
    block_height = line_height * len(lines)
    y = area_top + max(0, (area_bottom - area_top - block_height) // 2)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        line_w = bbox[2] - bbox[0]
        x = margin + max(0, (safe_right - margin - line_w) // 2)
        draw.text((x, y), line, font=body_font, fill=(255, 255, 255))
        y += line_height

    # Handle placed above the zone where Facebook's own Reels caption/UI usually sits
    footer_font = ImageFont.truetype(str(FONT_BOLD), 38)
    cta_font = ImageFont.truetype(str(FONT_REGULAR), 32)
    draw.text((margin, 1500), page_handle, font=footer_font, fill=accent)
    draw.text((margin, 1550), "Follow for daily memes", font=cta_font, fill=(220, 220, 220))

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
