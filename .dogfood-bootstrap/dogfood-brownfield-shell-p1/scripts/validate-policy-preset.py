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
policy_file = resolve_input(root, '.chatgpt/policy-status.yaml')
policy = yaml.safe_load(policy_file.read_text(encoding='utf-8')) or {}
errors = []
for key in ['policy_preset', 'change_class', 'execution_mode', 'handoff_policy']:
    if not str(policy.get(key, '')).strip():
        errors.append(f'Не заполнено поле политики: {key}')
if not isinstance(policy.get('minimum_evidence_required_all', []), list):
    errors.append('minimum_evidence_required_all должен быть списком')
if not isinstance(policy.get('minimum_evidence_required_any', []), list):
    errors.append('minimum_evidence_required_any должен быть списком')
if not isinstance(policy.get('active_default_scenarios', []), list):
    errors.append('active_default_scenarios должен быть списком')
if not policy.get('applied'):
    errors.append('Политика не была применена')
if errors:
    print('ПОЛИТИКА НЕКОРРЕКТНА')
    for err in errors:
        print('-', err)
    raise SystemExit(1)
policy['validated'] = True
policy_file.write_text(yaml.safe_dump(policy, allow_unicode=True, sort_keys=False), encoding='utf-8')
print('ПОЛИТИКА ВАЛИДНА')
