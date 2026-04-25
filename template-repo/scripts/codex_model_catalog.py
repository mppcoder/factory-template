#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import yaml

from factory_automation_common import now_utc, read_yaml


CATALOG_SOURCE = "codex debug models"


def find_repo_file(root: Path, rel_path: str) -> Path:
    candidates = [root / rel_path, root / "template-repo" / rel_path]
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


def model_routing_path(root: Path) -> Path:
    return find_repo_file(root, "codex-model-routing.yaml")


def load_model_routing(root: Path) -> tuple[dict, Path]:
    path = model_routing_path(root)
    return read_yaml(path), path


def simplify_models(payload: dict) -> dict[str, dict]:
    models: dict[str, dict] = {}
    for raw in payload.get("models", []):
        slug = str(raw.get("slug") or "").strip()
        if not slug:
            continue
        supported = [
            str(item.get("effort") or "").strip()
            for item in raw.get("supported_reasoning_levels", [])
            if str(item.get("effort") or "").strip()
        ]
        models[slug] = {
            "supported_reasoning_efforts": supported,
            "default_reasoning_effort": str(raw.get("default_reasoning_level") or "").strip(),
        }
    return models


def load_catalog_fixture(path: Path) -> dict[str, dict]:
    if path.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {}
    if "models" in data:
        return simplify_models(data)
    catalog = data.get("model_catalog", data)
    discovered = catalog.get("discovered_models", catalog) if isinstance(catalog, dict) else {}
    return discovered if isinstance(discovered, dict) else {}


def load_live_catalog(fixture: Path | None = None) -> tuple[dict[str, dict], str, str | None]:
    if fixture is not None:
        return load_catalog_fixture(fixture), f"fixture:{fixture}", None
    if shutil.which("codex") is None:
        return {}, CATALOG_SOURCE, "CLI `codex` not found; live model catalog was not checked"
    try:
        result = subprocess.run(
            ["codex", "debug", "models"],
            check=True,
            capture_output=True,
            text=True,
        )
        return simplify_models(json.loads(result.stdout)), CATALOG_SOURCE, None
    except Exception as exc:  # pragma: no cover - defensive boundary around external CLI
        return {}, CATALOG_SOURCE, f"Unable to read live model catalog with `codex debug models`: {exc}"


def configured_profiles(model_routing: dict, routing_spec: dict | None = None) -> dict[str, dict]:
    profile_routes = model_routing.get("profile_routes", {}) if isinstance(model_routing, dict) else {}
    if profile_routes:
        return {
            str(name): {
                "model": meta.get("selected_model", ""),
                "reasoning_effort": meta.get("selected_reasoning_effort", ""),
                "plan_mode_reasoning_effort": meta.get("selected_plan_mode_reasoning_effort", ""),
                "manual_review_required": bool(meta.get("manual_review_required", False)),
            }
            for name, meta in profile_routes.items()
            if isinstance(meta, dict)
        }
    profiles = (routing_spec or {}).get("profiles", {}) if isinstance(routing_spec, dict) else {}
    return profiles if isinstance(profiles, dict) else {}


def configured_task_classes(model_routing: dict, routing_spec: dict | None = None) -> dict[str, str]:
    task_routes = model_routing.get("task_class_routing", {}) if isinstance(model_routing, dict) else {}
    if task_routes:
        return {
            str(name): str(meta.get("selected_profile") or "")
            for name, meta in task_routes.items()
            if isinstance(meta, dict)
        }
    task_classes = (routing_spec or {}).get("task_classes", {}) if isinstance(routing_spec, dict) else {}
    return {
        str(name): str((meta or {}).get("profile") or name)
        for name, meta in task_classes.items()
        if isinstance(meta, dict)
    }


def catalog_snapshot(live_models: dict[str, dict], source: str, status: str = "available") -> dict:
    return {
        "last_checked_utc": now_utc(),
        "catalog_source": source,
        "catalog_check_status": status,
        "discovered_models": live_models,
    }


def compare_catalog(model_routing: dict, live_models: dict[str, dict], routing_spec: dict | None = None) -> dict:
    profiles = configured_profiles(model_routing, routing_spec)
    task_routes = configured_task_classes(model_routing, routing_spec)
    policy = model_routing.get("model_policy", {}) if isinstance(model_routing, dict) else {}
    configured_models = {str(meta.get("model") or "").strip() for meta in profiles.values()}
    configured_models.discard("")
    discovered = set(live_models)

    missing_configured_models = sorted(configured_models - discovered) if live_models else []
    new_candidate_models = sorted(discovered - configured_models)
    unsupported_reasoning: list[dict] = []
    for profile_name, meta in profiles.items():
        model = str(meta.get("model") or "").strip()
        live = live_models.get(model, {}) if live_models else {}
        supported = set(live.get("supported_reasoning_efforts", []))
        for field in ["reasoning_effort", "plan_mode_reasoning_effort"]:
            effort = str(meta.get(field) or "").strip()
            if live_models and effort and effort not in supported:
                unsupported_reasoning.append(
                    {
                        "profile": profile_name,
                        "model": model,
                        "field": field,
                        "effort": effort,
                        "supported_reasoning_efforts": sorted(supported),
                    }
                )

    profiles_that_can_be_upgraded: list[dict] = []
    candidate_order = list(policy.get("promotion_policy", {}).get("candidate_order", []))
    if live_models and candidate_order:
        ranked = [model for model in candidate_order if model in live_models]
        best = ranked[0] if ranked else ""
        for profile_name, meta in profiles.items():
            current = str(meta.get("model") or "").strip()
            if best and current != best and not meta.get("manual_review_required"):
                profiles_that_can_be_upgraded.append(
                    {
                        "profile": profile_name,
                        "current_model": current,
                        "candidate_model": best,
                        "manual_review_required": True,
                    }
                )

    profile_names = set(profiles)
    task_class_errors = [
        {"task_class": task_class, "selected_profile": profile}
        for task_class, profile in sorted(task_routes.items())
        if profile not in profile_names
    ]
    manual_review_profiles = sorted(
        name for name, meta in profiles.items() if bool(meta.get("manual_review_required", False))
    )
    return {
        "missing_configured_models": missing_configured_models,
        "unsupported_reasoning": unsupported_reasoning,
        "new_candidate_models": new_candidate_models,
        "profiles_that_can_be_upgraded": profiles_that_can_be_upgraded,
        "profiles_requiring_manual_review": manual_review_profiles,
        "task_class_profile_errors": task_class_errors,
    }
