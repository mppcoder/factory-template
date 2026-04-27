#!/usr/bin/env python3
from __future__ import annotations

import json
import argparse
from pathlib import Path

import yaml

from codex_model_catalog import (
    compare_catalog,
    configured_profiles,
    configured_task_classes,
    load_live_catalog,
    load_model_routing,
)


REQUIRED_FIELDS = [
    "launch_source",
    "task_class",
    "selected_profile",
    "selected_model",
    "selected_reasoning_effort",
    "selected_plan_mode_reasoning_effort",
    "apply_mode",
    "strict_launch_mode",
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
    "## Self-handoff для прямой задачи",
    "## Классификация",
    "## Выбранный профиль проекта",
    "## Выбранный сценарий",
    "## Текущий этап pipeline",
    "## Режим применения",
    "## Ручное применение через UI",
    "## Строгий режим запуска",
    "## Артефакты для обновления",
    "## Разрешение handoff",
    "## Маршрут defect-capture",
    "## Опциональная команда строгого запуска",
    "## Прямая команда Codex за launcher",
    "## Диагностика проблем",
    "## Следующий шаг",
]

DOC_CHECKS = [
    {
        "paths": ["README.md"],
        "snippets": [
            ["advisory", "advisory layer"],
            ["manual-ui (default)", "manual-ui"],
            ["model availability auto-check", "codex-model-routing.yaml"],
            ["новый чат + вставка handoff"],
            ["./scripts/launch-codex-task.sh", "launcher-команда"],
        ],
    },
    {
        "paths": ["scenario-pack/00-master-router.md"],
        "snippets": [
            ["Надежная единица маршрутизации"],
            ["новый task launch"],
            ["manual-ui (default)"],
            ["advisory слой сам по себе"],
        ],
    },
    {
        "paths": ["scenario-pack/15-handoff-to-codex.md"],
        "snippets": [
            ["manual-ui (default)"],
            ["strict_launch_mode"],
            ["live catalog"],
            ["sticky"],
        ],
    },
    {
        "paths": [
            "template/docs/codex-workflow.md",
            "docs/codex-workflow.md",
            "template-repo/template/docs/codex-workflow.md",
        ],
        "snippets": [
            ["manual-ui (default)"],
            ["model availability auto-check", "codex-model-routing.yaml"],
            ["надежная единица маршрутизации: новый task launch"],
            ["./scripts/launch-codex-task.sh"],
            ["sticky last-used state"],
        ],
    },
    {
        "paths": [
            "template/docs/integrations.md",
            "docs/integrations.md",
            "template-repo/template/docs/integrations.md",
        ],
        "snippets": [
            ["advisory layer"],
            ["live Codex catalog", "codex-model-routing.yaml"],
            ["manual-ui (default)"],
            ["новый task launch"],
            ["sticky last-used state"],
        ],
    },
]


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


def find_repo_file_any(root: Path, rel_paths: list[str]) -> Path | None:
    for rel_path in rel_paths:
        resolved = find_repo_file(root, rel_path)
        if resolved is not None:
            return resolved
    return None


