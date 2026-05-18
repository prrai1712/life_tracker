"""Dashboard (/) — mirrors legacy ``home()`` routing."""

from __future__ import annotations

from flask import Blueprint, render_template, request, url_for

from config.constants import APP_TITLE, DEFAULT_WHEEL_RESULTS, TABLE_OPTIONS
from services.new_api_service import NewAPIService
from services.old_api_service import OldAPIService
from utils.helper import dashboard_params, serialize_query

home_bp = Blueprint("home", __name__)


def _pagination_urls(view: str, p: dict) -> tuple[str, str]:
    """Prev / Next links preserving every filter knob."""
    base = dict(
        api_type=p["api_type"],
        size=p["size"],
        duration=p["duration"],
        matched_filter=p["matched_filter"],
        table_type_value=p["table_type_value"],
        wheel_results=p["wheel_results"],
    )
    next_pg = p["page"] + 1
    prev_pg = p["page"] - 1 if p["page"] > 0 else 0

    base_next = dict(base, page=next_pg)
    base_prev = dict(base, page=prev_pg)

    return url_for(view, **base_prev), url_for(view, **base_next)


@home_bp.route("/", methods=["GET"])
def dashboard():
    p = dashboard_params(request.args)

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

    prev_url, next_url = _pagination_urls("home.dashboard", p)

    return render_template(
        "index.html",
        app_title=APP_TITLE,
        rows=rows,
        api_type=p["api_type"],
        table_type=p["api_type"],
        page=p["page"],
        size=p["size"],
        duration=p["duration"],
        matched_filter=p["matched_filter"],
        table_type_value=p["table_type_value"],
        selected_wheel_results=p["wheel_results"],
        all_wheel_results=DEFAULT_WHEEL_RESULTS,
        current_page=p["page"],
        prev_url=prev_url,
        next_url=next_url,
        serialize_query=serialize_query,
        encode_filters=serialize_query,
        table_options=TABLE_OPTIONS,
        filter_bundle=p,
    )
