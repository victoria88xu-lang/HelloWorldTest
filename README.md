# AI Finance Radar

AI Finance Radar is a practical Streamlit MVP that ingests **real AI + finance RSS feeds**, ranks them for a **banking SRE / Equity Derivatives production support** profile, highlights high-signal updates with **Chinese spotlight summaries**, and sends **Bark daily push notifications**.

## Features

- Real RSS ingestion from AI + finance/banking sources.
- Dedup + recency sorting.
- Personalized rules-based scoring (0-100) with:
  - banking relevance
  - SRE/ops relevance
  - enterprise AI adoption relevance
- Attention labels:
  - `HIGH ATTENTION`
  - `WATCH`
  - `LOW PRIORITY`
- Chinese spotlight summary (`spotlight_cn`) per item.
- Streamlit detail links using `?item_id=<article_id>`.
- Bark push notifications with clickable URLs.
- Daily scheduler via GitHub Actions at **08:00 Singapore time**.

## Project structure

- `app.py` — Streamlit UI (Top Signals, Especially Important, All Signals, Trends, detail page by query param)
- `config.py` — RSS feeds, Bark URL, app base URL, scoring weights/keywords
- `rss_fetcher.py` — fetch + merge + deduplicate RSS entries
- `analyzer.py` — scoring, flags, summaries, trends, digest building
- `notifier.py` — Bark push helper
- `daily_job.py` — scheduled pipeline for daily digest push
- `storage.py` — lightweight file storage for latest analyzed signals cache
- `.github/workflows/daily.yml` — scheduled GitHub Actions workflow

## RSS sources

Configured in `config.py` (`RSS_FEEDS`):

AI:
- https://openai.com/blog/rss.xml
- https://www.anthropic.com/news/rss
- https://huggingface.co/blog/feed.xml
- https://ai.googleblog.com/feeds/posts/default

Finance / banking / tech:
- https://www.ft.com/technology?format=rss
- https://www.reuters.com/technology/rss
- https://www.reuters.com/finance/rss
- https://www.finextra.com/rss/headlines.aspx
- https://www.americanbanker.com/feeds/all.xml

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`.

## Streamlit deployment

1. Push this repository to GitHub.
2. Deploy on Streamlit Community Cloud.
3. Set app entrypoint to `app.py`.
4. Update `APP_BASE_URL` in `config.py` to your deployed URL.

## Bark push

Implemented in `notifier.py`:

```python
push_bark(title, body, url=None)
```

Current MVP uses hardcoded Bark endpoint in `config.py`:

- `BARK_URL = "https://api.day.app/fCipZZrf7xYwdxiqnVD8Ga/"`

> TODO: move Bark key/URL into secrets or environment variables for production.

In app sidebar:

- **Test Bark Push**
- **Send Sample Spotlight**

Each push includes a clickable URL that opens either:
- `APP_BASE_URL/?item_id=<top_article_id>`
- or homepage fallback.

The app also caches recent analyzed items to `data/latest_signals.json` so detail links still resolve even if a feed temporarily fails.

## Daily GitHub Actions push (08:00 Singapore)

Workflow file: `.github/workflows/daily.yml`

- Cron: `0 0 * * *` (UTC) = **08:00 Asia/Singapore (UTC+8)**
- Also supports manual trigger (`workflow_dispatch`)
- Runs:

```bash
python daily_job.py
```

## Docker (optional)

```bash
docker build -t ai-finance-radar:latest .
docker run --rm -p 8501:8501 ai-finance-radar:latest
```

## Notes

- MVP intentionally uses practical rules-based analysis (no heavy backend).
- Designed for fast scanning and operational relevance, not long report-style output.
