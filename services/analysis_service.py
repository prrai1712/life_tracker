"""Aggregate top winners across one Crazy Time result page."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from config.constants import EUR_TO_INR
from utils.helper import clean_text


class AnalysisService:
    """Produces (player_name, {total_bet, total_win}) sorted by winnings."""

    @classmethod
    def leaderboard(
        cls, games: List[Dict[str, Any]]
    ) -> List[Tuple[str, Dict[str, float]]]:
        tally: Dict[str, Dict[str, float]] = {}

        for game in games or []:
            for winner in (game.get("winners") or [])[:3]:
                name = clean_text(winner.get("screenName") or "Unknown")
                win_inr = float(winner.get("winnings") or 0) * EUR_TO_INR

                outcome = (
                    ((game.get("data") or {}).get("result") or {}).get("outcome")
                ) or {}
                mult_raw = outcome.get("maxMultiplier", 1)
                try:
                    mult = float(mult_raw)
                except (TypeError, ValueError):
                    mult = 1.0
                try:
                    est_bet = win_inr / mult if mult else 0.0
                except ZeroDivisionError:
                    est_bet = 0.0

                bucket = tally.setdefault(name, {"total_bet": 0.0, "total_win": 0.0})
                bucket["total_bet"] += est_bet
                bucket["total_win"] += win_inr

        return sorted(tally.items(), key=lambda kv: kv[1]["total_win"], reverse=True)

    @classmethod
    def page_avg_per_player_won(cls, games: List[Dict[str, Any]]) -> float:
        """
        Arithmetic mean of (total INR pool / winners) per round on this page.

        Aligns with the dashboard "Per Player Won" column, averaged across rows.
        """
        shares: List[float] = []
        for game in games or []:
            winners = int(game.get("totalWinners") or 0)
            if winners <= 0:
                continue
            pool_inr = float(game.get("totalAmount") or 0) * EUR_TO_INR
            shares.append(pool_inr / winners)

        return (sum(shares) / len(shares)) if shares else 0.0
