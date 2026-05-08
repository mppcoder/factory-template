# Handoff language validator flags YAML `scope:` key as English label

Дата: 2026-05-08

## Симптом

`bash template-repo/scripts/verify-all.sh` падал в `MATRIX_TEST` на строке:

```text
factory-bugflow | validate-handoff-language.py | pass | fail
```

Изолированная проверка показала, что `template-repo/scripts/validate-handoff-language.py` отклоняет `.chatgpt/handoff-response.md` из matrix fixture из-за строки `  scope:` внутри `goal_contract`.

## Ожидание

Validator должен запрещать человекочитаемые англоязычные labels вроде `Scope:` на верхнем уровне handoff, но не должен запрещать YAML keys внутри технического блока `goal_contract`.

## Факт

Regex проверял `^\s*scope\s*:`, из-за чего indented YAML key `  scope:` считался human-facing label.

## Классификация

- layer: validator / handoff language
- severity: medium
- reusable factory issue: yes
- affected command: `bash MATRIX_TEST.sh`

## Remediation

Regex для forbidden labels ограничен началом строки без indentation. Это сохраняет запрет для `Scope:` / `Goal:` / `Repo:` как human-facing labels и разрешает indented YAML keys как technical literal values.

## Verification

- `python3 template-repo/scripts/validate-handoff-language.py .matrix-test/bugflow/factory-bugflow/.chatgpt/handoff-response.md`
- `bash MATRIX_TEST.sh`
- `bash template-repo/scripts/verify-all.sh`
