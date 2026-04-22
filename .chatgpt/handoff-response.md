## Handoff в Codex

```text
Repo: factory-template
Цель: выполнить текущий handoff по проекту factory-template.
Приоритет: сначала правила repo (`AGENTS`, runbook, scenario-pack, policy files), затем общие инструкции без конфликта с ними.
Entry point: 00-master-router.md
Launch source: chatgpt-handoff
Task class: quick
Selected profile: quick
Selected model: gpt-5.4-mini
Selected reasoning effort: low
Pipeline stage: done
Handoff allowed: yes (forbidden)
Scope: работать только в пределах этого repo и связанных project artifacts.
Verify: использовать актуальные validators, verification-report.md и done-report.md.
```

## Wording для incidental defect

1. Continue in current chat
`Self-handoff для incidental bug подтвердил тот же route. Продолжение в этом чате допустимо, но только как continuation на уже текущем route, а не как auto-switch сессии.`

2. Recommended new Codex task/chat
`Self-handoff для incidental bug выбрал другой profile/model/reasoning. Канонический следующий шаг: скопировать новый handoff и запустить отдельный Codex task/chat для этого бага.`

3. ChatGPT deep research
`Bug требует отдельного исследования. Вместо remediation-handoff подготовь ChatGPT-ready deep research bug report/prompt и не делай вид, что текущая live-сессия безопасно покрывает этот маршрут.`

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
