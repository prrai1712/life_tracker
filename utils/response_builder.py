"""Consistent JSON responses for REST endpoints."""

from __future__ import annotations

from typing import Any, Dict

from flask import jsonify


def success(message: str, data: Dict[str, Any]):
    payload = {"success": True, "message": message, "data": data}
    response = jsonify(payload)
    response.status_code = 200
    return response


def failure(message: str, *, status: int = 400, extras: Dict[str, Any] | None = None):
    body: Dict[str, Any] = {"success": False, "message": message}
    if extras:
        body["data"] = extras
    response = jsonify(body)
    response.status_code = status
    return response

