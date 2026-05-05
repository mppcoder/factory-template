#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"worktree-manager: {msg}")


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dry-run-first isolated worktree manager for automation tasks.")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--source", choices=["issue", "task"], required=True)
    parser.add_argument("--id", help="Issue number or task id.")
    parser.add_argument("--issue", type=int)
    parser.add_argument("--task-id")
    parser.add_argument("--create", action="store_true")
    parser.add_argument("--cleanup", choices=["dry-run", "completed", "failed"])
    parser.add_argument("--stale-lock-cleanup", action="store_true")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def normalized_identity(args: argparse.Namespace) -> tuple[str, str, str, Path]:
    raw_id = args.id or (str(args.issue) if args.issue is not None else None) or args.task_id
    if not raw_id:
        fail("one id is required: --id, --issue, or --task-id")
    if args.source == "issue":
        if not re.fullmatch(r"\d+", raw_id):
            fail("issue id must be numeric")
        key = f"issue-{raw_id}"
        branch = f"codex/issue-{raw_id}"
        state = Path(".chatgpt/issue-runs") / key / "run.yaml"
    else:
        safe = raw_id.upper()
        if not re.fullmatch(r"[A-Z][A-Z0-9_-]*", safe):
            fail("task id must be uppercase-ish and path safe")
        key = f"task-{safe}"
        branch = f"codex/task-{safe}"
        state = Path(".chatgpt/task-runs") / safe / "run.yaml"
    return raw_id, key, branch, state


def write_run_state(path: Path, values: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schema: worktree-manager-run/v1"]
    for key, value in values.items():
        lines.append(f"{key}: \"{str(value).replace(chr(10), ' ')}\"")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ensure_no_secret_capture(root: Path) -> None:
    for rel in [".env", ".env.local", ".env.production"]:
        if (root / rel).exists():
            # Git worktree add does not copy untracked files. Keep the guard explicit in the plan.
            continue


def main() -> int:
    args = parse_args()
    root = Path(args.repo).resolve()
    if not root.exists():
        fail(f"repo does not exist: {root}")
    raw_id, key, branch, state_rel = normalized_identity(args)
    worktree_rel = Path(".worktrees/codex") / key
    worktree_path = root / worktree_rel
    lock_path = root / ".chatgpt/automation-runs/locks" / f"{key}.lock"
    state_path = root / state_rel
    write_mode = bool(args.write)
    action = "cleanup" if args.cleanup else "create"

    if branch in {"main", "master"} or branch.startswith("main/"):
        fail("main rewrite refused")
    if lock_path.exists() and action == "create" and not args.stale_lock_cleanup:
        fail("stale lock exists; use explicit cleanup command after human review")

    ensure_no_secret_capture(root)
    plan = {
        "source": args.source,
        "id": raw_id,
        "key": key,
        "branch": branch,
        "worktree_path": str(worktree_path),
        "lock_path": str(lock_path),
        "run_state": str(state_path),
        "mode": "write" if write_mode else "dry-run",
        "secrets": "not-copied; untracked .env files stay in repo root and are not captured",
        "main_rewrite": "refused",
    }

    if args.cleanup:
        if args.cleanup == "failed":
            plan["cleanup"] = "preserve failed worktree and lock for inspection"
        elif args.cleanup == "dry-run":
            plan["cleanup"] = "show cleanup plan only"
        else:
            plan["cleanup"] = "remove completed worktree only with --write"
        if write_mode and args.cleanup == "completed":
            proc = run(["git", "worktree", "remove", str(worktree_path)], root)
            if proc.returncode != 0 and worktree_path.exists():
                shutil.rmtree(worktree_path)
            if lock_path.exists():
                lock_path.unlink()
            write_run_state(state_path, {**plan, "status": "completed_cleanup"})
        print("worktree_manager_plan=" + repr(plan))
        return 0

    if not args.create:
        plan["status"] = "planned"
        print("worktree_manager_plan=" + repr(plan))
        return 0

    if write_mode:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path.write_text(f"schema: automation-lock/v1\nkey: {key}\npid: {os.getpid()}\n", encoding="utf-8")
        worktree_path.parent.mkdir(parents=True, exist_ok=True)
        proc = run(["git", "rev-parse", "--is-inside-work-tree"], root)
        if proc.returncode != 0:
            fail("write mode requires a git repository")
        proc = run(["git", "worktree", "add", "-B", branch, str(worktree_path), "HEAD"], root)
        if proc.returncode != 0:
            fail(proc.stderr.strip() or "git worktree add failed")
        write_run_state(state_path, {**plan, "status": "created"})
        plan["status"] = "created"
    else:
        plan["status"] = "dry_run_planned"
    print("worktree_manager_plan=" + repr(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
