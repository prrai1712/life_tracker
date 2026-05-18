"""Player analysis (/analysis) — same CrazyTime bundle as legacy app."""

from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for

from config.constants import APP_TITLE
from services.analysis_service import AnalysisService
from services.new_api_service import NewAPIService
from utils.helper import dashboard_params, serialize_query

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/analysis", methods=["GET"])
def analysis_page():
    p = dashboard_params(request.args, default_api_type="new")

    payload = NewAPIService.fetch_payload(
        page=p["page"],
        size=p["size"],
        duration=p["duration"],
        matched_filter=p["matched_filter"],
        table_type_value=p["table_type_value"],
        wheel_csv=p["wheel_csv"],
    )
    players = AnalysisService.leaderboard(payload)

    page_avg_per_player_won = AnalysisService.page_avg_per_player_won(payload)

    return render_template(
        "analysis.html",
        app_title=APP_TITLE,
        players=players,
        page_avg_per_player_won=page_avg_per_player_won,
        serialize_query=serialize_query,
        filter_bundle=p,
    )


@analysis_bp.get("/analysis/run")
def analysis_shortcut():
    query = request.query_string.decode(errors="ignore")
    target = url_for("analysis.analysis_page")
    return redirect(f"{target}?{query}" if query else target)
