#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


SCHEMA = "standards-watchlist/v1"


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def parse_utc(value: str) -> datetime | None:
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def validate(data: dict[str, Any], now: datetime) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append(f"schema должен быть `{SCHEMA}`")
    if data.get("network_required_for_quick_verify") is not False:
        errors.append("network_required_for_quick_verify должен быть false")
    if data.get("offline_first") is not True:
        errors.append("offline_first должен быть true")
    freshness_days = data.get("freshness_days")
    if not isinstance(freshness_days, int) or freshness_days <= 0:
        errors.append("freshness_days должен быть positive integer")
        freshness_days = 90
    proposal_path = str(data.get("proposal_path") or "")
    if "standards-update-proposal" not in proposal_path:
        errors.append("proposal_path должен указывать на standards-update-proposal")

    watch = data.get("watch", [])
    if not isinstance(watch, list) or not watch:
        errors.append("watch должен быть непустым list")
        return errors, warnings

    for index, item in enumerate(watch, 1):
        if not isinstance(item, dict):
            errors.append(f"watch[{index}] должен быть mapping")
            continue
        ref = str(item.get("standard_ref") or f"#{index}")
        for field in ["source_url", "selected_version", "last_checked_utc", "known_status", "drift_action"]:
            if not str(item.get(field) or "").strip():
                errors.append(f"watch[{ref}].{field} обязателен")
        if item.get("drift_action") != "proposal_required":
            errors.append(f"watch[{ref}].drift_action должен быть proposal_required")
        checked = parse_utc(str(item.get("last_checked_utc") or ""))
        if checked is None:
            errors.append(f"watch[{ref}].last_checked_utc должен быть ISO datetime")
            continue
        age_days = (now - checked).days
        if age_days > freshness_days:
            warnings.append(f"{ref}: last_checked stale ({age_days}d > {freshness_days}d); proposal-needed")
        if str(item.get("known_status") or "") in {"unknown", "stale", "revision_pending"}:
            warnings.append(f"{ref}: known_status={item.get('known_status')}; proposal-needed")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline-first standards watchlist check.")
    parser.add_argument("--root", default=".", help="Repo root")
    parser.add_argument("--watchlist", default="template-repo/standards/standards-watchlist.yaml")
    parser.add_argument("--strict-warnings", action="store_true", help="Treat stale warnings as failure.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    watchlist = Path(args.watchlist)
    if not watchlist.is_absolute():
        watchlist = root / watchlist
    errors, warnings = validate(load_yaml(watchlist), datetime.now(timezone.utc))
    if errors:
        print("STANDARDS WATCHLIST НЕВАЛИДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    if warnings:
        print("STANDARDS WATCHLIST WARNING")
        for warning in warnings:
            print(f"- {warning}")
        return 2 if args.strict_warnings else 0
    print("STANDARDS WATCHLIST OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
