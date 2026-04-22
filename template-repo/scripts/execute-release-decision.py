#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from factory_automation_common import (
    AutomationError,
    ensure_clean_repo,
    ensure_runtime_dirs,
    file_lock,
    gh_available,
    head_sha,
    last_sync_report,
    now_utc,
    parse_version_md,
    push_tag,
    read_text,
    release_dir,
    release_report_path,
    remote_url,
    repo_root,
    run_git,
    validate_release_decision_data,
    validate_verify_prereqs,
    write_report,
)


def render_notes(decision: dict, notes_body: str) -> str:
    return "\n".join(
        [
            f"# Release v{decision['version']}",
            "",
            f"- Channel: `{decision['channel']}`",
            f"- Approved by: `{decision['approved_by']}`",
            f"- Notes source: `{decision['notes_source']}`",
            "",
            notes_body.strip(),
            "",
        ]
    )


def publish_release(root: Path, tag: str, notes_path: Path) -> tuple[str, str, str]:
    if not gh_available():
        return "manual-fallback", "CLI `gh` не найден в окружении", ""
    auth = subprocess.run(["gh", "auth", "status"], cwd=root, text=True, capture_output=True, check=False)
    if auth.returncode != 0:
        return "manual-fallback", "CLI `gh` не авторизован", ""
    view = subprocess.run(
        ["gh", "release", "view", tag, "--json", "url", "-q", ".url"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if view.returncode == 0 and view.stdout.strip():
        return "already-published", "", view.stdout.strip()
    create = subprocess.run(
        ["gh", "release", "create", tag, "--title", tag, "--notes-file", str(notes_path)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if create.returncode != 0:
        return "manual-fallback", create.stderr.strip() or create.stdout.strip() or "gh release create failed", ""
    url = create.stdout.strip().splitlines()[-1] if create.stdout.strip() else ""
    return "published", "", url


def main() -> int:
    root = repo_root(sys.argv[1] if len(sys.argv) > 1 else ".")
    report_path = release_report_path(root)
    try:
        with file_lock(root, "release-executor.lock"):
            validate_verify_prereqs(root)
            decision = validate_release_decision_data(root)
            sync_report = last_sync_report(root)
            if sync_report.get("status") not in {"pushed", "no-op"}:
                raise AutomationError("release executor требует успешный VERIFIED_SYNC.sh перед запуском")
            if sync_report.get("commit_sha") != head_sha(root):
                raise AutomationError("release executor требует актуальный sync report для текущего HEAD")

            if decision.get("decision") == "no-release":
                report = {
                    "timestamp": now_utc(),
                    "decision": "no-release",
                    "status": "skipped-no-release",
                    "version": decision.get("version"),
                    "notes_source": decision.get("notes_source"),
                    "approved_by": decision.get("approved_by"),
                }
                write_report(report_path, report)
                print("RELEASE EXECUTOR: no-release, publish пропущен")
                return 0

            ensure_clean_repo(root)
            current_version = parse_version_md(root)
            decision_version = str(decision.get("version"))
            if current_version != decision_version:
                raise AutomationError(
                    f"VERSION.md={current_version} не совпадает с release-decision.yaml version={decision_version}"
                )

            ensure_runtime_dirs(root)
            notes_body = read_text(root / str(decision["notes_source"]))
            tag = f"v{decision_version}"
            notes_path = release_dir(root) / f"{tag}-notes.md"
            notes_path.write_text(render_notes(decision, notes_body), encoding="utf-8")

            existing = run_git(root, ["rev-parse", "-q", "--verify", f"refs/tags/{tag}"], check=False)
            head = head_sha(root)
            if existing.returncode == 0:
                tagged_sha = existing.stdout.strip()
                if tagged_sha != head:
                    raise AutomationError(f"Tag `{tag}` уже существует и указывает не на текущий HEAD")
            else:
                run_git(root, ["tag", "-a", tag, "-m", f"Release {tag}"])

            push_url = remote_url(root, "origin", "push")
            pushed_via, tag_push_status = push_tag(root, tag, push_url)
            publish_status, reason, release_url = publish_release(root, tag, notes_path)
            report = {
                "timestamp": now_utc(),
                "decision": "release",
                "status": publish_status,
                "version": decision_version,
                "tag": tag,
                "tag_push_status": tag_push_status,
                "tag_remote": pushed_via,
                "notes_source": decision.get("notes_source"),
                "notes_artifact": str(notes_path.relative_to(root)),
                "approved_by": decision.get("approved_by"),
                "release_url": release_url,
            }
            if publish_status == "manual-fallback":
                report["reason"] = reason
                report["manual_actions"] = [
                    f"Проверить tag `{tag}` в GitHub",
                    f"Открыть notes artifact `{notes_path.relative_to(root)}`",
                    "Опубликовать GitHub Release вручную через gh CLI или GitHub UI",
                ]
            write_report(report_path, report)
            print("RELEASE EXECUTOR ПРОЙДЕН")
            print(f"- tag: {tag}")
            print(f"- publish_status: {publish_status}")
            if release_url:
                print(f"- release_url: {release_url}")
            return 0
    except AutomationError as exc:
        write_report(
            report_path,
            {
                "timestamp": now_utc(),
                "decision": "release-error",
                "status": "failed",
                "reason": str(exc),
            },
        )
        print("RELEASE EXECUTOR НЕ ПРОЙДЕН")
        print(f"- {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
