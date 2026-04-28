# Пользовательский ранбук: путь с существующим repo

## Цель

Принять существующий repo как canonical project root, провести audit/adoption/conversion и завершить рабочее состояние как `greenfield-product`.

Brownfield with repo не является финальным типом проекта.

## Окно браузера

Контур: Browser ChatGPT Project.

1. В запросе укажите repo path и цель adoption.
2. Первый сценарий всегда `template-repo/scenario-pack/00-master-router.md`.
3. Handoff должен явно говорить, что brownfield done требует conversion или documented blocker.

## Окно удаленной IDE

Контур: VS Code Remote SSH на VPS.

1. Откройте существующий repo как `/projects/<project-slug>`.
2. Не создавайте рядом sibling `converted-repo`, `audit-repo` или `helper-repo`.
3. Repo-first core materialize-ится внутрь этого root.

## Чат Codex

Контур: Codex extension / Codex chat.

1. Откройте новый Codex chat/window.
2. Выберите model/reasoning вручную в picker.
3. Вставьте один handoff block.
4. Already-open session не является auto-switch boundary.

## Резервный терминальный путь

Контур: Terminal only fallback.

```bash
python3 template-repo/scripts/validate-brownfield-transition.py <project-root> --with-repo
python3 template-repo/scripts/validate-greenfield-conversion.py <project-root> --require-converted
```

## Внешние интерфейсы

Контур: GitHub UI / external UI.

Внешними остаются protected branches, human approval на risky migration, external deploy approvals и секреты.

## Секреты и подтверждения

Контур: Secrets и approvals.

Audit reports должны быть sanitized. Secrets, production dumps и private transcripts не коммитятся.
