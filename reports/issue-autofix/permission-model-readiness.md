# Готовность permission model

Дата: 2026-05-05

## Статус

- actor permission checks documented;
- label sync is dry-run by default;
- danger labels documented;
- workflow/gate/docs labels cross-validated by `validate-issue-autofix-labels.py`;
- no live label mutation is part of verification.

## Проверка

```bash
python3 template-repo/scripts/validate-issue-autofix-labels.py .
```
