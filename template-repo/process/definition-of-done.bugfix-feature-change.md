# Определение готовности для bugfix / feature / change

Задача не считается завершенной, если:
- найденный дефект был исправлен без bug report;
- reusable defect не имеет factory feedback;
- verification не подтверждает результат;
- в done-отчете не отражено, что было найдено и что было исправлено.
- при наличии pending external/user step финальный ответ не содержит блока `Инструкция пользователю`.
- остаются internal repo follow-up задачи, но финальный ответ оформлен как user-only closeout без inline handoff.
- required completion package для source-update/external contour был выдан только после дополнительного запроса пользователя, а не в основном финальном ответе.

## Минимум для Done
- verification-report.md заполнен;
- done-report.md заполнен;
- если в ходе работы выявлен defect, существует bug report в `reports/bugs/`;
- если defect reusable, существует запись в `reports/factory-feedback/` или meta-feedback;
- stage-state.yaml согласован;
- DoD и defect-capture валидации проходят.
- если остаются внешние действия или следующий шаг пользователя, финальный ответ завершен блоком `## Инструкция пользователю`.
- `done_complete` фиксируется только если внутренние repo-задачи закрыты или явно выведены за scope; release-followup, source-pack refresh и closeout-sync внутри repo не считаются внешними шагами.
- если required completion package нужен для source-update changes, он должен быть в том же финальном ответе и не может быть отложен до follow-up вопроса пользователя.
