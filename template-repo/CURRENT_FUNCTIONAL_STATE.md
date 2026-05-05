# Текущее функциональное состояние шаблона

## Что шаблон генерирует
- README, VERSION, CHANGELOG, CURRENT_FUNCTIONAL_STATE
- `.chatgpt` с state, presets и defect-flow
- `.chatgpt/project-lifecycle-dashboard.yaml` как единая repo-native панель состояния проекта от intake до release/deploy/operate/improve
- `.chatgpt/handoff-implementation-register.yaml` как lifecycle register для ChatGPT handoff / Codex self-handoff задач до verified, deactivation или archive closeout
- handoff replacement/write-off policy: старые handoff той же задачи в одном чате списываются через `superseded`/`replaces`/`superseded_by`, а не остаются активными
- greenfield и brownfield каркас
- reports и tasks для defect-aware работы

## Какие режимы поддерживаются
- greenfield
- brownfield

## Что делает launcher
- создает working project
- применяет presets
- подставляет версию фабрики и project origin
- создает начальный versioning layer
- добавляет release decision template и reusable sync/release scripts
- копирует executable routing contract: `codex-routing.yaml`, router scripts и named Codex profiles
- копирует canonical model routing policy: `codex-model-routing.yaml`
- подготавливает generated project к launch-time self-handoff и routing verification
- direct-task contour теперь включает отдельный visible response artifact для стартового self-handoff
- smoke и pre-release layer теперь прикрывают наличие этого visible direct-task response artifact
- handoff/completion layer теперь выдает отдельный executable launch boundary и troubleshooting для sticky last-used route state
- model availability auto-check сравнивает repo-configured mapping с live `codex debug models` и генерирует proposal без automatic profile promotion
- advanced automation substrate включает dry-run issue-autofix proof, permission/label gates, bounded runner, audit ledger, rollback policy, curator promotion flow и downstream sync guidance без full autonomous mode by default
- рендерит и валидирует lifecycle dashboard через `render-project-lifecycle-dashboard.py` и `validate-project-lifecycle-dashboard.py`
- валидирует handoff implementation register через `validate-handoff-implementation-register.py` и выводит его карточки в lifecycle dashboard
- проверяет, что в одной `handoff_group` нет нескольких активных handoff после уточнения или переработки handoff в том же чате

## Что еще описано на уровне фабрики
- единая визуальная архитектура шаблона и подробные workflows по запуску, развёртыванию и downstream-update contour
- operator guide для Project Lifecycle Dashboard / Control Tower, который агрегирует task/stage state, feature waves, orchestration cockpit, release readiness, runtime/deploy state и improvement queue без heavy runtime
- handoff implementation control: отдельный repo-native слой, который не смешивается с rework KPI register и не обещает auto-switch model/profile/reasoning

## Ограничения
- содержательное наполнение versioning файлов после генерации выполняется пользователем или сценариями
- matrix runner и bugflow требуют рабочей оболочки bash/pyyaml
- auto GitHub Release publication в generated project зависит от доступности и авторизации `gh`
- issue-autofix verification не мутирует live GitHub labels/issues; security/external-secret/blocked tasks and full autonomous mode остаются human-gated/refused
- выбор `task_class` пока делается по эвристике keyword matching, а не по semantic classifier
- named profile execution по-прежнему зависит от local Codex config, поэтому source docs и validators отдельно различают executable `selected_profile`, repo-configured `selected_model` / `selected_reasoning_effort` / `selected_plan_mode_reasoning_effort` и live Codex catalog availability
