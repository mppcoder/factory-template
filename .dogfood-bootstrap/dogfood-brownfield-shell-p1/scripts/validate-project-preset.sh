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
profile_file = resolve_input(root, '.chatgpt/project-profile.yaml')
task_index_file = Path(sys.argv[2]) if len(sys.argv) > 2 else resolve_input(root, '.chatgpt/task-index.yaml')
profile = yaml.safe_load(profile_file.read_text(encoding='utf-8')) or {}
task = yaml.safe_load(task_index_file.read_text(encoding='utf-8')) or {}
errors = []
for key in ['project_preset', 'project_title', 'recommended_mode', 'recommended_change_class', 'recommended_execution_mode']:
    if not str(profile.get(key, '')).strip():
        errors.append(f'Не заполнено поле профиля: {key}')
if not profile.get('applied'):
    errors.append('Профиль проекта не применен')
change = task.get('change', {}) if isinstance(task, dict) else {}
if not change.get('class'):
    errors.append('В task-index.yaml не указан класс изменения')
if not change.get('execution_mode'):
    errors.append('В task-index.yaml не указан режим выполнения')
if errors:
    print('ПРОВЕРКА ПРОФИЛЯ ПРОЕКТА НЕ ПРОЙДЕНА')
    for err in errors:
        print('-', err)
    raise SystemExit(1)
profile['validated'] = True
profile_file.write_text(yaml.safe_dump(profile, allow_unicode=True, sort_keys=False), encoding='utf-8')
print('ПРОФИЛЬ ПРОЕКТА ВАЛИДЕН')
