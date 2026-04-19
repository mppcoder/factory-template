#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
VERIFY = ROOT / '.chatgpt' / 'verification-report.md'
DONE = ROOT / '.chatgpt' / 'done-report.md'
STATE = ROOT / '.chatgpt' / 'stage-state.yaml'
CURRENT = ROOT / 'CURRENT_STATE.md'
CLASS = ROOT / '.chatgpt' / 'classification.md'
BUGFLOW = ROOT / '.chatgpt' / 'bugflow-status.yaml'
BUGDIR = ROOT / 'reports' / 'bugs'
FEEDBACK = ROOT / 'reports' / 'factory-feedback'

missing = [str(p) for p in [VERIFY, DONE, STATE, CURRENT] if not p.exists()]
if missing:
    print('DOD НЕ ПРОЙДЕН')
    for m in missing:
        print('-', m)
    raise SystemExit(1)

state = yaml.safe_load(STATE.read_text(encoding='utf-8')) or {}
gates = state.get('gates', {})
if gates.get('done_complete') is not True:
    print('DOD НЕ ПРОЙДЕН')
    print('- done_complete != true')
    raise SystemExit(1)
if gates.get('verification_complete') is not True:
    print('DOD НЕ ПРОЙДЕН')
    print('- verification_complete != true')
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
print('DOD ПРОЙДЕН')
