## Применение в Codex UI

- `apply_mode: manual-ui (default)`
- Для VS Code Codex extension откройте новый чат/окно Codex.
- Вручную выберите model `gpt-5.4` и reasoning `high` в picker.
- Только после этого вставьте handoff-блок ниже.
- новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же.
- Advisory handoff text сам по себе не переключает profile/model/reasoning в уже открытой или случайной Codex chat-сессии.
- Уже открытая live session не является надежным механизмом автопереключения.
- `selected_profile` — исполнимая граница; `selected_model` и `selected_reasoning_effort` — ожидаемая конфигурация profile, а не promise auto-switch.
- Если видите sticky last-used state, закройте текущую сессию, откройте новую и заново проверьте picker.

## Строгий launch mode (опционально)

- `strict_launch_mode: optional`
- Используйте этот путь, если нужна automation, reproducibility, shell-first или scripted launch.

```bash
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute
```

- Это strict executable boundary для нового task launch.
- Если manual UI apply выглядит stale или нужен строго воспроизводимый route, закройте текущую сессию и используйте эту команду.

## Handoff в Codex

```text
Repo: factory-template
Цель: выполнить текущий handoff по проекту factory-template.
Приоритет: сначала правила repo (`AGENTS`, runbook, scenario-pack, policy files), затем общие инструкции без конфликта с ними.
Entry point: 00-master-router.md
Launch source: chatgpt-handoff
Task class: deep
Selected profile: deep
Selected model: gpt-5.4
Selected reasoning effort: high
Apply mode: manual-ui (default)
Strict launch mode: optional
Optional strict launch command: ./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute
Direct Codex command behind launcher: codex --profile deep
Routing rule: advisory/handoff text != executable profile switch; reliable routing unit = new task launch only.
Manual UI rule: для VS Code Codex extension откройте новый чат/окно, вручную выберите model/reasoning в picker, затем вставьте этот handoff.
Live session rule: уже открытая live session = non-canonical fallback; не обещать auto-switch.
Pipeline stage: defect-capture -> classification -> remediation
Handoff allowed: yes
Scope: работать только в пределах этого repo и связанных project artifacts.
Verify: использовать актуальные validators, verification-report.md и done-report.md.
```

## Инструкция пользователю
1. Цель
Передать задачу в Codex уже по нормализованному handoff.
2. Где сделать
В VS Code Codex extension или, при необходимости strict routing, через терминал в текущем проекте.
3. Точные шаги
По умолчанию используйте блок `Применение в Codex UI`: новый чат/окно, ручной выбор model/reasoning в picker, затем вставка handoff-блока без пересборки из файлов вручную. Если нужна строгая воспроизводимость, используйте блок `Строгий launch mode (опционально)`.
4. Ожидаемый результат
Codex получает один цельный copy-paste handoff по правилам repo, а пользователь выбирает между manual UI apply по умолчанию и optional strict launch path.
5. Что прислать обратно
Итог выполнения или уточнение, если появится внешний блокирующий шаг.
