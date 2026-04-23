# Контекст для Codex

## Проект
factory-template

## Классификация
Reusable template defect в handoff/completion UX: шаблон верно отделял advisory/policy layer от executable routing layer, но default user-facing path для VS Code Codex extension ошибочно подавался как launcher-first вместо `manual-ui (default)`.

## Текущий этап
defect-capture -> classification -> remediation

## Change ID
chg-20260423-018

## Краткое резюме
Перевести handoff/completion слой на dual-path contract: `manual-ui (default)` для интерактивной работы через VS Code Codex extension и `launcher-first strict mode (optional)` для automation/reproducibility/shell-first, не обещая auto-switch в уже открытой live session.
