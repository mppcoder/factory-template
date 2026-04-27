#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def meaningful_lines(text: str) -> list[str]:
    lines: list[str] = []
    in_comment = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("<!--"):
            in_comment = True
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if not line or line.startswith("#") or line.startswith(">"):
            continue
        if "{{" in line or "}}" in line:
            continue
        lowered = line.lower()
        if "пока записей нет" in lowered or lowered in {"todo", "-"}:
            continue
        lines.append(line)
    return lines


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(read_text(path)) or {}
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def checkpoint_path(workspace: Path) -> Path:
    for candidate in [workspace / "logs" / "checkpoint.yaml", workspace / "logs" / "checkpoint.yml"]:
        if candidate.exists():
            return candidate
    return workspace / "logs" / "checkpoint.yaml"


def is_feature_execution_lite(workspace: Path) -> bool:
    return (
        checkpoint_path(workspace).exists()
        or (workspace / "logs" / "execution-plan.md").exists()
        or "feature-execution-lite" in read_text(workspace / "README.md")
    )


def has_archive_or_blocker(workspace: Path, root: Path) -> bool:
    normalized = workspace.resolve()
    if "work/completed" in str(normalized).replace("\\", "/"):
        return True
    if "completed" in normalized.parts:
        return True
    blocker = workspace / "closeout-blocker.md"
    return blocker.exists() and len(meaningful_lines(read_text(blocker))) >= 1


def proposal_status(text: str) -> tuple[str, bool]:
    status_match = re.search(r"status:\s*([a-zA-Z_-]+)", text)
    status = status_match.group(1).strip() if status_match else ""
    has_justification = bool(re.search(r"justification:\s*\S+", text))
    return status, has_justification


def validate_artifact_eval_report(root: Path, report: Path, errors: list[str]) -> None:
    script = root / "template-repo" / "scripts" / "validate-artifact-eval-report.py"
    if not script.exists():
        script = root / "scripts" / "validate-artifact-eval-report.py"
    if not script.exists():
        errors.append("artifact eval validator not found")
        return
    proc = subprocess.run(
        [sys.executable, str(script), str(report)],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        errors.append(f"invalid artifact eval report `{rel(report, root)}`")


def validate_advanced(workspace: Path, root: Path, errors: list[str]) -> None:
    execution_plan = workspace / "logs" / "execution-plan.md"
    checkpoint = checkpoint_path(workspace)
    decisions = workspace / "decisions.md"
    tasks_dir = workspace / "tasks"
    if not execution_plan.exists():
        errors.append(f"feature-execution-lite: missing `{rel(execution_plan, root)}`")
    if not checkpoint.exists():
        errors.append(f"feature-execution-lite: missing `{rel(checkpoint, root)}`")
        return
    data = load_yaml(checkpoint)
    final = data.get("final_verification") if isinstance(data.get("final_verification"), dict) else {}
    if final.get("status") != "passed":
        errors.append(f"feature-execution-lite: `{rel(checkpoint, root)}` final_verification.status != passed")
    checkpoint_tasks = data.get("tasks") if isinstance(data.get("tasks"), dict) else {}
    if not checkpoint_tasks:
        errors.append(f"feature-execution-lite: `{rel(checkpoint, root)}` has no tasks")
    task_files = sorted(tasks_dir.glob("T-*.md")) if tasks_dir.exists() else []
    if not task_files:
        errors.append(f"feature-execution-lite: `{rel(tasks_dir, root)}` has no T-*.md task waves")
    for path in task_files:
        text = read_text(path)
        if "wave:" not in text:
            errors.append(f"feature-execution-lite: `{rel(path, root)}` has no wave")
    decision_text = read_text(decisions)
    for fragment in ["execution_wave:", "review_rounds:", "boundary:"]:
        if fragment not in decision_text:
            errors.append(f"feature-execution-lite: `{rel(decisions, root)}` lacks `{fragment}`")
    done_text = read_text(workspace / "done-report.md")
    if "artifact eval evidence" not in done_text.lower():
        errors.append(f"feature-execution-lite: `{rel(workspace / 'done-report.md', root)}` lacks artifact eval evidence note")
    report_match = re.search(r"report:\s*`([^`]+artifact[^`]+\.md)`", done_text)
    if report_match:
        report = Path(report_match.group(1))
        if not report.is_absolute():
            report = root / report
        if not report.exists():
            errors.append(f"feature-execution-lite: linked artifact eval report not found `{rel(report, root)}`")
        else:
            validate_artifact_eval_report(root, report, errors)
    elif "status: not_required" not in done_text and "status: missing_required" not in done_text:
        errors.append(f"feature-execution-lite: artifact eval evidence is neither linked nor justified")


def validate_workspace(workspace: Path, root: Path, errors: list[str]) -> None:
    if not workspace.exists():
        errors.append(f"workspace not found: `{rel(workspace, root)}`")
        return
    done = workspace / "done-report.md"
    decisions = workspace / "decisions.md"
    proposal = workspace / "project-knowledge-update-proposal.md"
    downstream = workspace / "downstream-impact.md"
    if not done.exists():
        errors.append(f"missing done report: `{rel(done, root)}`")
    elif len(meaningful_lines(read_text(done))) < 5:
        errors.append(f"weak done report: `{rel(done, root)}`")
    if not decisions.exists():
        errors.append(f"missing decisions: `{rel(decisions, root)}`")
    elif len(meaningful_lines(read_text(decisions))) < 3:
        errors.append(f"empty decisions: `{rel(decisions, root)}`")
    if not proposal.exists():
        errors.append(f"missing project-knowledge update proposal: `{rel(proposal, root)}`")
    else:
        status, justified = proposal_status(read_text(proposal))
        if status not in {"required", "not_required"}:
            errors.append(f"invalid project-knowledge proposal status: `{rel(proposal, root)}`")
        if status == "not_required" and not justified:
            errors.append(f"not_required project-knowledge proposal lacks justification: `{rel(proposal, root)}`")
    if not downstream.exists():
        errors.append(f"missing downstream impact note: `{rel(downstream, root)}`")
    if not has_archive_or_blocker(workspace, root):
        errors.append(f"feature is neither archived nor blocked: `{rel(workspace, root)}`")
    if is_feature_execution_lite(workspace):
        validate_advanced(workspace, root, errors)


def discover_closed_workspaces(root: Path) -> list[Path]:
    out: list[Path] = []
    for base in [root / "work" / "completed", root / "template-repo" / "work" / "completed"]:
        if not base.exists():
            continue
        for child in sorted(base.iterdir()):
            if child.is_dir() and (child / "done-report.md").exists():
                out.append(child)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Project Knowledge done-loop closeout artifacts.")
    parser.add_argument("root", nargs="?", default=".", help="Repo root. Defaults to current directory.")
    parser.add_argument("--workspace", action="append", help="Closed feature workspace to validate.")
    parser.add_argument("--allow-empty", action="store_true", help="Pass when no closed feature workspaces are found.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []
    workspaces = [Path(item).expanduser().resolve() for item in args.workspace or []]
    if not workspaces:
        workspaces = discover_closed_workspaces(root)
    if not workspaces and not args.allow_empty:
        errors.append("no closed feature workspace found")
    for workspace in workspaces:
        validate_workspace(workspace, root, errors)

    if errors:
        print("PROJECT KNOWLEDGE DONE LOOP НЕВАЛИДЕН")
        for error in errors:
            print("-", error)
        return 1
    print("PROJECT KNOWLEDGE DONE LOOP ВАЛИДЕН")
    if not workspaces:
        print("workspace_audit=skipped (no closed feature workspaces found)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
