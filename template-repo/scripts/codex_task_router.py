#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import yaml

from factory_automation_common import now_utc, read_text, read_yaml, write_yaml


def load_routing_spec(root: Path) -> dict:
    spec_path = root / "codex-routing.yaml"
    if not spec_path.exists():
        fallback = root / "template-repo" / "codex-routing.yaml"
        if fallback.exists():
            spec_path = fallback
    data = yaml.safe_load(spec_path.read_text(encoding="utf-8")) if spec_path.exists() else {}
    return data if isinstance(data, dict) else {}


def read_task_text(task_file: Path | None, task_text: str | None) -> str:
    if task_text and task_text.strip():
        return task_text.strip()
    if task_file and task_file.exists():
        return task_file.read_text(encoding="utf-8", errors="ignore").strip()
    return ""


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def parse_structured_handoff(text: str) -> dict:
    if not text.strip():
        return {}
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        data = None
    if isinstance(data, dict):
        return data

    yaml_block: list[str] = []
    in_block = False
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped and not in_block:
            continue
        if stripped.startswith("#") and not in_block:
            continue
        if stripped.startswith("## ") and in_block:
            break
        looks_like_mapping = ":" in line and not stripped.startswith("```")
        looks_like_list_item = bool(yaml_block) and (line.startswith("  - ") or line.startswith("- "))
        if looks_like_mapping or looks_like_list_item or (yaml_block and line.startswith(" ")):
            yaml_block.append(line)
            in_block = True
            continue
        if in_block:
            break
    if yaml_block:
        try:
            data = yaml.safe_load("\n".join(yaml_block))
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict):
            return data

    result: dict[str, object] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        result[key] = value
    return result


def normalize_model_name(model: str) -> str:
    normalized = _normalize(model)
    if "gpt-5.5" in normalized:
        return "gpt-5.5"
    if "gpt-5.4-mini" in normalized:
        return "gpt-5.4-mini"
    if "gpt-5.4" in normalized:
        return "gpt-5.4"
    return normalized


def stringify_override(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value).strip()


def stringify_yes_no_override(value: object) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    text = stringify_override(value)
    lowered = _normalize(text)
    if lowered in {"true", "yes"}:
        return "yes"
    if lowered in {"false", "no"}:
        return "no"
    return text


def explicit_routing_overrides(text: str) -> dict:
    data = parse_structured_handoff(text)
    if not isinstance(data, dict):
        return {}
    overrides: dict[str, object] = {}
    for key in [
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
    ]:
        value = data.get(key)
        if value not in (None, "", []):
            overrides[key] = value
    return overrides


def infer_task_class(spec: dict, text: str, explicit_task_class: str | None = None) -> tuple[str, list[str]]:
    task_classes = spec.get("task_classes", {})
    default_task_class = spec.get("defaults", {}).get("task_class", "build")
    if explicit_task_class:
        if explicit_task_class not in task_classes:
            raise ValueError(f"Неизвестный task class: {explicit_task_class}")
        return explicit_task_class, [f"explicit task class override: {explicit_task_class}"]

    normalized = _normalize(text)
    scores: dict[str, int] = {}
    reasons: dict[str, list[str]] = {}
    for task_class, meta in task_classes.items():
        score = 0
        hits: list[str] = []
        for keyword in meta.get("keywords", []):
            token = _normalize(str(keyword))
            if token and token in normalized:
                score += len(token.split()) + 1
                hits.append(keyword)
        if score:
            scores[task_class] = score
            reasons[task_class] = hits

    if not scores:
        return default_task_class, [f"no keyword hit; fallback to default task class `{default_task_class}`"]

    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    chosen, _score = ordered[0]
    return chosen, [f"keyword hit: {hit}" for hit in reasons.get(chosen, [])]


def selected_profile(spec: dict, task_class: str) -> tuple[str, dict]:
    task_meta = (spec.get("task_classes", {}) or {}).get(task_class, {})
    profile_name = task_meta.get("profile", task_class)
    profile = (spec.get("profiles", {}) or {}).get(profile_name, {})
    if not profile:
        raise ValueError(f"Для task class `{task_class}` не найден profile `{profile_name}`")
    return profile_name, profile


