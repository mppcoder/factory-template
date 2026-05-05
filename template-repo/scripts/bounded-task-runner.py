#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path

from automation_run_ledger import append_entry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", type=int)
    parser.add_argument("--task-id")
    parser.add_argument("--handoff")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--one", action="store_true")
    parser.add_argument("--max-concurrency", type=int, default=1)
    parser.add_argument("--allow-parallel", action="store_true")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--no-pr", action="store_true")
    return parser.parse_args()


def write_run(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schema: bounded-task-run/v1"]
    for key, value in values.items():
        lines.append(f"{key}: \"{str(value).replace(chr(10), ' ')}\"")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    if args.max_concurrency > 1 and not args.allow_parallel:
        raise SystemExit("max_concurrency > 1 requires --allow-parallel and documented worktree isolation")
    if args.max_concurrency > 1:
        raise SystemExit("parallel execution is refused until worktree isolation is implemented and tested")
    if not (args.issue or args.task_id or args.handoff):
        raise SystemExit("one source is required: --issue, --task-id, or --handoff")

    source = "handoff"
    identifier = args.handoff or "unknown"
    branch = "codex/task-run"
    run_path = Path(".chatgpt/task-runs/manual/run.yaml")
    if args.issue:
      source = "github-issue"
      identifier = str(args.issue)
      branch = f"codex/issue-{args.issue}"
      run_path = Path(".chatgpt/issue-runs") / f"issue-{args.issue}" / "run.yaml"
    elif args.task_id:
      source = "ft-task"
      identifier = args.task_id
      if not re.fullmatch(r"[A-Z]+-TASK-\d{4}", args.task_id):
          raise SystemExit("task id must look like FT-TASK-0001")
      branch = f"codex/task-{args.task_id}"
      run_path = Path(".chatgpt/task-runs") / args.task_id / "run.yaml"

    script_prefix = "template-repo/scripts" if Path("template-repo/scripts").exists() else "scripts"
    launcher_command = f"bash {script_prefix}/launch-codex-task.sh --launch-source direct-task --task-text bounded-runner:{source}:{identifier} --dry-run"
    status = "dry_run_planned"
    if args.handoff:
        launcher_command = f"bash {script_prefix}/launch-codex-task.sh --launch-source direct-task --task-file {args.handoff} --dry-run"

    if not args.dry_run:
        subprocess.run(["git", "switch", "-C", branch], check=True)
        subprocess.run(launcher_command.split(), check=False)
        status = "one_task_launcher_dry_run_complete"

    write_run(
        run_path,
        {
            "source": source,
            "identifier": identifier,
            "status": status,
            "branch": branch,
            "max_concurrency": str(args.max_concurrency),
            "dry_run": str(args.dry_run).lower(),
            "no_push": str(args.no_push).lower(),
            "no_pr": str(args.no_pr).lower(),
            "launcher_command": launcher_command,
            "safety": "no auto-merge, no production deploy, no security/external-secret tasks",
        },
    )
    append_entry(
        Path(".chatgpt") / "automation-runs" / "ledger.jsonl",
        {
            "issue_or_task_id": f"{source}:{identifier}",
            "trigger": "bounded-task-runner",
            "actor": os.environ.get("GITHUB_ACTOR", "local"),
            "gate_result": "prechecked-or-manual",
            "handoff_path": args.handoff or "",
            "branch": branch,
            "launcher_command": launcher_command,
            "verification_commands_results": "pending",
            "pr_url": "",
            "blockers": "",
            "final_status": status,
        },
    )
    print(f"bounded_runner_status={status}")
    print(f"run_yaml={run_path}")
    print(f"launcher_command={launcher_command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
