# Русское ядро фабрики проектов v2.4.2

Это стабилизационный релиз фабрики проектов для связки:

- **ChatGPT Project** — сценарии, интервью, анализ, нормализация.
- **Codex** — исполнение по подготовленному handoff.
- **Repo** — единственный источник правды по документам и изменениям.

## Canonical Entry Modes

Шаблон сейчас поддерживает 3 канонических режима запуска и сопровождения:

1. Новый проект с нуля
   Основа: `greenfield` путь для нового продукта или сервиса.
   Типовой вход: `product-dev`.

2. Перевод на шаблон имеющегося проекта без репо
   Основа: `brownfield` путь для live-системы, где нет нормализованного исходного repo и сначала нужен evidence-first контур.
   Типовой вход: `brownfield-dogfood-codex-assisted`.

3. Перевод на шаблон имеющегося проекта с репо
   Основа: `brownfield` путь для уже существующего репозитория или инженерного контура.
   Типовые входы: `legacy-modernization`, `integration-project`, `audit-only`.

Во всех трех случаях для generated project используется один и тот же базовый Sources pack:

- экспорт полного `scenario-pack`

Различается не набор загружаемых файлов, а стартовый маршрут по сценариям и выбранный preset.

## Подготовка после распаковки

```bash
cd factory-v2.4.2
bash POST_UNZIP_SETUP.sh
bash MATRIX_TEST.sh
bash CLEAN_VERIFY_ARTIFACTS.sh
```

Если после self-tests нужен `PRE_RELEASE_AUDIT.sh` или сборка релиза, сначала очистите временные артефакты:

```bash
bash CLEAN_VERIFY_ARTIFACTS.sh
bash PRE_RELEASE_AUDIT.sh
```

Для работы с внешними границами без ручной сборки файлов:

```bash
bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh
bash GENERATE_BOUNDARY_ACTIONS.sh
bash VALIDATE_FACTORY_FEEDBACK.sh <working-project>
bash INGEST_FACTORY_FEEDBACK.sh <working-project> --dry-run
bash TRIAGE_INCOMING_LEARNINGS.sh --dry-run
```

`INGEST_FACTORY_FEEDBACK.sh` сначала прогоняет `VALIDATE_FACTORY_FEEDBACK.sh` и останавливает ingest на пустом или шаблонном `meta-feedback`, если не передан `--allow-incomplete`.

Для handoff в Codex:

```bash
python3 template-repo/scripts/create-codex-task-pack.sh <working-project>
python3 template-repo/scripts/validate-codex-task-pack.sh <working-project>
```

`validate-codex-task-pack.sh` проверяет, что `codex-context.md`, `codex-task-pack.md`, `boundary-actions.md` и `done-checklist.md` не только созданы, но и согласованы с `active-scenarios.yaml`.

`VALIDATE_FACTORY_TEMPLATE_OPS.sh` теперь проверяет не только структуру `sources-pack-*`, но и их semantic profile, а также direct Sources profile:

- `sources-pack-core-20` обязан содержать сценарное ядро, runbook layer и policy presets;
- `core-hot-15` обязан содержать ровно 15 hot-файлов для ежедневной прямой загрузки;
- `core-cold-5` обязан содержать ровно 5 cold/reference файлов без дублей hot-set;
- `sources-pack-release-20` обязан содержать release-facing docs и release scripts;
- `sources-pack-bugfix-20` обязан содержать launcher, validator layer и feedback/handoff validators.

Состав archive pack и direct profile теперь берётся из единого declarative manifest:

- `packaging/sources/sources-profiles.yaml`

Phase recommendation теперь тоже декларативна:

- `controlled-fixes` -> `sources-pack-core-20.tar.gz`
- `release` -> `sources-pack-release-20.tar.gz`
- `bugfix-drift` -> `sources-pack-bugfix-20.tar.gz`

Автоопределение фазы теперь считается из `git status` и правил в `factory-template-ops-policy.yaml`.

Для `release` одной правки release-файлов недостаточно:

- detector смотрит на changed paths;
- и отдельно проверяет checked intent signals в `RELEASE_CHECKLIST.md`.

Для `bugfix-drift` тоже нужен не только file drift:

- detector смотрит на bug/validator changed paths;
- и отдельно проверяет intent signals внутри `reports/bugs/*.md`.

Проверить текущую рекомендацию можно так:

