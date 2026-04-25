#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Не найден файл: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"YAML должен быть mapping: {path}")
    return data


def contract_path_for(root: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    candidates = [
        root / "template-repo" / "tree-contract.yaml",
        root / "tree-contract.yaml",
        Path(__file__).resolve().parents[1] / "tree-contract.yaml",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise SystemExit("Не найден tree-contract.yaml")


def add_missing_paths(root: Path, paths: list[str], label: str, errors: list[str]) -> None:
    for item in paths:
        if not (root / item).exists():
            errors.append(f"{label}: отсутствует обязательный путь: {item}")


def add_forbidden_paths(root: Path, paths: list[str], label: str, errors: list[str]) -> None:
    for item in paths:
        if (root / item).exists():
            errors.append(f"{label}: найден запрещенный путь: {item}")


def is_under_or_same(path: str, allowed: str) -> bool:
    return path == allowed or path.startswith(f"{allowed.rstrip('/')}/")


def iter_repo_paths(root: Path) -> list[str]:
    ignored_parts = {
        ".git",
        ".release-stage",
        ".factory-runtime",
        ".matrix-test",
        ".smoke-test",
        ".bugflow-test",
        ".tmp-run",
        ".pytest_cache",
        "__pycache__",
        "_factory-sync-export",
        "_boundary-actions",
    }
    paths: list[str] = []
    for item in root.rglob("*"):
        relative_parts = item.relative_to(root).parts
        if any(part in ignored_parts for part in relative_parts):
            continue
        paths.append(item.relative_to(root).as_posix())
    return paths


def validate_top_level(root: Path, contour: dict[str, Any], label: str, errors: list[str]) -> None:
    allowed = set(contour.get("allowed_top_level", []) or [])
    if not allowed:
        return
    ignored = set(contour.get("ignored_transient_top_level", []) or [])
    for item in root.iterdir():
        name = item.name
        if name in allowed or name in ignored:
            continue
        errors.append(f"{label}: top-level путь не описан контрактом: {name}")


def validate_path_terms(root: Path, contract: dict[str, Any], errors: list[str]) -> None:
    policy = contract.get("naming_policy", {}) or {}
    terms = policy.get("forbidden_path_terms", {}) or {}
    if not isinstance(terms, dict):
        errors.append("naming_policy.forbidden_path_terms должен быть mapping")
        return
    all_paths = iter_repo_paths(root)
    for term, rule in terms.items():
        allowed = (rule or {}).get("allowed_paths", []) or []
        for path in all_paths:
            if term.lower() not in path.lower():
                continue
            if any(is_under_or_same(path, item) for item in allowed):
                continue
            errors.append(
                f"naming: термин '{term}' найден вне compatibility/optional allowlist: {path}"
            )


def validate_active_ux_literals(root: Path, contract: dict[str, Any], errors: list[str]) -> None:
    policy = contract.get("naming_policy", {}) or {}
    literals = policy.get("compatibility_aliases_forbidden_in_primary_ux", []) or []
    scan_paths = policy.get("active_ux_scan_paths", []) or []
    for rel_path in scan_paths:
        path = root / rel_path
        if not path.exists() or not path.is_file():
            errors.append(f"naming: active UX scan path отсутствует: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for literal in literals:
            if literal in text:
                errors.append(
                    f"naming: legacy alias '{literal}' surfaced in primary UX file {rel_path}"
                )


def alias_target(alias_value: Any) -> str:
    if isinstance(alias_value, str):
        return alias_value
    if isinstance(alias_value, dict):
        return str(alias_value.get("target", ""))
    return ""


def validate_compatibility_aliases(root: Path, contract: dict[str, Any], errors: list[str]) -> None:
    layer = contract.get("compatibility_layer", {}) or {}
    aliases_rel = layer.get("aliases_file", "template-repo/compatibility-aliases.yaml")
    aliases_path = root / aliases_rel
    if not aliases_path.exists():
        errors.append(f"compatibility: отсутствует файл aliases: {aliases_rel}")
        return

    aliases_data = load_yaml(aliases_path)
    if aliases_data.get("compatibility_only") is not True:
        errors.append("compatibility: compatibility-aliases.yaml должен иметь compatibility_only: true")
    aliases = aliases_data.get("preset_aliases", {}) or {}
    canonical = set((contract.get("naming_policy", {}) or {}).get("canonical_project_presets", []) or [])
    forbidden = set(
        (contract.get("naming_policy", {}) or {}).get(
            "compatibility_aliases_forbidden_in_primary_ux", []
        )
        or []
    )
    if set(aliases) != forbidden:
        errors.append("compatibility: preset_aliases должен совпадать со списком forbidden primary UX aliases")
    for alias, value in aliases.items():
        target = alias_target(value)
        if target not in canonical:
            errors.append(f"compatibility: alias {alias} указывает на неизвестный canonical preset: {target}")

    project_presets = root / "template-repo" / "project-presets.yaml"
    if project_presets.exists():
        data = load_yaml(project_presets)
        if "preset_aliases" in data:
            errors.append("compatibility: preset_aliases нельзя держать в template-repo/project-presets.yaml")


def validate_contour(target_root: Path, contour: dict[str, Any], label: str, errors: list[str]) -> None:
    add_missing_paths(target_root, contour.get("root_markers", []) or [], label, errors)
    add_missing_paths(target_root, contour.get("required_paths", []) or [], label, errors)
    add_missing_paths(target_root, contour.get("contour_required_paths", []) or [], label, errors)
    add_forbidden_paths(target_root, contour.get("forbidden_paths", []) or [], label, errors)
    validate_top_level(target_root, contour, label, errors)


def generated_contour_for(root: Path, contract: dict[str, Any]) -> str | None:
    profile_path = root / ".chatgpt" / "project-profile.yaml"
    if not profile_path.exists():
        return None
    profile = load_yaml(profile_path)
    preset = str(profile.get("project_preset", "")).strip()
    for name, contour in (contract.get("contours", {}) or {}).items():
        if not name.startswith("generated_"):
            continue
        if preset in (contour.get("presets", []) or []):
            return name
    return None


def validate_factory_root(root: Path, contract: dict[str, Any], errors: list[str]) -> None:
    contours = contract.get("contours", {}) or {}
    factory = contours.get("factory_root")
    if not isinstance(factory, dict):
        errors.append("contours.factory_root отсутствует или не является mapping")
        return
    validate_contour(root, factory, "factory_root", errors)
    for nested_name in factory.get("validate_nested_contours", []) or []:
        nested = contours.get(nested_name, {}) or {}
        nested_root = root / str(nested.get("relative_root", ""))
        validate_contour(nested_root, nested, nested_name, errors)
    validate_compatibility_aliases(root, contract, errors)
    validate_active_ux_literals(root, contract, errors)
    validate_path_terms(root, contract, errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate factory-template tree contract.")
    parser.add_argument("root", nargs="?", default=".", help="Factory root or generated project root.")
    parser.add_argument("--contract", help="Explicit path to tree-contract.yaml.")
    parser.add_argument("--contour", help="Force a specific contour name.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    contract_path = contract_path_for(root, args.contract)
    contract = load_yaml(contract_path)
    contours = contract.get("contours", {}) or {}
    errors: list[str] = []

    if args.contour:
        contour = contours.get(args.contour)
        if not isinstance(contour, dict):
            errors.append(f"Неизвестный contour: {args.contour}")
        else:
            target_root = root / str(contour.get("relative_root", ""))
            validate_contour(target_root, contour, args.contour, errors)
    elif (root / "FACTORY_MANIFEST.yaml").exists() and (root / "template-repo").exists():
        validate_factory_root(root, contract, errors)
    else:
        contour_name = generated_contour_for(root, contract)
        if contour_name is None:
            errors.append("Не удалось определить contour: это не factory root и не generated project")
        else:
            validate_contour(root, contours[contour_name], contour_name, errors)
            project_aliases = root / "project-presets.yaml"
            if project_aliases.exists() and "preset_aliases" in load_yaml(project_aliases):
                errors.append("generated: project-presets.yaml не должен содержать preset_aliases")
            if not (root / "compatibility-aliases.yaml").exists():
                errors.append("generated: отсутствует compatibility-aliases.yaml")

    if errors:
        print("TREE CONTRACT НЕ ПРОЙДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"TREE CONTRACT ПРОЙДЕН: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
