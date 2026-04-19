# Определение готовности для bugfix / feature / change

Задача не считается завершенной, если:
- найденный дефект был исправлен без bug report;
- reusable defect не имеет factory feedback;
- verification не подтверждает результат;
- в done-отчете не отражено, что было найдено и что было исправлено.

## Минимум для Done
- verification-report.md заполнен;
- done-report.md заполнен;
- если в ходе работы выявлен defect, существует bug report в `reports/bugs/`;
- если defect reusable, существует запись в `reports/factory-feedback/` или meta-feedback;
- stage-state.yaml согласован;
- DoD и defect-capture валидации проходят.
