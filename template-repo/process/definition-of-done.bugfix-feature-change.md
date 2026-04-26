# Определение готовности для bugfix / feature / change

Задача не считается завершенной, если:
- найденный дефект был исправлен без bug report;
- reusable defect не имеет factory feedback;
- verification не подтверждает результат;
- в done-отчете не отражено, что было найдено и что было исправлено.
- при настроенном `origin` отсутствует успешный `verified-sync-report`;
- финальный closeout выдан при dirty worktree или branch ahead относительно `origin/*` без конкретного blocker;
- при наличии pending external/user step финальный ответ не содержит блока `Инструкция пользователю`.
- внешних шагов не осталось, но финальный ответ не говорит это явно и оставляет пользователю неясность, нужен ли следующий manual step.
- остаются internal repo follow-up задачи, но финальный ответ оформлен как user-only closeout без inline handoff.
- required completion package для repo-first instruction/external contour был выдан только после дополнительного запроса пользователя, а не в основном финальном ответе.
- unresolved incidental defect был найден, но не получил bug report, self-handoff и явный next-step route.

## Минимум для Done
- verification-report.md заполнен;
- done-report.md заполнен;
- если `origin` настроен и verified sync был доступен, существует `.factory-runtime/reports/verified-sync-report.yaml` со статусом `pushed` или `no-op`;
- перед финальным ответом выполнен `git status --short --branch`, а commit hash / sync status отражен в closeout или blocker явно назван;
- если в ходе работы выявлен defect, существует bug report в `reports/bugs/`;
- если найден unresolved incidental defect, существует bug report с route decision и self-handoff outcome;
- если defect reusable, существует запись в `reports/factory-feedback/` или meta-feedback;
- stage-state.yaml согласован;
- DoD и defect-capture валидации проходят.
- если остаются внешние действия или следующий шаг пользователя, финальный ответ завершен блоком `## Инструкция пользователю`.
- если внешних действий не осталось, финальный ответ явно содержит фразу уровня `Внешних действий не требуется`.
- `done_complete` фиксируется только если внутренние repo-задачи закрыты или явно выведены за scope; release-followup, source-pack refresh и closeout-sync внутри repo не считаются внешними шагами.
- если required completion package нужен для repo-first instruction changes, он должен быть в том же финальном ответе и не может быть отложен до follow-up вопроса пользователя.