def load_routing_spec(root: Path) -> tuple[dict, Path | None]:
    for rel in ["codex-routing.yaml", "template-repo/codex-routing.yaml"]:
        path = root / rel
        if path.exists():
            return load_yaml(path), path
    return {}, None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Codex routing and model mapping.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root")
    parser.add_argument("--strict", action="store_true", help="Fail if live catalog is unavailable or mapped models are missing")
    parser.add_argument("--catalog-fixture", help="JSON/YAML fixture for live catalog validation")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
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
    model_routing, model_routing_path = load_model_routing(root)
    profiles = spec.get("profiles", {}) or {}
    task_classes = spec.get("task_classes", {}) or {}
    if not spec_path:
        errors.append("Не найден codex-routing.yaml")
    if not profiles:
        errors.append("codex-routing.yaml не содержит profiles")
    if not model_routing_path.exists():
        errors.append("Не найден codex-model-routing.yaml")

    model_profiles = configured_profiles(model_routing, spec)
    model_task_routes = configured_task_classes(model_routing, spec)
    allowed_profiles = set((model_routing.get("model_policy", {}) or {}).get("allowed_profiles", []))
    if allowed_profiles and set(model_profiles) - allowed_profiles:
        errors.append("codex-model-routing.yaml содержит profile вне model_policy.allowed_profiles")
    for task_class, profile_name in model_task_routes.items():
        if profile_name not in model_profiles:
            errors.append(
                f"codex-model-routing.yaml task_class_routing.{task_class} ссылается на отсутствующий profile `{profile_name}`"
            )
    for profile_name, model_profile in model_profiles.items():
        spec_profile = profiles.get(profile_name, {})
        if not spec_profile:
            errors.append(f"codex-model-routing.yaml profile `{profile_name}` отсутствует в codex-routing.yaml")
            continue
        if str(spec_profile.get("model", "")) != str(model_profile.get("model", "")):
            errors.append(f"profiles.{profile_name}.model не совпадает с codex-model-routing.yaml")
        if str(spec_profile.get("reasoning_effort", "")) != str(model_profile.get("reasoning_effort", "")):
            errors.append(f"profiles.{profile_name}.reasoning_effort не совпадает с codex-model-routing.yaml")
        if str(spec_profile.get("plan_mode_reasoning_effort", "")) != str(model_profile.get("plan_mode_reasoning_effort", "")):
            errors.append(f"profiles.{profile_name}.plan_mode_reasoning_effort не совпадает с codex-model-routing.yaml")
    for task_class, meta in task_classes.items():
        profile_name = str((meta or {}).get("profile") or task_class)
        if profile_name not in profiles:
            errors.append(f"task_classes.{task_class} ссылается на отсутствующий profile `{profile_name}`")

    fixture = Path(args.catalog_fixture).resolve() if args.catalog_fixture else None
    live_models, _source, live_models_error = load_live_catalog(fixture)
    if live_models_error:
        warnings.append(live_models_error)
        if args.strict:
            errors.append("strict mode: live model catalog unavailable")
    catalog_findings = compare_catalog(model_routing, live_models, spec)
    for item in catalog_findings["task_class_profile_errors"]:
        errors.append(f"task class `{item['task_class']}` maps to missing profile `{item['selected_profile']}`")
    for model in catalog_findings["missing_configured_models"]:
        message = f"configured selected_model `{model}` отсутствует в live `codex debug models`"
        if args.strict:
            errors.append(message)
        else:
            warnings.append(message)
    for item in catalog_findings["unsupported_reasoning"]:
        errors.append(
            f"profiles.{item['profile']} использует {item['field']} `{item['effort']}`, не поддерживаемый model `{item['model']}`"
        )

    for profile_name, profile in model_profiles.items():
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
            supported = {str(item or '').strip() for item in live.get("supported_reasoning_efforts", [])}
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
            for section in [
                "## Применение в Codex UI",
                "## Строгий launch mode (опционально)",
                "## Handoff в Codex",
            ]:
                if section not in direct_response_text:
                    errors.append(f"direct-task response не содержит publishable section `{section}`")
            if "Не завершай ответ только self-handoff block" not in direct_response_text:
                errors.append("direct-task response не содержит запрет остановки на self-handoff без продолжения")
            if "## Инструкция пользователю" not in direct_response_text:
                errors.append("direct-task response не содержит обязательное упоминание финального блока `## Инструкция пользователю`")
            if "Внешних действий не требуется." not in direct_response_text:
                errors.append("direct-task response не содержит обязательную формулу для closeout без внешних действий")
            if "Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью." not in direct_response_text:
                errors.append("direct-task response не содержит обязательный continuation outcome для fully done closeout")

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
        if str(expected.get("plan_mode_reasoning_effort", "")) != str(launch.get("selected_plan_mode_reasoning_effort", "")):
            errors.append("selected_plan_mode_reasoning_effort в task-launch.yaml не совпадает с plan reasoning выбранного profile")
    if profile and profile in model_profiles:
        expected_model = model_profiles[profile]
        if str(expected_model.get("model", "")) != str(launch.get("selected_model", "")):
            errors.append("selected_model в task-launch.yaml не совпадает с codex-model-routing.yaml")
        if str(expected_model.get("reasoning_effort", "")) != str(launch.get("selected_reasoning_effort", "")):
            errors.append("selected_reasoning_effort в task-launch.yaml не совпадает с codex-model-routing.yaml")
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

    for check in DOC_CHECKS:
        rel_paths = check.get("paths", [])
        snippets_groups = check.get("snippets", [])
        doc_path = find_repo_file_any(root, rel_paths)
        if doc_path is None:
            joined = ", ".join(f"`{item}`" for item in rel_paths)
            errors.append(f"Не найден source-facing routing doc (ожидался один из: {joined})")
            continue
        doc_text = doc_path.read_text(encoding="utf-8", errors="ignore")
        doc_text_lower = doc_text.lower()
        for group in snippets_groups:
            alternatives = group if isinstance(group, list) else [group]
            if not any(fragment.lower() in doc_text_lower for fragment in alternatives):
                expected = " / ".join(f"`{fragment}`" for fragment in alternatives)
                errors.append(f"{doc_path}: отсутствует обязательный routing fragment (любой из: {expected})")

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
