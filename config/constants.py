"""
Application constants aligned with the original Crazy Time dashboard.

Override endpoints or headers via environment variables where noted.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List

# --- Currency conversion (EUR winnings → INR totals in downstream UI) ---
USD_TO_INR: float = float(os.getenv("USD_TO_INR_RATE", "107.4"))
EUR_TO_INR: float = float(os.getenv("EUR_TO_INR_RATE", "96.5"))

# Wheel chips presented in filters (pseudo option "ALL" handled in frontend + routes)
DEFAULT_WHEEL_RESULTS: List[str] = [
    "Pachinko",
    "CashHunt",
    "CrazyBonus",
    "CoinFlip",
    "1",
    "2",
    "5",
    "10",
]

# Mirrors upstream CrazyTime filters: comma separated truth flags
DEFAULT_MATCHED: str = "true,false"

# UI table keys → Evolution table identifiers
TABLE_MAPPING: Dict[str, str] = {
    "crazytime": "CrazyTime0000001",
    "crazytime-a": "CrazyTime0000002",
}

TABLE_OPTIONS: tuple[tuple[str, str], ...] = (
    ("crazytime", "CrazyTime"),
    ("crazytime-a", "CrazyTime-A"),
)

# Same hosts and paths as legacy monolithic app.py
CASINO_OLD_API_URL: str = os.getenv(
    "CASINO_OLD_API_URL",
    "https://api-cs.casino.org/cg-neptune-notification-center/api/halloffame",
)

CASINO_NEW_API_URL: str = os.getenv(
    "CASINO_NEW_API_URL",
    "https://api-cs.casino.org/svc-evolution-game-events/api/crazytime",
)

CASINO_ORIGIN: str = os.getenv("CASINO_ORIGIN", "https://www.casinoorg-india.com")
CASINO_REFERER: str = os.getenv("CASINO_REFERER", "https://www.casinoorg-india.com/")

CASINO_HEADERS: Dict[str, str] = {
    "accept": "*/*",
    "origin": CASINO_ORIGIN,
    "referer": CASINO_REFERER,
    "user-agent": os.getenv(
        "CASINO_USER_AGENT",
        (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
        ),
    ),
}

REQUEST_TIMEOUT_SECONDS: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "45"))

APP_TITLE: str = os.getenv("LIFE_TRACKER_TITLE", "Crazy Time Dashboard")


def load_custom_headers(extra: str | None = None) -> Dict[str, str]:
    """Optional JSON overlay for outbound headers (ADVANCED_USERS only)."""

    merged = dict(CASINO_HEADERS)
    blob = extra or os.getenv("CASINO_HEADERS_JSON", "").strip()

    if not blob:
        return merged

    try:
        payload = json.loads(blob)
        if isinstance(payload, dict):
            merged.update({str(k): str(v) for k, v in payload.items()})
    except (json.JSONDecodeError, TypeError):
        pass
    return merged
