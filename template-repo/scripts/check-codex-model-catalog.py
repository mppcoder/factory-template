#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from codex_model_catalog import (
    catalog_snapshot,
    compare_catalog,
    configured_profiles,
    configured_task_classes,
    load_live_catalog,
    load_model_routing,
)
from codex_task_router import load_routing_spec
from factory_automation_common import write_yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Codex live model catalog against repo model routing.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root")
    parser.add_argument("--json", action="store_true", help="Напечатать JSON summary")
    parser.add_argument("--write-proposal", action="store_true", help="Записать proposal artifact для model routing")
    parser.add_argument("--apply-safe", action="store_true", help="Обновить только безопасные catalog metadata")
    parser.add_argument("--catalog-fixture", help="JSON/YAML fixture with a `codex debug models` payload or discovered_models map")
    return parser.parse_args()


def proposed_mapping(model_routing: dict, live_models: dict[str, dict]) -> dict:
    profiles = configured_profiles(model_routing)
    policy = model_routing.get("model_policy", {}) if isinstance(model_routing, dict) else {}
    candidate_order = list(policy.get("promotion_policy", {}).get("candidate_order", []))
    ranked = [model for model in candidate_order if model in live_models]
    best = ranked[0] if ranked else ""
    result: dict[str, dict] = {}
    for name, meta in profiles.items():
        current_model = str(meta.get("model") or "").strip()
        target_model = current_model
        review_required = bool(meta.get("manual_review_required", False))
        if best and best != current_model:
            target_model = best
            review_required = True
        result[name] = {
            "selected_model": target_model,
            "selected_reasoning_effort": meta.get("reasoning_effort", ""),
            "selected_plan_mode_reasoning_effort": meta.get("plan_mode_reasoning_effort", ""),
            "manual_review_required": review_required,
        }
    return result


def render_proposal(root: Path, summary: dict) -> str:
    current = summary["current_mapping"]
    proposed = summary["proposed_mapping"]
    live = summary["live_catalog"]
    findings = summary["findings"]
    prompt_policy = summary.get("prompt_migration_policy", {})
    current_lines = "\n".join(
        f"- {name}: {meta.get('model')} / {meta.get('reasoning_effort')} / plan {meta.get('plan_mode_reasoning_effort')}"
        for name, meta in current.items()
    )
    proposed_lines = "\n".join(
        f"- {name}: {meta.get('selected_model')} / {meta.get('selected_reasoning_effort')} / plan {meta.get('selected_plan_mode_reasoning_effort')} / manual_review_required={meta.get('manual_review_required')}"
        for name, meta in proposed.items()
    )
    live_lines = "\n".join(
        f"- {name}: {', '.join(meta.get('supported_reasoning_efforts', []))}"
        for name, meta in live.items()
    ) or "- live catalog unavailable"
    files = [
        "template-repo/codex-model-routing.yaml",
        "template-repo/codex-routing.yaml",
        "template-repo/template/.codex/config.toml",
        "template-repo/scripts/codex_task_router.py",
        "template-repo/scripts/validate-codex-routing.py",
        "template-repo/scripts/validate-gpt55-prompt-contract.py или successor validator для новой model",
        "tests/artifact-eval/specs/*prompt-contract*.yaml",
        "reports/prompt-migration/",
    ]
    file_lines = "\n".join(f"- {item}" for item in files)
    manual_review_required = bool(
        findings["profiles_that_can_be_upgraded"]
        or findings["missing_configured_models"]
        or findings["unsupported_reasoning"]
    )
    risks = []
    if findings["missing_configured_models"]:
        risks.append("настроенная модель отсутствует в live catalog")
    if findings["unsupported_reasoning"]:
        risks.append("настроенный reasoning effort не поддерживается live catalog")
    if findings["profiles_that_can_be_upgraded"]:
        risks.append("promotion модели для profile меняет executable routing и требует ручного review")
    risk_lines = "\n".join(f"- {item}" for item in risks) if risks else "- риски совместимости не обнаружены"
    source_lines = "\n".join(
        f"- {item}" for item in prompt_policy.get("official_source_baseline", [])
    ) or "- official source baseline не настроен"
    prompt_review_lines = "\n".join(
        f"- {item}" for item in prompt_policy.get("required_prompt_review", [])
    ) or "- prompt review policy не настроена"
    prompt_artifact_lines = "\n".join(
        f"- {item}" for item in prompt_policy.get("required_artifacts", [])
    ) or "- prompt artifacts не настроены"
    prompt_manual_lines = "\n".join(
        f"- {item}" for item in prompt_policy.get("manual_review_required_for", [])
    ) or "- manual prompt review boundary не настроен"
    prompt_review_required = bool(
        findings["profiles_that_can_be_upgraded"]
        or findings["new_candidate_models"]
        or findings["missing_configured_models"]
        or findings["unsupported_reasoning"]
    )
    return f"""# Proposal по маршрутизации моделей

## Текущий mapping
{current_lines}

## Сводка live catalog
источник: {summary['catalog_source']}
статус: {summary['catalog_status']}

{live_lines}

## Предложенный mapping
{proposed_lines}

## Evidence поддержки reasoning
{live_lines}

## Риски совместимости
{risk_lines}

## Политика prompt migration
default action: {prompt_policy.get('default_action', 'not-configured')}
prompt_review_required: {str(prompt_review_required).lower()}

Official OpenAI source baseline:
{source_lines}

Required prompt review:
{prompt_review_lines}

Required prompt artifacts:
{prompt_artifact_lines}

Manual review required for:
{prompt_manual_lines}

Новая model не считается drop-in replacement. Перед promotion profile mapping нужно проверить prompt-like artifacts по актуальным официальным рекомендациям OpenAI, обновить prompt contract / validators / evals и сохранить repo-first invariants.

## Точные файлы для обновления
{file_lines}

## Нужен ручной review
{str(manual_review_required).lower()}

## Findings JSON / данные findings
```json
{json.dumps(findings, ensure_ascii=False, indent=2)}
```
"""