def choose_profile_from_overrides(spec: dict, task_class: str, overrides: dict) -> tuple[str, dict, list[str]] | None:
    profiles = spec.get("profiles", {}) or {}
    requested_profile = str(overrides.get("selected_profile") or "").strip()
    if requested_profile and requested_profile in profiles:
        return requested_profile, profiles[requested_profile], [f"explicit selected_profile override: {requested_profile}"]

    requested_model = normalize_model_name(str(overrides.get("selected_model") or "").strip())
    requested_reasoning = _normalize(str(overrides.get("selected_reasoning_effort") or "").strip())
    requested_plan_reasoning = _normalize(str(overrides.get("selected_plan_mode_reasoning_effort") or "").strip())
    candidates: list[tuple[str, dict]] = []
    for name, profile in profiles.items():
        profile_model = normalize_model_name(str(profile.get("model", "")))
        profile_reasoning = _normalize(str(profile.get("reasoning_effort", "")))
        profile_plan_reasoning = _normalize(str(profile.get("plan_mode_reasoning_effort", "")))
        if requested_model and requested_model != profile_model:
            continue
        if requested_reasoning and requested_reasoning != profile_reasoning:
            continue
        if requested_plan_reasoning and requested_plan_reasoning != profile_plan_reasoning:
            continue
        candidates.append((name, profile))

    if not candidates:
        return None

    task_meta = (spec.get("task_classes", {}) or {}).get(task_class, {})
    default_profile_name = str(task_meta.get("profile", task_class))
    for name, profile in candidates:
        if name == default_profile_name:
            reasons = [
                f"explicit reasoning/model override matched default profile: {name}",
            ]
            return name, profile, reasons

    preferred_order = ["deep", "review", "build", "quick"]
    for preferred in preferred_order:
        for name, profile in candidates:
            if name == preferred:
                reasons = [f"explicit reasoning/model override selected compatible profile: {name}"]
                if requested_profile and requested_profile not in profiles:
                    reasons.append(f"requested profile `{requested_profile}` is not executable in routing spec")
                return name, profile, reasons

    name, profile = candidates[0]
    reasons = [f"explicit reasoning/model override selected compatible profile: {name}"]
    if requested_profile and requested_profile not in profiles:
        reasons.append(f"requested profile `{requested_profile}` is not executable in routing spec")
    return name, profile, reasons


def detect_defect_path(text: str) -> str:
    normalized = _normalize(text)
    if re.search(r"\bbug\b|defect|regression|gap|unexpected|broken|ошиб|дефект|регресс|несогласован|инконсист", normalized):
        return "reproduce -> evidence -> bug report -> layer classification -> factory feedback if reusable -> remediation"
    return "not-required-by-text-signal"


def gather_project_profile(root: Path) -> str:
    profile = read_yaml(root / ".chatgpt" / "project-profile.yaml")
    return str(
        profile.get("project_preset")
        or profile.get("project_title")
        or "unknown-project-profile"
    )


def gather_pipeline_stage(root: Path) -> str:
    stage = read_yaml(root / ".chatgpt" / "stage-state.yaml")
    return str((stage.get("stage") or {}).get("current") or "unknown-stage")


def gather_selected_scenario(root: Path) -> str:
    active = read_yaml(root / ".chatgpt" / "active-scenarios.yaml")
    raw = active.get("active_scenarios", active.get("active", []))
    if isinstance(raw, list) and raw:
        return str(raw[0])
    scenario_pack = active.get("scenario_pack", {})
    if isinstance(scenario_pack, dict) and scenario_pack.get("entrypoint"):
        return str(scenario_pack["entrypoint"])
    return "00-master-router.md"


def handoff_allowed(root: Path) -> str:
    stage = read_yaml(root / ".chatgpt" / "stage-state.yaml")
    policy = read_yaml(root / ".chatgpt" / "policy-status.yaml")
    allowed = bool((stage.get("gates") or {}).get("codex_handoff_allowed"))
    handoff_policy = str(policy.get("handoff_policy") or "forbidden")
    if allowed:
        return f"yes ({handoff_policy})"
    return f"no ({handoff_policy})"


