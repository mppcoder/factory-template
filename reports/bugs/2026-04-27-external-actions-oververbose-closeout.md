# Слишком сложный closeout внешних действий

Дата: 2026-04-27

## Summary

Финальный closeout мог превращать отсутствие внешних действий в длинный audit-style completion package: перечислялись factory ChatGPT Project, downstream sync, downstream ChatGPT Project, VPS approval, secrets boundary и другие contour'ы со статусом `не требуется`.

Пользователю в таком случае нужна не таблица всех возможных контуров, а короткий итог:

- что реально нужно сделать снаружи Codex;
- или явная строка `Внешних действий не требуется.`

## Classification

- Layer: `factory-template`
- Severity: `medium`
- Type: `reusable closeout UX defect`
- Route: `closeout/external-actions-simplification`
- Pipeline stage: `defect-capture -> remediation`

## Evidence

Последний post-2.5 closeout содержал длинный реестр с несколькими строками `не требуется`, хотя текущая repo-задача была закрыта внутри Codex через verified sync и не требовала немедленного внешнего действия пользователя.

Существующие правила в `00-master-router.md`, `16-done-closeout.md`, `boundary-actions.md` и generated checklist требовали полный contour register даже тогда, когда реальных действий нет.

## Remediation

- Compact default: если внешних действий нет, финальный ответ говорит только `Внешних действий не требуется.`
- Если внешние действия есть, `## Инструкция пользователю` перечисляет только реальные user/manual/external actions.
- Full contour audit допускается только если пользователь явно запросил полный реестр или задача является release/security approval, где отсутствие действия по контуру само является значимым решением.
- Validator должен закреплять compact outcome и ловить oververbose no-op ledger.

## Status

`remediated-in-current-scope`
