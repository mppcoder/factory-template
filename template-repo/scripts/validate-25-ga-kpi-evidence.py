#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


def fail(message: str) -> None:
    print("GA KPI EVIDENCE НЕВАЛИДЕН")
    print(f"- {message}")
    raise SystemExit(1)


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"отсутствует {path}")
    return path.read_text(encoding="utf-8")


def metric_int(text: str, key: str) -> int:
    match = re.search(rf"- {re.escape(key)}: `(\d+)`", text)
    if not match:
        fail(f"onboarding acceptance не содержит `{key}`")
    return int(match.group(1))


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

    scorecard = yaml.safe_load((root / "docs/releases/release-scorecard.yaml").read_text(encoding="utf-8")) or {}
    truth = scorecard.get("release_truth", {})
    ga_ready = truth.get("ga_ready") is True

    if not ga_ready:
        print("GA KPI EVIDENCE ПРОПУЩЕН: ga_ready=false")
        return 0

    acceptance = read_text(root / "onboarding-smoke/ACCEPTANCE_REPORT.md")
    total = metric_int(acceptance, "total scenarios")
    passed = metric_int(acceptance, "passed scenarios")
    completion = metric_int(acceptance, "completion_rate_percent")
    max_minutes = metric_int(acceptance, "max_time_to_first_success_minutes_ceiling")
    interventions = metric_int(acceptance, "total_manual_interventions")

    if total < 1 or passed != total:
        fail(f"novice pilot должен пройти полностью: passed={passed}, total={total}")
    if completion < 92:
        fail(f"M25-02 ниже full-порога: {completion}% < 92%")
    if max_minutes > 25:
        fail(f"M25-01 ниже full-порога: {max_minutes} минут > 25 минут")
    if interventions > 1:
        fail(f"M25-03 ниже full-порога: interventions={interventions} > 1")

    safe_sync = read_text(root / "reports/release/2.5-downstream-safe-sync-report.md")
    safe_rate = metric_int(safe_sync, "success_rate_percent")
    if safe_rate < 99:
        fail(f"M25-04 ниже full-порога: {safe_rate}% < 99%")

    handoff = yaml.safe_load((root / ".chatgpt/handoff-rework-register.yaml").read_text(encoding="utf-8")) or {}
    entries = handoff.get("entries", [])
    if not entries:
        fail("handoff-rework-register не содержит entries")
    max_loops = max(int(item.get("rework_loops", 99)) for item in entries if isinstance(item, dict))
    if max_loops > 1:
        fail(f"M25-06 ниже full-порога: max rework loops={max_loops} > 1")

    evidence = read_text(root / "docs/releases/2.5-ga-kpi-evidence.md")
    required_markers = [
        "`M25-01`: pass",
        "`M25-02`: pass",
        "`M25-03`: pass",
        "`M25-04`: pass",
        "`M25-05`: pass",
        "`M25-06`: pass",
        "`M25-07`: pass",
        "`M25-08`: pass",
    ]
    missing = [marker for marker in required_markers if marker not in evidence]
    if missing:
        fail(f"consolidated KPI evidence не содержит markers: {', '.join(missing)}")

    blocker = read_text(root / "reports/bugs/2026-04-26-25-ga-readiness-gap.md")
    if "Status: closed" not in blocker:
        fail("GA blocker report должен быть закрыт после KPI remediation")

    print("GA KPI EVIDENCE ВАЛИДЕН")
    print(f"- novice scenarios: {passed}/{total}")
    print(f"- completion_rate_percent: {completion}")
    print(f"- safe_sync_success_rate_percent: {safe_rate}")
    print(f"- max_handoff_rework_loops: {max_loops}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
