#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Не найден файл: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"YAML должен быть mapping: {path}")
    return data


def find_manifest(root: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    for candidate in (
        root / "template-repo" / "mode-parity.yaml",
        root / "mode-parity.yaml",
        Path(__file__).resolve().parents[1] / "mode-parity.yaml",
    ):
        if candidate.exists():
            return candidate
    raise SystemExit("Не найден mode-parity.yaml")


def find_presets(root: Path) -> Path | None:
    for candidate in (root / "template-repo" / "project-presets.yaml", root / "project-presets.yaml"):
        if candidate.exists():
            return candidate
    return None


def is_factory_root(root: Path) -> bool:
    return (root / "FACTORY_MANIFEST.yaml").exists() and (root / "template-repo" / "template").exists()


def add_missing(root: Path, paths: list[str], label: str, errors: list[str]) -> None:
    for rel_path in paths:
        if not (root / rel_path).exists():
            errors.append(f"{label}: отсутствует путь `{rel_path}`")


def validate_manifest_shape(manifest: dict[str, Any], errors: list[str]) -> None:
    core_ids = manifest.get("core_capability_ids", []) or []
    core = manifest.get("core_capabilities", {}) or {}
    modes = manifest.get("modes", {}) or {}
    differences = manifest.get("mode_specific_capabilities", {}) or {}
    states = ((manifest.get("lifecycle_state_model", {}) or {}).get("states", {}) or {})
    required_states = {
        "greenfield-active",
        "brownfield-without-repo-intake",
        "brownfield-without-repo-reconstruction",
        "brownfield-with-repo-audit",
        "brownfield-with-repo-adoption",
        "brownfield-to-greenfield-conversion",
        "greenfield-converted",
    }
    missing_states = sorted(required_states - set(states))
    if missing_states:
        errors.append(f"lifecycle_state_model.states отсутствуют: {', '.join(missing_states)}")

    if not core_ids:
        errors.append("core_capability_ids пуст")
    if set(core_ids) != set(core):
        errors.append("core_capability_ids не совпадает с ключами core_capabilities")
    for capability_id, capability in core.items():
        if not isinstance(capability, dict):
            errors.append(f"core_capabilities.{capability_id} должен быть mapping")
            continue
        if not capability.get("justification"):
            errors.append(f"core_capabilities.{capability_id}: нет justification")
        if not capability.get("generated_paths"):
            errors.append(f"core_capabilities.{capability_id}: нет generated_paths")
        if not capability.get("source_paths"):
            errors.append(f"core_capabilities.{capability_id}: нет source_paths")

    for diff_id, diff in differences.items():
        if not isinstance(diff, dict):
            errors.append(f"mode_specific_capabilities.{diff_id} должен быть mapping")
            continue
        if not diff.get("justification"):
            errors.append(f"mode_specific_capabilities.{diff_id}: нет justification")
        if not diff.get("required_paths"):
            errors.append(f"mode_specific_capabilities.{diff_id}: нет required_paths")

    if "template-base" not in modes:
        errors.append("modes.template-base отсутствует")

    expected_core = list(core_ids)
    for mode_name, mode in modes.items():
        if not isinstance(mode, dict):
            errors.append(f"modes.{mode_name} должен быть mapping")
            continue
        actual_core = mode.get("core_capabilities", []) or []
        if actual_core != expected_core:
            errors.append(f"modes.{mode_name}: core_capabilities отличается от canonical списка")
        for diff_id in mode.get("allowed_differences", []) or []:
            if diff_id not in differences:
                errors.append(f"modes.{mode_name}: неизвестная allowed difference `{diff_id}`")
        for state in mode.get("lifecycle_states", []) or []:
            if state not in states:
                errors.append(f"modes.{mode_name}: неизвестный lifecycle state `{state}`")
        if mode.get("transitional"):
            if mode.get("target_project_preset") != "greenfield-product":
                errors.append(f"modes.{mode_name}: transitional mode должен иметь target_project_preset greenfield-product")
            if mode.get("target_lifecycle_state") != "greenfield-converted":
                errors.append(f"modes.{mode_name}: transitional mode должен иметь target_lifecycle_state greenfield-converted")
            if mode.get("conversion_required") is not True:
                errors.append(f"modes.{mode_name}: transitional mode должен иметь conversion_required: true")


def validate_factory_sources(root: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    template_root = root / "template-repo" / "template"
    add_missing(root, ["docs/mode-parity-matrix.md", "template-repo/mode-parity.yaml"], "factory", errors)
    add_missing(template_root, (manifest.get("modes", {}) or {}).get("template-base", {}).get("required_paths", []) or [], "template-base", errors)

    for capability_id, capability in (manifest.get("core_capabilities", {}) or {}).items():
        add_missing(root, capability.get("source_paths", []) or [], f"core:{capability_id}", errors)

    for diff_id, diff in (manifest.get("mode_specific_capabilities", {}) or {}).items():
        add_missing(template_root, diff.get("required_paths", []) or [], f"mode-specific:{diff_id}", errors)


def validate_presets(root: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    presets_path = find_presets(root)
    if not presets_path:
        errors.append("project-presets.yaml не найден")
        return

    data = load_yaml(presets_path)
    presets = data.get("project_presets", {}) or {}
    modes = manifest.get("modes", {}) or {}
    required_core = set(manifest.get("all_presets_required_artifacts", []) or [])
    seen_presets: dict[str, str] = {}

    for mode_name, mode in modes.items():
        if mode.get("kind") != "generated":
            continue
        for preset_name in mode.get("presets", []) or []:
            if preset_name in seen_presets:
                errors.append(f"preset `{preset_name}` объявлен в двух parity modes: {seen_presets[preset_name]} и {mode_name}")
            seen_presets[preset_name] = mode_name
            preset = presets.get(preset_name)
            if not isinstance(preset, dict):
                errors.append(f"preset `{preset_name}` отсутствует в project-presets.yaml")
                continue
            if preset.get("parity_mode") != mode_name:
                errors.append(f"preset `{preset_name}` должен иметь parity_mode: {mode_name}")
            artifacts = set(preset.get("required_artifacts", []) or [])
            missing = sorted(required_core - artifacts)
            if missing:
                errors.append(f"preset `{preset_name}` не содержит core required_artifacts: {', '.join(missing)}")
            for diff_id in mode.get("allowed_differences", []) or []:
                diff = (manifest.get("mode_specific_capabilities", {}) or {}).get(diff_id, {}) or {}
                missing_diff = sorted(set(diff.get("required_paths", []) or []) - artifacts)
                if missing_diff:
                    errors.append(f"preset `{preset_name}` не содержит mode-specific artifacts для {diff_id}: {', '.join(missing_diff)}")

    extra = sorted(set(presets) - set(seen_presets))
    if extra:
        errors.append(f"project-presets.yaml содержит presets без parity mode: {', '.join(extra)}")


def validate_docs(root: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    docs_path = root / "docs" / "mode-parity-matrix.md"
    if not docs_path.exists():
        errors.append("docs: отсутствует docs/mode-parity-matrix.md")
        return
    text = docs_path.read_text(encoding="utf-8")
    for capability_id in manifest.get("core_capability_ids", []) or []:
        if capability_id not in text:
            errors.append(f"docs/mode-parity-matrix.md не содержит capability `{capability_id}`")
    for mode_name in (manifest.get("modes", {}) or {}):
        if mode_name != "template-base" and mode_name not in text:
            errors.append(f"docs/mode-parity-matrix.md не содержит mode `{mode_name}`")


def generated_mode_for(root: Path, manifest: dict[str, Any], errors: list[str]) -> tuple[str | None, dict[str, Any] | None]:
    profile_path = root / ".chatgpt" / "project-profile.yaml"
    if not profile_path.exists():
        errors.append("generated: отсутствует .chatgpt/project-profile.yaml")
        return None, None
    profile = load_yaml(profile_path)
    preset = str(profile.get("project_preset", "")).strip()
    for mode_name, mode in (manifest.get("modes", {}) or {}).items():
        if preset in (mode.get("presets", []) or []):
            return mode_name, mode
    errors.append(f"generated: preset `{preset}` не найден в mode-parity.yaml")
    return None, None


def validate_generated_project(root: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    mode_name, mode = generated_mode_for(root, manifest, errors)
    if not mode_name or not mode:
        return
    for capability_id in manifest.get("core_capability_ids", []) or []:
        capability = (manifest.get("core_capabilities", {}) or {}).get(capability_id, {}) or {}
        add_missing(root, capability.get("generated_paths", []) or [], f"generated:{mode_name}:{capability_id}", errors)
    for diff_id in mode.get("allowed_differences", []) or []:
        diff = (manifest.get("mode_specific_capabilities", {}) or {}).get(diff_id, {}) or {}
        add_missing(root, diff.get("required_paths", []) or [], f"generated:{mode_name}:{diff_id}", errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mode parity across template and generated project modes.")
    parser.add_argument("root", nargs="?", default=".", help="Factory root or generated project root.")
    parser.add_argument("--manifest", help="Explicit path to mode-parity.yaml.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    manifest_path = find_manifest(root, args.manifest)
    manifest = load_yaml(manifest_path)
    errors: list[str] = []

    validate_manifest_shape(manifest, errors)
    if is_factory_root(root):
        validate_factory_sources(root, manifest, errors)
        validate_presets(root, manifest, errors)
        validate_docs(root, manifest, errors)
    else:
        validate_generated_project(root, manifest, errors)

    if errors:
        print("MODE PARITY НЕ ПРОЙДЕН")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"MODE PARITY ПРОЙДЕН: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
