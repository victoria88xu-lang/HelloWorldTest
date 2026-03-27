"""Notification layer for Bark push."""

from __future__ import annotations

import requests

from config import BARK_URL


def push_bark(title: str, body: str, url: str | None = None) -> tuple[bool, str]:
    payload = {
        "title": title,
        "body": body,
        "url": url,
        "group": "ai-finance-radar",
        "level": "active",
    }
    try:
        response = requests.post(BARK_URL, json=payload, timeout=12)
        response.raise_for_status()
        return True, "Bark push sent successfully."
    except Exception as exc:  # graceful failure for MVP
        return False, f"Bark push failed: {exc}"
