# Русское ядро фабрики проектов v2.4.0

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
cd factory-v2.4.0
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

Состав curated packs и параметры boundary-инструкций задаются декларативно в:

- `factory-template-ops-policy.yaml`
- `factory_template_only_pack/templates/factory-template-boundary-actions.template.md`

Короткие release-facing operator docs:

- `RELEASE_CHECKLIST.md`
- `VERIFY_SUMMARY.md`
- `RELEASE_NOTE_TEMPLATE.md`
- `COMMIT_MESSAGE_GUIDE.md`

Короткая карта поддерживаемых режимов:

- `ENTRY_MODES.md`

Примечание по git sync в этом окружении:

- `git commit`, `git push`, `git fetch` и смену `origin` выполняйте последовательно
- если обычный `git push origin main` ведет себя нестабильно, используйте прямой SSH push на `git@github.com:mppcoder/factory-template.git`

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

## Что нового в финальной версии 2.4.0
- финальный пакет собран на базе подтвержденного `rc2-smokefix` кандидата;
- `SMOKE_TEST.sh`, `EXAMPLES_TEST.sh` и `MATRIX_TEST.sh` подтверждены на чисто распакованном архиве;
- release metadata и build output синхронизированы под финальное имя `factory-v2.4.0`;
- стабилизационный smoke-fix и version alignment вошли в основной релиз.

## Базовый функционал ветки 2.4.0
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


## Стандарт versioning/documentation layer

Во всех контурах используются одинаковые файлы:
- `VERSION.md`
- `CHANGELOG.md`
- `CURRENT_FUNCTIONAL_STATE.md`
- `.chatgpt/project-origin.md`

Это правило действует для фабрики, шаблона, greenfield-проектов и brownfield-проектов.
