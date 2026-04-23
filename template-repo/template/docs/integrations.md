# Интеграции

Перечислите внешние сервисы, API и обмены данными.

## ChatGPT Project Repo Instruction

Для проекта задайте repo-first правило:

1. В поле `Instructions` ChatGPT Project внесите только короткую repo-first инструкцию.
2. На каждый запрос сначала открывается GitHub repo проекта.
3. Первое обязательное чтение: `template-repo/scenario-pack/00-master-router.md`.
4. Ответ формируется только после прохождения маршрута из router-сценария.

Если где-то остаются legacy export-артефакты, считайте их вспомогательным reference-слоем, а не основным источником сценариев.

Для запуска Codex этого недостаточно:
- Instructions и router-сценарии являются advisory layer;
- для интерактивной работы в VS Code Codex extension используйте `manual-ui (default)`: новый чат/окно Codex, ручной выбор model/reasoning в picker, затем вставка handoff;
- launcher-first через `./scripts/launch-codex-task.sh` остается optional strict mode для automation, reproducibility и shell-first запуска;
- новый чат + вставка handoff и executable new task launch — не одно и то же;
- строгая executable-маршрутизация по-прежнему подтверждается только через новый task launch;
- уже открытая live session не является надежным auto-switch механизмом;
- если проявился sticky last-used state, закройте текущую сессию, откройте новую и при необходимости используйте strict launch path.
