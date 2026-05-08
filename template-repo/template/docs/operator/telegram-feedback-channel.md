# Канал Telegram Feedback

Telegram Feedback Channel - optional delivery/control layer поверх repo-first project artifacts. Он не заменяет `.chatgpt` indexes, reports, validators, GitHub Issues или lifecycle dashboard.

## Файлы

- `.chatgpt/telegram-feedback-event.schema.yaml` - event envelope schema.
- `.chatgpt/telegram-feedback-channel.example.yaml` - safe config example without secrets.
- `reports/notifications/outbox.jsonl` - runtime outbound delivery log, git-ignored.
- `reports/notifications/inbound-audit.jsonl` - runtime inbound command audit, git-ignored.

## Типы событий

P0 event kinds: `task.completed`, `codex.completed`, `user_action.required`, `bug.detected`, `bug.fixed`, `verification.failed`, `update.available`, `update.recommended`, `release.published`, `deploy.done`.

## Контуры проекта

Каждый event содержит `project_contour`. По нему можно отправлять уведомления в отдельный Telegram chat или forum topic:

- `template` -> `template-general`: основной шаблон, тема `general`;
- `battle-development` -> `battle-development`: разработка боевого проекта на базе шаблона;
- `battle-deploy` -> `battle-deploy`: развертывание боевого проекта;
- `battle-operate` -> `battle-operate`: сопровождение боевого проекта;
- `battle-updates` -> `battle-updates`: обновления и рекомендации;
- `downstream-feedback` -> `downstream-feedback`: feedback из downstream/battle проектов в фабрику.

`project_contour` имеет приоритет над fallback mapping по `kind`.

## Безопасность

Храните `TELEGRAM_BOT_TOKEN` только в env или secret store. Inbound commands требуют `TELEGRAM_ALLOWED_CHAT_IDS` и `TELEGRAM_ALLOWED_USER_IDS`.

Allowed inbound commands: `status`, `ack`, `defer`, `bug`, `handoff_draft`, `feedback`. Telegram commands не должны запускать shell, Codex, deploy, merge, push или destructive actions.

## Настройка

1. Скопируйте `.chatgpt/telegram-feedback-channel.example.yaml` в локальный untracked config, если проекту нужна live Telegram delivery.
2. Замените chat ids и optional forum topic ids для нужных project contours.
3. Для основного шаблона настройте `template-general` на Telegram topic `general`.
4. Установите `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_CHAT_IDS` и `TELEGRAM_ALLOWED_USER_IDS` вне repo.
5. Проверьте local config и выполните dry-run перед real delivery.

Telegram delivery - это evidence of notification only. Project закрывается или переоткрывается только через repo-native artifacts и validators.
