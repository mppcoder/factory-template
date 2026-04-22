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

SYNC_HEADER = """<!--
SYNCED FILE - DO NOT EDIT MANUALLY
Source of truth: template-repo/AGENTS.md
This root AGENTS.md is a materialized clone for the downstream repo.
Manual edits in this clone will be overwritten by the canonical template sync flow.
-->
"""


def render_materialized_clone(text: str) -> str:
    return f"{SYNC_HEADER}\n{text.strip()}\n"


manifest = yaml.safe_load(Path(r"$MANIFEST").read_text(encoding='utf-8')) or {}
template = Path(r"$TEMPLATE_ROOT").resolve()
project = Path(r"$PROJECT_ROOT").resolve()
out = Path(r"$OUT").resolve()
summary = []
changed = []
generated_dir = out / 'generated-files'
def project_zone(zone: str) -> Path:
    if zone.startswith('template-repo/template/'):
        return project / zone.replace('template-repo/template/', '', 1)
    return project / zone
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
for mapping in manifest.get('materialized_files', []):
    source = template / mapping['source']
    target = project / mapping['target']
    if not source.exists():
        continue
    rendered = source.read_text(encoding='utf-8')
    if mapping.get('mode') == 'materialized-clone':
        rendered = render_materialized_clone(rendered)
    current = target.read_text(encoding='utf-8') if target.exists() else ''
    if current == rendered:
        continue
    generated_target = generated_dir / mapping['target']
    generated_target.parent.mkdir(parents=True, exist_ok=True)
    generated_target.write_text(rendered, encoding='utf-8')
    patch = ''.join(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            rendered.splitlines(keepends=True),
            fromfile=str(target),
            tofile=str(target),
        )
    )
    name = mapping['target'].replace('/', '__') + '.patch'
    (out / name).write_text(patch, encoding='utf-8')
    changed.append(f"{mapping['source']} => {mapping['target']}")
    summary.append(
        f"- materialized clone: {mapping['source']}\n  target: {mapping['target']}\n  режим: generated-sync"
    )
for zone in manifest.get('advisory_only_zones', []):
    if (template / zone).exists() and project_zone(zone).exists():
        summary.append(f"- advisory-only зона: {zone}")
(out/'changed-files.txt').write_text('\n'.join(changed) + ('\n' if changed else ''), encoding='utf-8')
(out/'template-sync.patch').write_text(''.join(p.read_text(encoding='utf-8') + '\n' for p in sorted(out.glob('*.patch'))), encoding='utf-8')
(out/'patch-summary.md').write_text('# Сводка patch bundle\n\n' + ('\n'.join(summary) if summary else 'Изменений не обнаружено.') + '\n\n## Режим\n' + r"$MODE" + '\n', encoding='utf-8')
print(f'Patch bundle собран в {out}')
PYCODE
if [ "$MODE" = "--dry-run" ]; then echo 'Режим dry-run: patch bundle подготовлен без применения.'; fi
