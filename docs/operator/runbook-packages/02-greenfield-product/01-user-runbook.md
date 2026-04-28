# Пользовательский ранбук: greenfield-product

## Цель

Создать или вести новый боевой проект, который с первого рабочего состояния является `greenfield-product`.

## Окно браузера

Контур: Browser ChatGPT Project.

1. Держите в Project только короткую repo-first инструкцию.
2. Source-of-truth находится в repo проекта.
3. Первый сценарий: `template-repo/scenario-pack/00-master-router.md`.
4. Для большой задачи получите один цельный handoff block с `Язык ответа Codex: русский`.

## Окно удаленной IDE

Контур: VS Code Remote SSH на VPS.

1. Откройте конечный project root: `/projects/<project-slug>`.
2. В `/projects` не держите `_release`, temporary repo или helper repo как sibling active roots.
3. Если нужны входящие материалы, кладите их в `/projects/<project-slug>/_incoming/`.

## Чат Codex

Контур: Codex extension / Codex chat.

1. Откройте новый Codex chat/window в VS Code Remote SSH context.
2. Вручную выберите model/reasoning по handoff.
3. Вставьте один handoff block.
4. Уже открытая live session является только non-canonical fallback.

## Резервный терминальный путь

Контур: Terminal only fallback.

```bash
python3 template-repo/scripts/first-project-wizard.py
python3 template-repo/scripts/preflight-vps-check.py --project-slug <project-slug>
```

## Внешние интерфейсы

Контур: GitHub UI / external UI.

Создание внешнего repo, protected branch policy, required approvals и release decisions остаются внешними, если Codex не имеет доступного write path или требуется human approval.

## Секреты и подтверждения

Контур: Secrets и approvals.

Secrets вводятся только во внешнем runtime/secret manager/UI. В repo попадают только `.env.example` и sanitized reports.