def artifacts_to_update(spec: dict, root: Path, defect_path: str) -> list[str]:
    defaults = list(spec.get("defaults", {}).get("artifacts_to_update", []))
    profile = read_yaml(root / ".chatgpt" / "project-profile.yaml")
    for item in profile.get("required_artifacts", []):
        if isinstance(item, str) and item not in defaults:
            defaults.append(item)
    if defect_path != "not-required-by-text-signal":
        for rel in ["reports/bugs/", "reports/factory-feedback/"]:
            if rel not in defaults:
                defaults.append(rel)
    return defaults


def launch_artifact_path(launch_source: str) -> str:
    if launch_source == "direct-task":
        return ".chatgpt/direct-task-source.md"
    return ".chatgpt/codex-input.md"


def repo_launch_command(launch_source: str, artifact_path: str) -> str:
    return (
        f"./scripts/launch-codex-task.sh --launch-source {launch_source} "
        f"--task-file {artifact_path} --execute"
    )


def codex_profile_command(profile_name: str) -> str:
    return f"codex --profile {profile_name}"


def build_launch_record(
    root: Path,
    launch_source: str,
    task_text: str,
    explicit_task_class: str | None = None,
) -> dict:
    spec = load_routing_spec(root)
    overrides = explicit_routing_overrides(task_text)
    requested_task_class = str(overrides.get("task_class") or "").strip()
    task_class_override = explicit_task_class
    if not task_class_override and requested_task_class in (spec.get("task_classes", {}) or {}):
        task_class_override = requested_task_class

    task_class, reasons = infer_task_class(spec, task_text, task_class_override)
    explicit_profile = choose_profile_from_overrides(spec, task_class, overrides)
    if explicit_profile is not None:
        profile_name, profile, profile_reasons = explicit_profile
        reasons.extend(profile_reasons)
    else:
        profile_name, profile = selected_profile(spec, task_class)
    defect_path = detect_defect_path(task_text)
    project_profile = stringify_override(overrides.get("project_profile")) or gather_project_profile(root)
    selected_scenario = stringify_override(overrides.get("selected_scenario")) or gather_selected_scenario(root)
    pipeline_stage = stringify_override(overrides.get("pipeline_stage")) or gather_pipeline_stage(root)
    apply_mode = stringify_override(overrides.get("apply_mode")) or str(
        (spec.get("validation", {}) or {}).get("apply_mode_default", "manual-ui")
    )
    strict_launch_mode = stringify_override(overrides.get("strict_launch_mode")) or str(
        (spec.get("validation", {}) or {}).get("strict_launch_mode_default", "optional")
    )
    artifacts = overrides.get("artifacts_to_update")
    if isinstance(artifacts, list) and artifacts:
        artifacts_list = [str(item) for item in artifacts if str(item).strip()]
    else:
        artifacts_list = artifacts_to_update(spec, root, defect_path)
    handoff_allowed_value = stringify_yes_no_override(overrides.get("handoff_allowed")) or handoff_allowed(root)
    defect_capture_path = stringify_override(overrides.get("defect_capture_path")) or defect_path
    handoff_artifact = launch_artifact_path(launch_source)
    selected_codex_command = codex_profile_command(profile_name)
    selected_launch_command = repo_launch_command(launch_source, handoff_artifact)
    return {
        "launch": {
            "timestamp_utc": now_utc(),
            "launch_unit": spec.get("routing_contract", {}).get("launch_unit", "new-task-launch"),
            "launch_source": launch_source,
            "router_layer": "executable",
            "task_class": task_class,
            "task_class_reasons": reasons,
            "selected_profile": profile_name,
            "selected_model": profile.get("model", ""),
            "selected_reasoning_effort": profile.get("reasoning_effort", ""),
            "selected_plan_mode_reasoning_effort": profile.get("plan_mode_reasoning_effort", ""),
            "apply_mode": apply_mode,
            "strict_launch_mode": strict_launch_mode,
            "project_profile": project_profile,
            "selected_scenario": selected_scenario,
            "pipeline_stage": pipeline_stage,
            "artifacts_to_update": artifacts_list,
            "handoff_allowed": handoff_allowed_value,
            "defect_capture_path": defect_capture_path,
            "task_summary": task_text.splitlines()[0].strip()[:240] if task_text.strip() else "",
            "launch_boundary_rule": spec.get("routing_contract", {}).get("launch_boundary_rule", ""),
            "interactive_default_rule": spec.get("routing_contract", {}).get("interactive_default_rule", ""),
            "executable_switch_rule": spec.get("routing_contract", {}).get("executable_switch_rule", ""),
            "strict_launch_rule": spec.get("routing_contract", {}).get("strict_launch_rule", ""),
            "live_session_fallback_rule": spec.get("routing_contract", {}).get("live_session_fallback_rule", ""),
            "model_expectation_rule": spec.get("routing_contract", {}).get("model_expectation_rule", ""),
            "advisory_layers": spec.get("routing_contract", {}).get("advisory_layers", []),
            "executable_layers": spec.get("routing_contract", {}).get("executable_layers", []),
            "launch_artifact_path": handoff_artifact,
            "launch_command": selected_launch_command,
            "codex_profile_command": selected_codex_command,
            "strict_launch_use_cases": (spec.get("validation", {}) or {}).get("strict_launch_use_cases", []),
            "troubleshooting": spec.get("validation", {}).get("troubleshooting", []),
            "direct_self_handoff_required": launch_source == "direct-task",
            "direct_self_handoff_completed": False,
            "requested_task_class": requested_task_class or None,
            "requested_selected_profile": stringify_override(overrides.get("selected_profile")) or None,
            "requested_selected_model": stringify_override(overrides.get("selected_model")) or None,
            "requested_selected_reasoning_effort": stringify_override(overrides.get("selected_reasoning_effort")) or None,
        }
    }


