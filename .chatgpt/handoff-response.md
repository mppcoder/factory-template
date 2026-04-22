## Handoff в Codex

```text
Repo: factory-template
Цель: выполнить текущий handoff по проекту factory-template.
Приоритет: сначала правила repo (`AGENTS`, runbook, scenario-pack, policy files), затем общие инструкции без конфликта с ними.
Entry point: 00-master-router.md
Launch source: chatgpt-handoff
Task class: build
Selected profile: build
Selected model: gpt-5.4
Selected reasoning effort: medium
Pipeline stage: done
Handoff allowed: yes (forbidden)
Scope: работать только в пределах этого repo и связанных project artifacts.
Verify: использовать актуальные validators, verification-report.md и done-report.md.
```

## Инструкция пользователю
1. Цель
Передать задачу в Codex уже по нормализованному handoff.
2. Где сделать
В текущем проекте.
3. Точные шаги
Использовать подготовленный handoff-блок выше без пересборки из файлов вручную.
4. Ожидаемый результат
Codex получает один цельный copy-paste handoff и работает по правилам repo.
5. Что прислать обратно
Итог выполнения или уточнение, если появится внешний блокирующий шаг.
