#!/usr/bin/env python3
from __future__ import annotations
import sys, yaml
from pathlib import Path

def resolve_input(raw: str, default_rel: str) -> Path:
    p = Path(raw)
    if p.is_dir():
        return p / default_rel
    return p
root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
state_file = resolve_input(str(root), '.chatgpt/stage-state.yaml')
project_root = root if root.is_dir() else root.parent.parent
state = yaml.safe_load(state_file.read_text(encoding='utf-8')) or {}
errors = []
project = state.get('project', {})
stage = state.get('stage', {})
gates = state.get('gates', {})
for key in ['current', 'previous', 'next']:
    if key not in stage:
        errors.append(f'В stage-state.yaml отсутствует раздел stage.{key}')
for key in ['intake_complete','classification_complete','reuse_check_complete','reality_check_complete','conflict_detection_complete','spec_validated','tech_spec_validated','task_validation_complete','codex_handoff_allowed','verification_complete','done_complete']:
    if key not in gates:
        errors.append(f'В stage-state.yaml отсутствует gate: {key}')
if gates.get('done_complete') and not gates.get('verification_complete'):
    errors.append('done_complete=true требует verification_complete=true')
if gates.get('verification_complete') and not gates.get('task_validation_complete'):
    errors.append('verification_complete=true требует task_validation_complete=true')
if gates.get('codex_handoff_allowed'):
    for dep in ['reuse_check_complete','reality_check_complete','conflict_detection_complete']:
        if not gates.get(dep):
            errors.append(f'codex_handoff_allowed=true требует {dep}=true')
if gates.get('tech_spec_validated') and not (project_root/'.chatgpt/tech-spec.md').exists():
    errors.append('tech_spec_validated=true требует файл .chatgpt/tech-spec.md')
if gates.get('spec_validated') and not (project_root/'.chatgpt/user-spec.md').exists():
    errors.append('spec_validated=true требует файл .chatgpt/user-spec.md')
if gates.get('task_validation_complete') and not (project_root/'.chatgpt/task-index.yaml').exists():
    errors.append('task_validation_complete=true требует файл .chatgpt/task-index.yaml')
if project.get('mode') not in ['greenfield','brownfield']:
    errors.append('project.mode должен быть greenfield или brownfield')
if errors:
    print('ПРОВЕРКА ЭТАПОВ НЕ ПРОЙДЕНА')
    for err in errors:
        print('-', err)
    raise SystemExit(1)
print('ЭТАПЫ И СОСТОЯНИЯ КОРРЕКТНЫ')
