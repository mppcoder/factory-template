#!/usr/bin/env bash
set -euo pipefail

PATCH_BUNDLE="${1:-}"
MODE="${2:---check}"
EXTRA="${3:-}"

if [ -z "$PATCH_BUNDLE" ]; then
  echo "Использование: rollback-template-patch.sh <каталог-patch-bundle> [--check|--rollback] [--restore-project-snapshot]"
  exit 1
fi
if [ ! -d "$PATCH_BUNDLE" ]; then
  echo "ОШИБКА: каталог patch bundle не найден"
  exit 1
fi

APPLY_DIR="$PATCH_BUNDLE/applied-safe-zones"
STATE_FILE="$APPLY_DIR/rollback-state.json"
if [ ! -f "$STATE_FILE" ]; then
  echo "ОШИБКА: rollback-state.json не найден. Сначала выполните apply-template-patch.sh --apply-safe-zones"
  exit 1
fi

case "$MODE" in
  --check)
    if [ -n "$EXTRA" ]; then
      echo "ОШИБКА: для --check не поддерживаются дополнительные флаги"
      exit 1
    fi
    python3 - <<'PYCODE' "$STATE_FILE"
from __future__ import annotations

import json
import sys
from pathlib import Path

state_path = Path(sys.argv[1]).resolve()
state = json.loads(state_path.read_text(encoding="utf-8"))
files = state.get("files", [])
print(f"Rollback state: {state_path}")
print(f"project_root: {state.get('project_root')}")
print(f"patch_bundle: {state.get('patch_bundle')}")
print(f"applied_at: {state.get('applied_at')}")
print(f"status: {state.get('status', 'unknown')}")
metadata = state.get("bundle_metadata") or {}
print(f"template_version: {metadata.get('template_version', 'unknown')}")
print(f"sync_contract_version: {metadata.get('sync_contract_version', 'unknown')}")
print(f"project_snapshot_enabled: {state.get('project_snapshot_enabled', False)}")
print(f"project_snapshot_path: {state.get('project_snapshot_path_relative_to_apply_dir')}")
print(f"tracked_files: {len(files)}")
for item in files:
    rel = item.get("relative_path")
    existed = item.get("existed_before")
    backup = item.get("backup_path_relative_to_apply_dir")
    print(f"- {rel}: existed_before={existed}, backup={backup}")
print("")
print("Guidance: --rollback restores tracked safe-generated/safe-clone files only.")
print("Guidance: --rollback --restore-project-snapshot also restores the full project snapshot when available.")
PYCODE
    ;;
  --rollback)
    RESTORE_PROJECT_SNAPSHOT="0"
    if [ -n "$EXTRA" ]; then
      if [ "$EXTRA" = "--restore-project-snapshot" ]; then
        RESTORE_PROJECT_SNAPSHOT="1"
      else
        echo "ОШИБКА: поддерживается только дополнительный флаг --restore-project-snapshot"
        exit 1
      fi
    fi
    RESTORE_PROJECT_SNAPSHOT="$RESTORE_PROJECT_SNAPSHOT" python3 - <<'PYCODE' "$STATE_FILE" "$APPLY_DIR"
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path

state_path = Path(sys.argv[1]).resolve()
apply_dir = Path(sys.argv[2]).resolve()
state = json.loads(state_path.read_text(encoding="utf-8"))
project_root = Path(state.get("project_root", "")).resolve()
restore_project_snapshot = os.environ.get("RESTORE_PROJECT_SNAPSHOT", "0") == "1"

if not project_root.exists():
    raise SystemExit(f"ОШИБКА: project_root не существует: {project_root}")

restored = 0
removed = 0
missing_backup = 0
snapshot_restored = False

for item in reversed(state.get("files", [])):
    if item.get("applied") is False:
        continue
    target = Path(item.get("target", "")).resolve()
    rel = item.get("relative_path", "")
    existed_before = bool(item.get("existed_before", False))
    backup_rel = item.get("backup_path_relative_to_apply_dir")

    try:
        target.relative_to(project_root)
    except ValueError as exc:
        raise SystemExit(f"ОШИБКА: target вне project_root: {target}") from exc

    if existed_before:
        if not backup_rel:
            missing_backup += 1
            continue
        backup = (apply_dir / backup_rel).resolve()
        if not backup.exists():
            missing_backup += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup, target)
        restored += 1
        continue

    if target.exists():
        if target.is_file():
            target.unlink()
            removed += 1
            parent = target.parent
            while parent != project_root and parent.exists() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
        else:
            raise SystemExit(f"ОШИБКА: ожидается файл, но target директория: {target}")


def is_excluded(rel: Path) -> bool:
    return rel.parts and rel.parts[0] in {".git", "_factory-sync-export"}


def restore_project_snapshot_from_archive(snapshot_archive: Path) -> None:
    global snapshot_restored
    with tempfile.TemporaryDirectory(prefix="factory-snapshot-restore-") as tmpdir:
        temp_root = Path(tmpdir)
        with tarfile.open(snapshot_archive, "r:gz") as tar:
            tar.extractall(temp_root)
        snapshot_root = temp_root / "project-snapshot"
        if not snapshot_root.exists():
            raise SystemExit(f"ОШИБКА: snapshot archive поврежден: {snapshot_archive}")

        snapshot_files: set[Path] = set()
        for src in snapshot_root.rglob("*"):
            if not src.is_file():
                continue
            rel = src.relative_to(snapshot_root)
            snapshot_files.add(rel)
            dst = project_root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

        for dst in sorted(project_root.rglob("*"), reverse=True):
            rel = dst.relative_to(project_root)
            if is_excluded(rel):
                continue
            if dst.is_file() and rel not in snapshot_files:
                dst.unlink()
                continue
            if dst.is_dir():
                try:
                    next(dst.iterdir())
                except StopIteration:
                    dst.rmdir()
        snapshot_restored = True


if restore_project_snapshot:
    snapshot_rel = state.get("project_snapshot_path_relative_to_apply_dir")
    if not snapshot_rel:
        raise SystemExit("ОШИБКА: project snapshot не найден в rollback-state.json")
    snapshot_archive = (apply_dir / snapshot_rel).resolve()
    if not snapshot_archive.exists():
        raise SystemExit(f"ОШИБКА: snapshot archive не найден: {snapshot_archive}")
    restore_project_snapshot_from_archive(snapshot_archive)

rollback_report = {
    "rolled_back_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "state_file": str(state_path),
    "project_root": str(project_root),
    "restored_files": restored,
    "removed_files": removed,
    "missing_backup_entries": missing_backup,
    "project_snapshot_restored": snapshot_restored,
}
(apply_dir / "rollback-result.json").write_text(
    json.dumps(rollback_report, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(
    "Rollback завершен: "
    f"restored={restored}, removed={removed}, missing_backup={missing_backup}, "
    f"snapshot_restored={snapshot_restored}"
)
if missing_backup:
    raise SystemExit(2)
PYCODE
    ;;
  *)
    echo "ОШИБКА: поддерживаются только режимы --check и --rollback"
    exit 1
    ;;
esac