def write_launch_record(root: Path, record: dict) -> Path:
    path = root / ".chatgpt" / "task-launch.yaml"
    write_yaml(path, record)
    return path


def render_normalized_handoff(record: dict, task_text: str, title: str) -> str:
    launch = record.get("launch", {})
    artifacts = launch.get("artifacts_to_update", [])
    artifacts_lines = "\n".join(f"- {item}" for item in artifacts) if artifacts else "- none"
    reasons = launch.get("task_class_reasons", [])
    reason_lines = "\n".join(f"- {item}" for item in reasons) if reasons else "- none"
    manual_ui_lines = "\n".join(
        [
            "- Откройте новый чат/окно Codex в VS Code extension.",
            f"- Вручную выберите model `{launch.get('selected_model', '')}` и reasoning `{launch.get('selected_reasoning_effort', '')}` в picker.",
            "- Только после этого вставьте handoff.",
            "- Уже открытая live session не считается надежным auto-switch boundary.",
        ]
    )
    strict_launch_use_cases = launch.get("strict_launch_use_cases", [])
    strict_launch_lines = "\n".join(f"- {item}" for item in strict_launch_use_cases) if strict_launch_use_cases else "- none"
    troubleshooting = launch.get("troubleshooting", [])
    troubleshooting_lines = "\n".join(f"- {item}" for item in troubleshooting) if troubleshooting else "- none"
    return f"""# {title}

## Источник запуска
{launch.get('launch_source', '')}

## Класс задачи
{launch.get('task_class', '')}

## Evidence для класса задачи
{reason_lines}

## Выбранный профиль
{launch.get('selected_profile', '')}

## Выбранная модель
{launch.get('selected_model', '')}

## Выбранное reasoning effort
{launch.get('selected_reasoning_effort', '')}

## Выбранное reasoning effort для plan mode
{launch.get('selected_plan_mode_reasoning_effort', '')}

## Режим применения
{launch.get('apply_mode', '')}

## Ручное применение через UI
{manual_ui_lines}

## Строгий режим запуска
{launch.get('strict_launch_mode', '')}

## Профиль проекта
{launch.get('project_profile', '')}

## Выбранный сценарий
{launch.get('selected_scenario', '')}

## Этап pipeline
{launch.get('pipeline_stage', '')}

## Артефакты для обновления
{artifacts_lines}

## Разрешение handoff
{launch.get('handoff_allowed', '')}

## Маршрут defect-capture
{launch.get('defect_capture_path', '')}

## Правило launch boundary
{launch.get('launch_boundary_rule', '')}

## Правило интерактивного режима по умолчанию
{launch.get('interactive_default_rule', '')}

## Правило executable switch
{launch.get('executable_switch_rule', '')}

## Правило строгого запуска
{launch.get('strict_launch_rule', '')}

## Правило fallback для live session
{launch.get('live_session_fallback_rule', '')}

## Правило ожиданий по модели
{launch.get('model_expectation_rule', '')}

## Путь launch artifact
`{launch.get('launch_artifact_path', '')}`

## Опциональная команда строгого запуска
`{launch.get('launch_command', '')}`

## Сценарии для строгого запуска
{strict_launch_lines}

## Прямая команда Codex за launcher
`{launch.get('codex_profile_command', '')}`

## Диагностика проблем
{troubleshooting_lines}

## Текст задачи
{task_text.strip() or '-'}"""


