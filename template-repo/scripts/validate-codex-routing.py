#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


REQUIRED_FIELDS = [
    "launch_source",
    "task_class",
    "selected_profile",
    "selected_model",
    "selected_reasoning_effort",
    "project_profile",
    "selected_scenario",
    "pipeline_stage",
    "artifacts_to_update",
    "handoff_allowed",
    "defect_capture_path",
    "launch_artifact_path",
    "launch_command",
    "codex_profile_command",
]

DIRECT_TASK_RESPONSE_SECTIONS = [
    "## Direct Task Self-Handoff",
    "## Classification",
    "## Selected project profile",
    "## Selected scenario",
    "## Current pipeline stage",
    "## Artifacts to update",
    "## Handoff allowed",
    "## Defect capture path",
    "## Executable launch command",
    "## Direct Codex command behind launcher",
    "## Troubleshooting",
    "## Next step",
]

DOC_CHECKS = {
    "README.md": [
        "advisory",
        "новом task launch",
        "./scripts/launch-codex-task.sh",
    ],
    "scenario-pack/00-master-router.md": [
        "Надежная единица маршрутизации",
        "новый task launch",
        "advisory слой сам по себе",
    ],
    "scenario-pack/15-handoff-to-codex.md": [
        "явный launch command",
        "advisory layer не переключает",
        "sticky",
    ],
    "template/docs/codex-workflow.md": [
        "надежная единица маршрутизации: новый task launch",
        "./scripts/launch-codex-task.sh",
        "sticky last-used state",
    ],
    "template/docs/integrations.md": [
        "advisory layer",
        "новый task launch",
        "sticky last-used state",
    ],
}


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
    return data if isinstance(data, dict) else {}


