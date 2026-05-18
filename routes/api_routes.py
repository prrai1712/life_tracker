"""JSON proxies for dashboards (same semantics as HTML pages)."""

from __future__ import annotations

from flask import Blueprint, request

from services.analysis_service import AnalysisService
from services.new_api_service import NewAPIService
from services.old_api_service import OldAPIService
from utils.helper import dashboard_params
from utils.response_builder import failure, success

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("/games")
def games_endpoint():
    p = dashboard_params(request.args)
    try:
        if p["api_type"] == "old":
            rows = OldAPIService.fetch_rows(page=p["page"], size=p["size"])
        else:
            raw = NewAPIService.fetch_payload(
                page=p["page"],
                size=p["size"],
                duration=p["duration"],
                matched_filter=p["matched_filter"],
                table_type_value=p["table_type_value"],
                wheel_csv=p["wheel_csv"],
            )
            rows = NewAPIService.build_rows(raw)
    except Exception as exc:
        return failure("Unable to load games", extras={"detail": str(exc)}, status=500)

    payload = {
        "api_type": p["api_type"],
        "pagination": {"page": p["page"], "size": p["size"]},
        "rows": rows,
    }

    return success("Games fetched successfully", payload)


@api_bp.get("/analysis")
def analysis_endpoint():
    p = dashboard_params(request.args, default_api_type="new")
    try:
        payload_json = NewAPIService.fetch_payload(
            page=p["page"],
            size=p["size"],
            duration=p["duration"],
            matched_filter=p["matched_filter"],
            table_type_value=p["table_type_value"],
            wheel_csv=p["wheel_csv"],
        )

        leaderboard = [
            {"player_name": name, **stats}
            for name, stats in AnalysisService.leaderboard(payload_json)
        ]

        page_avg = AnalysisService.page_avg_per_player_won(payload_json)

    except Exception as exc:

        return failure(
            "Unable to build analysis", extras={"detail": str(exc)}, status=500
        )

    return success(
        "Analysis fetched successfully",
        {
            "players": leaderboard,
            "page_avg_per_player_won": round(page_avg, 2),
        },
    )
