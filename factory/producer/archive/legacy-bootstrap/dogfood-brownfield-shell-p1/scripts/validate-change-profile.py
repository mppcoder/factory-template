#!/usr/bin/env python3
from __future__ import annotations
import sys, yaml

from pathlib import Path

def resolve_input(raw: str, default_rel: str) -> Path:
    p = Path(raw)
    if p.is_dir():
        return p / default_rel
    return p

root = sys.argv[1] if len(sys.argv) > 1 else '.'
task_index = resolve_input(root, '.chatgpt/task-index.yaml')
classes_file = Path(sys.argv[2]) if len(sys.argv) > 2 else resolve_input(root, 'change-classes.yaml')
task = yaml.safe_load(task_index.read_text(encoding='utf-8'))
classes = yaml.safe_load(classes_file.read_text(encoding='utf-8')).get('change_classes', {})
change = task.get('change', {})
change_class = change.get('class')
mode = change.get('execution_mode')
errs = []
if change_class not in classes:
    errs.append(f'Неизвестный класс изменения: {change_class}')
else:
    if mode not in classes[change_class].get('allowed_execution_modes', []):
        errs.append(f'Режим выполнения не разрешен для класса {change_class}: {mode}')
if errs:
    print('ПРОФИЛЬ ИЗМЕНЕНИЯ НЕКОРРЕКТЕН')
    for err in errs:
        print('-', err)
    raise SystemExit(1)
print('ПРОФИЛЬ ИЗМЕНЕНИЯ КОРРЕКТЕН')
