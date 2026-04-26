# Bug Report: task-based Codex routing remains advisory and collapses into one static session profile

## Идентификатор
bug-010-task-routing-stuck-on-static-profile

## Краткий заголовок
`factory-template` обещает выбор модели и reasoning mode по типу задачи, но фактически не имеет исполняемого routing layer на границе нового task launch.

## Где найдено
Repo: `factory-template`

Затронутые зоны:
- `docs/operator/factory-template/03-mode-routing-factory-template.md`
- `factory/producer/ops/codex-config-factory-template.toml`
- `docs/operator/factory-template/07-AGENTS-factory-template.md`
- `template-repo/template/.codex/config.toml`
- `template-repo/template/docs/codex-workflow.md`
- `template-repo/scripts/create-codex-task-pack.py`

## Шаги воспроизведения
1. Открыть routing docs и увидеть, что repo обещает выбор профиля по классу задачи.
2. Открыть `.codex/config.toml` и проверить, что template задает один статический runtime profile без task launcher/router.
3. Проверить, что ни launcher, ни handoff generation, ни direct-task bootstrap не запускают новый Codex task с `--profile` или эквивалентным override layer.
4. Проверить, что direct task flow не создает нормализованный self-handoff по тем же сценарным полям, что и ChatGPT Project flow.

## Ожидаемое поведение
- Выбор модели и reasoning mode должен происходить на новом task launch через исполняемый router/profile layer.
- ChatGPT Project handoff и direct task to Codex должны использовать один словарь task classes, один набор handoff fields и один сценарный bootstrap.
- В repo не должно оставаться двусмысленного обещания, что AGENTS/project instructions/static config сами переключат модель в уже открытой сессии.

## Фактическое поведение
- Routing описан в policy/docs слое как рекомендация "переключать профиль" внутри живой сессии.
- Template config закрепляет один static profile/runtime и не содержит executable task launcher.
- Handoff artifacts не фиксируют selected profile/model/reasoning как фактический launch decision.
- Direct task outside ChatGPT Project не обязан создавать полный self-handoff и поэтому выпадает из общего scenario discipline.

## Evidence
- `docs/operator/factory-template/03-mode-routing-factory-template.md` описывает "Практический протокол внутри живой сессии" и ручное переключение между `default-dev` / `fast-routine` / `heavy-analysis` / `release-verify`.
- `factory/producer/ops/codex-config-factory-template.toml` задает `profile = "default-dev"` и не содержит launch router.
- `template-repo/template/.codex/config.toml` вообще содержит только один базовый runtime (`gpt-5.4`, `medium`) без named task profiles.
- `template-repo/template/docs/codex-workflow.md` описывает один дефолтный режим и subagents, но не task-launch routing.
- `template-repo/scripts/create-codex-task-pack.py` генерирует advisory handoff artifacts, но не executable launch decision и не direct self-handoff bootstrap.

## Слой дефекта
factory-template

## Временный обход
- Запускать каждую новую задачу вручную в новой сессии Codex с явно выбранным профилем.
- Перед direct task вручную оформлять self-handoff по scenario-pack и только потом продолжать remediation.

## Решение / статус
in-progress
