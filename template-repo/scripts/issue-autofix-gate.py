#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

BLOCKING_LABELS = {"security", "needs-human", "external-secret", "blocked", "agent:running"}
READY_LABEL = "agent:ready"
HIGH_RISK_LABEL = "risk:high"
HIGH_RISK_APPROVAL = "agent:approved-high-risk"
PERMITTED_ROLES = {"admin", "maintain", "write"}


def run_gh(args: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def gh_available() -> bool:
    try:
        return run_gh(["--version"]).returncode == 0
    except FileNotFoundError:
        return False


def read_event_issue(issue_number: int) -> dict[str, Any] | None:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        return None
    path = Path(event_path)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    issue = data.get("issue")
    if issue and int(issue.get("number", -1)) == issue_number:
        return issue
    return None


def fetch_issue(repo: str, issue: int) -> dict[str, Any]:
    if gh_available():
        proc = run_gh([
            "api",
            f"repos/{repo}/issues/{issue}",
            "--jq",
            "{number, title, body, labels: [.labels[].name], pull_request}",
        ])
        if proc.returncode == 0:
            return json.loads(proc.stdout)
    event_issue = read_event_issue(issue)
    if event_issue:
        return {
            "number": event_issue.get("number"),
            "title": event_issue.get("title", ""),
            "body": event_issue.get("body", ""),
            "labels": [label.get("name", "") for label in event_issue.get("labels", [])],
            "pull_request": event_issue.get("pull_request"),
        }
    raise RuntimeError("issue_lookup_failed")


def actor_permission(repo: str, actor: str) -> str:
    if not gh_available():
        return "unknown"
    proc = run_gh(["api", f"repos/{repo}/collaborators/{actor}/permission", "--jq", ".permission"])
    if proc.returncode != 0:
        return "unknown"
    return proc.stdout.strip()


def has_actionable_scope(body: str, labels: set[str]) -> bool:
    lowered = body.lower()
    if any(marker in lowered for marker in ["шаг", "reproduction", "steps", "acceptance", "критер", "expected", "ожидаем"]):
        return True
    if {"type:docs", "type:change", "type:factory-feedback"} & labels:
        return any(marker in lowered for marker in ["expected", "ожидаем", "outcome", "результат", "критер"])
    return False


def comment_issue(repo: str, issue: int, body: str) -> None:
    if not os.environ.get("GH_TOKEN") or not gh_available():
        return
    run_gh(["issue", "comment", str(issue), "--repo", repo, "--body", body])


def add_labels(repo: str, issue: int, labels: list[str]) -> None:
    if not os.environ.get("GH_TOKEN") or not gh_available():
        return
    if labels:
        run_gh(["issue", "edit", str(issue), "--repo", repo, "--add-label", ",".join(labels)])


def write_gate_result(path: Path, values: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schema: issue-autofix-gate/v1"]
    for key, value in values.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {str(value).lower()}")
        else:
            safe = str(value).replace("\n", " ").replace(":", "-")
            lines.append(f"{key}: {safe}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--issue", required=True, type=int)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--event-label", default="")
    parser.add_argument("--comment-body-file")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = Path(".chatgpt") / "issue-runs" / f"issue-{args.issue}"
    result_path = run_dir / "gate-result.yaml"
    try:
        issue = fetch_issue(args.repo, args.issue)
    except Exception as exc:
        print("eligible=false")
        print(f"reason=workflow_failure:{exc}")
        return 1

    labels = set(issue.get("labels") or [])
    body = issue.get("body") or ""
    command_body = ""
    if args.comment_body_file:
        command_body = Path(args.comment_body_file).read_text(encoding="utf-8")
    command_requested = command_body.lstrip().startswith("/factory fix")
    high_risk_approved = HIGH_RISK_APPROVAL in labels or "--approve-high-risk" in command_body
    permission = actor_permission(args.repo, args.actor)
    reasons: list[str] = []
    status_label = ""

    if issue.get("pull_request") is not None:
        reasons.append("target_is_pull_request")
    if permission not in PERMITTED_ROLES:
        reasons.append(f"actor_permission_not_trusted:{permission}")
        status_label = "agent:blocked"
    if READY_LABEL not in labels and not command_requested:
        reasons.append("missing_agent_ready_label_or_factory_fix_command")
        status_label = "status:needs-info"
    blockers = sorted(BLOCKING_LABELS & labels)
    if blockers:
        reasons.append("blocked_label:" + ",".join(blockers))
        status_label = "agent:blocked"
    if HIGH_RISK_LABEL in labels and not high_risk_approved:
        reasons.append("high_risk_requires_explicit_approval")
        status_label = "agent:blocked"
    if not has_actionable_scope(body, labels):
        reasons.append("missing_reproduction_or_acceptance_criteria")
        status_label = status_label or "status:needs-info"
    if args.event_label and args.event_label != READY_LABEL and not command_requested:
        reasons.append("event_label_is_not_agent_ready")

    eligible = not reasons
    write_gate_result(
        result_path,
        {
            "repo": args.repo,
            "issue_number": args.issue,
            "actor": args.actor,
            "actor_permission": permission,
            "eligible": eligible,
            "reasons": reasons or ["ok"],
            "labels": sorted(labels),
        },
    )

    if eligible:
        if not args.dry_run:
            add_labels(args.repo, args.issue, ["agent:claimed"])
        print("eligible=true")
        print("reason=ok")
        return 0

    reason_text = "; ".join(reasons)
    if not args.dry_run:
        if status_label:
            add_labels(args.repo, args.issue, [status_label])
        comment_issue(
            args.repo,
            args.issue,
            "Автоисправление не запущено: " + reason_text + ". Добавьте недостающие данные или снимите блокирующие labels.",
        )
    print("eligible=false")
    print(f"reason={reason_text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
