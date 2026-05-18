"""Evolution Crazy Time (`svc-evolution-game-events`) → dashboard rows."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from config.constants import CASINO_NEW_API_URL, EUR_TO_INR, TABLE_MAPPING

from services.casino_client import CasinoOrgHttpClient
from utils.helper import clean_text


class NewAPIService:
    """Fetches JSON list once; ``build_rows`` maps it to template-friendly dicts."""

    @classmethod
    def fetch_payload(
        cls,
        *,
        page: int,
        size: Any,
        duration: Any,
        matched_filter: str,
        table_type_value: str,
        wheel_csv: str,
    ) -> List[Dict[str, Any]]:
        table_id = TABLE_MAPPING.get(table_type_value)
        blob = CasinoOrgHttpClient.get_json(
            CASINO_NEW_API_URL,
            params={
                "page": page,
                "size": size,
                "sort": "data.settledAt,desc",
                "duration": duration,
                "wheelResults": wheel_csv,
                "isTopSlotMatched": matched_filter,
                "tableId": table_id,
            },
        )
        return blob if isinstance(blob, list) else []

    @classmethod
    def build_rows(cls, games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [cls._row(game, idx) for idx, game in enumerate(games, start=1)]

    @classmethod
    def _row(cls, game: Dict[str, Any], index: int) -> Dict[str, Any]:
        data = game.get("data") or {}
        outcome = (data.get("result") or {}).get("outcome") or {}
        top_slot = outcome.get("topSlot") or {}
        wheel_block = outcome.get("wheelResult") or {}

        max_mult = outcome.get("maxMultiplier", "N/A")
        is_matched = clean_text(outcome.get("isTopSlotMatchedToWheelResult", False))

        total_winners = game.get("totalWinners") or 0
        total_inr = float(game.get("totalAmount") or 0) * EUR_TO_INR
        share = total_inr / total_winners if total_winners else 0.0

        winners_out: List[Dict[str, str]] = []
        for winner in (game.get("winners") or [])[:3]:
            name = clean_text(winner.get("screenName") or "Unknown")
            win_inr = float(winner.get("winnings") or 0) * EUR_TO_INR
            try:
                ratio = win_inr / float(max_mult)
            except (TypeError, ValueError, ZeroDivisionError):
                ratio = 0.0
            winners_out.append(
                {
                    "screen_name": name,
                    "winnings": f"{win_inr:,.2f}",
                    "ratio": f"{ratio:,.2f}",
                }
            )

        return {
            "index": index,
            "top_slot": clean_text(top_slot.get("wheelSector", "N/A")),
            "top_slot_multiplier": clean_text(top_slot.get("multiplier", "N/A")),
            "wheel_result": clean_text(wheel_block.get("wheelSector", "N/A")),
            "max_multiplier": clean_text(max_mult),
            "is_matched": is_matched,
            "started_at": cls._stamp(data.get("startedAt")),
            "settled_at": cls._stamp(data.get("settledAt")),
            "total_winners": total_winners,
            "total_amount": f"{total_inr:,.2f}",
            "per_player_won": f"{share:,.2f}",
            "winners": winners_out,
        }

    @staticmethod
    def _stamp(raw: Any) -> str:
        if not raw:
            return "N/A"
        try:
            dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            return clean_text(dt.strftime("%d %b %Y %H:%M:%S"))
        except (TypeError, ValueError):
            return "N/A"
