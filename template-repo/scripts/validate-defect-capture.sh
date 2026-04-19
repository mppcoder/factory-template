#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
chat = ROOT / '.chatgpt'
classification = (chat / 'classification.md').read_text(encoding='utf-8', errors='ignore') if (chat / 'classification.md').exists() else ''
verify_text = (chat / 'verification-report.md').read_text(encoding='utf-8', errors='ignore') if (chat / 'verification-report.md').exists() else ''
state = yaml.safe_load((chat / 'bugflow-status.yaml').read_text(encoding='utf-8')) if (chat / 'bugflow-status.yaml').exists() else {}
state = state or {}
reports = ROOT / 'reports' / 'bugs'
feedback = ROOT / 'reports' / 'factory-feedback'
defect_active = bool(state.get('defect_detected')) or ('## Есть ли обнаруженный дефект\nда' in classification) or bool(re.search(r'\bbug\b|дефект|регрес|regression|gap|ошибк', verify_text, re.I))
needs_feedback = bool(state.get('factory_feedback_required')) or ('## Нужен ли feedback в фабрику\nда' in classification)
bug_reports = [p for p in reports.glob('*.md')] if reports.exists() else []
feedback_reports = [p for p in feedback.glob('*.md')] if feedback.exists() else []
if defect_active and state.get('bug_report_required', True) and not bug_reports:
    print('DEFECT CAPTURE НЕ ПРОЙДЕН')
    print('- Defect flow активирован, но нет bug report в reports/bugs/')
    raise SystemExit(1)
if needs_feedback and not feedback_reports:
    print('DEFECT CAPTURE НЕ ПРОЙДЕН')
    print('- Нужен feedback в фабрику, но reports/factory-feedback пуст')
    raise SystemExit(1)
print('DEFECT CAPTURE ПРОЙДЕН')
