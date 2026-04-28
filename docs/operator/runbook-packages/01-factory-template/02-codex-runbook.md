# Ранбук для Codex: factory-template

## Маршрут

- `launch_source`: `chatgpt-handoff` или `direct-task`.
- `project_profile`: `factory-template as greenfield-product + factory-producer-owned layer`.
- `selected_scenario`: `template-repo/scenario-pack/00-master-router.md -> template-repo/scenario-pack/15-handoff-to-codex.md`.
- `apply_mode`: `manual-ui` by default.
- `strict_launch_mode`: `optional`.

## Старт

1. Прочитай `template-repo/scenario-pack/00-master-router.md`.
2. Если route отправляет дальше, прочитай repo-файлы маршрута.
3. Для `chatgpt-handoff` дай только route receipt, не self-handoff.
4. Для `direct-task` сначала покажи visible self-handoff.
5. Работай repo-first: repo rules выше общих инструкций, пока они не конфликтуют со старшими системными правилами.

## Реализация

- Разделяй factory-producer-owned paths и generated/battle project root.
- Не переносите `factory/producer/*` в downstream active root.
- При mismatch сначала defect-capture, затем remediation.
- Internal follow-up внутри repo выполняй сам: docs, validators, reports, manifests, verify, verified sync при доступности.

## Язык handoff

Любой copy-paste handoff обязан содержать строку:

```text
Язык ответа Codex: русский. Отвечай пользователю по-русски.
```

Нельзя выдавать handoff ссылкой на файл или несколькими блоками.
