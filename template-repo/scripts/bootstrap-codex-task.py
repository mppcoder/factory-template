#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from codex_task_router import (
    build_launch_record,
    read_task_text,
    render_direct_task_response,
    render_normalized_handoff,
    write_launch_record,
    write_markdown,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap normalized Codex handoff and launch log.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root")
    parser.add_argument("--task-file", help="Path to task file")
    parser.add_argument("--task-text", help="Inline task text")
    parser.add_argument("--task-class", help="Explicit task class override")
    parser.add_argument("--launch-source", choices=["chatgpt-handoff", "direct-task"], required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    task_file = Path(args.task_file).resolve() if args.task_file else None
    task_text = read_task_text(task_file, args.task_text)
    record = build_launch_record(root, args.launch_source, task_text, args.task_class)

    launch_path = write_launch_record(root, record)
    launch_input_path = root / record["launch"]["launch_artifact_path"]
    write_markdown(launch_input_path, task_text.strip() or "-")
    handoff_path = root / ".chatgpt" / "normalized-codex-handoff.md"
    write_markdown(handoff_path, render_normalized_handoff(record, task_text, "Normalized Codex Handoff"))

    launch = record["launch"]
    if args.launch_source == "direct-task":
        self_handoff_path = root / ".chatgpt" / "direct-task-self-handoff.md"
        write_markdown(self_handoff_path, render_normalized_handoff(record, task_text, "Direct Task Self-Handoff"))
        direct_response_path = root / ".chatgpt" / "direct-task-response.md"
        write_markdown(direct_response_path, render_direct_task_response(record, task_text))
        record["launch"]["direct_self_handoff_completed"] = True
        write_launch_record(root, record)
        print(f"direct_self_handoff={self_handoff_path}")
        print(f"direct_task_response={direct_response_path}")

    print(f"task_launch={launch_path}")
    print(f"launch_input={launch_input_path}")
    print(f"normalized_handoff={handoff_path}")
    print(f"selected_profile={launch['selected_profile']}")
    print(f"selected_model={launch['selected_model']}")
    print(f"selected_reasoning_effort={launch['selected_reasoning_effort']}")
    print(f"apply_mode={launch['apply_mode']}")
    print(f"strict_launch_mode={launch['strict_launch_mode']}")
    print(f"launch_artifact_path={launch['launch_artifact_path']}")
    print(f"launch_command={launch['launch_command']}")
    print(f"codex_profile_command={launch['codex_profile_command']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
