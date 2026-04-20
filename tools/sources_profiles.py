#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILES_PATH = ROOT / "packaging" / "sources" / "sources-profiles.yaml"


def profiles_path_from_policy(policy: dict | None = None) -> Path:
    policy = policy or {}
    rel = policy.get("sources_profiles_manifest", "packaging/sources/sources-profiles.yaml")
    return ROOT / rel


def load_sources_profiles(path: Path | None = None) -> dict:
    target = path or DEFAULT_PROFILES_PATH
    return yaml.safe_load(target.read_text(encoding="utf-8")) or {}


def get_profiles(policy: dict | None = None) -> dict[str, dict]:
    data = load_sources_profiles(profiles_path_from_policy(policy))
    profiles = data.get("profiles", {})
    if not isinstance(profiles, dict):
        return {}
    return profiles


def find_profile_by_export_name(profiles: dict[str, dict], export_name: str) -> tuple[str | None, dict | None]:
    for profile_name, profile in profiles.items():
        if isinstance(profile, dict) and profile.get("export_name") == export_name:
            return profile_name, profile
    return None, None
