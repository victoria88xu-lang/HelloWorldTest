"""Simple file-based storage for latest analyzed signals."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path("data")
SIGNALS_FILE = DATA_DIR / "latest_signals.json"


def save_signals(items: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    serializable = []
    for item in items:
        payload = {k: v for k, v in item.items() if k != "published_dt"}
        serializable.append(payload)
    SIGNALS_FILE.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")


def load_signals_from_cache() -> list[dict[str, Any]]:
    if not SIGNALS_FILE.exists():
        return []
    try:
        return json.loads(SIGNALS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []
