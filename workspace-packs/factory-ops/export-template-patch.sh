#!/usr/bin/env bash
set -euo pipefail
TEMPLATE_ROOT="${1:-}"
PROJECT_ROOT="${2:-}"
MODE="${3:---dry-run}"
if [ -z "$TEMPLATE_ROOT" ] || [ -z "$PROJECT_ROOT" ]; then
  echo "Использование: export-template-patch.sh <template-root> <working-project-root> [--dry-run|--advisory]"
  exit 1
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$SCRIPT_DIR/factory-sync-manifest.yaml"
OUT="$PROJECT_ROOT/_factory-sync-export"
mkdir -p "$OUT"
python3 - <<PYCODE
from pathlib import Path
import yaml, difflib
manifest = yaml.safe_load(Path(r"$MANIFEST").read_text(encoding='utf-8')) or {}
template = Path(r"$TEMPLATE_ROOT").resolve()
project = Path(r"$PROJECT_ROOT").resolve()
out = Path(r"$OUT").resolve()
summary = []
changed = []
def project_zone(zone: str) -> Path:
    return project / zone.replace('template-repo/template/', '').replace('template-repo/', '')
for zone in manifest.get('sync_zones', []):
    t_zone = template / zone
    p_zone = project_zone(zone)
    if not t_zone.exists() or not p_zone.exists():
        continue
    for p_file in p_zone.rglob('*'):
        if not p_file.is_file():
            continue
        rel = p_file.relative_to(p_zone)
        t_file = t_zone / rel
        if not t_file.exists() or not t_file.is_file():
            continue
        try:
            a = t_file.read_text(encoding='utf-8').splitlines(keepends=True)
            b = p_file.read_text(encoding='utf-8').splitlines(keepends=True)
        except Exception:
            continue
        if a == b:
            continue
        patch = ''.join(difflib.unified_diff(a, b, fromfile=str(t_file), tofile=str(p_file)))
        name = zone.replace('/', '__') + '__' + str(rel).replace('/', '__') + '.patch'
        (out / name).write_text(patch, encoding='utf-8')
        changed.append(f"{zone}/{rel}")
        summary.append(f"- зона: {zone}\n  файл: {rel}\n  режим: safe-sync")
for zone in manifest.get('advisory_only_zones', []):
    if (template / zone).exists() and project_zone(zone).exists():
        summary.append(f"- advisory-only зона: {zone}")
(out/'changed-files.txt').write_text('\n'.join(changed) + ('\n' if changed else ''), encoding='utf-8')
(out/'template-sync.patch').write_text(''.join(p.read_text(encoding='utf-8') + '\n' for p in sorted(out.glob('*.patch'))), encoding='utf-8')
(out/'patch-summary.md').write_text('# Сводка patch bundle\n\n' + ('\n'.join(summary) if summary else 'Изменений не обнаружено.') + '\n\n## Режим\n' + r"$MODE" + '\n', encoding='utf-8')
print(f'Patch bundle собран в {out}')
PYCODE
if [ "$MODE" = "--dry-run" ]; then echo 'Режим dry-run: patch bundle подготовлен без применения.'; fi
