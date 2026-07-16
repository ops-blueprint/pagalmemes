#!/usr/bin/env python3
"""Turn a static vertical (1080x1920) meme card into a short Reel-format video.

Free, local, ffmpeg-only: a slow "Ken Burns" zoom on the still image, plus a
silent audio track (some platforms expect an audio stream to be present).
No stock footage, no paid APIs, no royalty-free-music licensing to worry about
since there's no audio content, just silence.
"""
import argparse
import subprocess
from pathlib import Path

DURATION = 6
FPS = 30


def make_reel(image_path, out_path, duration=DURATION, fps=FPS):
    image_path = str(image_path)
    out_path = str(out_path)
    frames = duration * fps

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-vf",
        f"scale=8000:-1,zoompan=z='min(zoom+0.0015,1.15)':d={frames}:s=1080x1920:fps={fps}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-t", str(duration),
        "-c:a", "aac", "-shortest",
        out_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr[-2000:]}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Animate a static card into a short Reel video")
    parser.add_argument("--image", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--duration", type=int, default=DURATION)
    args = parser.parse_args()

    make_reel(args.image, args.out, duration=args.duration)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
