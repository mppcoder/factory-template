# Codex workflow для этого проекта

## Routing contract
- advisory layer: `AGENTS`, scenario-pack, runbooks, ChatGPT Project instructions;
- executable layer: `codex-routing.yaml`, `.codex/config.toml` named profiles и `./scripts/launch-codex-task.sh`;
- надежная единица маршрутизации: новый task launch.

## Named profiles
- `quick`: docs / triage / search
- `build`: feature / fix / implementation
- `deep`: root-cause / audit / architecture
- `review`: review / tests / cleanup

## Как запускать
- не проверяйте routing в старой уже открытой сессии Codex;
- для новой задачи запускайте `./scripts/launch-codex-task.sh --launch-source <chatgpt-handoff|direct-task> ...`;
- для direct task launcher сначала создает `.chatgpt/direct-task-self-handoff.md`, а затем фиксирует route в `.chatgpt/task-launch.yaml`.

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
- загрузка архивов в `/projects/_incoming`;
- ввод секретов и работа с внешними UI.
