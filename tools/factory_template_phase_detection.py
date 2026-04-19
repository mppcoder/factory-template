#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "factory-template-ops-policy.yaml"
IGNORED_PREFIXES = (
    "_sources-export/",
    "_boundary-actions/",
)
IGNORED_NAMES = (
    "__pycache__",
    ".pytest_cache",
)


def load_policy() -> dict:
    return yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}


def ignore_path(path: str) -> bool:
    if any(path.startswith(prefix) for prefix in IGNORED_PREFIXES):
        return True
    return any(name in path.split("/") for name in IGNORED_NAMES)


def read_changed_paths(root: Path = ROOT) -> list[str]:
    git_dir = root / ".git"
    if not git_dir.exists():
        return []
    proc = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    changed: list[str] = []
    for raw in proc.stdout.splitlines():
        line = raw.rstrip()
        if len(line) < 4:
            continue
        payload = line[3:]
        if " -> " in payload:
            payload = payload.split(" -> ", 1)[1]
        payload = payload.strip()
        if payload and not ignore_path(payload):
            changed.append(payload)
    return changed


def matches_rule(path: str, exact_paths: list[str], prefixes: list[str]) -> bool:
    if path in exact_paths:
        return True
    return any(path.startswith(prefix) for prefix in prefixes)


def detect_phase(policy: dict, changed_paths: list[str] | None = None) -> dict[str, object]:
    boundary = policy.get("boundary_actions", {}) if isinstance(policy, dict) else {}
    phase_recommendations = boundary.get("phase_recommendations", {})
    phase_detection = boundary.get("phase_detection", {})
    default_phase = boundary.get("default_phase", "controlled-fixes")
    changed_paths = changed_paths if changed_paths is not None else read_changed_paths(ROOT)

    detected_phase = default_phase
    reasons: list[str] = []
    matches_by_phase: dict[str, list[str]] = {}

    if isinstance(phase_detection, dict):
        for phase_name, cfg in phase_detection.items():
            if not isinstance(cfg, dict):
                continue
            exact_paths = cfg.get("exact_paths", [])
            prefixes = cfg.get("path_prefixes", [])
            min_matches = cfg.get("min_matches", 1)
            if not isinstance(exact_paths, list):
                exact_paths = []
            if not isinstance(prefixes, list):
                prefixes = []
            if not isinstance(min_matches, int) or min_matches < 1:
                min_matches = 1
            matched = [
                path for path in changed_paths
                if matches_rule(path, exact_paths, prefixes)
            ]
            matches_by_phase[phase_name] = matched
            if len(matched) >= min_matches:
                detected_phase = phase_name
                reasons.append(
                    f"{phase_name}: matched {len(matched)} path(s) with threshold {min_matches}"
                )
                break

    if not reasons:
        if changed_paths:
            reasons.append(
                f"default phase `{default_phase}` used: changed paths did not meet release/bugfix thresholds"
            )
        else:
            reasons.append(
                f"default phase `{default_phase}` used: working tree is clean"
            )

    active_cfg = phase_recommendations.get(detected_phase, {}) if isinstance(phase_recommendations, dict) else {}
    recommended_pack = boundary.get("recommended_sources_pack", "sources-pack-core-20.tar.gz")
    rationale = "phase recommendation not configured"
    if isinstance(active_cfg, dict):
        recommended_pack = active_cfg.get("recommended_sources_pack", recommended_pack)
        rationale = active_cfg.get("rationale", rationale)

    return {
        "phase": detected_phase,
        "recommended_sources_pack": recommended_pack,
        "rationale": rationale,
        "reasons": reasons,
        "changed_paths": changed_paths,
        "matches_by_phase": matches_by_phase,
    }
