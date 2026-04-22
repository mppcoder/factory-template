#!/usr/bin/env python3
from __future__ import annotations

import sys

from factory_automation_common import (
    AutomationError,
    changed_paths,
    file_lock,
    head_sha,
    now_utc,
    push_branch,
    repo_root,
    resolve_sync_plan,
    run_git,
    sync_report_path,
    write_report,
)


def main() -> int:
    root = repo_root(sys.argv[1] if len(sys.argv) > 1 else ".")
    report_path = sync_report_path(root)
    try:
        with file_lock(root, "verified-sync.lock"):
            paths = changed_paths(root)
            if not paths:
                report = {
                    "timestamp": now_utc(),
                    "status": "no-op",
                    "change_id": None,
                    "branch": None,
                    "remote": None,
                    "push_status": "skipped-no-diff",
                    "commit_sha": head_sha(root),
                    "staged_paths": [],
                }
                write_report(report_path, report)
                print("VERIFIED SYNC: no-op, diff отсутствует")
                return 0

            plan = resolve_sync_plan(root, paths)
            branch = plan["branch"]
            push_url = plan["push_url"]
            change = plan["change"]

            run_git(root, ["add", "-A", "--", *paths])
            proc = run_git(root, ["diff", "--cached", "--name-only"], check=False)
            staged = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
            if not staged:
                report = {
                    "timestamp": now_utc(),
                    "status": "no-op",
                    "change_id": change.get("id"),
                    "verify_mode": plan["mode"],
                    "branch": branch,
                    "remote": push_url,
                    "push_status": "skipped-denylist-only",
                    "commit_sha": head_sha(root),
                    "staged_paths": [],
                }
                write_report(report_path, report)
                print("VERIFIED SYNC: no-op, после denylist не осталось допустимых изменений")
                return 0

            message = plan["commit_message"]
            run_git(root, ["commit", "-m", message])
            commit_sha = head_sha(root)
            pushed_via, push_status = push_branch(root, branch, push_url)
            report = {
                "timestamp": now_utc(),
                "status": "pushed",
                "change_id": change.get("id"),
                "verify_mode": plan["mode"],
                "branch": branch,
                "remote": pushed_via,
                "push_status": push_status,
                "commit_sha": commit_sha,
                "commit_message": message,
                "staged_paths": staged,
            }
            write_report(report_path, report)
            print("VERIFIED SYNC ПРОЙДЕН")
            print(f"- verify_mode: {plan['mode']}")
            print(f"- commit: {commit_sha}")
            print(f"- branch: {branch}")
            print(f"- remote: {pushed_via}")
            print(f"- push_status: {push_status}")
            return 0
    except AutomationError as exc:
        write_report(
            report_path,
            {
                "timestamp": now_utc(),
                "status": "failed",
                "reason": str(exc),
            },
        )
        print("VERIFIED SYNC НЕ ПРОЙДЕН")
        print(f"- {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
