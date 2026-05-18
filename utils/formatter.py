"""Small display helpers kept separate from ingestion logic."""

from __future__ import annotations


def comma_inr(value: float) -> str:
    """Comma-separated rupee amount for templates that expect plain strings."""
    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return "0.00"
