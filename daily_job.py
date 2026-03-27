"""Daily scheduled job for AI Finance Radar."""

from __future__ import annotations

from analyzer import analyze_articles, build_daily_digest
from notifier import push_bark
from rss_fetcher import fetch_articles


def main() -> int:
    raw = fetch_articles()
    analyzed = analyze_articles(raw)
    title, body, url = build_daily_digest(analyzed, max_items=5)
    ok, message = push_bark(title=title, body=body, url=url)
    print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
