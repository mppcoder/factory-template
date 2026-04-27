# Реестр исправлений

Фиксируйте повторно используемые исправления и workaround'ы.

## Управление спецификациями

- Если tech-spec или task потеряли связь с user-spec, добавьте `US-*` anchors в user-spec и `User Intent Binding` в tech-spec/tasks.
- Если агент сознательно не следует исходному intent, не прячьте это в задаче: добавьте `DEV-*` в `User-Spec Deviations`.
- Если после выполнения задачи появилось устойчивое решение, запишите краткий вывод в `decisions.md`, а затем при необходимости перенесите в `project-knowledge/`.
- Если done завершен без `project-knowledge-update-proposal.md`, восстановите closeout через `close-feature-workspace.py` или создайте blocker: иначе decisions легко теряются после архива.
