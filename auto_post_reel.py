#!/usr/bin/env python3
"""Generate 5 fresh memes, render each as a vertical Reel-format card, stitch
them into one compilation video with ffmpeg (each gets its own zoom segment,
one music track over the whole thing), and post it to the Page as a video.

Runs on the same schedule as auto_post_one.py (the static-image poster) --
see .github/workflows/auto_post_reels.yml.
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

MEMES_PER_REEL = 5
SECONDS_PER_MEME = 4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Generate the video but don't post it")
    parser.add_argument("--count", type=int, default=MEMES_PER_REEL)
    args = parser.parse_args()

    load_dotenv(BASE_DIR / "fb_auto_poster" / ".env")

    used = fetch_memes.load_used()
    memes = fetch_memes.pick_memes(count=args.count, used=used)

    if not memes:
        print("No memes available -- skipping this run.")
        return

    for m in memes:
        used.add(m["text"][:80])
    fetch_memes.save_used(used)

    out_dir = BASE_DIR / "content_pipeline" / "output" / "_auto_reels"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    handle = os.environ.get("PAGE_HANDLE", "@YourPage")
    image_paths = []
    for i, meme in enumerate(memes, start=1):
        image_path = out_dir / f"reel_{stamp}_{i}.png"
        make_meme_cards.make_meme_card_vertical(meme, image_path, page_handle=handle)
        image_paths.append(image_path)

    video_path = out_dir / f"reel_{stamp}.mp4"
    music_path, attribution = make_reel.pick_track()
    make_reel.make_multi_reel(image_paths, video_path, per_image_duration=SECONDS_PER_MEME, music_path=music_path)

    categories = ", ".join(sorted({m["category"] for m in memes}))
    caption = (
        f"{len(memes)} relatable moments hit different 😅 Follow for daily memes!\n\n"
        f"#Memes #Reels #Relatable #DailyMemes #{categories.replace(', ', ' #').replace('_', '')}\n\n"
        f"Music: {attribution}"
    )

    page_id = os.environ.get("FB_PAGE_ID")
    token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
    result = post_to_facebook.post_video_to_page(page_id, token, video_path, caption, dry_run=args.dry_run)
    print(f"{'[dry-run] Would post' if args.dry_run else 'Posted'} compilation reel "
          f"({len(memes)} memes: {categories}): {result}")


if __name__ == "__main__":
    main()
