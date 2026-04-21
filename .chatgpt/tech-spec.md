# Техническая спецификация

## Архитектура правила
- Router, decision policy, handoff rules и done-closeout должны одинаково различать `internal follow-up pending`, `external boundary pending`, `mixed follow-up` и `fully done`.
- Internal repo follow-up имеет precedence над user footer: если внутренняя работа еще не закрыта, сначала обязателен inline handoff.
- Footer `Инструкция пользователю` остается обязательным только для реальных external boundary steps.

## Internal Follow-up
- К internal repo follow-up относятся release-followup, source-pack refresh, export/manifests refresh, closeout artifact sync, verify/done/release-facing consistency pass и release bundle preparation внутри repo.
- Такие задачи блокируют user-only closeout и `done_complete`, пока не будут закрыты или явно выведены за scope.

## Generation / Validation
- `create-codex-task-pack.sh` должен явно писать, что internal repo follow-up остается работой Codex.
- `validate-codex-task-pack.sh` должен проверять, что boundary-actions не подменяет внутренний handoff user footer'ом.
