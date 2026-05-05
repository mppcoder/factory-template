#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    raise SystemExit(f"validate-worktree-manager: {msg}")


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    script = root / "template-repo/scripts/worktree_manager.py"
    docs = [
        root / "docs/operator/factory-template/worktree-manager.md",
        root / "template-repo/template/docs/operator/worktree-manager.md",
    ]
    if not script.exists():
        fail("missing worktree_manager.py")
    text = script.read_text(encoding="utf-8")
    for doc in docs:
        if not doc.exists():
            fail(f"missing {doc}")
        text += "\n" + doc.read_text(encoding="utf-8")
    for marker in [
        ".worktrees/codex/issue-<N>",
        ".worktrees/codex/task-<ID>",
        ".chatgpt/automation-runs/locks",
        ".chatgpt/issue-runs/issue-<N>/run.yaml",
        ".chatgpt/task-runs/<TASK-ID>/run.yaml",
        "--write",
        "dry-run",
        "no secrets",
        "no main rewrite",
        "stale lock",
    ]:
        if marker not in text:
            fail(f"missing marker: {marker}")
    with tempfile.TemporaryDirectory() as tmp_raw:
        tmp = Path(tmp_raw)
        run(["git", "init", "-b", "main"], tmp)
        (tmp / "README.md").write_text("fixture\n", encoding="utf-8")
        run(["git", "add", "README.md"], tmp)
        run(["git", "-c", "user.email=a@example.test", "-c", "user.name=Validator", "commit", "-m", "init"], tmp)
        script_abs = script.resolve()
        dry = run([sys.executable, str(script_abs), "--repo", str(tmp), "--source", "issue", "--issue", "7", "--create"], tmp)
        if dry.returncode != 0 or "dry_run_planned" not in dry.stdout:
            fail(dry.stderr.strip() or "dry-run plan failed")
        write = run([sys.executable, str(script_abs), "--repo", str(tmp), "--source", "task", "--task-id", "FT-TASK-0007", "--create", "--write"], tmp)
        if write.returncode != 0:
            fail(write.stderr.strip() or "write smoke failed")
        if not (tmp / ".worktrees/codex/task-FT-TASK-0007").exists():
            fail("worktree was not created in temp repo")
        if not (tmp / ".chatgpt/task-runs/FT-TASK-0007/run.yaml").exists():
            fail("run.yaml missing")
    print("validate-worktree-manager=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
