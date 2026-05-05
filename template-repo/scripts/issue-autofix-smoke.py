#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


NEGATIVE_EXPECTED = {
    "security-label": "blocked_label:security",
    "external-secret": "blocked_label:external-secret",
    "blocked-label": "blocked_label:blocked",
    "risk-high-no-approval": "high_risk_requires_explicit_approval",
    "missing-acceptance": "missing_reproduction_or_acceptance_criteria",
    "pull-request": "target_is_pull_request",
    "command-injection-text": "command_injection_like_content_refused",
    "secret-like-content": "secret_like_content_requires_human_redaction",
}


def run(cmd: list[str], *, cwd: Path, env: dict[str, str], check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    fixtures = root / "tests" / "issue-autofix"
    scripts = root / "template-repo" / "scripts"
    positive = fixtures / "positive" / "docs-change-issue.json"
    if not positive.exists():
        raise SystemExit(f"missing positive fixture: {positive}")

    with tempfile.TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        env = os.environ.copy()
        env["GITHUB_EVENT_PATH"] = str(positive)
        env["ISSUE_AUTOFIX_ACTOR_PERMISSION"] = "write"
        gate = run(
            [sys.executable, str(scripts / "issue-autofix-gate.py"), "--repo", "example/repo", "--issue", "101", "--actor", "maintainer", "--dry-run"],
            cwd=tmp,
            env=env,
        )
        if "eligible=true" not in gate.stdout:
            raise SystemExit("positive fixture was not eligible")

        out = tmp / "codex-input.md"
        run_yaml = tmp / "run.yaml"
        run(
            [sys.executable, str(scripts / "create-issue-codex-handoff.py"), "--repo", "example/repo", "--issue", "101", "--out", str(out), "--run-yaml", str(run_yaml)],
            cwd=tmp,
            env=env,
        )
        text = out.read_text(encoding="utf-8")
        if "## Untrusted User Content" not in text or "```text" not in text:
            raise SystemExit("handoff does not mark issue content as untrusted data")
        if "dry-run" not in text or "auto-merge" not in text:
            raise SystemExit("handoff does not preserve dry-run/no auto-merge safety wording")
        if "schema: issue-autofix-run/v1" not in run_yaml.read_text(encoding="utf-8"):
            raise SystemExit("run.yaml was not generated")

        runner = run(
            [sys.executable, str(scripts / "bounded-task-runner.py"), "--issue", "101", "--one", "--dry-run", "--no-push", "--no-pr"],
            cwd=tmp,
            env=env,
        )
        if "bounded_runner_status=dry_run_planned" not in runner.stdout:
            raise SystemExit("bounded runner did not remain dry-run")
        ledger = tmp / ".chatgpt" / "automation-runs" / "ledger.jsonl"
        run(
            [
                sys.executable,
                str(scripts / "automation_run_ledger.py"),
                "--ledger",
                str(ledger),
                "--issue",
                "101",
                "--trigger",
                "synthetic-dry-run",
                "--actor",
                "maintainer",
                "--gate-result",
                "eligible",
                "--handoff-path",
                str(out),
                "--branch",
                "codex/issue-101",
                "--launcher-command",
                "bounded-task-runner --dry-run",
                "--verification",
                "issue-autofix-smoke=pass",
                "--final-status",
                "dry_run_complete",
            ],
            cwd=tmp,
            env=env,
        )
        if not ledger.exists():
            raise SystemExit("ledger entry was not written")

        for name, expected in NEGATIVE_EXPECTED.items():
            fixture = fixtures / "negative" / f"{name}.json"
            if not fixture.exists():
                raise SystemExit(f"missing negative fixture: {fixture}")
            case_dir = tmp / f"neg-{name}"
            case_dir.mkdir()
            case_env = env.copy()
            case_env["GITHUB_EVENT_PATH"] = str(fixture)
            proc = run(
                [sys.executable, str(scripts / "issue-autofix-gate.py"), "--repo", "example/repo", "--issue", "102", "--actor", "maintainer", "--dry-run"],
                cwd=case_dir,
                env=case_env,
            )
            if "eligible=false" not in proc.stdout or expected not in proc.stdout:
                raise SystemExit(f"negative fixture did not refuse as expected: {name}\n{proc.stdout}")
            if not (case_dir / ".chatgpt" / "issue-runs" / "issue-102" / "gate-result.yaml").exists():
                raise SystemExit(f"negative fixture did not write gate result: {name}")

    print("issue-autofix-smoke=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
