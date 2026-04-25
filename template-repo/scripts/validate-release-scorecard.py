#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True

from factory_automation_common import AutomationError, read_text, read_yaml, repo_root


SCORECARD_PATH = Path("docs/releases/release-scorecard.yaml")


def require_mapping(data: object, label: str) -> dict:
    if not isinstance(data, dict):
        raise AutomationError(f"{label} должен быть YAML mapping")
    return data


def require_scalar(data: dict, key: str) -> str:
    value = data.get(key)
    if value is None or str(value).strip() == "":
        raise AutomationError(f"release-scorecard не содержит обязательное поле `{key}`")
    return str(value)


def validate_required_fields(truth: dict) -> None:
    for key in [
        "canonical_file",
        "release_line",
        "release_label",
        "current_stage",
        "status",
        "last_updated",
        "status_source_policy",
        "next_decision",
    ]:
        require_scalar(truth, key)
    if truth.get("canonical_file") != str(SCORECARD_PATH):
        raise AutomationError("canonical_file должен указывать на docs/releases/release-scorecard.yaml")
    if truth.get("ga_ready") is not False:
        raise AutomationError("ga_ready должен быть false, пока 2.5 не объявлен GA")
    if truth.get("rc_ready") is not True:
        raise AutomationError("rc_ready должен быть true для текущего RC closeout candidate")


def validate_gates(truth: dict) -> None:
    gates = truth.get("gates")
    if not isinstance(gates, list) or not gates:
        raise AutomationError("release-scorecard должен содержать непустой список gates")
    seen: set[str] = set()
    for index, gate in enumerate(gates, start=1):
        if not isinstance(gate, dict):
            raise AutomationError(f"gate #{index} должен быть mapping")
        gate_id = str(gate.get("id", "")).strip()
        status = str(gate.get("status", "")).strip()
        if not gate_id:
            raise AutomationError(f"gate #{index} не содержит id")
        if gate_id in seen:
            raise AutomationError(f"дублирующийся gate id: {gate_id}")
        seen.add(gate_id)
        if status not in {"closed", "passed", "pending", "blocked"}:
            raise AutomationError(f"gate {gate_id} содержит неизвестный status `{status}`")


def validate_doc_assertions(root: Path, truth: dict) -> None:
    assertions = truth.get("doc_assertions")
    if not isinstance(assertions, list) or not assertions:
        raise AutomationError("release-scorecard должен содержать doc_assertions")
    for item in assertions:
        if not isinstance(item, dict):
            raise AutomationError("каждый doc_assertion должен быть mapping")
        rel = str(item.get("path", "")).strip()
        if not rel:
            raise AutomationError("doc_assertion без path")
        path = root / rel
        if not path.exists():
            raise AutomationError(f"doc_assertion указывает на отсутствующий файл: {rel}")
        text = read_text(path)
        must_contain = item.get("must_contain")
        if not isinstance(must_contain, list) or not must_contain:
            raise AutomationError(f"doc_assertion для {rel} должен содержать непустой must_contain")
        for marker in must_contain:
            marker_text = str(marker)
            if marker_text not in text:
                raise AutomationError(f"{rel} не содержит release-truth marker: {marker_text}")


def validate_forbidden_markers(root: Path, truth: dict) -> None:
    markers = truth.get("forbidden_doc_markers", [])
    if not isinstance(markers, list):
        raise AutomationError("forbidden_doc_markers должен быть списком")
    for item in markers:
        if not isinstance(item, dict):
            raise AutomationError("каждый forbidden_doc_marker должен быть mapping")
        rel = str(item.get("path", "")).strip()
        marker = str(item.get("marker", ""))
        if not rel or not marker:
            raise AutomationError("forbidden_doc_marker должен содержать path и marker")
        path = root / rel
        if path.exists() and marker in read_text(path):
            raise AutomationError(f"{rel} содержит запрещенный release-truth marker: {marker}")


def main() -> int:
    root = repo_root(sys.argv[1] if len(sys.argv) > 1 else ".")
    try:
        scorecard_path = root / SCORECARD_PATH
        if not scorecard_path.exists():
            raise AutomationError(f"отсутствует {SCORECARD_PATH}")
        data = require_mapping(read_yaml(scorecard_path), str(SCORECARD_PATH))
        truth = require_mapping(data.get("release_truth"), "release_truth")
        validate_required_fields(truth)
        validate_gates(truth)
        validate_doc_assertions(root, truth)
        validate_forbidden_markers(root, truth)
    except AutomationError as exc:
        print("RELEASE SCORECARD НЕВАЛИДЕН")
        print(f"- {exc}")
        return 1
    print("RELEASE SCORECARD ВАЛИДЕН")
    print(f"- source: {SCORECARD_PATH}")
    print(f"- status: {truth.get('release_label')}")
    print(f"- stage: {truth.get('current_stage')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
