"""HTTP access layer for Casino.org JSON endpoints."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import requests

from config.constants import REQUEST_TIMEOUT_SECONDS, load_custom_headers

logger = logging.getLogger(__name__)


class CasinoOrgHttpClient:
    """Thin wrapper around ``requests``: one session, timeouts, shared headers."""

    _session = requests.Session()

    @classmethod
    def get_json(cls, url: str, *, params: Dict[str, Any]) -> Optional[Any]:
        try:
            response = cls._session.get(
                url,
                headers=load_custom_headers(),
                params=params,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            logger.warning("GET %s failed: %s", url, exc)
            return None
