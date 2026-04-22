#!/usr/bin/env python3
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path
import yaml

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
VERIFY = ROOT / '.chatgpt' / 'verification-report.md'
DONE = ROOT / '.chatgpt' / 'done-report.md'
STATE = ROOT / '.chatgpt' / 'stage-state.yaml'
CURRENT = ROOT / 'CURRENT_FUNCTIONAL_STATE.md'
CLASS = ROOT / '.chatgpt' / 'classification.md'
BUGFLOW = ROOT / '.chatgpt' / 'bugflow-status.yaml'
BUGDIR = ROOT / 'reports' / 'bugs'
FEEDBACK = ROOT / 'reports' / 'factory-feedback'
SYNC_REPORT = ROOT / '.factory-runtime' / 'reports' / 'verified-sync-report.yaml'
CLASSES_FILE = ROOT / 'change-classes.yaml'
if not CLASSES_FILE.exists():
    CLASSES_FILE = Path(__file__).resolve().parents[1] / 'change-classes.yaml'

missing = [str(p) for p in [VERIFY, DONE, STATE, CURRENT] if not p.exists()]
if missing:
    print('DOD НЕ ПРОЙДЕН')
    for m in missing:
        print('-', m)
    raise SystemExit(1)

state = yaml.safe_load(STATE.read_text(encoding='utf-8')) or {}
gates = state.get('gates', {})
task_index = yaml.safe_load((ROOT / '.chatgpt' / 'task-index.yaml').read_text(encoding='utf-8')) if (ROOT / '.chatgpt' / 'task-index.yaml').exists() else {}
task_index = task_index or {}
change = task_index.get('change', {}) if isinstance(task_index, dict) else {}
classes = yaml.safe_load(CLASSES_FILE.read_text(encoding='utf-8')) if CLASSES_FILE.exists() else {}
classes = (classes or {}).get('change_classes', {}) if isinstance(classes, dict) else {}
change_class = change.get('class')
class_cfg = classes.get(change_class, {}) if isinstance(classes, dict) else {}
if gates.get('done_complete') is not True:
    print('DOD НЕ ПРОЙДЕН')
    print('- done_complete != true')
    raise SystemExit(1)
if gates.get('verification_complete') is not True:
    print('DOD НЕ ПРОЙДЕН')
    print('- verification_complete != true')
    raise SystemExit(1)
for gate in class_cfg.get('required_gates', []) if isinstance(class_cfg, dict) else []:
    if gates.get(gate) is not True:
        print('DOD НЕ ПРОЙДЕН')
        print(f'- для класса {change_class} gate {gate} должен быть true')
        raise SystemExit(1)
for rel in class_cfg.get('required_artifacts', []) if isinstance(class_cfg, dict) else []:
    if not (ROOT / rel).exists():
        print('DOD НЕ ПРОЙДЕН')
        print(f'- для класса {change_class} отсутствует обязательный артефакт {rel}')
        raise SystemExit(1)


def meaningful(path: Path, min_lines: int = 3) -> bool:
    lines = []
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or line.startswith('>') or line in {'-', '*'}:
            continue
        if re.match(r'^(Заполните|Подсказка:|Пример:|TODO)', line):
            continue
        lines.append(line)
    return len(lines) >= min_lines


def has_origin_remote(root: Path) -> bool:
    proc = subprocess.run(
        ['git', 'remote', 'get-url', '--push', 'origin'],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode == 0 and proc.stdout.strip():
        return True
    proc = subprocess.run(
        ['git', 'remote', 'get-url', 'origin'],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode == 0 and bool(proc.stdout.strip())


if not meaningful(VERIFY):
    print('DOD НЕ ПРОЙДЕН')
    print('- verification-report.md заполнен слишком слабо')
    raise SystemExit(1)
if not meaningful(DONE):
    print('DOD НЕ ПРОЙДЕН')
    print('- done-report.md заполнен слишком слабо')
    raise SystemExit(1)

classification = CLASS.read_text(encoding='utf-8', errors='ignore') if CLASS.exists() else ''
verify_text = VERIFY.read_text(encoding='utf-8', errors='ignore')
done_text = DONE.read_text(encoding='utf-8', errors='ignore')
bugflow = yaml.safe_load(BUGFLOW.read_text(encoding='utf-8')) if BUGFLOW.exists() else {}
bugflow = bugflow or {}
defect_active = bool(bugflow.get('defect_detected')) or ('## Есть ли обнаруженный дефект\nда' in classification) or bool(re.search(r'\bbug\b|дефект|регрес|ошибк|gap', verify_text + '\n' + done_text, re.I))
reports = [p for p in BUGDIR.glob('*.md')] if BUGDIR.exists() else []
feedback = [p for p in FEEDBACK.glob('*.md')] if FEEDBACK.exists() else []
if defect_active and bugflow.get('bug_report_required', True) and not reports:
    print('DOD НЕ ПРОЙДЕН')
    print('- найден defect flow, но отсутствует bug report в reports/bugs/')
    raise SystemExit(1)
if defect_active and bugflow.get('factory_feedback_required', False) and not feedback:
    print('DOD НЕ ПРОЙДЕН')
    print('- defect reusable, но отсутствует factory feedback в reports/factory-feedback/')
    raise SystemExit(1)
if has_origin_remote(ROOT):
    if not SYNC_REPORT.exists():
        print('DOD НЕ ПРОЙДЕН')
        print('- при настроенном origin требуется .factory-runtime/reports/verified-sync-report.yaml')
        raise SystemExit(1)
    sync_report = yaml.safe_load(SYNC_REPORT.read_text(encoding='utf-8')) or {}
    status = str(sync_report.get('status', '')).strip()
    push_status = str(sync_report.get('push_status', '')).strip()
    if status not in {'pushed', 'no-op'}:
        print('DOD НЕ ПРОЙДЕН')
        print(f'- verified sync report должен иметь status `pushed` или `no-op`, сейчас `{status or "empty"}`')
        raise SystemExit(1)
    if status == 'pushed' and push_status != 'success':
        print('DOD НЕ ПРОЙДЕН')
        print(f'- verified sync report для pushed-state должен иметь push_status `success`, сейчас `{push_status or "empty"}`')
        raise SystemExit(1)
print('DOD ПРОЙДЕН')
