#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


BROWNFIELD_WITHOUT_REPO_PRESETS = {"brownfield-without-repo"}
BROWNFIELD_WITH_REPO_PRESETS = {
    "brownfield-with-repo-modernization",
    "brownfield-with-repo-integration",
    "brownfield-with-repo-audit",
}
BROWNFIELD_PRESETS = BROWNFIELD_WITHOUT_REPO_PRESETS | BROWNFIELD_WITH_REPO_PRESETS
TRANSITION_STATES = {
    "brownfield-without-repo-intake",
    "brownfield-without-repo-reconstruction",
    "brownfield-with-repo-audit",
    "brownfield-with-repo-adoption",
    "brownfield-to-greenfield-conversion",
}


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
    structures = tree.get("project_structures", {}) or {}
    for key in ("transitional_brownfield_without_repo", "transitional_brownfield_with_repo", "converted_greenfield"):
        if key not in structures:
            errors.append(f"tree-contract: отсутствует project_structures.{key}")
    states = parity.get("lifecycle_state_model", {}).get("states", {}) or {}
    for state in TRANSITION_STATES | {"greenfield-converted"}:
        if state not in states:
            errors.append(f"mode-parity: отсутствует lifecycle state `{state}`")


def validate_generated(root: Path, args: argparse.Namespace, errors: list[str]) -> None:
    profile = load_yaml(root / ".chatgpt" / "project-profile.yaml")
    stage = load_yaml(root / ".chatgpt" / "stage-state.yaml")
    preset = str(profile.get("project_preset", "")).strip()
    lifecycle_state = str(
        nested_get(stage, "lifecycle", "lifecycle_state")
        or profile.get("lifecycle_state")
        or ""
    ).strip()
    target_preset = str(profile.get("target_project_preset", "")).strip()
    target_state = str(
        nested_get(stage, "lifecycle", "target_lifecycle_state")
        or profile.get("target_lifecycle_state")
        or ""
    ).strip()
    conversion_required = bool(
        nested_get(stage, "lifecycle", "conversion_required")
        or profile.get("conversion_required")
    )

    if args.without_repo and preset not in BROWNFIELD_WITHOUT_REPO_PRESETS:
        errors.append(f"expected brownfield-without-repo preset, got `{preset}`")
    elif args.with_repo and preset not in BROWNFIELD_WITH_REPO_PRESETS:
        errors.append(f"expected brownfield-with-repo preset, got `{preset}`")
    elif not args.without_repo and not args.with_repo and preset not in BROWNFIELD_PRESETS:
        errors.append(f"expected brownfield transition preset, got `{preset}`")

    if lifecycle_state not in TRANSITION_STATES:
        errors.append(f"lifecycle_state must be transitional brownfield state, got `{lifecycle_state}`")
    if target_preset != "greenfield-product":
        errors.append("target_project_preset must be greenfield-product")
    if target_state != "greenfield-converted":
        errors.append("target_lifecycle_state must be greenfield-converted")
    if not conversion_required:
        errors.append("conversion_required must be true for brownfield transition")

    common = [
        "AGENTS.md",
        "template-repo/scenario-pack/00-master-router.md",
        ".chatgpt/project-profile.yaml",
        ".chatgpt/stage-state.yaml",
        "brownfield/system-inventory.md",
        "brownfield/as-is-architecture.md",
        "brownfield/gap-register.md",
        ".chatgpt/evidence-register.md",
        ".chatgpt/reality-check.md",
    ]
    add_missing(root, common, "brownfield-transition", errors)
    if args.without_repo or preset in BROWNFIELD_WITHOUT_REPO_PRESETS:
        add_missing(
            root,
            [
                "brownfield/reverse-engineering-plan.md",
                "brownfield/reverse-engineering-summary.md",
                "brownfield/decision-log.md",
            ],
            "brownfield-without-repo",
            errors,
        )
    if args.with_repo or preset in BROWNFIELD_WITH_REPO_PRESETS:
        add_missing(
            root,
            [
                "brownfield/repo-audit.md",
                "brownfield/change-map.md",
                "brownfield/risks-and-constraints.md",
                ".chatgpt/conflict-report.md",
            ],
            "brownfield-with-repo",
            errors,
        )

    blocker_paths = [
        root / "brownfield" / "conversion-blocker.md",
        root / ".chatgpt" / "conversion-blocker.md",
    ]
    blocker_recorded = any(path.exists() for path in blocker_paths)
    conversion_ready = target_preset == "greenfield-product" and target_state == "greenfield-converted"
    if not conversion_ready and not blocker_recorded:
        errors.append("brownfield transition must have greenfield conversion target or explicit blocker")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate brownfield transitional adoption state.")
    parser.add_argument("root", nargs="?", default=".", help="Factory root or generated project root.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--without-repo", action="store_true", help="Require brownfield-without-repo transition.")
    group.add_argument("--with-repo", action="store_true", help="Require brownfield-with-repo transition.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []
    if is_factory_root(root):
        validate_factory_contract(root, errors)
    else:
        validate_generated(root, args, errors)

    if errors:
        print("BROWNFIELD TRANSITION НЕ ПРОЙДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"BROWNFIELD TRANSITION ПРОЙДЕН: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
