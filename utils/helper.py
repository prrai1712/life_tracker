"""Request parsing, sanitisation, and query-string helpers for dashboards."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, MutableMapping

from urllib.parse import urlencode

from config.constants import DEFAULT_MATCHED, DEFAULT_WHEEL_RESULTS


def clean_text(value: Any) -> str:
    """Strip broken UTF-16 surrogates (same behaviour as original monolithic app)."""
    if value is None:
        return "N/A"
    chunk = str(value)
    try:
        return chunk.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return "N/A"


def coerce_page(raw: Any) -> int:
    try:
        parsed = int(float(str(raw)))
    except (TypeError, ValueError):
        parsed = 0
    return max(parsed, 0)


def dedupe_stable(values: Iterable[str]) -> List[str]:
    """Keep first-seen ordering for multi-select values."""
    seen: MutableMapping[str, None] = {}
    ordered: List[str] = []
    for item in values:
        token = str(item)
        if token and token not in seen:
            seen[token] = None
            ordered.append(token)
    return ordered


def normalise_wheel_selection(args: Mapping[str, Any]) -> List[str]:
    selections = list(args.getlist("wheel_results"))
    if not selections or "ALL" in selections:
        return DEFAULT_WHEEL_RESULTS.copy()
    return dedupe_stable(selections)


def build_wheel_csv(selection: Iterable[str]) -> str:
    payload = dedupe_stable(selection)
    if not payload:
        payload = DEFAULT_WHEEL_RESULTS.copy()
    return ",".join(payload)


def serialize_query(bundle: Mapping[str, Any]) -> str:
    """Rebuild query string with repeated wheel_results keys."""
    tuples: List[tuple[str, str]] = [
        ("api_type", str(bundle.get("api_type", "old"))),
        ("page", str(bundle.get("page", 0))),
        ("size", str(bundle.get("size", 20))),
        ("duration", str(bundle.get("duration", 144))),
        ("matched_filter", str(bundle.get("matched_filter", DEFAULT_MATCHED))),
        ("table_type_value", str(bundle.get("table_type_value", "crazytime-a"))),
    ]
    wheels = (
        dedupe_stable(bundle.get("wheel_results") or []) or DEFAULT_WHEEL_RESULTS.copy()
    )
    for needle in wheels:
        tuples.append(("wheel_results", needle))
    return urlencode(tuples, doseq=True)


def dashboard_params(
    args: Mapping[str, Any], *, default_api_type: str = "old"
) -> Dict[str, Any]:
    """Parse GET params for `/`, `/analysis`, `/api/*` (mirror original defaults)."""
    wheel_results = normalise_wheel_selection(args)
    fallback = default_api_type if default_api_type in {"old", "new"} else "old"

    api_choice = str(args.get("api_type", fallback)).strip().lower()
    if api_choice not in {"old", "new"}:
        api_choice = fallback

    duration_raw = args.get("duration")
    duration = duration_raw if duration_raw not in (None, "") else 144

    return {
        "api_type": api_choice,
        "page": coerce_page(args.get("page", 0)),
        "size": args.get("size", 20),
        "duration": duration,
        "matched_filter": str(args.get("matched_filter", DEFAULT_MATCHED)),
        "table_type_value": str(args.get("table_type_value", "crazytime-a")),
        "wheel_results": wheel_results,
        "wheel_csv": build_wheel_csv(wheel_results),
    }
