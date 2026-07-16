#!/usr/bin/env python3
"""Generate one fresh meme, render it as a vertical Reel-format card, animate it
into a short video with ffmpeg, and post it to the Page as a video.

Runs alongside auto_post_one.py (the static-image poster) on a separate cron
schedule -- see .github/workflows/auto_post_reels.yml.
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
import make_reel
import post_to_facebook


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Generate the video but don't post it")
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

    out_dir = BASE_DIR / "content_pipeline" / "output" / "_auto_reels"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = out_dir / f"reel_{stamp}.png"
    video_path = out_dir / f"reel_{stamp}.mp4"

    handle = os.environ.get("PAGE_HANDLE", "@YourPage")
    make_meme_cards.make_meme_card_vertical(meme, image_path, page_handle=handle)
    make_reel.make_reel(image_path, video_path)

    caption = f"{meme['text']}\n\n#Memes #Reels #Relatable #DailyMemes #{meme['category'].replace('_', '')}"

    page_id = os.environ.get("FB_PAGE_ID")
    token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
    result = post_to_facebook.post_video_to_page(page_id, token, video_path, caption, dry_run=args.dry_run)
    print(f"{'[dry-run] Would post' if args.dry_run else 'Posted'} reel ({meme['category']}): {result}")


if __name__ == "__main__":
    main()
