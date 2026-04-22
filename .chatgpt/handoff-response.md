## Launch в Codex

```bash
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute
```

- Выполняйте этот launch command из корня repo как новый task launch.
- Advisory handoff text сам по себе не переключает profile/model/reasoning в уже открытой или случайной Codex chat-сессии.
- `selected_profile` — исполнимая граница; `selected_model` и `selected_reasoning_effort` — ожидаемая конфигурация profile, а не promise auto-switch.
- Если видите sticky last-used state, закройте текущую сессию и снова выполните launch command, а затем проверьте local named profile.

## Handoff в Codex

```text
Repo: factory-template
Цель: выполнить текущий handoff по проекту factory-template.
Приоритет: сначала правила repo (`AGENTS`, runbook, scenario-pack, policy files), затем общие инструкции без конфликта с ними.
Entry point: 00-master-router.md
Launch source: chatgpt-handoff
Task class: review
Selected profile: review
Selected model: gpt-5.4
Selected reasoning effort: high
Executable launch command: ./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute
Direct Codex command behind launcher: codex --profile review
Routing rule: advisory/handoff text != executable profile switch; reliable routing unit = new task launch only.
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
Сначала выполнить launch command из блока `Launch в Codex`, затем вставить handoff-блок без пересборки из файлов вручную.
4. Ожидаемый результат
Codex стартует на явной launch boundary и получает один цельный copy-paste handoff по правилам repo.
5. Что прислать обратно
Итог выполнения или уточнение, если появится внешний блокирующий шаг.