def render_direct_task_response(record: dict, task_text: str) -> str:
    launch = record.get("launch", {})
    artifacts = launch.get("artifacts_to_update", [])
    artifacts_lines = "\n".join(f"- {item}" for item in artifacts) if artifacts else "- none"
    manual_ui_lines = "\n".join(
        [
            "- Откройте новый чат/окно Codex.",
            f"- Вручную выберите model `{launch.get('selected_model', '')}` и reasoning `{launch.get('selected_reasoning_effort', '')}` в picker.",
            "- Только после этого продолжайте работу по self-handoff.",
            "- Уже открытая live session не является надежным auto-switch boundary.",
        ]
    )
    strict_launch_use_cases = launch.get("strict_launch_use_cases", [])
    strict_launch_lines = "\n".join(f"- {item}" for item in strict_launch_use_cases) if strict_launch_use_cases else "- none"
    troubleshooting = launch.get("troubleshooting", [])
    troubleshooting_lines = "\n".join(f"- {item}" for item in troubleshooting) if troubleshooting else "- none"
    return f"""## Self-handoff для прямой задачи

## Классификация
direct-task

## Выбранный профиль проекта
{launch.get('project_profile', '')}

## Выбранный сценарий
{launch.get('selected_scenario', '')}

## Текущий этап pipeline
{launch.get('pipeline_stage', '')}

## Класс задачи
{launch.get('task_class', '')}

## Выбранный профиль
{launch.get('selected_profile', '')}

## Выбранная модель
{launch.get('selected_model', '')}

## Выбранное reasoning effort
{launch.get('selected_reasoning_effort', '')}

## Режим применения
{launch.get('apply_mode', '')}

## Ручное применение через UI
{manual_ui_lines}

## Строгий режим запуска
{launch.get('strict_launch_mode', '')}

## Артефакты для обновления
{artifacts_lines}

## Разрешение handoff
{launch.get('handoff_allowed', '')}

## Маршрут defect-capture
{launch.get('defect_capture_path', '')}

## Источник запуска
{launch.get('launch_source', '')}

## Правило launch boundary
{launch.get('launch_boundary_rule', '')}

## Правило интерактивного режима по умолчанию
{launch.get('interactive_default_rule', '')}

## Правило executable switch
{launch.get('executable_switch_rule', '')}

## Правило строгого запуска
{launch.get('strict_launch_rule', '')}

## Правило fallback для live session
{launch.get('live_session_fallback_rule', '')}

## Правило ожиданий по модели
{launch.get('model_expectation_rule', '')}

## Опциональная команда строгого запуска
`{launch.get('launch_command', '')}`

## Сценарии для строгого запуска
{strict_launch_lines}

## Прямая команда Codex за launcher
`{launch.get('codex_profile_command', '')}`

## Диагностика проблем
{troubleshooting_lines}

## Текст задачи
{task_text.strip() or '-'}

## Следующий шаг
Только после этого блока допустимы remediation / implementation / verification."""


def write_markdown(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path
