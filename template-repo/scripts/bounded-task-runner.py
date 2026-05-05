#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from automation_run_ledger import append_entry
from permission_model import decide


REFUSED_MARKERS = {"security", "external-secret", "needs-human", "blocked"}


def fail(msg: str) -> None:
    raise SystemExit(f"bounded-task-runner: {msg}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bounded dry-run-first task runner.")
    parser.add_argument("--source", choices=["issue", "task"])
    parser.add_argument("--queue")
    parser.add_argument("--issue", type=int)
    parser.add_argument("--task-id")
    parser.add_argument("--handoff")
    parser.add_argument("--risk", choices=["low", "medium", "high"], default="low")
    parser.add_argument("--labels", default="")
    parser.add_argument("--acceptance", default="provided")
    parser.add_argument("--approval-file")
    parser.add_argument("--approval-id")
    parser.add_argument("--actor", default=os.environ.get("GITHUB_ACTOR", "local"))
    parser.add_argument("--actor-permission", default="maintain")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--one", action="store_true")
    parser.add_argument("--max-concurrency", type=int, default=1)
    parser.add_argument("--allow-parallel", action="store_true")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--no-pr", action="store_true")
    return parser.parse_args()


def read_approval(path: str | None) -> dict | None:
    if not path:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_task(args: argparse.Namespace) -> None:
    labels = {item.strip() for item in args.labels.split(",") if item.strip()}
    refused = sorted(labels & REFUSED_MARKERS)
    if refused:
        fail("refused labels: " + ", ".join(refused))
    if args.risk == "high" and not args.approval_file:
        fail("risk:high requires explicit approval")
    if not args.acceptance or args.acceptance == "missing":
        fail("missing acceptance criteria")


def source_identity(args: argparse.Namespace) -> tuple[str, str, str, Path]:
    if args.source == "issue" or args.issue:
        if not args.issue:
            fail("--source issue requires --issue")
        ident = str(args.issue)
        branch = f"codex/issue-{ident}"
        run_path = Path(".chatgpt/issue-runs") / f"issue-{ident}" / "run.yaml"
        return "issue", ident, branch, run_path
    if args.source == "task" or args.task_id:
        if not args.task_id:
            fail("--source task requires --task-id")
        if not re.fullmatch(r"[A-Z]+-TASK-\d{4}|[A-Z][A-Z0-9_-]+", args.task_id):
            fail("task id must look like FT-TASK-0001 or a safe uppercase id")
        branch = f"codex/task-{args.task_id}"
        run_path = Path(".chatgpt/task-runs") / args.task_id / "run.yaml"
        return "task", args.task_id, branch, run_path
    if args.handoff:
        return "handoff", args.handoff, "codex/task-run", Path(".chatgpt/task-runs/manual/run.yaml")
    fail("one source is required: --source issue --issue, --source task --task-id, or --handoff")


def write_run(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schema: bounded-task-run/v1"]
    for key, value in values.items():
        lines.append(f"{key}: \"{str(value).replace(chr(10), ' ')}\"")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_validator(name: str) -> None:
    script = Path("template-repo/scripts") / name
    if not script.exists():
        fail(f"missing required validator: {name}")
    proc = subprocess.run([sys.executable, str(script), "."], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        fail(f"{name} failed: {proc.stderr.strip() or proc.stdout.strip()}")


def main() -> int:
    args = parse_args()
    validate_task(args)
    source, identifier, branch, run_path = source_identity(args)
    target = f"{source}/{identifier}"
    approval = read_approval(args.approval_file)
    scope = "parallel-runner" if args.max_concurrency > 1 else ("high-risk" if args.risk == "high" else "issue-fix")

    if args.max_concurrency < 1:
        fail("max_concurrency must be >= 1")
    if args.max_concurrency > 1:
        if not args.allow_parallel:
            fail("max_concurrency > 1 requires --allow-parallel")
        decision = decide("parallel-runner", args.actor, args.actor_permission, target, approval)
        if not decision["allowed"]:
            fail("parallel runner approval refused: " + decision["reason"])
        run_validator("validate-worktree-manager.py")
        run_validator("validate-automation-run-ledger.py")
        run_validator("validate-automation-rollback.py")
    elif args.risk == "high":
        decision = decide("high-risk", args.actor, args.actor_permission, target, approval)
        if not decision["allowed"]:
            fail("high-risk approval refused: " + decision["reason"])
    else:
        decision = decide("issue-fix", args.actor, args.actor_permission, target)

    script_prefix = "template-repo/scripts" if Path("template-repo/scripts").exists() else "scripts"
    launcher_command = f"bash {script_prefix}/launch-codex-task.sh --launch-source direct-task --task-text bounded-runner:{source}:{identifier} --dry-run"
    if args.handoff:
        launcher_command = f"bash {script_prefix}/launch-codex-task.sh --launch-source direct-task --task-file {args.handoff} --dry-run"
    worktree = f".worktrees/codex/{source}-{identifier}".replace("/", "-") if args.max_concurrency > 1 else ""
    rollback_plan = f"reports/full-autonomous-mode/rollback-{source}-{identifier}.md"
    status = "parallel_dry_run_planned" if args.max_concurrency > 1 else "dry_run_planned"

    if args.write and args.max_concurrency == 1:
        subprocess.run(["git", "switch", "-C", branch], check=True)
        subprocess.run(launcher_command.split(), check=False)
        status = "one_task_launcher_dry_run_complete"
    elif args.write and args.max_concurrency > 1:
        fail("parallel write execution is not enabled by this runner; use approved per-worktree launches")

    write_run(
        run_path,
        {
            "source": source,
            "identifier": identifier,
            "status": status,
            "claim": f"{source}:{identifier}",
            "exact_command": " ".join(sys.argv),
            "worktree_path": worktree,
            "branch": branch,
            "commit_hash": "",
            "pr_plan_url": "" if args.no_pr else "planned-after-human-review",
            "verification_result": "pending",
            "rollback_plan_path": rollback_plan,
            "max_concurrency": str(args.max_concurrency),
            "dry_run": str(not args.write).lower(),
            "no_push": str(args.no_push).lower(),
            "no_pr": str(args.no_pr).lower(),
            "launcher_command": launcher_command,
            "safety": "no auto-merge, no production deploy, no security/external-secret tasks",
        },
    )
    append_entry(
        Path(".chatgpt") / "automation-runs" / "ledger.jsonl",
        {
            "run_id": f"bounded-{source}-{identifier}",
            "issue_or_task_id": target,
            "trigger": "bounded-task-runner",
            "actor": args.actor,
            "permission_decision": decision,
            "approvals": [approval.get("approval_id")] if approval else [],
            "worktree": worktree,
            "branch": branch,
            "commands": [launcher_command],
            "launcher_command": launcher_command,
            "verification": "pending",
            "verification_commands_results": "pending",
            "pr_url": "",
            "rollback_plan": rollback_plan,
            "final_status": status,
        },
    )
    print(f"bounded_runner_status={status}")
    print(f"run_yaml={run_path}")
    print(f"launcher_command={launcher_command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
