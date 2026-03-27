"""RSS ingestion for AI Finance Radar."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import feedparser

from config import MAX_ARTICLES, RSS_FEEDS


_TAG_RE = re.compile(r"<[^>]+>")


def clean_text(text: str) -> str:
    text = _TAG_RE.sub(" ", text or "")
    return re.sub(r"\s+", " ", text).strip()


def normalize_title(title: str) -> str:
    normalized = re.sub(r"[^a-z0-9\s]", "", (title or "").lower())
    return re.sub(r"\s+", " ", normalized).strip()


def make_article_id(title: str, link: str) -> str:
    base = f"{normalize_title(title)}|{link.strip()}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()[:16]


def parse_published(entry: Any) -> datetime:
    candidates = [
        getattr(entry, "published", None),
        getattr(entry, "updated", None),
        entry.get("published"),
        entry.get("updated"),
    ]
    for value in candidates:
        if not value:
            continue
        try:
            dt = parsedate_to_datetime(value)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            continue
    return datetime.now(timezone.utc)


def fetch_articles(feeds: list[str] | None = None) -> list[dict[str, Any]]:
    feed_urls = feeds or RSS_FEEDS
    merged: list[dict[str, Any]] = []
    seen_titles: set[str] = set()

    for feed_url in feed_urls:
        parsed = feedparser.parse(feed_url)
        source_name = parsed.feed.get("title", feed_url)

        for entry in parsed.entries:
            title = clean_text(entry.get("title", ""))
            link = entry.get("link", "").strip()
            summary = clean_text(entry.get("summary", "") or entry.get("description", ""))
            published_dt = parse_published(entry)
            normalized = normalize_title(title)

            if not title or not link or normalized in seen_titles:
                continue

            seen_titles.add(normalized)

            merged.append(
                {
                    "id": make_article_id(title, link),
                    "title": title,
                    "link": link,
                    "published": published_dt.isoformat(),
                    "published_dt": published_dt,
                    "summary": summary,
                    "source": source_name,
                }
            )

    merged.sort(key=lambda x: x["published_dt"], reverse=True)
    return merged[:MAX_ARTICLES]
