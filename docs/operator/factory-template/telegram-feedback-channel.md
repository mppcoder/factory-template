# Канал Telegram Feedback

Telegram Feedback Channel - repo-native слой доставки и безопасного управления для `factory-template` и downstream/battle проектов. Он не создает новую базу задач и не заменяет repo artifacts как source of truth.

## Источник истины

Telegram events выводятся из существующих repo contours:

- `.chatgpt/chat-handoff-index.yaml`
- `.chatgpt/codex-work-index.yaml`
- `.chatgpt/handoff-implementation-register.yaml`
- lifecycle dashboard/card artifacts
- `reports/factory-feedback/`
- `reports/bugs/`
- update/release governance artifacts
- validators and closeout scripts

Outbound delivery пишет audit records в `reports/notifications/outbox.jsonl`. Inbound commands пишут sanitized audit records в `reports/notifications/inbound-audit.jsonl`. Runtime JSONL files находятся в `.gitignore`.

## Артефакты

- Event schema: `template-repo/template/.chatgpt/telegram-feedback-event.schema.yaml`
- Example config: `template-repo/template/.chatgpt/telegram-feedback-channel.example.yaml`
- Notifier: `template-repo/scripts/factory_notify_telegram.py`
- Validator: `template-repo/scripts/validate-telegram-feedback-channel.py`
- P0 fixtures: `tests/telegram-feedback-channel/events/p0-events.yaml`

## Таксономия P0 событий

Поддерживаемые P0 kinds:

- `task.completed`
- `codex.completed`
- `user_action.required`
- `bug.detected`
- `bug.fixed`
- `verification.failed`
- `update.available`
- `update.recommended`
- `release.published`
- `deploy.done`

`downstream.feedback` также зарезервирован для upstream feedback из battle проектов обратно в фабрику.

## Маршрутизация Telegram

Маршрутизация состоит из двух слоев:

- `project_contour` выбирает отдельную Telegram destination/topic для проектного контура;
- `kind_to_topic` остается fallback для старых или общих уведомлений.

Приоритет у `project_contour`. Так у каждого контура проекта может быть отдельная Telegram тема или отдельный чат:

- `template` -> `template-general`: основной шаблон, тема `general`;
- `battle-development` -> `battle-development`: разработка боевого проекта на базе шаблона;
- `battle-deploy` -> `battle-deploy`: развертывание боевого проекта на базе шаблона;
- `battle-operate` -> `battle-operate`: сопровождение/операционная поддержка боевого проекта;
- `battle-updates` -> `battle-updates`: обновления и рекомендации по обновлениям боевого проекта;
- `downstream-feedback` -> `downstream-feedback`: feedback из downstream/battle проектов обратно в фабрику.

`topics` могут указывать на разные Telegram чаты или на разные forum topics внутри одного чата. Для основного шаблона canonical topic name - `template-general`; operator-facing имя темы в Telegram: `general`.

Также остаются topic names для fallback по типам событий:

- `factory-main`
- `codex-completions`
- `user-actions`
- `bugs`
- `updates`
- `downstream-projects`

Если forum topics еще не настроены, держите `message_thread_id: null` в локальном config. Placeholders заменяются только в локальной config copy, не в template example.

## Безопасность

`TELEGRAM_BOT_TOKEN` должен жить только в env или secret store. Его нельзя коммитить.

Inbound commands require both allowlists:

- `TELEGRAM_ALLOWED_CHAT_IDS`
- `TELEGRAM_ALLOWED_USER_IDS`

Allowed inbound commands намеренно узкие: `status`, `ack`, `defer`, `bug`, `handoff_draft`, `feedback`. Telegram не должен запускать arbitrary shell, Codex, deploy, merge, push или destructive actions.

## Dry-run

Validate schema, config and fixtures:

```bash
python3 template-repo/scripts/validate-telegram-feedback-channel.py --allow-placeholders
```

Run notifier without a token:

```bash
python3 template-repo/scripts/factory_notify_telegram.py send \
  --event tests/telegram-feedback-channel/events/p0-events.yaml \
  --dry-run \
  --outbox /tmp/telegram-feedback-outbox.jsonl
```

Audit an inbound safe command fixture:

```bash
TELEGRAM_ALLOWED_CHAT_IDS=123456789 TELEGRAM_ALLOWED_USER_IDS=987654321 \
python3 template-repo/scripts/factory_notify_telegram.py audit-inbound \
  --payload tests/telegram-feedback-channel/inbound/ack-command.json \
  --audit /tmp/telegram-feedback-inbound-audit.jsonl
```

## Live-настройка

1. Создайте bot в BotFather и храните token вне repo как `TELEGRAM_BOT_TOKEN`.
2. Получите destination `chat_id` для каждого контура или один общий `chat_id` с разными forum topics.
3. Для основного шаблона создайте topic `general` и подставьте его id в `template-general.message_thread_id`.
4. Создайте локальный config из `.chatgpt/telegram-feedback-channel.example.yaml`.
5. Замените placeholders для нужных контуров и установите `enabled: true`.
6. Установите `TELEGRAM_ALLOWED_CHAT_IDS` и `TELEGRAM_ALLOWED_USER_IDS`.
7. Запустите validator против локального config без `--allow-placeholders`.
8. Выполните один `--dry-run`, затем real send только после проверки outbox entry.

## Точки интеграции

- Closeout task completed: emit `task.completed` из `.chatgpt/done-report.md` / `.chatgpt/task-index.yaml`.
- Codex completed: emit `codex.completed` из `.chatgpt/codex-work-index.yaml` или `.chatgpt/handoff-implementation-register.yaml`.
- User action required: emit `user_action.required` из `.chatgpt/boundary-actions.md`.
- Bug detected/fixed: emit `bug.detected` / `bug.fixed` из `reports/bugs/` и reusable feedback из `reports/factory-feedback/`.
- Validator failed: emit `verification.failed` только после capture failure evidence.
- Update available/recommended: emit из `.chatgpt/software-update-watchlist.yaml` и `.chatgpt/software-update-readiness.yaml`.
- Release/deploy: emit `release.published` / `deploy.done` из release governance reports.
- Downstream feedback: emit `downstream.feedback` из `reports/factory-feedback/incoming-learnings/`.

## Границы

Telegram status не canonical. Canonical state остается в repo artifacts. Dedupe использует `dedupe_key`, а outbox фиксирует delivery attempts. Green Telegram delivery alone не закрывает goal, task, bug, update, release или deploy.