def write_proposal(root: Path, summary: dict) -> Path:
    path = root / "reports" / "model-routing" / "model-routing-proposal.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_proposal(root, summary), encoding="utf-8")
    return path


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    model_routing, model_path = load_model_routing(root)
    routing_spec = load_routing_spec(root)
    fixture = Path(args.catalog_fixture).resolve() if args.catalog_fixture else None
    live_models, source, error = load_live_catalog(fixture)
    status = "unavailable" if error else "available"
    findings = compare_catalog(model_routing, live_models, routing_spec)
    summary = {
        "model_routing_path": str(model_path.relative_to(root)) if model_path.is_relative_to(root) else str(model_path),
        "catalog_source": source,
        "catalog_status": status,
        "catalog_warning": error,
        "current_mapping": configured_profiles(model_routing, routing_spec),
        "task_class_routing": configured_task_classes(model_routing, routing_spec),
        "live_catalog": live_models,
        "findings": findings,
        "proposed_mapping": proposed_mapping(model_routing, live_models),
        "prompt_migration_policy": (model_routing.get("prompt_migration_policy", {}) or {}),
        "apply_safe_performed": False,
        "proposal_path": None,
    }

    if args.apply_safe and live_models:
        model_routing["model_catalog"] = catalog_snapshot(live_models, source, status)
        write_yaml(model_path, model_routing)
        summary["apply_safe_performed"] = True
    elif args.apply_safe and error:
        summary["catalog_warning"] = f"{error}; safe apply skipped"

    if args.write_proposal:
        proposal_path = write_proposal(root, summary)
        summary["proposal_path"] = str(proposal_path.relative_to(root))

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    print("ПРОВЕРКА CODEX MODEL CATALOG")
    print(f"catalog_source={source}")
    print(f"catalog_status={status}")
    if summary["catalog_warning"]:
        print(f"WARNING: {summary['catalog_warning']}")
    print(f"configured_profiles={', '.join(sorted(summary['current_mapping']))}")
    print(f"live_models={', '.join(sorted(live_models)) if live_models else 'unavailable'}")
    for key, value in findings.items():
        print(f"{key}={json.dumps(value, ensure_ascii=False)}")
    if summary["proposal_path"]:
        print(f"proposal_path={summary['proposal_path']}")
    if summary["apply_safe_performed"]:
        print("safe_apply=updated model_catalog snapshot only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
