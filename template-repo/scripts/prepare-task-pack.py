#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_REGISTRY = "template-repo/template/.chatgpt/task-registry.yaml"
DEFAULT_DASHBOARD = "template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml"
PREVIEW_SCRIPT = "template-repo/scripts/preview-task-handoff.py"
HANDOFF_SCRIPT = "template-repo/scripts/task-to-codex-handoff.py"
HANDOFF_VALIDATOR = "template-repo/scripts/validate-codex-task-handoff.py"
REGISTRY_VALIDATOR = "template-repo/scripts/validate-task-registry.py"
STATUS_SCRIPT = "template-repo/scripts/update-task-status.py"


def default_preview_path(task_id: str) -> str:
    return f"reports/handoffs/{task_id}-preview.md"


def default_handoff_path(task_id: str) -> str:
    return f"reports/handoffs/{task_id}-codex-handoff.md"


def run_step(label: str, cmd: list[str], *, dry_run: bool) -> None:
    printable = " ".join(cmd)
    if dry_run:
        print(f"dry_run_step={label}")
        print(f"command={printable}")
        return
    print(f"step={label}")
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Готовит repo-native task pack: preview, Codex handoff, validation, optional ready_for_codex transition."
    )
    parser.add_argument("--registry", default=DEFAULT_REGISTRY)
    parser.add_argument("--dashboard", default=DEFAULT_DASHBOARD)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--preview-output", default="")
    parser.add_argument("--handoff-output", default="")
    parser.add_argument("--mark-ready-for-codex", action="store_true")
    parser.add_argument("--sync-dashboard", action="store_true")
    parser.add_argument("--reason", default="Task pack prepared: preview, generated handoff and validation completed.")
    parser.add_argument("--write", action="store_true", help="Без этого флага команда только показывает planned commands.")
    args = parser.parse_args()

    preview_output = args.preview_output or default_preview_path(args.task_id)
    handoff_output = args.handoff_output or default_handoff_path(args.task_id)
    dry_run = not args.write

    print(f"task_pack_prepare={'dry_run' if dry_run else 'write'}")
    print(f"task_id={args.task_id}")
    print(f"preview_output={preview_output}")
    print(f"handoff_output={handoff_output}")
    print("launch_boundary=does_not_start_codex")
    print("route_boundary=advisory_preview_only_no_model_or_reasoning_autoswitch")

    run_step(
        "validate_registry",
        [sys.executable, REGISTRY_VALIDATOR, args.registry],
        dry_run=dry_run,
    )
    run_step(
        "write_preview",
        [
            sys.executable,
            PREVIEW_SCRIPT,
            "--registry",
            args.registry,
            "--task-id",
            args.task_id,
            "--handoff-output",
            handoff_output,
            "--output",
            preview_output,
        ],
        dry_run=dry_run,
    )
    run_step(
        "write_handoff",
        [
            sys.executable,
            HANDOFF_SCRIPT,
            "--registry",
            args.registry,
            "--task-id",
            args.task_id,
            "--output",
            handoff_output,
        ],
        dry_run=dry_run,
    )
    run_step(
        "validate_handoff",
        [sys.executable, HANDOFF_VALIDATOR, handoff_output],
        dry_run=dry_run,
    )
    if args.mark_ready_for_codex:
        status_cmd = [
            sys.executable,
            STATUS_SCRIPT,
            "--registry",
            args.registry,
            "--dashboard",
            args.dashboard,
            "--task-id",
            args.task_id,
            "--status",
            "ready_for_codex",
            "--reason",
            args.reason,
            "--evidence",
            preview_output,
            "--evidence",
            handoff_output,
        ]
        if args.sync_dashboard:
            status_cmd.append("--sync-dashboard")
        if args.write:
            status_cmd.append("--write")
        run_step("mark_ready_for_codex", status_cmd, dry_run=dry_run)
    else:
        print("mark_ready_for_codex=skipped")
        print("hint=Use --mark-ready-for-codex --write after reviewing preview and handoff.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
