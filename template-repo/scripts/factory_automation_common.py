#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import shutil
import subprocess
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

import yaml


VERIFY_REQUIRED_FILES = [
    ".chatgpt/task-index.yaml",
    ".chatgpt/stage-state.yaml",
    ".chatgpt/verification-report.md",
]

DENY_PREFIXES = [
    ".factory-runtime/",
    ".release-stage/",
    "_sources-export/",
    "_boundary-actions/",
    "_artifacts/",
    ".smoke-test/",
    ".matrix-test/",
    ".bugflow-test/",
    "audit-smoke-project/",
    "__pycache__/",
    ".pytest_cache/",
]

DENY_SUFFIXES = [
    ".log",
    ".pyc",
]


class AutomationError(RuntimeError):
    pass


def repo_root(value: str | None = None) -> Path:
    return Path(value or ".").resolve()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def read_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def runtime_dir(root: Path) -> Path:
    return root / ".factory-runtime"


def reports_dir(root: Path) -> Path:
    return runtime_dir(root) / "reports"


def release_dir(root: Path) -> Path:
    return runtime_dir(root) / "release"


def locks_dir(root: Path) -> Path:
    return runtime_dir(root) / "locks"


def ensure_runtime_dirs(root: Path) -> None:
    reports_dir(root).mkdir(parents=True, exist_ok=True)
    release_dir(root).mkdir(parents=True, exist_ok=True)
    locks_dir(root).mkdir(parents=True, exist_ok=True)


