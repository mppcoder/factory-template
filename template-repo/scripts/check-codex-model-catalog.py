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
    parser.add_argument("--json", action="store_true", help="Print JSON summary")
    parser.add_argument("--write-proposal", action="store_true", help="Write a model routing proposal artifact")
    parser.add_argument("--apply-safe", action="store_true", help="Refresh safe catalog metadata only")
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
    ]
    file_lines = "\n".join(f"- {item}" for item in files)
    manual_review_required = bool(
        findings["profiles_that_can_be_upgraded"]
        or findings["missing_configured_models"]
        or findings["unsupported_reasoning"]
    )
    risks = []
    if findings["missing_configured_models"]:
        risks.append("configured model missing from live catalog")
    if findings["unsupported_reasoning"]:
        risks.append("configured reasoning effort unsupported by live catalog")
    if findings["profiles_that_can_be_upgraded"]:
        risks.append("profile model promotion changes executable routing and needs manual review")
    risk_lines = "\n".join(f"- {item}" for item in risks) if risks else "- no compatibility risk detected"
    return f"""# Model Routing Proposal

## Current Mapping
{current_lines}

## Live Catalog Summary
source: {summary['catalog_source']}
status: {summary['catalog_status']}

{live_lines}

## Proposed Mapping
{proposed_lines}

## Reasoning Support Evidence
{live_lines}

## Compatibility Risks
{risk_lines}

## Exact Files To Update
{file_lines}

## Manual Review Required
{str(manual_review_required).lower()}

## Findings JSON
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

    print("CODEX MODEL CATALOG CHECK")
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