```bash
bash DETECT_FACTORY_TEMPLATE_PHASE.sh
bash PHASE_DETECTION_TEST.sh
```

Эта рекомендация автоматически попадает в `_sources-export/factory-template/SUMMARY.md` и `_boundary-actions/factory-template-boundary-actions.md`, но для постоянной ежедневной работы рекомендуется hybrid-схема: direct hot-set `core-hot-15/` + cold/reference archive `core-cold-5.tar.gz`, а canonical archive `sources-pack-core-20.tar.gz` остаётся полным steady-work snapshot.

Состав curated packs и параметры boundary-инструкций задаются декларативно в:

- `factory-template-ops-policy.yaml`
- `factory_template_only_pack/templates/factory-template-boundary-actions.template.md`

Короткие release-facing operator docs:

- `RELEASE_CHECKLIST.md`
- `VERIFY_SUMMARY.md`
- `RELEASE_NOTE_TEMPLATE.md`
- `COMMIT_MESSAGE_GUIDE.md`
- `docs/releases/sources-pack-usage.md`

Короткая карта поддерживаемых режимов:

- `ENTRY_MODES.md`

Примечание по git sync в этом окружении:

- `git commit`, `git push`, `git fetch` и смену `origin` выполняйте последовательно
- если обычный `git push origin main` ведет себя нестабильно, используйте прямой SSH push на `git@github.com:mppcoder/factory-template.git`
- если нужен canonical verified path, используйте `bash VERIFIED_SYNC.sh`
- если после уже пройденного green verify остался только low-risk follow-up вроде `.gitignore` или небольших docs/closeout правок, `bash VERIFIED_SYNC.sh` может сам перейти в lightweight follow-up mode и закоммитить их без отдельного ручного подтверждения
- если нужен release path после отдельного решения, используйте `bash EXECUTE_RELEASE_DECISION.sh`

Для нового automation contour доступны validators:

- `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
- `bash VALIDATE_RELEASE_DECISION.sh`
- `bash VALIDATE_RELEASE_NOTES_SOURCE.sh`
- `bash VALIDATE_RELEASE_REPORT.sh`

## Что входит в релиз
- `template-repo/` — шаблон нового рабочего проекта.
- `meta-template-project/` — контур развития самой фабрики.
- `working-project-examples/` — примеры greenfield и brownfield проектов.
- `workspace-packs/factory-ops/` — optional operational-слой для drift, patch export и hooks.
- `registry/` — журнал версий фабрики и происхождения проектов.

## Что не должно попадать в релиз
- тестовые рабочие проекты;
- временные каталоги smoke/matrix прогонов;
- логи и служебные следы локальной сборки.

## Что нового в релизе 2.4.2
- добавлен declarative direct Sources profile `core-hot-15` для ежедневной работы в ChatGPT Project;
- добавлен cold/reference remainder archive `core-cold-5` для hybrid-схемы без дублей;
- canonical archive `sources-pack-core-20` зафиксирован как steady-work snapshot;
- export, validation и boundary guidance теперь поддерживают hybrid-схему `direct hot-set + cold archive remainder + canonical archive`;
- release metadata и build output синхронизированы под имя `factory-v2.4.2`.

## Базовый функционал ветки 2.4.2
- введен обязательный defect-capture layer;
- добавлены process-файлы по обработке дефектов и DoD для bugfix/feature/change;
- добавлены шаблоны bug report, factory feedback и ChatGPT handoff для дефектов;
- в generated project появились `reports/bugs/`, `reports/factory-feedback/`, `tasks/chatgpt/`, `tasks/codex/`;
- Codex task pack теперь умеет включать обязательный bug-capture block;
- DoD учитывает defect flow.

## Известные ограничения
- quality-валидация остаётся эвристической, а не семантической;
- advisory/back-sync слой по-прежнему рассчитан на контролируемое применение, а не на безусловный sync всех зон;
- содержательное наполнение `user-spec`, `tech-spec`, `reality-check` требует сценарного слоя и участия пользователя.
- auto GitHub Release publication выполняется только при явном `release-decision.yaml` и доступном `gh auth`.


## Стандарт versioning/documentation layer

Во всех контурах используются одинаковые файлы:
- `VERSION.md`
- `CHANGELOG.md`
- `CURRENT_FUNCTIONAL_STATE.md`
- `.chatgpt/project-origin.md`

Это правило действует для фабрики, шаблона, greenfield-проектов и brownfield-проектов.
