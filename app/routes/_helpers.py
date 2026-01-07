from __future__ import annotations

from flask import jsonify, request


def get_json() -> dict:
    return request.get_json(silent=True) or {}


def ok(data, status: int = 200):
    return jsonify({"ok": True, "data": data}), status


def err(message: str, status: int = 400):
    return jsonify({"ok": False, "error": message}), status
