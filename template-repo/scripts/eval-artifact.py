#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


SCHEMA = "artifact-eval/v1"
VALID_CASE_KINDS = {"trigger-positive", "trigger-negative", "comparison", "compliance"}
VALID_BASELINE = {"pass", "fail", "unclear", "not_applicable"}


@dataclass
class AssertionResult:
    assertion_id: str
    category: str
    description: str
    status: str
    evidence: str


@dataclass
class CaseResult:
    case_id: str
    kind: str
    prompt: str
    expected: str
    baseline_expected: str
    status: str
    passed: int
    total: int
    assertions: list[AssertionResult]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(read_text(path)) or {}
    except Exception as exc:
        raise SystemExit(f"invalid yaml: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"invalid spec: {path} должен быть YAML mapping")
    return data


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def has_fragment(text: str, fragment: str) -> bool:
    return fragment in text


def has_regex(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE) is not None


def evaluate_assertion(assertion: dict[str, Any], target_text: str) -> AssertionResult:
    assertion_id = str(assertion.get("id") or "unnamed").strip()
    category = str(assertion.get("category") or "compliance").strip()
    description = str(assertion.get("description") or assertion.get("text") or "").strip()
    evidence: list[str] = []
    failures: list[str] = []
    checks = 0

    for fragment in as_list(assertion.get("must_contain")):
        checks += 1
        if has_fragment(target_text, fragment):
            evidence.append(f"contains `{fragment}`")
        else:
            failures.append(f"missing `{fragment}`")

    any_fragments = as_list(assertion.get("must_contain_any"))
    if any_fragments:
        checks += 1
        matched = [fragment for fragment in any_fragments if has_fragment(target_text, fragment)]
        if matched:
            evidence.append(f"contains any `{matched[0]}`")
        else:
            failures.append("missing any of " + ", ".join(f"`{item}`" for item in any_fragments))

    for fragment in as_list(assertion.get("must_not_contain")):
        checks += 1
        if has_fragment(target_text, fragment):
            failures.append(f"forbidden `{fragment}`")
        else:
            evidence.append(f"does not contain `{fragment}`")

    for pattern in as_list(assertion.get("regex_contains")):
        checks += 1
        if has_regex(target_text, pattern):
            evidence.append(f"matches /{pattern}/")
        else:
            failures.append(f"missing regex /{pattern}/")

    for pattern in as_list(assertion.get("regex_not_contains")):
        checks += 1
        if has_regex(target_text, pattern):
            failures.append(f"forbidden regex /{pattern}/")
        else:
            evidence.append(f"does not match /{pattern}/")

    if checks == 0:
        failures.append("assertion has no deterministic checks")

    status = "FAIL" if failures else "PASS"
    return AssertionResult(
        assertion_id=assertion_id,
        category=category,
        description=description,
        status=status,
        evidence="; ".join(failures or evidence),
    )


def normalize_case(raw: dict[str, Any], default_kind: str) -> dict[str, Any]:
    case = dict(raw)
    case.setdefault("kind", default_kind)
    case.setdefault("baseline_expected", "fail" if default_kind == "trigger-positive" else "pass")
    case.setdefault("expected", case.get("expected_behavior", ""))
    return case


def collect_cases(spec: dict[str, Any]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    expected_trigger = spec.get("expected_trigger") or {}
    if isinstance(expected_trigger, dict):
        for item in expected_trigger.get("cases", []) or []:
            if isinstance(item, dict):
                cases.append(normalize_case(item, "trigger-positive"))
    for item in spec.get("non_trigger_cases", []) or []:
        if isinstance(item, dict):
            cases.append(normalize_case(item, "trigger-negative"))
    for item in spec.get("cases", []) or []:
        if isinstance(item, dict):
            cases.append(normalize_case(item, str(item.get("kind") or "comparison")))
    return cases


def collect_global_assertions(spec: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for key, category in [
        ("process_assertions", "process"),
        ("outcome_assertions", "outcome"),
        ("compliance_assertions", "compliance"),
        ("assertions", "compliance"),
    ]:
        for assertion in spec.get(key, []) or []:
            if isinstance(assertion, dict):
                item = dict(assertion)
                item.setdefault("category", category)
                out.append(item)
    return out


def evaluate_case(case: dict[str, Any], target_text: str) -> CaseResult:
    case_id = str(case.get("id") or "unnamed").strip()
    kind = str(case.get("kind") or "comparison").strip()
    if kind not in VALID_CASE_KINDS:
        kind = "comparison"
    baseline_expected = str(case.get("baseline_expected") or "unclear").strip()
    if baseline_expected not in VALID_BASELINE:
        baseline_expected = "unclear"

    assertions = []
    for assertion in case.get("assertions", []) or []:
        if isinstance(assertion, dict):
            assertions.append(evaluate_assertion(assertion, target_text))

    passed = sum(1 for item in assertions if item.status == "PASS")
    total = len(assertions)
    status = "PASS" if total > 0 and passed == total else "FAIL"
    return CaseResult(
        case_id=case_id,
        kind=kind,
        prompt=str(case.get("prompt") or case.get("situation") or "").strip(),
        expected=str(case.get("expected") or case.get("expected_behavior") or "").strip(),
        baseline_expected=baseline_expected,
        status=status,
        passed=passed,
        total=total,
        assertions=assertions,
    )


def pct(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else round(numerator / denominator, 4)


def render_report(
    spec: dict[str, Any],
    spec_path: Path,
    root: Path,
    target_path: Path,
    case_results: list[CaseResult],
    global_results: list[AssertionResult],
    status: str,
    metrics: dict[str, Any],
) -> str:
    report_date = str(spec.get("report_date") or "1970-01-01")
    artifact_id = str(spec.get("id") or spec_path.stem)
    artifact_type = str(spec.get("artifact_type") or "prompt-like")
    expected_output = spec.get("expected_output") or {}
    expected_output_text = expected_output if isinstance(expected_output, str) else expected_output.get("guided", "")

    lines: list[str] = [
        f"# Отчёт Artifact Eval: {artifact_id}",
        "",
        f"Дата: {report_date}",
        f"Schema: {SCHEMA}",
        f"Status: {status}",
        f"Spec: {rel(spec_path, root)}",
        f"Target: {rel(target_path, root)}",
        f"Artifact type: {artifact_type}",
        "Generated by: eval-artifact.py",
        "",
        "## Сводка",
        "",
        f"- case_pass_rate: {metrics['case_passed']}/{metrics['case_total']} ({metrics['case_pass_rate']:.0%})",
        f"- assertion_pass_rate: {metrics['assertion_passed']}/{metrics['assertion_total']} ({metrics['assertion_pass_rate']:.0%})",
        f"- trigger_accuracy: {metrics['trigger_passed']}/{metrics['trigger_total']} ({metrics['trigger_accuracy']:.0%})",
        f"- false_negative_rate: {metrics['false_negative_count']}/{metrics['positive_total']} ({metrics['false_negative_rate']:.0%})",
        f"- false_positive_rate: {metrics['false_positive_count']}/{metrics['negative_total']} ({metrics['false_positive_rate']:.0%})",
        f"- baseline_delta_cases: +{metrics['baseline_delta_cases']}",
        "",
        "## Ожидаемый результат",
        "",
        str(expected_output_text or "Artifact дает более точный routing/output, чем unguided baseline."),
        "",
        "## Кейсы",
        "",
        "| Кейс | Вид | Baseline | Guided | Проверки | Prompt |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for result in case_results:
        prompt = result.prompt.replace("\n", " ").replace("|", "\\|")
        if len(prompt) > 110:
            prompt = prompt[:107] + "..."
        lines.append(
            f"| {result.case_id} | {result.kind} | {result.baseline_expected} | "
            f"{result.status} | {result.passed}/{result.total} | {prompt} |"
        )

    lines.extend(["", "## Проверки", "", "| Scope | Assertion | Category | Result | Evidence |", "| --- | --- | --- | --- | --- |"])
    for result in case_results:
        for assertion in result.assertions:
            evidence = assertion.evidence.replace("\n", " ").replace("|", "\\|")
            lines.append(
                f"| {result.case_id} | {assertion.assertion_id} | {assertion.category} | "
                f"{assertion.status} | {evidence} |"
            )
    for assertion in global_results:
        evidence = assertion.evidence.replace("\n", " ").replace("|", "\\|")
        lines.append(
            f"| global | {assertion.assertion_id} | {assertion.category} | {assertion.status} | {evidence} |"
        )

    lines.extend(["", "## Сравнение baseline и guided", ""])
    if metrics["baseline_delta_cases"]:
        lines.append(f"- Guided artifact добавляет value в {metrics['baseline_delta_cases']} case(s), где baseline ожидаемо слабее.")
    else:
        lines.append("- Baseline delta не доказан этим spec; проверьте discriminating assertions.")
    lines.append(f"- Thresholds: case_pass_rate >= {metrics['min_case_pass_rate']:.0%}, assertion_pass_rate >= {metrics['min_assertion_pass_rate']:.0%}, false_positive_rate <= {metrics['max_false_positive_rate']:.0%}.")

    lines.extend(["", "## Вердикт", "", f"{status}: deterministic desk-eval завершен для `{rel(target_path, root)}`."])
    return "\n".join(lines) + "\n"


def run_eval(spec_path: Path, root: Path) -> tuple[str, dict[str, Any], dict[str, Any]]:
    spec = load_yaml(spec_path)
    if spec.get("schema") != SCHEMA:
        raise SystemExit(f"invalid spec schema: expected {SCHEMA}")
    target_raw = str(spec.get("target_artifact") or "").strip()
    if not target_raw:
        raise SystemExit("invalid spec: target_artifact is required")
    target_path = (root / target_raw).resolve()
    target_text = read_text(target_path)
    if not target_text.strip():
        raise SystemExit(f"target artifact is empty or missing: {rel(target_path, root)}")

    case_results = [evaluate_case(item, target_text) for item in collect_cases(spec)]
    global_results = [evaluate_assertion(item, target_text) for item in collect_global_assertions(spec)]

    all_assertions = [assertion for case in case_results for assertion in case.assertions] + global_results
    assertion_total = len(all_assertions)
    assertion_passed = sum(1 for item in all_assertions if item.status == "PASS")
    case_total = len(case_results)
    case_passed = sum(1 for item in case_results if item.status == "PASS")
    trigger_cases = [item for item in case_results if item.kind in {"trigger-positive", "trigger-negative"}]
    positive_cases = [item for item in case_results if item.kind == "trigger-positive"]
    negative_cases = [item for item in case_results if item.kind == "trigger-negative"]
    false_negative_count = sum(1 for item in positive_cases if item.status != "PASS")
    false_positive_count = sum(1 for item in negative_cases if item.status != "PASS")
    baseline_delta_cases = sum(1 for item in case_results if item.baseline_expected == "fail" and item.status == "PASS")

    thresholds = spec.get("thresholds") or {}
    min_case_pass_rate = float(thresholds.get("min_case_pass_rate", 0.8))
    min_assertion_pass_rate = float(thresholds.get("min_assertion_pass_rate", 0.8))
    max_false_positive_rate = float(thresholds.get("max_false_positive_rate", 0.2))

    metrics = {
        "case_total": case_total,
        "case_passed": case_passed,
        "case_pass_rate": pct(case_passed, case_total),
        "assertion_total": assertion_total,
        "assertion_passed": assertion_passed,
        "assertion_pass_rate": pct(assertion_passed, assertion_total),
        "trigger_total": len(trigger_cases),
        "trigger_passed": sum(1 for item in trigger_cases if item.status == "PASS"),
        "trigger_accuracy": pct(sum(1 for item in trigger_cases if item.status == "PASS"), len(trigger_cases)),
        "positive_total": len(positive_cases),
        "negative_total": len(negative_cases),
        "false_negative_count": false_negative_count,
        "false_positive_count": false_positive_count,
        "false_negative_rate": pct(false_negative_count, len(positive_cases)),
        "false_positive_rate": pct(false_positive_count, len(negative_cases)),
        "baseline_delta_cases": baseline_delta_cases,
        "min_case_pass_rate": min_case_pass_rate,
        "min_assertion_pass_rate": min_assertion_pass_rate,
        "max_false_positive_rate": max_false_positive_rate,
    }
    status = "PASS"
    if case_total == 0 or assertion_total == 0:
        status = "FAIL"
    if metrics["case_pass_rate"] < min_case_pass_rate:
        status = "FAIL"
    if metrics["assertion_pass_rate"] < min_assertion_pass_rate:
        status = "FAIL"
    if metrics["false_positive_rate"] > max_false_positive_rate:
        status = "FAIL"

    report = render_report(spec, spec_path, root, target_path, case_results, global_results, status, metrics)
    payload = {"status": status, "metrics": metrics, "target": rel(target_path, root)}
    return report, payload, spec


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic artifact desk-eval from artifact-eval/v1 spec.")
    parser.add_argument("spec", help="Path to artifact eval YAML spec.")
    parser.add_argument("--root", default=".", help="Repo root. Defaults to current directory.")
    parser.add_argument("--output", help="Markdown report path. If omitted, prints to stdout.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary to stdout.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    spec_path = Path(args.spec).expanduser()
    if not spec_path.is_absolute():
        spec_path = (root / spec_path).resolve()

    report, payload, _spec = run_eval(spec_path, root)
    if args.output:
        output = Path(args.output).expanduser()
        if not output.is_absolute():
            output = (root / output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        payload["report"] = rel(output, root)
    else:
        print(report, end="")

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