def find_repo_file(root: Path, rel_path: str) -> Path | None:
    candidates = [
        root / "template-repo" / rel_path,
        root / rel_path,
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def load_routing_spec(root: Path) -> tuple[dict, Path | None]:
    for rel in ["codex-routing.yaml", "template-repo/codex-routing.yaml"]:
        path = root / rel
        if path.exists():
            return load_yaml(path), path
    return {}, None


def load_live_model_catalog() -> tuple[dict[str, dict], str | None]:
    if shutil.which("codex") is None:
        return {}, "CLI `codex` не найден; live model catalog не проверен"
    try:
        result = subprocess.run(
            ["codex", "debug", "models"],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
    except Exception as exc:  # pragma: no cover - defensive
        return {}, f"Не удалось прочитать live model catalog через `codex debug models`: {exc}"

    models = {}
    for model in payload.get("models", []):
        slug = str(model.get("slug") or "").strip()
        if not slug:
            continue
        models[slug] = model
    return models, None


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    path = root / ".chatgpt" / "task-launch.yaml"
    if not path.exists():
        print("CODEX ROUTING НЕВАЛИДЕН")
        print("- Не найден .chatgpt/task-launch.yaml")
        return 1

    data = load_yaml(path)
    launch = data.get("launch", {})
    errors: list[str] = []
    warnings: list[str] = []
    for field in REQUIRED_FIELDS:
        if not launch.get(field):
            errors.append(f"Отсутствует обязательное поле launch.{field}")

    spec, spec_path = load_routing_spec(root)
    profiles = spec.get("profiles", {}) or {}
    task_classes = spec.get("task_classes", {}) or {}
    if not spec_path:
        errors.append("Не найден codex-routing.yaml")
    if not profiles:
        errors.append("codex-routing.yaml не содержит profiles")
    for task_class, meta in task_classes.items():
        profile_name = str((meta or {}).get("profile") or task_class)
        if profile_name not in profiles:
            errors.append(f"task_classes.{task_class} ссылается на отсутствующий profile `{profile_name}`")

    live_models, live_models_error = load_live_model_catalog()
    if live_models_error:
        warnings.append(live_models_error)
    for profile_name, profile in profiles.items():
        model = str(profile.get("model") or "").strip()
        reasoning = str(profile.get("reasoning_effort") or "").strip()
        plan_reasoning = str(profile.get("plan_mode_reasoning_effort") or "").strip()
        if not model:
            errors.append(f"profiles.{profile_name} не содержит model")
            continue
        if live_models:
            live = live_models.get(model)
            if live is None:
                errors.append(f"profiles.{profile_name} использует model `{model}`, которого нет в live `codex debug models`")
                continue
            supported = {str(item.get('effort') or '').strip() for item in live.get("supported_reasoning_levels", [])}
            if reasoning and reasoning not in supported:
                errors.append(
                    f"profiles.{profile_name} использует reasoning `{reasoning}`, не поддерживаемый model `{model}`"
                )
            if plan_reasoning and plan_reasoning not in supported:
                errors.append(
                    f"profiles.{profile_name} использует plan reasoning `{plan_reasoning}`, не поддерживаемый model `{model}`"
                )

    if launch.get("launch_source") == "direct-task":
        self_handoff = root / ".chatgpt" / "direct-task-self-handoff.md"
        if not self_handoff.exists():
            errors.append("Для direct-task отсутствует .chatgpt/direct-task-self-handoff.md")
        if not launch.get("direct_self_handoff_completed"):
            errors.append("Для direct-task не отмечен direct_self_handoff_completed")
        direct_response = root / ".chatgpt" / "direct-task-response.md"
        if not direct_response.exists():
            errors.append("Для direct-task отсутствует .chatgpt/direct-task-response.md")
        else:
            direct_response_text = direct_response.read_text(encoding="utf-8")
            for section in DIRECT_TASK_RESPONSE_SECTIONS:
                if section not in direct_response_text:
                    errors.append(f"direct-task response не содержит обязательный раздел `{section}`")

    normalized = root / ".chatgpt" / "normalized-codex-handoff.md"
    if not normalized.exists():
        errors.append("Отсутствует .chatgpt/normalized-codex-handoff.md")

    profile = str(launch.get("selected_profile", ""))
    launch_command = str(launch.get("launch_command", ""))
    codex_profile_command = str(launch.get("codex_profile_command", ""))
    launch_artifact = str(launch.get("launch_artifact_path", ""))
    if profile and profile not in profiles:
        errors.append(f"selected_profile `{profile}` отсутствует в codex-routing.yaml")
    if profile and profile in profiles:
        expected = profiles[profile]
        if str(expected.get("model", "")) != str(launch.get("selected_model", "")):
            errors.append("selected_model в task-launch.yaml не совпадает с model выбранного profile")
        if str(expected.get("reasoning_effort", "")) != str(launch.get("selected_reasoning_effort", "")):
            errors.append("selected_reasoning_effort в task-launch.yaml не совпадает с reasoning выбранного profile")
    if "launch-codex-task.sh" not in launch_command:
        errors.append("launch_command не фиксирует repo launcher")
    if launch.get("launch_source") and f"--launch-source {launch.get('launch_source')}" not in launch_command:
        errors.append("launch_command не фиксирует launch_source")
    if launch_artifact and launch_artifact not in launch_command:
        errors.append("launch_command не фиксирует launch_artifact_path")
    if launch_artifact and not (root / launch_artifact).exists():
        errors.append(f"launch_artifact_path `{launch_artifact}` не существует в repo")
    if profile and f"--profile {profile}" not in codex_profile_command:
        errors.append("codex_profile_command не фиксирует selected_profile через --profile")

    for rel_path, snippets in DOC_CHECKS.items():
        doc_path = find_repo_file(root, rel_path)
        if doc_path is None:
            errors.append(f"Не найден source-facing routing doc `{rel_path}`")
            continue
        doc_text = doc_path.read_text(encoding="utf-8", errors="ignore")
        for snippet in snippets:
            if snippet not in doc_text:
                errors.append(f"{doc_path}: отсутствует обязательный routing fragment `{snippet}`")

    if errors:
        print("CODEX ROUTING НЕВАЛИДЕН")
        for error in errors:
            print("-", error)
        for warning in warnings:
            print("-", f"WARNING: {warning}")
        return 1

    print("CODEX ROUTING ВАЛИДЕН")
    for warning in warnings:
        print("-", f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
