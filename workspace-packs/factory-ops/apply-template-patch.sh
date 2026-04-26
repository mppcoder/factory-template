#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATCH_BUNDLE="${1:-}"
MODE="${2:---check}"
EXTRA="${3:-}"
if [ -z "$PATCH_BUNDLE" ]; then
  echo "Использование: apply-template-patch.sh <каталог-patch-bundle> [--check|--dry-run|--apply-safe-zones] [--with-project-snapshot]"
  exit 1
fi
if [ ! -d "$PATCH_BUNDLE" ]; then
  echo "ОШИБКА: каталог patch bundle не найден"
  exit 1
fi
case "$MODE" in
  --check)
    if [ -n "$EXTRA" ]; then
      echo "ОШИБКА: для --check не поддерживаются дополнительные флаги"
      exit 1
    fi
    echo "Найден patch bundle: $PATCH_BUNDLE"
    find "$PATCH_BUNDLE" -maxdepth 1 -type f | sort
    python3 - <<'PYCODE' "$PATCH_BUNDLE"
from __future__ import annotations

import json
import sys
from pathlib import Path

bundle = Path(sys.argv[1]).resolve()
metadata_file = bundle / "bundle-metadata.json"
preview_file = bundle / "preview-changes.json"
generated_root = bundle / "generated-files"
metadata = json.loads(metadata_file.read_text(encoding="utf-8")) if metadata_file.exists() else {}
preview = json.loads(preview_file.read_text(encoding="utf-8")) if preview_file.exists() else []
generated_files = sorted(
    str(path.relative_to(generated_root)).replace("\\", "/")
    for path in generated_root.rglob("*")
    if path.is_file()
) if generated_root.exists() else []

print("")
print("Tiered apply preview:")
print(f"- template_version: {metadata.get('template_version', 'unknown')}")
print(f"- sync_contract_version: {metadata.get('sync_contract_version', 'unknown')}")
for tier in metadata.get("tier_order") or ("safe-generated", "safe-clone", "advisory-review", "manual-project-owned"):
    bucket = (metadata.get("tiers") or {}).get(tier, {})
    print(
        f"- {tier}: preview={bucket.get('total', 0)}, "
        f"generated={bucket.get('generated', 0)}, "
        f"patches={bucket.get('patch_files', 0)}, "
        f"apply_eligible={bucket.get('apply_eligible', tier in {'safe-generated', 'safe-clone'})}"
    )
print(f"- generated files ready for safe apply: {len(generated_files)}")
if generated_files:
    for item in generated_files:
        print(f"  - {item}")
blocked = [item for item in preview if item.get("will_generate") and not item.get("apply_eligible")]
if blocked:
    raise SystemExit("ОШИБКА: non-safe item marked will_generate=true")
print("")
print("Guidance: --apply-safe-zones copies only generated safe-generated/safe-clone files and records rollback metadata.")
print("Guidance: advisory-review/manual-project-owned entries are preview-only; review patch-summary.md before any manual copy.")
PYCODE
    ;;
  --dry-run)
    if [ -n "$EXTRA" ]; then
      echo "ОШИБКА: для --dry-run не поддерживаются дополнительные флаги"
      exit 1
    fi
    echo "Dry-run: проверка patch bundle завершена, применение не выполнялось."
    ;;
  --apply-safe-zones)
    CREATE_PROJECT_SNAPSHOT="0"
    if [ -n "$EXTRA" ]; then
      if [ "$EXTRA" = "--with-project-snapshot" ]; then
        CREATE_PROJECT_SNAPSHOT="1"
      else
        echo "ОШИБКА: поддерживается только дополнительный флаг --with-project-snapshot"
        exit 1
      fi
    fi
    APPLY_DIR="$PATCH_BUNDLE/applied-safe-zones"
    PROJECT_ROOT="$(cd "$PATCH_BUNDLE/.." && pwd)"
    BACKUP_DIR="$APPLY_DIR/rollback-backup"
    mkdir -p "$APPLY_DIR" "$BACKUP_DIR"
    for f in changed-files.txt patch-summary.md template-sync.patch; do [ -f "$PATCH_BUNDLE/$f" ] && cp "$PATCH_BUNDLE/$f" "$APPLY_DIR/$f"; done
    PATCH_BUNDLE="$PATCH_BUNDLE" PROJECT_ROOT="$PROJECT_ROOT" APPLY_DIR="$APPLY_DIR" BACKUP_DIR="$BACKUP_DIR" CREATE_PROJECT_SNAPSHOT="$CREATE_PROJECT_SNAPSHOT" python3 - <<'PYCODE'
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import tarfile
from pathlib import Path

