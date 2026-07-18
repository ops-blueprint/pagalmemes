#!/usr/bin/env python3
"""Pick unused meme captions from the in-house bank, tracking dedupe state."""
import json
import random
from pathlib import Path

from meme_bank import ALL_MEMES
from template_bank import SPLIT_JOKES, COMPARISON_JOKES

BASE_DIR = Path(__file__).resolve().parent
USED_LOG = BASE_DIR / "used_memes.json"

CATEGORY_LABEL = {
    "work": "WORK LIFE",
    "adulting": "ADULTING",
    "social_media": "ONLINE LIFE",
    "food": "FOOD MOOD",
    "weekend": "WEEKEND VIBES",
    "relationships": "RELATIONSHIPS",
    "introvert": "INTROVERT LIFE",
    "toxic_friends": "FRIEND FAILS",
    "trends": "TRENDING NOW",
}

CATEGORY_ACCENT = {
    "work": (239, 68, 68),
    "adulting": (59, 130, 246),
    "social_media": (168, 85, 247),
    "food": (250, 204, 21),
    "weekend": (34, 197, 94),
    "relationships": (236, 72, 153),
    "introvert": (94, 234, 212),
    "toxic_friends": (251, 113, 133),
    "trends": (249, 115, 22),
}


def load_used():
    if USED_LOG.exists():
        return set(json.loads(USED_LOG.read_text()))
    return set()


def save_used(used):
    USED_LOG.write_text(json.dumps(sorted(used), indent=2))


def pick_memes(count, used):
    available = [(cat, text) for cat, text in ALL_MEMES if text[:80] not in used]
    if not available:
        # Whole bank has been used at least once -- reset and start the rotation over
        used.clear()
        available = list(ALL_MEMES)

    random.shuffle(available)

    picked = []
    seen_categories = {}
    for category, text in available:
        if len(picked) >= count:
            break
        if seen_categories.get(category, 0) >= 2 and len(picked) < count - 1:
            continue
        picked.append({
            "category": category,
            "label": CATEGORY_LABEL.get(category, category.upper()),
            "accent": CATEGORY_ACCENT.get(category, (245, 158, 11)),
            "text": text,
        })
        seen_categories[category] = seen_categories.get(category, 0) + 1

    if len(picked) < count:
        for category, text in available:
            if len(picked) >= count:
                break
            if any(p["text"] == text for p in picked):
                continue
            picked.append({
                "category": category,
                "label": CATEGORY_LABEL.get(category, category.upper()),
                "accent": CATEGORY_ACCENT.get(category, (245, 158, 11)),
                "text": text,
            })

    return picked


def pick_split_joke(used):
    """Pick one unused (expectation, reality) pair. Dedupe keys are prefixed
    'split:' so they share used_memes.json without colliding with other banks."""
    available = [(t, b) for t, b in SPLIT_JOKES if f"split:{t[:60]}" not in used]
    if not available:
        for t, b in SPLIT_JOKES:
            used.discard(f"split:{t[:60]}")
        available = list(SPLIT_JOKES)
    return random.choice(available)


def pick_comparison_joke(used):
    """Pick one unused (rejected, approved) pair. Dedupe keys are prefixed
    'cmp:' so they share used_memes.json without colliding with other banks."""
    available = [(r, a) for r, a in COMPARISON_JOKES if f"cmp:{r[:60]}" not in used]
    if not available:
        for r, a in COMPARISON_JOKES:
            used.discard(f"cmp:{r[:60]}")
        available = list(COMPARISON_JOKES)
    return random.choice(available)
