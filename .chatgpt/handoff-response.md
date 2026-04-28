## Применение в Codex UI

- `apply_mode: manual-ui (default) (default)`
- Для VS Code Codex extension откройте новый чат/окно Codex.
- Вручную выберите model `gpt-5.5` и reasoning `high` в picker.
- Только после этого вставьте handoff-блок ниже.
- новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же.
- Advisory handoff text сам по себе не переключает profile/model/reasoning в уже открытой или случайной Codex chat-сессии.
- Уже открытая live session не является надежным механизмом автопереключения.
- `selected_profile` — исполнимая граница; `selected_model` и `selected_reasoning_effort` — repo-configured mapping profile, а не promise auto-switch или live availability guarantee.
- `model_catalog_status: available`; `selected_model` требует live validation, если catalog недоступен или stale.
- Если видите sticky last-used state, закройте текущую сессию, откройте новую и заново проверьте picker.

## Строгий launch mode (опционально)

- `strict_launch_mode: optional`
- Используйте этот путь, если нужна automation, reproducibility, shell-first или scripted launch.

```bash
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute
```

- Это строгая executable boundary для нового task launch.
- Если ручное применение через UI выглядит устаревшим или нужен строго воспроизводимый route, закройте текущую сессию и используйте эту команду.

## Handoff в Codex

```text
Репозиторий: factory-template
Цель: выполнить текущий handoff по проекту factory-template.
Язык ответа Codex: русский. Отвечай пользователю по-русски; английский оставляй только для technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.
Приоритет: сначала правила repo (`AGENTS`, runbook, scenario-pack, policy files), затем общие инструкции без конфликта с ними.
Точка входа: 00-master-router.md
Источник запуска: chatgpt-handoff
Класс задачи: deep
Выбранный профиль: deep
Выбранная модель: gpt-5.5
Выбранное reasoning effort: high
Выбранное plan mode reasoning effort: high
Статус model catalog: available
Примечание по live availability: selected_model совпадает с последним сохраненным snapshot repo catalog; перед внешними обещаниями повторите live catalog check
Режим применения: manual-ui (default) (default)
Строгий режим запуска: optional
Опциональная команда строгого запуска: ./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --execute
Прямая команда Codex за launcher: codex --profile deep
Правило маршрутизации: advisory/handoff text не равен executable profile switch; надежная единица маршрутизации — только новый task launch.
Правило приема ChatGPT handoff: если launch_source = chatgpt-handoff, Codex исполняет этот входящий handoff; первый ответ может содержать только handoff receipt / route receipt и не должен называть его self-handoff.
Правило full orchestration: если handoff содержит parent orchestration plan, пользовательское действие заканчивается после вставки; parent Codex сам запускает repo-native orchestrator с validation gate и `--execute`, а ручная shell-команда пользователя является только troubleshooting/strict fallback.
Правило ручного UI: для VS Code Codex extension откройте новый чат/окно, вручную выберите model/reasoning в picker, затем вставьте этот handoff.
Правило live session: уже открытая live session = non-canonical fallback; не обещать auto-switch.
Этап pipeline: source-map -> prompt-inventory -> migration-plan -> remediation -> verification -> closeout
Разрешение handoff: yes
Область работы: работать только в пределах этого repo и связанных project artifacts.
Проверка: использовать актуальные validators, verification-report.md и done-report.md.
```

## Инструкция пользователю
1. Цель
Передать задачу в Codex уже по нормализованному handoff.
2. Где сделать
В VS Code Codex extension или, при необходимости strict routing, через терминал в текущем проекте.
3. Точные шаги
По умолчанию используйте блок `Применение в Codex UI`: новый чат/окно, ручной выбор model/reasoning в picker, затем вставка handoff-блока без пересборки из файлов вручную. Если нужна строгая воспроизводимость, используйте блок `Строгий launch mode (опционально)`.
4. Ожидаемый результат
Codex получает один цельный handoff для вставки по правилам repo, а пользователь выбирает между ручным применением через UI по умолчанию и опциональным строгим launch path.
5. Что прислать обратно
Итог выполнения или уточнение, если появится внешний блокирующий шаг.
