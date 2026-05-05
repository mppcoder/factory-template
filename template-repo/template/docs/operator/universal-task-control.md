# Universal Task Control в generated project

## Назначение

Universal Task Control помогает вести задачи проекта через repo-native очередь: задача получает `FT-TASK-NNNN`, понятный маршрут, preview, Codex handoff, evidence и видимый статус в dashboard.

Canonical registry generated project:

```bash
.chatgpt/task-registry.yaml
```

Все команды ниже выполняются из root generated repo. Они не запускают Codex сами, не переключают model/profile/reasoning и не обращаются к GitHub API.

## Быстрый путь

1. Проверить registry:

```bash
python3 scripts/validate-task-registry.py .chatgpt/task-registry.yaml
```

2. Посмотреть следующий task id:

```bash
python3 scripts/allocate-task-id.py --registry .chatgpt/task-registry.yaml
```

3. Добавить draft task:

```bash
python3 scripts/allocate-task-id.py \
  --registry .chatgpt/task-registry.yaml \
  --append-draft \
  --title "Add operator checklist" \
  --goal "Подготовить короткий checklist для следующего шага." \
  --task-class docs \
  --source-kind manual \
  --source-ref ""
```

4. Перевести задачу в `ready_for_handoff`, когда route понятен:

```bash
python3 scripts/update-task-status.py \
  --registry .chatgpt/task-registry.yaml \
  --dashboard .chatgpt/project-lifecycle-dashboard.yaml \
  --task-id FT-TASK-0002 \
  --status ready_for_handoff \
  --reason "Task route is clear." \
  --sync-dashboard \
  --write
```

5. Сделать preview:

```bash
python3 scripts/preview-task-handoff.py \
  --registry .chatgpt/task-registry.yaml \
  --task-id FT-TASK-0002 \
  --output reports/handoffs/FT-TASK-0002-preview.md
```

6. Подготовить task pack и явно перевести в `ready_for_codex`:

```bash
python3 scripts/prepare-task-pack.py \
  --registry .chatgpt/task-registry.yaml \
  --dashboard .chatgpt/project-lifecycle-dashboard.yaml \
  --task-id FT-TASK-0002 \
  --mark-ready-for-codex \
  --sync-dashboard \
  --write
```

7. Проверить generated handoff:

```bash
python3 scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0002-codex-handoff.md
```

8. Обновить очередь:

```bash
python3 scripts/render-task-queue.py \
  --registry .chatgpt/task-registry.yaml \
  --output reports/task-queue.md
```

## Переходы статусов

- `draft`: задача создана, но route еще не готов.
- `ready_for_handoff`: route понятен, можно генерировать preview/handoff.
- `ready_for_codex`: handoff создан и валидирован, но Codex еще не запущен.
- `codex_running`: задача выполняется в Codex session.
- `implemented` или `verification_pending`: изменения есть, verification еще не закрыта.
- `human_review`: нужен человек, consent, secret entry, review или external approval.
- `verified`: проверки и evidence есть.

Не ставьте green status без evidence или accepted reason. Если нужен внешний шаг, заполните `human_boundary.external_user_action` и вынесите его в closeout.

## GitHub Issue Forms / формы задач

`.github/ISSUE_TEMPLATE/*.yml` в generated project нужны для локальных задач текущего repo. Обычные формы `Bug`, `Feature`, `Docs`, `Research`, `Audit`, `Release`, `Curator` не отправляют данные upstream.

Форма `Downstream feedback` нужна только когда вы сознательно готовите sanitized feedback в сторону `factory-template`. Не вставляйте secrets, приватные логи, приватные repo URLs или клиентские данные. Public/upstream отправка требует review и consent.

Локальный bridge из sanitized issue draft:

```bash
python3 scripts/issue-to-task-registry.py \
  --registry .chatgpt/task-registry.yaml \
  --issue-file reports/handoffs/example-issue-draft.yaml
```

Bridge читает локальный JSON/YAML/Markdown draft, не обращается к GitHub API и не публикует данные.

## Dashboard / панель проекта

Generated dashboard source:

```bash
.chatgpt/project-lifecycle-dashboard.yaml
```

Universal Task Control section должен показывать:

- `registry_path: .chatgpt/task-registry.yaml`;
- счетчики `ready_for_handoff`, `ready_for_codex`, `codex_running`, `human_review`;
- `status: pending`, если открытых задач нет;
- no false green: зеленый статус допустим только с evidence.

Перерендерить dashboard/card:

```bash
python3 scripts/render-project-lifecycle-dashboard.py --format markdown --output reports/project-lifecycle-dashboard.md
python3 scripts/render-project-lifecycle-dashboard.py --format chatgpt-card --output reports/project-status-card.md
```

## Sync существующего downstream project

При обновлении уже существующего проекта нельзя слепо перезаписывать `.chatgpt/task-registry.yaml`: там могут быть реальные пользовательские задачи, statuses, evidence и boundaries.

Safe sync:

- обновляйте scripts/docs/templates отдельно от registry state;
- сохраняйте `tasks`, `next_task_number`, `evidence`, `last_status_change`;
- новые поля добавляйте migration-style;
- перед изменением semantics создавайте отчет в `reports/`.
