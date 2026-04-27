#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def first_existing(workspace: Path, candidates: list[str]) -> Path | None:
    for candidate in candidates:
        path = workspace / candidate
        if path.exists():
            return path
    return None


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
        if lowered in {"- пока записей нет.", "пока записей нет.", "- пока не указано", "todo"}:
            continue
        lines.append(line)
    return lines


def section_text(text: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_decisions(decisions_text: str) -> list[str]:
    lines = []
    for line in meaningful_lines(section_text(decisions_text, "Записи") or decisions_text):
        if line.startswith("- decision:") or line.startswith("**Decision:**"):
            value = re.sub(r"^(- decision:|\*\*Decision:\*\*)\s*", "", line).strip()
            if value and value.lower() not in {"нет", "none", "нет новых решений"}:
                lines.append(value)
        elif line.startswith("- summary:") or line.startswith("**Summary:**"):
            value = re.sub(r"^(- summary:|\*\*Summary:\*\*)\s*", "", line).strip()
            if value:
                lines.append(value)
    if lines:
        return lines
    return meaningful_lines(decisions_text)[:8]


def extract_followups(decisions_text: str) -> list[str]:
    followups: list[str] = []
    for line in meaningful_lines(decisions_text):
        if line.startswith("- follow_up:"):
            value = line.split(":", 1)[1].strip()
            if value and value.lower() not in {"нет", "none", "не требуется"}:
                followups.append(value)
    return followups


def summarize_markdown(text: str, fallback: str) -> str:
    for line in meaningful_lines(text):
        cleaned = line.lstrip("-* ").strip()
        if cleaned:
            return cleaned[:280]
    return fallback


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


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(read_text(path)) or {}
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def run_validator(root: Path, workspace: Path) -> tuple[bool, str]:
    script = root / "template-repo" / "scripts" / "validate-feature-execution-lite.py"
    if not script.exists():
        script = root / "scripts" / "validate-feature-execution-lite.py"
    if not script.exists():
        return False, "validate-feature-execution-lite.py не найден"
    proc = subprocess.run(
        [sys.executable, str(script), str(root), "--workspace", str(workspace), "--require-advanced"],
        text=True,
        capture_output=True,
        check=False,
    )
    output = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, output


def normalize_artifact_eval_report(report: str | None, root: Path) -> Path | None:
    if not report:
        return None
    path = Path(report).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def validate_artifact_eval_report(root: Path, report: Path) -> tuple[bool, str]:
    script = root / "template-repo" / "scripts" / "validate-artifact-eval-report.py"
    if not script.exists():
        script = root / "scripts" / "validate-artifact-eval-report.py"
    if not script.exists():
        return False, "validate-artifact-eval-report.py не найден"
    proc = subprocess.run(
        [sys.executable, str(script), str(report)],
        text=True,
        capture_output=True,
        check=False,
    )
    output = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, output


def project_knowledge_targets(followups: list[str], decisions: list[str]) -> list[str]:
    text = "\n".join(followups + decisions).lower()
    targets: list[str] = []
    if any(word in text for word in ["архитект", "component", "schema", "data", "интеграц"]):
        targets.append("project-knowledge/architecture.md")
    if any(word in text for word in ["deploy", "release", "verification", "поставка", "выклад"]):
        targets.append("project-knowledge/deployment.md")
    if any(word in text for word in ["pattern", "паттерн", "правило", "workflow", "loop"]):
        targets.append("project-knowledge/patterns.md")
    if any(word in text for word in ["constraint", "огранич", "нельзя", "must"]):
        targets.append("project-knowledge/constraints.md")
    if followups and not targets:
        targets.append("project-knowledge/project.md")
    return sorted(set(targets))


def build_project_knowledge_proposal(feature_id: str, decisions: list[str], followups: list[str]) -> str:
    targets = project_knowledge_targets(followups, decisions)
    status = "required" if followups or targets else "not_required"
    justification = (
        "В decisions.md есть follow_up или устойчивые решения, которые нужно рассмотреть для переноса."
        if status == "required"
        else "В decisions.md не найдено устойчивых follow_up; рабочие решения остаются в архиве feature."
    )
    lines = [
        f"# Project Knowledge update proposal: {feature_id}",
        "",
        "## Status",
        "",
        f"- status: {status}",
        f"- justification: {justification}",
        "",
        "## Proposed updates",
        "",
    ]
    if targets:
        for target in targets:
            lines.append(f"- `{target}`: перенести устойчивый вывод из decisions.md после человеческой проверки формулировки.")
    else:
        lines.append("- Не требуется.")
    lines.extend(["", "## Source decisions", ""])
    if decisions:
        for item in decisions:
            lines.append(f"- {item}")
    else:
        lines.append("- Нет извлеченных решений.")
    if followups:
        lines.extend(["", "## Follow-up candidates", ""])
        for item in followups:
            lines.append(f"- {item}")
    return "\n".join(lines)


def build_downstream_impact(feature_id: str, pk_required: bool, advanced: bool) -> str:
    impact = "required-review" if pk_required or advanced else "not-required"
    reason = (
        "Feature меняет устойчивые знания или advanced execution evidence; downstream sync должен увидеть closeout note."
        if impact == "required-review"
        else "Feature закрыта без изменений template-owned или project-knowledge source-of-truth."
    )
    return "\n".join(
        [
            f"# Downstream impact: {feature_id}",
            "",
            "## Status",
            "",
            f"- downstream_template_sync: {impact}",
            "- downstream_project_sources: review-project-knowledge-proposal",
            f"- reason: {reason}",
            "",
            "## Notes",
            "",
            "- Если feature меняла template-owned файлы, включите это в обычный downstream sync package.",
            "- Если менялись только project-owned знания, переносите их вручную через diff/merge guidance.",
        ]
    )


def build_done_report(
    *,
    feature_id: str,
    root: Path,
    workspace: Path,
    user_spec: Path | None,
    tech_spec: Path | None,
    decisions_path: Path,
    decisions: list[str],
    followups: list[str],
    advanced: bool,
    advanced_ok: bool | None,
    advanced_output: str,
    artifact_report: Path | None,
    artifact_ok: bool | None,
    artifact_required: bool,
    archive_target: Path,
    archive_blocker: str | None,
) -> str:
    user_summary = summarize_markdown(read_text(user_spec) if user_spec else "", "User-spec не найден.")
    tech_summary = summarize_markdown(read_text(tech_spec) if tech_spec else "", "Tech-spec не найден.")
    lines = [
        f"# Feature closeout report: {feature_id}",
        "",
        f"> generated_at: {datetime.now(timezone.utc).isoformat()}",
        f"> source_workspace: {rel(workspace, root)}",
        "",
        "## Feature summary",
        "",
        f"- user_spec_summary: {user_summary}",
        f"- tech_spec_summary: {tech_summary}",
        "",
        "## Source artifacts read",
        "",
        f"- user-spec: `{rel(user_spec, root) if user_spec else 'missing'}`",
        f"- tech-spec: `{rel(tech_spec, root) if tech_spec else 'missing'}`",
        f"- decisions: `{rel(decisions_path, root)}`",
        "",
        "## Decisions extracted",
        "",
    ]
    if decisions:
        lines.extend(f"- {item}" for item in decisions)
    else:
        lines.append("- Нет извлеченных решений.")
    lines.extend(["", "## Project Knowledge update proposal", ""])
    if followups:
        lines.append("- proposal: `project-knowledge-update-proposal.md`")
        lines.extend(f"- candidate: {item}" for item in followups)
    else:
        lines.append("- proposal: `project-knowledge-update-proposal.md`")
        lines.append("- result: not_required; устойчивых follow_up не найдено.")
    lines.extend(["", "## Downstream impact", "", "- note: `downstream-impact.md`", ""])
    lines.extend(["## Done evidence", ""])
    if advanced:
        status = "passed" if advanced_ok else "failed"
        lines.append(f"- feature-execution-lite validation: {status}")
        if advanced_output:
            first_line = advanced_output.splitlines()[0]
            lines.append(f"- feature-execution-lite validator: {first_line}")
    else:
        lines.append("- feature-execution-lite validation: not_applicable")
    lines.append("- artifact eval evidence:")
    if artifact_report:
        artifact_status = "passed" if artifact_ok else "failed"
        lines.append(f"  - report: `{rel(artifact_report, root)}`")
        lines.append(f"  - status: {artifact_status}")
    elif artifact_required:
        lines.append("  - status: missing_required")
    else:
        lines.append("  - status: not_required")
        lines.append("  - reason: Feature closeout did not change reusable scenario, skill, policy or advanced template artifact.")
    lines.extend(["", "## Archive", ""])
    if archive_blocker:
        lines.append(f"- status: blocked")
        lines.append(f"- blocker: {archive_blocker}")
    else:
        lines.append("- status: archived")
        lines.append(f"- target: `{rel(archive_target, root)}`")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Close a feature workspace with Project Knowledge done-loop artifacts.")
    parser.add_argument("workspace", help="Path to work/features/<feature-id> workspace.")
    parser.add_argument("--root", default=".", help="Repo root. Defaults to current directory.")
    parser.add_argument("--archive-base", help="Archive base directory. Defaults to <root>/work/completed.")
    parser.add_argument("--feature-id", help="Override feature id. Defaults to workspace directory name.")
    parser.add_argument("--artifact-eval-report", help="Optional artifact-eval report to link as done evidence.")
    parser.add_argument("--artifact-eval-required", action="store_true", help="Fail closeout if artifact eval evidence is missing.")
    parser.add_argument("--skip-archive", action="store_true", help="Do not move workspace; write closeout-blocker.md instead.")
    parser.add_argument("--archive-blocker", help="Blocker text to document when --skip-archive is used.")
    parser.add_argument("--force", action="store_true", help="Replace existing archive target.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    workspace = Path(args.workspace).expanduser().resolve()
    feature_id = args.feature_id or workspace.name
    archive_base = Path(args.archive_base).expanduser().resolve() if args.archive_base else root / "work" / "completed"
    archive_target = archive_base / feature_id

    errors: list[str] = []
    if not workspace.exists() or not workspace.is_dir():
        errors.append(f"workspace not found: {workspace}")

    user_spec = first_existing(workspace, ["specs/user-spec.md", "user-spec.md"])
    tech_spec = first_existing(workspace, ["specs/tech-spec.md", "tech-spec.md"])
    decisions_path = workspace / "decisions.md"
    if not user_spec:
        errors.append("missing user-spec")
    if not tech_spec:
        errors.append("missing tech-spec")
    if not decisions_path.exists():
        errors.append("missing decisions.md")

    decisions_text = read_text(decisions_path)
    decisions = extract_decisions(decisions_text)
    followups = extract_followups(decisions_text)
    if not decisions:
        errors.append("decisions.md is empty or placeholder-only")

    advanced = is_feature_execution_lite(workspace)
    advanced_ok: bool | None = None
    advanced_output = ""
    if advanced:
        advanced_ok, advanced_output = run_validator(root, workspace)
        if not advanced_ok:
            errors.append("feature-execution-lite validation failed")

    artifact_report = normalize_artifact_eval_report(args.artifact_eval_report, root)
    artifact_ok: bool | None = None
    if artifact_report:
        if not artifact_report.exists():
            errors.append(f"artifact eval report not found: {artifact_report}")
            artifact_ok = False
        else:
            artifact_ok, artifact_output = validate_artifact_eval_report(root, artifact_report)
            if not artifact_ok:
                errors.append(f"artifact eval report invalid: {artifact_output}")
    elif args.artifact_eval_required:
        errors.append("artifact eval report is required but missing")

    archive_blocker = args.archive_blocker if args.skip_archive else None
    if args.skip_archive and not archive_blocker:
        archive_blocker = "Archive skipped by operator; move workspace to work/completed when blocker is resolved."

    if errors:
        print("FEATURE CLOSEOUT НЕ ВЫПОЛНЕН")
        for error in errors:
            print("-", error)
        if workspace.exists():
            write_text(workspace / "closeout-blocker.md", "# Closeout blocker\n\n" + "\n".join(f"- {error}" for error in errors))
        return 1

    pk_proposal = build_project_knowledge_proposal(feature_id, decisions, followups)
    pk_required = "- status: required" in pk_proposal
    write_text(workspace / "project-knowledge-update-proposal.md", pk_proposal)
    write_text(workspace / "downstream-impact.md", build_downstream_impact(feature_id, pk_required, advanced))
    write_text(
        workspace / "done-report.md",
        build_done_report(
            feature_id=feature_id,
            root=root,
            workspace=workspace,
            user_spec=user_spec,
            tech_spec=tech_spec,
            decisions_path=decisions_path,
            decisions=decisions,
            followups=followups,
            advanced=advanced,
            advanced_ok=advanced_ok,
            advanced_output=advanced_output,
            artifact_report=artifact_report,
            artifact_ok=artifact_ok,
            artifact_required=args.artifact_eval_required,
            archive_target=archive_target,
            archive_blocker=archive_blocker,
        ),
    )

    if args.skip_archive:
        write_text(workspace / "closeout-blocker.md", f"# Closeout blocker\n\n- {archive_blocker}")
        print(f"FEATURE CLOSEOUT BLOCKED: {workspace}")
        return 0

    archive_base.mkdir(parents=True, exist_ok=True)
    if archive_target.exists():
        if not args.force:
            print("FEATURE CLOSEOUT НЕ ВЫПОЛНЕН")
            print(f"- archive target already exists: {archive_target}")
            return 1
        shutil.rmtree(archive_target)
    shutil.move(str(workspace), str(archive_target))
    print(f"FEATURE CLOSEOUT ВЫПОЛНЕН: {archive_target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
