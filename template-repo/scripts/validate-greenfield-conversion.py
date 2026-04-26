#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


GREENFIELD_REQUIRED = [
    "greenfield/vision.md",
    "greenfield/problem-statement.md",
    "greenfield/scope-v1.md",
    "greenfield/architecture-options.md",
    "greenfield/initial-task-list.md",
]
CORE_REQUIRED = [
    "AGENTS.md",
    "template-repo/scenario-pack/00-master-router.md",
    ".chatgpt/project-profile.yaml",
    ".chatgpt/stage-state.yaml",
    "template-repo/tree-contract.yaml",
    "template-repo/mode-parity.yaml",
]
CONVERSION_GATES = [
    "repo_first_core_present",
    "master_router_present",
    "scenario_pack_accessible",
    "active_project_profile_updated_to_greenfield_product",
    "lifecycle_state_greenfield_converted",
    "greenfield_required_artifacts_present",
    "brownfield_evidence_archived_or_referenced",
    "project_owned_zones_protected",
    "template_owned_zones_marked",
    "sync_manifest_safe_for_downstream",
    "validators_green",
]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Не найден файл: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"YAML должен быть mapping: {path}")
    return data


def add_missing(root: Path, paths: list[str], label: str, errors: list[str]) -> None:
    for rel_path in paths:
        if not (root / rel_path).exists():
            errors.append(f"{label}: отсутствует путь `{rel_path}`")


def nested_get(data: dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def is_factory_root(root: Path) -> bool:
    return (root / "FACTORY_MANIFEST.yaml").exists() and (root / "template-repo").is_dir()


def validate_factory_contract(root: Path, errors: list[str]) -> None:
    tree = load_yaml(root / "template-repo" / "tree-contract.yaml")
    parity = load_yaml(root / "template-repo" / "mode-parity.yaml")
    tree_gates = set(tree.get("conversion_gates", []) or [])
    parity_gates = set(parity.get("conversion_gates", []) or [])
    required = set(CONVERSION_GATES)
    missing_tree = sorted(required - tree_gates)
    missing_parity = sorted(required - parity_gates)
    if missing_tree:
        errors.append(f"tree-contract conversion_gates missing: {', '.join(missing_tree)}")
    if missing_parity:
        errors.append(f"mode-parity conversion_gates missing: {', '.join(missing_parity)}")
    structures = tree.get("project_structures", {}) or {}
    converted = structures.get("converted_greenfield", {}) or {}
    if converted.get("active_project_preset") != "greenfield-product":
        errors.append("project_structures.converted_greenfield must target greenfield-product")


def validate_generated(root: Path, require_converted: bool, errors: list[str]) -> None:
    add_missing(root, CORE_REQUIRED + GREENFIELD_REQUIRED, "greenfield-conversion", errors)
    profile = load_yaml(root / ".chatgpt" / "project-profile.yaml")
    stage = load_yaml(root / ".chatgpt" / "stage-state.yaml")
    preset = str(profile.get("project_preset", "")).strip()
    mode = str(profile.get("recommended_mode", "")).strip()
    lifecycle_state = str(
        nested_get(stage, "lifecycle", "lifecycle_state")
        or profile.get("lifecycle_state")
        or ""
    ).strip()

    if preset != "greenfield-product":
        errors.append(f"project_preset must be greenfield-product, got `{preset}`")
    if mode != "greenfield":
        errors.append(f"recommended_mode must be greenfield, got `{mode}`")
    allowed_states = {"greenfield-active", "greenfield-converted"}
    if lifecycle_state not in allowed_states:
        errors.append(f"lifecycle_state must be greenfield-active or greenfield-converted, got `{lifecycle_state}`")
    if require_converted and lifecycle_state != "greenfield-converted":
        errors.append("converted validation requires lifecycle_state: greenfield-converted")

    if lifecycle_state == "greenfield-converted" or require_converted:
        if not (root / "brownfield").exists():
            errors.append("converted greenfield must retain brownfield/ as historical evidence or reference")
        protected_markers = [
            root / ".chatgpt" / "project-owned-zones.yaml",
            root / "brownfield" / "risks-and-constraints.md",
            root / "brownfield" / "gap-register.md",
        ]
        if not any(path.exists() for path in protected_markers):
            errors.append("converted greenfield must record protected project-owned/brownfield history zones")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate greenfield-product conversion gates.")
    parser.add_argument("root", nargs="?", default=".", help="Factory root or generated project root.")
    parser.add_argument("--require-converted", action="store_true", help="Require lifecycle_state greenfield-converted.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []
    if is_factory_root(root):
        validate_factory_contract(root, errors)
    else:
        validate_generated(root, args.require_converted, errors)

    if errors:
        print("GREENFIELD CONVERSION НЕ ПРОЙДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"GREENFIELD CONVERSION ПРОЙДЕН: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
