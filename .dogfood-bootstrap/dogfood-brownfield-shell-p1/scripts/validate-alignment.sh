#!/usr/bin/env python3
from __future__ import annotations
import sys, yaml
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
chat = root / '.chatgpt'
classification = chat / 'classification.md'
bugflow = chat / 'bugflow-status.yaml'
if not classification.exists():
    print('ALIGNMENT НЕ ПРОЙДЕН')
    print('- отсутствует .chatgpt/classification.md')
    raise SystemExit(1)
if not bugflow.exists():
    print('ALIGNMENT НЕ ПРОЙДЕН')
    print('- отсутствует .chatgpt/bugflow-status.yaml')
    raise SystemExit(1)
state = yaml.safe_load(bugflow.read_text(encoding='utf-8')) or {}
reports = root / 'reports' / 'bugs'
feedback = root / 'reports' / 'factory-feedback'
if state.get('defect_detected') and state.get('bug_report_required') and not any(reports.glob('*.md')):
    print('ALIGNMENT НЕ ПРОЙДЕН')
    print('- defect найден, но bug report отсутствует')
    raise SystemExit(1)
if state.get('factory_feedback_required') and not any(feedback.glob('*.md')):
    print('ALIGNMENT НЕ ПРОЙДЕН')
    print('- нужен factory feedback, но reports/factory-feedback пуст')
    raise SystemExit(1)
print('ALIGNMENT ПРОЙДЕН')
