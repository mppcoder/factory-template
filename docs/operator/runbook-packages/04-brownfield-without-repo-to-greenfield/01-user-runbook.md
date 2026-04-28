# Пользовательский ранбук: путь без repo

## Цель

Принять входящие материалы без нормализованного repo, реконструировать canonical repo внутри target project root, затем пройти with-repo adoption/conversion и завершить как `greenfield-product`.

Brownfield without repo — это intake/reconstruction path, не финальный тип проекта.

## Окно браузера

Контур: Browser ChatGPT Project.

1. Опишите, какие материалы есть и где они лежат.
2. Первый сценарий: `template-repo/scenario-pack/00-master-router.md`.
3. Handoff должен требовать, чтобы temporary/reconstructed/intermediate repos не были siblings в `/projects`.

## Окно удаленной IDE

Контур: VS Code Remote SSH на VPS.

1. Создайте target root `/projects/<project-slug>/`.
2. Входящие материалы кладите только в `/projects/<project-slug>/_incoming/`.
3. Temporary/reconstructed/helper repos держите внутри `/projects/<project-slug>/`, например `reconstructed-repo/`.
4. После conversion уберите transitional workspace из active path: archive, rename или move в historical area.

## Чат Codex

Контур: Codex extension / Codex chat.

1. Откройте новый Codex chat/window в target root.
2. Выберите model/reasoning вручную.
3. Вставьте один handoff block с `Язык ответа Codex: русский`.
4. Не используйте старую live session как доказательство profile switch.

## Резервный терминальный путь

Контур: Terminal only fallback.

```bash
python3 template-repo/scripts/validate-brownfield-transition.py <project-root> --without-repo
python3 template-repo/scripts/validate-brownfield-transition.py <project-root> --with-repo
python3 template-repo/scripts/validate-greenfield-conversion.py <project-root> --require-converted
```

## Внешние интерфейсы

Контур: GitHub UI / external UI.

External inputs: исходные архивы, ownership approvals, GitHub repo creation если Codex write path недоступен, secrets и runtime approvals.

## Секреты и подтверждения

Контур: Secrets и approvals.

Входящие материалы проверяйте на секреты до коммита. Private dumps и transcripts не добавляйте в repo.
