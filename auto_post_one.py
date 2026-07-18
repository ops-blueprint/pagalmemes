#!/usr/bin/env python3
"""Generate one fresh meme card and post it immediately to the Page.

Content comes from in-house original joke banks (content_pipeline/meme_bank.py
and template_bank.py) -- not scraped from Reddit/Instagram/meme-template
sites, so no copyright risk. Mixes three original formats: a single punchy
statement, an Expectation-vs-Reality split, and an approve/reject comparison
(icon-based layouts, no copyrighted characters or images involved).

Designed to be triggered by a scheduled GitHub Actions job (see
.github/workflows/auto_post.yml).
"""
import argparse
import datetime
import os
import random
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "content_pipeline"))
sys.path.insert(0, str(BASE_DIR / "fb_auto_poster"))

from dotenv import load_dotenv

import fetch_memes
import make_meme_cards
import post_to_facebook

FORMAT_WEIGHTS = {"single": 0.5, "split": 0.25, "comparison": 0.25}


def build_post(used, handle, out_path):
    fmt = random.choices(list(FORMAT_WEIGHTS.keys()), weights=list(FORMAT_WEIGHTS.values()), k=1)[0]

    if fmt == "single":
        memes = fetch_memes.pick_memes(count=1, used=used)
        if not memes:
            return None
        meme = memes[0]
        used.add(meme["text"][:80])
        make_meme_cards.make_meme_card(meme, out_path, page_handle=handle)
        caption = f"{meme['text']}\n\n#Memes #Relatable #DailyMemes #Mood #{meme['category'].replace('_', '')}"
        label = meme["category"]

    elif fmt == "split":
        top, bottom = fetch_memes.pick_split_joke(used)
        used.add(f"split:{top[:60]}")
        make_meme_cards.make_split_card(top, bottom, out_path, page_handle=handle)
        caption = f"Expectation: {top}\nReality: {bottom}\n\n#Memes #Relatable #ExpectationVsReality #DailyMemes"
        label = "split"

    else:
        rejected, approved = fetch_memes.pick_comparison_joke(used)
        used.add(f"cmp:{rejected[:60]}")
        make_meme_cards.make_comparison_card(rejected, approved, out_path, page_handle=handle)
        caption = f"{approved} > {rejected}\n\n#Memes #Relatable #DailyMemes #TooReal"
        label = "comparison"

    return caption, label


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Generate the card but don't post it")
    args = parser.parse_args()

    load_dotenv(BASE_DIR / "fb_auto_poster" / ".env")

    used = fetch_memes.load_used()

    out_dir = BASE_DIR / "content_pipeline" / "output" / "_auto"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = out_dir / f"post_{stamp}.png"

    handle = os.environ.get("PAGE_HANDLE", "@YourPage")
    result = build_post(used, handle, image_path)

    if result is None:
        print("No memes available -- skipping this run.")
        return

    caption, label = result
    fetch_memes.save_used(used)

    page_id = os.environ.get("FB_PAGE_ID")
    token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
    api_result = post_to_facebook.post_photo_to_page(page_id, token, image_path, caption, dry_run=args.dry_run)
    print(f"{'[dry-run] Would post' if args.dry_run else 'Posted'} meme ({label}): {api_result}")


if __name__ == "__main__":
    main()
