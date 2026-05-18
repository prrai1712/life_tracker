"""Legacy Hall of Fame (CRAZY_TIME) feed → dashboard rows."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from config.constants import CASINO_OLD_API_URL, USD_TO_INR

from services.casino_client import CasinoOrgHttpClient
from utils.helper import clean_text


class OldAPIService:
    """Pagination only is forwarded upstream; spin filters match the legacy app."""

    @classmethod
    def fetch_rows(cls, *, page: int, size: Any) -> List[Dict[str, Any]]:
        blob = CasinoOrgHttpClient.get_json(
            CASINO_OLD_API_URL,
            params={
                "page": page,
                "size": size,
                "sort": ["multiplier,desc", "settledAt,desc"],
                "gameShow": "CRAZY_TIME",
                "multiplier": 2501,
                "spinOutcomes": "HotSpot,CashHunt,Billy Bones' Map,coinRush",
            },
        )

        if not isinstance(blob, list):
            return []

        rows: List[Dict[str, Any]] = []
        for idx, game in enumerate(blob, start=1):
            spin_outcome = clean_text(game.get("spinOutcome") or "N/A")
            multiplier = game.get("multiplier") or 0
            total_winners = game.get("totalWinners") or 0
            total_inr = float(game.get("totalAmount") or 0) * USD_TO_INR

            avg = total_inr / total_winners if total_winners else 0.0
            winners_out: List[Dict[str, str]] = []
            for winner in (game.get("winners") or [])[:3]:
                name = clean_text(winner.get("screenName") or "Unknown")
                win_inr = float(winner.get("winnings") or 0) * USD_TO_INR
                ratio = win_inr / multiplier if multiplier else 0.0
                winners_out.append(
                    {
                        "screen_name": name,
                        "winnings": f"{win_inr:,.2f}",
                        "ratio": f"{ratio:,.2f}",
                    }
                )

            rows.append(
                {
                    "index": idx,
                    "spin_outcome": spin_outcome,
                    "multiplier": multiplier,
                    "started_at": cls._stamp(game.get("startedAt")),
                    "settled_at": cls._stamp(game.get("settledAt")),
                    "total_winners": total_winners,
                    "total_amount": f"{total_inr:,.2f}",
                    "avg_per_winner": f"{avg:,.2f}",
                    "winners": winners_out,
                }
            )

        return rows

    @staticmethod
    def _stamp(raw: Any) -> str:
        if not raw:
            return "N/A"
        try:
            dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            return clean_text(dt.strftime("%d %b %Y %H:%M:%S"))
        except (TypeError, ValueError):
            return "N/A"
