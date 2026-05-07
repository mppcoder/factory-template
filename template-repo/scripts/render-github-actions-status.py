#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from factory_automation_common import now_utc


def run_json(command: list[str]) -> Any:
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout or "null")


def safe_text(value: Any) -> str:
    text = str(value or "").strip()
    return text or "unknown"


def render_report(repo: str, workflow: str, run: dict[str, Any], run_view: dict[str, Any]) -> str:
    jobs = run_view.get("jobs") if isinstance(run_view.get("jobs"), list) else []
    conclusion = safe_text(run.get("conclusion"))
    status = safe_text(run.get("status"))
    lines = [
        "# Статус GitHub Actions",
        "",
        f"Generated UTC: `{now_utc()}`",
        f"Repository: `{repo}`",
        "Access path: `authenticated gh`",
        f"Workflow: `{workflow}`",
        "Scope: latest workflow run observed through authenticated GitHub CLI; no public URL fallback was used.",
        "Self-reference boundary: a committed status report records the latest observed run at render time; the commit that updates this report may trigger a newer run that must be rendered again after it completes.",
        "",
        "## Последний workflow run",
        "",
        f"- database_id: `{safe_text(run.get('databaseId'))}`",
        f"- title: `{safe_text(run.get('displayTitle'))}`",
        f"- head_sha: `{safe_text(run.get('headSha'))}`",
        f"- head_branch: `{safe_text(run.get('headBranch'))}`",
        f"- event: `{safe_text(run.get('event'))}`",
        f"- status/conclusion: `{status}` / `{conclusion}`",
        f"- created_at: `{safe_text(run.get('createdAt'))}`",
        f"- updated_at: `{safe_text(run.get('updatedAt'))}`",
        f"- url: `{safe_text(run.get('url'))}`",
        "",
        "## Задачи workflow",
        "",
    ]
    if jobs:
        for job in jobs:
            lines.append(
                f"- `{safe_text(job.get('name'))}`: `{safe_text(job.get('status'))}` / "
                f"`{safe_text(job.get('conclusion'))}` ({safe_text(job.get('url'))})"
            )
    else:
        lines.append("- no jobs returned by `gh run view`")
    lines.extend(
        [
            "",
            "## Текущий вывод",
            "",
            f"- latest_actions_result: `{conclusion}`",
            "- github_issues_open: recorded separately during triage with `gh issue list`",
            "- github_prs_open: recorded separately during triage with `gh pr list`",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_unavailable(repo: str, workflow: str, reason: str) -> str:
    return "\n".join(
        [
            "# Статус GitHub Actions",
            "",
            f"Generated UTC: `{now_utc()}`",
            f"Repository: `{repo}`",
            "Access path: `authenticated gh unavailable`",
            f"Workflow: `{workflow}`",
            f"Blocker: `{reason}`",
            "Self-reference boundary: once authenticated `gh` or GitHub connector Actions read access is available, rerender this report and commit the observed latest run.",
            "",
            "## Последний workflow run",
            "",
            "- database_id: `unknown`",
            "- status/conclusion: `blocked` / `unknown`",
            "",
            "## Задачи workflow",
            "",
            "- unavailable",
            "",
            "## Текущий вывод",
            "",
            "- latest_actions_result: `unknown`",
        ]
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a repo-local latest GitHub Actions status report via authenticated gh.")
    parser.add_argument("--repo", default="mppcoder/factory-template")
    parser.add_argument("--workflow", default="CI")
    parser.add_argument("--output", default="reports/ci/latest-actions-status.md")
    parser.add_argument("--allow-unavailable", action="store_true")
    args = parser.parse_args()

    output = Path(args.output)
    try:
        runs = run_json(
            [
                "gh",
                "run",
                "list",
                "--repo",
                args.repo,
                "--workflow",
                args.workflow,
                "--limit",
                "1",
                "--json",
                "databaseId,status,conclusion,headSha,headBranch,event,createdAt,updatedAt,displayTitle,url",
            ]
        )
        if not isinstance(runs, list) or not runs:
            raise RuntimeError("no workflow runs returned")
        run = runs[0]
        run_view = run_json(
            [
                "gh",
                "run",
                "view",
                str(run.get("databaseId")),
                "--repo",
                args.repo,
                "--json",
                "databaseId,status,conclusion,headSha,displayTitle,url,jobs",
            ]
        )
        report = render_report(args.repo, args.workflow, run, run_view if isinstance(run_view, dict) else {})
    except Exception as exc:
        if not args.allow_unavailable:
            raise
        report = render_unavailable(args.repo, args.workflow, str(exc))

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(f"github_actions_status_report={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
