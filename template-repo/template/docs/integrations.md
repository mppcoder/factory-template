# Интеграции

Перечислите внешние сервисы, API и обмены данными.

## Repo-first инструкция для ChatGPT Project

Для проекта задайте repo-first правило:

1. В поле `Instructions` ChatGPT Project внесите только короткую repo-first инструкцию.
2. На каждый запрос сначала открывается GitHub repo проекта через GitHub connector / repo tool / authenticated `gh`.
3. Первое обязательное чтение: `template-repo/scenario-pack/00-master-router.md`.
4. Ответ формируется только после прохождения маршрута из router-сценария.

Public `github.com` / raw URL fallback допустим только при named blocker: connector unavailable, no permission, repo not installed in connector, authenticated repo tool unavailable или explicit user request for public URL.

Если где-то остаются legacy export-артефакты, считайте их вспомогательным reference-слоем, а не основным источником сценариев.

Для запуска Codex этого недостаточно:
- Instructions и router-сценарии являются advisory layer;
- для интерактивной работы в VS Code Codex extension используйте `manual-ui (default)`: новый чат/окно Codex, ручной выбор model/reasoning в picker, затем вставка handoff;
- launcher-first через `./scripts/launch-codex-task.sh` остается optional strict mode для automation, reproducibility и shell-first запуска;
- новый чат + вставка handoff и executable new task launch — не одно и то же;
- строгая executable-маршрутизация по-прежнему подтверждается только через новый task launch;
- уже открытая live session не является надежным auto-switch механизмом;
- если проявился sticky last-used state, закройте текущую сессию, откройте новую и при необходимости используйте strict launch path.

## Model routing и live Codex catalog

`codex-model-routing.yaml` фиксирует repo-configured mapping: task class -> selected_profile -> selected_model / selected_reasoning_effort / selected_plan_mode_reasoning_effort. Live Codex catalog проверяется отдельно через `scripts/check-codex-model-catalog.py`, который использует `codex debug models`, если CLI доступен.

Тот же файл хранит `prompt_migration_policy`: при появлении новой model или promotion profile mapping нужно обновить prompt policy по official OpenAI docs, а не только поменять slug. Proposal должен назвать affected prompt-like artifacts, `reports/prompt-migration/`, validators/evals и manual review boundary.

Ручной выбор в UI picker и strict launcher profile selection не одно и то же:
- `manual-ui`: пользователь открывает новый VS Code Codex chat/window, вручную выбирает model/reasoning и вставляет handoff;
- strict launcher: repo launcher передает `--profile` в новый executable launch;
- уже открытая session: только fallback, без обещания auto-switch.

Диагностика:
- новый model появился в live catalog: сначала создайте proposal через `--write-proposal`; не продвигайте profile mapping без review;
- новая model меняет prompt guidance: обновите prompt contract и Artifact Eval checks до profile promotion;
- configured model исчез: проверьте live catalog до обещания availability;
- unsupported reasoning level: выберите supported reasoning или другую model;
- sticky model в VS Code picker: откройте новый chat/window и выберите model заново;
- handoff вставлен в уже открытый chat: повторите через `manual-ui` или strict launcher boundary.