def run_git(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and proc.returncode != 0:
        raise AutomationError(proc.stderr.strip() or proc.stdout.strip() or f"git {' '.join(args)} failed")
    return proc


def ensure_git_repo(root: Path) -> None:
    run_git(root, ["rev-parse", "--git-dir"])


def current_branch(root: Path) -> str:
    branch = run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    if not branch or branch == "HEAD":
        raise AutomationError("Нужна активная ветка; detached HEAD не поддерживается")
    return branch


def head_sha(root: Path) -> str:
    return run_git(root, ["rev-parse", "HEAD"]).stdout.strip()


def remote_url(root: Path, remote: str = "origin", kind: str = "push") -> str:
    args = ["remote", "get-url"]
    if kind == "push":
        args.append("--push")
    args.append(remote)
    proc = run_git(root, args, check=False)
    if proc.returncode == 0:
        return proc.stdout.strip()
    if kind == "push":
        proc = run_git(root, ["remote", "get-url", remote], check=False)
        if proc.returncode == 0:
            return proc.stdout.strip()
    raise AutomationError(f"Не удалось определить {kind} URL для remote `{remote}`")


def fallback_push_url(url: str) -> str:
    env_override = os.environ.get("FACTORY_SYNC_FALLBACK_PUSH_URL", "").strip()
    if env_override:
        return env_override
    https_match = re.match(r"^https://github\.com/([^/]+)/([^/]+?)(?:\.git)?$", url)
    if https_match:
        owner, repo = https_match.groups()
        return f"git@github.com:{owner}/{repo}.git"
    return url


def validate_verify_prereqs(root: Path) -> tuple[dict, dict]:
    ensure_git_repo(root)
    missing = [rel for rel in VERIFY_REQUIRED_FILES if not (root / rel).exists()]
    if missing:
        raise AutomationError(f"Отсутствуют обязательные verify-артефакты: {', '.join(missing)}")
    stage = read_yaml(root / ".chatgpt" / "stage-state.yaml")
    if not stage.get("gates", {}).get("verification_complete"):
        raise AutomationError("Нельзя запускать verified sync: verification_complete != true")
    verification_report = read_text(root / ".chatgpt" / "verification-report.md")
    if len([line for line in verification_report.splitlines() if line.strip()]) < 4:
        raise AutomationError("verification-report.md заполнен слишком слабо для verified sync")
    task_index = read_yaml(root / ".chatgpt" / "task-index.yaml")
    change = task_index.get("change", {})
    if not change.get("id") or not change.get("title") or not change.get("summary"):
        raise AutomationError("task-index.yaml должен содержать change.id, change.title и change.summary")
    branch = current_branch(root)
    push_url = remote_url(root, "origin", "push")
    return task_index, {"branch": branch, "push_url": push_url}


def validate_release_decision_data(root: Path) -> dict:
    decision_path = root / ".chatgpt" / "release-decision.yaml"
    data = read_yaml(decision_path)
    required = ["decision", "version", "channel", "notes_source", "approved_by", "timestamp"]
    missing = [key for key in required if not str(data.get(key, "")).strip()]
    if missing:
        raise AutomationError(f"release-decision.yaml не содержит обязательные поля: {', '.join(missing)}")
    decision = str(data.get("decision", "")).strip()
    if decision not in {"release", "no-release"}:
        raise AutomationError("release-decision.yaml: decision должен быть `release` или `no-release`")
    version = str(data.get("version", "")).strip()
    if not re.match(r"^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9._-]+)?$", version):
        raise AutomationError("release-decision.yaml: version должен быть похож на semver")
    notes_source = root / str(data.get("notes_source", "")).strip()
    if not notes_source.exists():
        raise AutomationError(f"release-decision.yaml: notes_source не найден: {notes_source.relative_to(root)}")
    if not read_text(notes_source).strip():
        raise AutomationError("release-decision.yaml: notes_source пуст")
    return data


def tracked_runtime_report(root: Path, name: str) -> Path:
    ensure_runtime_dirs(root)
    return reports_dir(root) / name


@contextmanager
def file_lock(root: Path, name: str):
    ensure_runtime_dirs(root)
    lock_path = locks_dir(root) / name
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise AutomationError(f"Уже выполняется `{name}`; lock-файл не освобожден") from exc
    try:
        os.write(fd, f"pid={os.getpid()}\nstarted_at={now_utc()}\n".encode("utf-8"))
        os.close(fd)
        yield lock_path
    finally:
        if lock_path.exists():
            lock_path.unlink()


def classify_commit_type(change_class: str) -> str:
    mapping = {
        "small-fix": "fix",
        "feature": "feat",
        "refactor": "refactor",
        "migration": "feat",
        "brownfield-audit": "docs",
        "brownfield-stabilization": "fix",
    }
    return mapping.get(change_class, "feat")


def build_commit_message(change: dict) -> str:
    prefix = classify_commit_type(str(change.get("class", "")))
    title = str(change.get("title", "")).strip() or str(change.get("summary", "")).strip() or "update repo state"
    return f"{prefix}: {title}"


def is_denied_path(rel: str) -> bool:
    normalized = rel.strip()
    if not normalized:
        return True
    if normalized.startswith('"') and normalized.endswith('"'):
        normalized = normalized[1:-1]
    for prefix in DENY_PREFIXES:
        if normalized.startswith(prefix):
            return True
    for suffix in DENY_SUFFIXES:
        if normalized.endswith(suffix):
            return True
    return False


def changed_paths(root: Path) -> list[str]:
    proc = run_git(root, ["status", "--porcelain", "--untracked-files=all"], check=False)
    if proc.returncode != 0:
        raise AutomationError("Не удалось прочитать git status")
    result: list[str] = []
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        rel = line[3:]
        if " -> " in rel:
            rel = rel.split(" -> ", 1)[1]
        if is_denied_path(rel):
            continue
        result.append(rel)
    unique: list[str] = []
    seen: set[str] = set()
    for rel in result:
        if rel not in seen:
            seen.add(rel)
            unique.append(rel)
    return unique


def sync_report_path(root: Path) -> Path:
    return tracked_runtime_report(root, "verified-sync-report.yaml")


def release_report_path(root: Path) -> Path:
    return tracked_runtime_report(root, "release-report.yaml")


def write_report(path: Path, data: dict) -> None:
    write_yaml(path, data)


def last_sync_report(root: Path) -> dict:
    return read_yaml(sync_report_path(root))


def parse_version_md(root: Path) -> str:
    text = read_text(root / "VERSION.md")
    match = re.search(r"^## Текущая версия\s+([^\n]+)$", text, re.M)
    if not match:
        raise AutomationError("Не удалось определить текущую версию из VERSION.md")
    return match.group(1).strip()


def ensure_clean_repo(root: Path) -> None:
    proc = run_git(root, ["status", "--porcelain"], check=False)
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    dirty = []
    for line in lines:
        rel = line[3:]
        if " -> " in rel:
            rel = rel.split(" -> ", 1)[1]
        if not is_denied_path(rel):
            dirty.append(rel)
    if dirty:
        raise AutomationError(f"Repo должен быть чистым перед release executor; есть diff: {', '.join(dirty)}")


def push_branch(root: Path, branch: str, push_url: str) -> tuple[str, str]:
    proc = run_git(root, ["push", "origin", branch], check=False)
    if proc.returncode == 0:
        return "origin", "success"
    fallback = fallback_push_url(push_url)
    proc2 = run_git(root, ["push", fallback, branch], check=False)
    if proc2.returncode == 0:
        return fallback, "success-fallback"
    raise AutomationError(
        "Не удалось выполнить push ни через origin, ни через fallback URL:\n"
        f"origin: {(proc.stderr or proc.stdout).strip()}\n"
        f"fallback: {(proc2.stderr or proc2.stdout).strip()}"
    )


def push_tag(root: Path, tag: str, push_url: str) -> tuple[str, str]:
    proc = run_git(root, ["push", "origin", tag], check=False)
    if proc.returncode == 0:
        return "origin", "success"
    fallback = fallback_push_url(push_url)
    proc2 = run_git(root, ["push", fallback, tag], check=False)
    if proc2.returncode == 0:
        return fallback, "success-fallback"
    raise AutomationError(
        "Не удалось отправить tag ни через origin, ни через fallback URL:\n"
        f"origin: {(proc.stderr or proc.stdout).strip()}\n"
        f"fallback: {(proc2.stderr or proc2.stdout).strip()}"
    )


def gh_available() -> bool:
    return shutil.which("gh") is not None
