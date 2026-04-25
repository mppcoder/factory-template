# Codex workflow для этого проекта

## Контракт routing
- advisory layer: `AGENTS`, scenario-pack, runbooks, ChatGPT Project instructions;
- executable layer: `codex-routing.yaml`, `.codex/config.toml` named profiles и `./scripts/launch-codex-task.sh`;
- надежная единица маршрутизации: новый task launch.

## Именованные profiles
- `quick`: docs / triage / search
- `build`: feature / fix / implementation
- `deep`: root-cause / audit / architecture
- `review`: review / tests / cleanup

## Как запускать
- не проверяйте routing в старой уже открытой сессии Codex;
- для интерактивной работы через VS Code Codex extension используйте `manual-ui (default)`: откройте новый чат/окно Codex, вручную выставьте `selected_model` и `selected_reasoning_effort` в picker, затем вставьте handoff;
- `selected_profile` фиксирует intended route для repo; `selected_model` и `selected_reasoning_effort` описывают ожидаемую конфигурацию этого profile, но не auto-switch в уже открытой live session;
- `launcher-first strict mode` через `./scripts/launch-codex-task.sh --launch-source <chatgpt-handoff|direct-task> ...` нужен для automation, reproducibility, shell-first и scripted launch;
- `новый чат + вставка handoff` и `new task launch через executable launcher` — не одно и то же;
- для direct task launcher сначала создает `.chatgpt/direct-task-self-handoff.md` и `.chatgpt/direct-task-response.md`, а затем фиксирует route в `.chatgpt/task-launch.yaml`;
- первый substantive ответ Codex по direct task должен явно показать self-handoff block до remediation.
- если после manual UI apply или strict launch виден sticky last-used state, завершите текущую сессию, откройте новую и при необходимости выполните launcher еще раз, а затем сверьте model с `codex debug models`.

## Model availability auto-check

Repo-configured mapping живет в `codex-model-routing.yaml`: `task_class_routing` выбирает profile, `profile_routes` выбирает model/reasoning/plan-mode reasoning. Live Codex catalog не является тем же самым: его нужно проверять командой `python3 scripts/check-codex-model-catalog.py .`, которая вызывает `codex debug models`, когда CLI доступен.

`--write-proposal` создает `reports/model-routing/model-routing-proposal.md` с текущим mapping, сводкой live catalog, предложенным mapping, evidence поддержки reasoning, рисками и точными файлами для обновления. `--apply-safe` может обновить только snapshot-поля catalog; promotion новых моделей в profile mapping требует ручного review.

Диагностика:
- новый model есть в live catalog, но отсутствует в routing: сначала создайте proposal, затем осознанно обновите `codex-model-routing.yaml` и named profiles в `.codex/config.toml`;
- configured model исчез: handoff должен сказать, что `selected_model` repo-configured и требует live validation; strict validator может упасть;
- unsupported reasoning: выберите supported reasoning или другой `selected_model` до release-facing handoff;
- sticky model в VS Code picker: откройте новый chat/window и вручную проверьте picker;
- handoff вставлен в уже открытую session: считайте это non-canonical fallback, а не executable route switching.

## Когда handoff допустим
Переключение в рабочий Codex launch допустимо только после того, как:
- собран минимальный evidence pack;
- заполнены `reality-check.md`, `evidence-register.md`, `reverse-engineering-summary.md`;
- определены safe zones и rollback plan;
- handoff в Codex больше не противоречит policy preset.

## Внешние boundary-действия
Эти действия остаются за оператором:
- создание новых GitHub repos;
- подключение репозиториев и app sources в ChatGPT Projects;
- загрузка архивов в `/projects/<project-root>/_incoming/`;
- ввод секретов и работа с внешними UI.

## Canonical VPS layout
- `/projects` содержит только project roots;
- `_incoming` допускается только как подпапка проекта: `/projects/<project-root>/_incoming/`;
- brownfield temporary, intermediate и reconstructed repos нельзя раскладывать плоско рядом в `/projects`.
