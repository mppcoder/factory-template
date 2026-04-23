#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from codex_task_router import build_launch_record, read_task_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve Codex task class and selected profile.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root")
    parser.add_argument("--task-file", help="Path to task file")
    parser.add_argument("--task-text", help="Inline task text")
    parser.add_argument("--task-class", help="Explicit task class override")
    parser.add_argument("--launch-source", choices=["chatgpt-handoff", "direct-task"], required=True)
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    task_file = Path(args.task_file).resolve() if args.task_file else None
    task_text = read_task_text(task_file, args.task_text)
    record = build_launch_record(root, args.launch_source, task_text, args.task_class)
    if args.json:
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return 0

    launch = record["launch"]
    print("CODEX TASK ROUTE RESOLVED")
    print(f"launch_source={launch['launch_source']}")
    print(f"task_class={launch['task_class']}")
    print(f"selected_profile={launch['selected_profile']}")
    print(f"selected_model={launch['selected_model']}")
    print(f"selected_reasoning_effort={launch['selected_reasoning_effort']}")
    print(f"selected_plan_mode_reasoning_effort={launch['selected_plan_mode_reasoning_effort']}")
    print(f"apply_mode={launch['apply_mode']}")
    print(f"strict_launch_mode={launch['strict_launch_mode']}")
    print(f"selected_scenario={launch['selected_scenario']}")
    print(f"pipeline_stage={launch['pipeline_stage']}")
    print(f"handoff_allowed={launch['handoff_allowed']}")
    print(f"defect_capture_path={launch['defect_capture_path']}")
    print(f"launch_artifact_path={launch['launch_artifact_path']}")
    print(f"launch_command={launch['launch_command']}")
    print(f"codex_profile_command={launch['codex_profile_command']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
