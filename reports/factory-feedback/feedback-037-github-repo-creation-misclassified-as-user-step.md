# FEEDBACK-037: GitHub repo creation должен быть internal step при доступном write path

Дата: 2026-04-26

## Наблюдение

Brownfield no-repo closeout может ошибочно остановиться после local repo creation и попросить пользователя создать GitHub repo вручную.

## Правило

Если текущая задача создала local project repo и следующий естественный шаг — remote publication:

- Codex сначала проверяет `gh auth status` или GitHub connector;
- если owner/name однозначны и write path доступен, Codex сам создает repo, добавляет `origin` и выполняет push;
- external boundary допустим только при конкретном blocker;
- при blocker инструкция пользователю должна содержать owner/repo, visibility, exact command/UI step, expected URL, verification command и что прислать обратно.

## Current remediation

Создан и запушен repo:

```text
https://github.com/mppcoder/openclaw-brownfield
```

Latest project repo commit:

```text
7b3d1a4 Publish OpenClaw brownfield repo and fix generated verify
```

## Status

Captured; rule promoted into scenario-pack and generated boundary-action validator.