patch_bundle = Path(os.environ["PATCH_BUNDLE"]).resolve()
project_root = Path(os.environ["PROJECT_ROOT"]).resolve()
apply_dir = Path(os.environ["APPLY_DIR"]).resolve()
backup_dir = Path(os.environ["BACKUP_DIR"]).resolve()
generated = patch_bundle / "generated-files"
create_project_snapshot = os.environ.get("CREATE_PROJECT_SNAPSHOT", "0") == "1"
snapshot_path = apply_dir / "project-snapshot.tar.gz"


def should_exclude(rel_parts: tuple[str, ...]) -> bool:
    if not rel_parts:
        return False
    return rel_parts[0] in {".git", "_factory-sync-export"}


if create_project_snapshot:
    with tarfile.open(snapshot_path, "w:gz") as tar:
        for source in sorted(project_root.rglob("*")):
            if source.is_dir() or not source.is_file():
                continue
            rel = source.relative_to(project_root)
            if should_exclude(rel.parts):
                continue
            tar.add(source, arcname=Path("project-snapshot") / rel)

state = {
    "version": 3,
    "status": "preparing",
    "patch_bundle": str(patch_bundle),
    "project_root": str(project_root),
    "applied_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "files": [],
    "bundle_metadata": json.loads((patch_bundle / "bundle-metadata.json").read_text(encoding="utf-8"))
    if (patch_bundle / "bundle-metadata.json").exists()
    else {},
    "project_snapshot_enabled": create_project_snapshot,
    "project_snapshot_path_relative_to_apply_dir": snapshot_path.relative_to(apply_dir).as_posix() if create_project_snapshot else None,
}
preview_items = json.loads((patch_bundle / "preview-changes.json").read_text(encoding="utf-8")) if (patch_bundle / "preview-changes.json").exists() else []
eligible_targets = {
    str(item.get("target", "")).replace("\\", "/")
    for item in preview_items
    if item.get("will_generate") and item.get("apply_eligible")
}
blocked_preview = [item for item in preview_items if item.get("will_generate") and not item.get("apply_eligible")]
if blocked_preview:
    raise SystemExit("ОШИБКА: bundle содержит generated preview для non-safe tier")

if generated.exists():
    for source in sorted(generated.rglob("*")):
        if not source.is_file():
            continue

        rel = source.relative_to(generated)
        rel_posix = rel.as_posix()
        if ".." in rel.parts:
            raise SystemExit(f"ОШИБКА: небезопасный путь в generated-files: {rel}")
        if rel_posix not in eligible_targets:
            raise SystemExit(f"ОШИБКА: generated file отсутствует в safe preview: {rel_posix}")

        target = (project_root / rel).resolve()
        try:
            target.relative_to(project_root)
        except ValueError as exc:
            raise SystemExit(f"ОШИБКА: выход за пределы project root: {target}") from exc

        existed_before = target.exists()
        backup_rel = None
        if existed_before:
            if target.is_dir():
                raise SystemExit(f"ОШИБКА: целевой путь является директорией: {target}")
            backup_target = backup_dir / rel
            backup_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup_target)
            backup_rel = backup_target.relative_to(apply_dir).as_posix()

        state["files"].append(
            {
                "relative_path": rel_posix,
                "target": str(target),
                "existed_before": existed_before,
                "backup_path_relative_to_apply_dir": backup_rel,
                "applied": False,
            }
        )

state_path = apply_dir / "rollback-state.json"
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for item in state["files"]:
    rel = Path(item["relative_path"])
    source = generated / rel
    target = Path(item["target"]).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    item["applied"] = True
state["status"] = "applied"
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Rollback state сохранен: {state_path}")
print(f"Отслеживаемых файлов: {len(state['files'])}")
print(f"Safe-generated/safe-clone files applied: {len(state['files'])}")
if create_project_snapshot:
    print(f"Project snapshot сохранен: {snapshot_path}")
PYCODE
    echo "Safe-generated/safe-clone files синхронизированы в downstream repo root через controlled sync path."
    echo "Advisory-review/manual-project-owned preview остался в patch-summary.md и preview-changes.json без автоматического применения."
    echo "Для отката используйте: $SCRIPT_DIR/rollback-template-patch.sh $PATCH_BUNDLE --rollback"
    echo "Для полного отката с project snapshot (если создавался): $SCRIPT_DIR/rollback-template-patch.sh $PATCH_BUNDLE --rollback --restore-project-snapshot"
    echo "Каталог результата: $APPLY_DIR"
    ;;
  *)
    echo "ОШИБКА: поддерживаются только режимы --check, --dry-run и --apply-safe-zones"
    exit 1
    ;;
esac
