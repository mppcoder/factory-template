# Пользовательский ранбук: factory-template

## Цель

Развивать сам шаблон фабрики проектов в repo `/projects/factory-template`.
Этот repo является `greenfield-product`, чей продукт — фабрика проектов, и имеет дополнительный `factory-producer-owned` слой.

## Окно браузера

Контур: Browser ChatGPT Project.

1. Используйте короткую repo-first инструкцию.
2. На каждый запрос сначала открывайте GitHub repo `mppcoder/factory-template`.
3. Первое обязательное чтение: `template-repo/scenario-pack/00-master-router.md`.
4. Handoff в Codex должен быть одним цельным блоком и содержать `Язык ответа Codex: русский`.

## Окно удаленной IDE

Контур: VS Code Remote SSH на VPS.

1. Подключитесь к VPS через Remote SSH.
2. Откройте папку `/projects/factory-template`.
3. Не открывайте sibling temporary repo как активный root.
4. `_incoming`, temporary и reconstructed workspaces держите внутри project root.

## Чат Codex

Контур: Codex extension / Codex chat.

1. Откройте новый Codex chat/window.
2. Вручную выберите `selected_model` и `selected_reasoning_effort` в picker.
3. Вставьте один цельный handoff block.
4. Не считайте уже открытую сессию надежным auto-switch mechanism.

## Резервный терминальный путь

Контур: Terminal only fallback.

Terminal fallback нужен только для troubleshooting или strict reproduction:

```bash
python3 template-repo/scripts/resolve-codex-task-route.py --task-class deep
bash template-repo/scripts/verify-all.sh quick
```

## Внешние интерфейсы

Контур: GitHub UI / external UI.

Внешними остаются release/no-release decision, обязательный human review, protected-branch approvals и ручные UI-действия, если `gh`/connector недоступны или checks блокируют merge.

## Секреты и подтверждения

Контур: Secrets и approvals.

Не храните secrets, `.env`, токены, private transcripts или runtime approvals в repo, handoff, fixtures или reports.
