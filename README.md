# pagalmemes automation

Fully automated meme posting for a Facebook Page, same architecture as the
facts-automation project but with original relatable-humor content instead of
facts. All free resources, no Reddit/Instagram scraping (avoids copyright and
platform-ToS risk entirely).

## How content works

- `content_pipeline/meme_bank.py` — hand-written original one-liners, organized
  by category (work, adulting, social media, food, weekend, relationships,
  introvert life). Add more anytime by editing this file.
- `content_pipeline/fetch_memes.py` — picks unused memes, rotates through the
  whole bank before repeating (tracked in `content_pipeline/used_memes.json`).
- `content_pipeline/make_meme_cards.py` — renders each as a bold, centered
  1080x1350 card with a category badge.
- `auto_post_one.py` — ties it together and posts one meme via the Facebook
  Graph API. Meant to be triggered on a schedule (see below).

## One-time setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r content_pipeline/requirements.txt -r fb_auto_poster/requirements.txt
cp fb_auto_poster/.env.example fb_auto_poster/.env
# then fill in FB_PAGE_ID and FB_PAGE_ACCESS_TOKEN in that .env file
```

## Test locally

```bash
source .venv/bin/activate
PAGE_HANDLE="@pagalmemes" python3 auto_post_one.py --dry-run   # no live post
PAGE_HANDLE="@pagalmemes" python3 auto_post_one.py             # real post
```

## Automating on a schedule

Same pattern as facts-automation: a GitHub Actions workflow triggers
`auto_post_one.py` on a cron schedule, with `FB_PAGE_ID` and
`FB_PAGE_ACCESS_TOKEN` stored as repo secrets (Settings -> Secrets and
variables -> Actions).
