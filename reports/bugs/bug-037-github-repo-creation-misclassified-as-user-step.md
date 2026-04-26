# BUG-037: GitHub repo creation был ошибочно отнесен к ручному шагу пользователя

Дата: 2026-04-26

## Кратко

После создания локального brownfield project repo closeout оставил GitHub remote creation как пользовательский optional step. В текущей среде `gh` был авторизован и имел write permissions, поэтому создание GitHub repo, добавление `origin` и push должны были быть выполнены Codex.

## Симптом

Финальный ответ сообщал, что remote creation является внешней границей, хотя не был проверен доступный GitHub write path.

## Evidence

- `gh auth status` подтвердил login `mppcoder`.
- Token scopes включали `repo` и related write scopes.
- `gh repo view mppcoder/openclaw-brownfield` до remediation возвращал repository not found.
- `gh repo create mppcoder/openclaw-brownfield --private --source=. --remote=origin --push` успешно создал repo и отправил `main`.

## Impact

- Пользователь получил ручной шаг без реального blocker.
- Field pilot closeout снова требовал ручного продолжения вместо выполнения доступной repo operation.
- External action instructions были недостаточно конкретны: не было owner/repo, visibility, exact command, expected remote URL и verification command.

## Classification

- Defect layer: closeout / external-boundary classification.
- Reusable issue: yes.
- Severity: high для no-repo brownfield flow.

## Remediation

- Создан GitHub repo `https://github.com/mppcoder/openclaw-brownfield`.
- `/projects/openclaw-brownfield` получил `origin` и tracking `main`.
- Push выполнен до commit `7b3d1a4`.
- `00-master-router.md`, `16-done-closeout.md`, `create-codex-task-pack.py` и `validate-codex-task-pack.py` усилены правилом: GitHub repo/remote creation является internal Codex work, если `gh`/connector доступен и owner/name однозначны.

## Verification

- `git -C /projects/openclaw-brownfield status --short --branch` -> clean, `main...origin/main`.
- `gh repo view mppcoder/openclaw-brownfield` -> repo exists.

## Status

Fixed in current scope.

