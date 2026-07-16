#!/usr/bin/env python3
"""Generate one fresh meme card and post it immediately to the Page.

Content comes from an in-house original joke bank (content_pipeline/meme_bank.py)
-- not scraped from Reddit/Instagram, so no copyright or API-lockdown risk.
Designed to be triggered by a scheduled GitHub Actions job (see
.github/workflows/auto_post.yml).
"""
import argparse
import datetime
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "content_pipeline"))
sys.path.insert(0, str(BASE_DIR / "fb_auto_poster"))

from dotenv import load_dotenv

import fetch_memes
import make_meme_cards
import post_to_facebook


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Generate the card but don't post it")
    args = parser.parse_args()

    load_dotenv(BASE_DIR / "fb_auto_poster" / ".env")

    used = fetch_memes.load_used()
    memes = fetch_memes.pick_memes(count=1, used=used)

    if not memes:
        print("No memes available -- skipping this run.")
        return

    meme = memes[0]
    used.add(meme["text"][:80])
    fetch_memes.save_used(used)

    out_dir = BASE_DIR / "content_pipeline" / "output" / "_auto"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = out_dir / f"post_{stamp}.png"

    handle = os.environ.get("PAGE_HANDLE", "@YourPage")
    make_meme_cards.make_meme_card(meme, image_path, page_handle=handle)

    caption = f"{meme['text']}\n\n#Memes #Relatable #DailyMemes #Mood #{meme['category'].replace('_', '')}"

    page_id = os.environ.get("FB_PAGE_ID")
    token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
    result = post_to_facebook.post_photo_to_page(page_id, token, image_path, caption, dry_run=args.dry_run)
    print(f"{'[dry-run] Would post' if args.dry_run else 'Posted'} meme ({meme['category']}): {result}")


if __name__ == "__main__":
    main()
