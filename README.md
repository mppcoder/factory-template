# Русское ядро фабрики проектов v2.4.4

Это стабилизационный релиз фабрики проектов для связки:

- **ChatGPT Project** — сценарии, интервью, анализ, нормализация.
- **Codex** — исполнение по подготовленному handoff.
- **Repo** — единственный источник правды по документам и изменениям.

## Canonical Entry Modes

Шаблон сейчас поддерживает 3 канонических режима запуска и сопровождения:

1. Новый проект с нуля
   Основа: `greenfield` путь для нового продукта или сервиса.
   Типовой вход: `greenfield-product`.

2. Перевод на шаблон имеющегося проекта без репо
   Основа: `brownfield` путь для live-системы, где нет нормализованного исходного repo и сначала нужен evidence-first контур.
   Типовой вход: `brownfield-without-repo`.

3. Перевод на шаблон имеющегося проекта с репо
   Основа: `brownfield` путь для уже существующего репозитория или инженерного контура.
   Типовые входы: `brownfield-with-repo-modernization`, `brownfield-with-repo-integration`, `brownfield-with-repo-audit`.

Во всех трех случаях для generated project используется один и тот же базовый repo-first контур:

- прямое чтение `scenario-pack` из GitHub repo

Различается не набор загружаемых файлов, а стартовый маршрут по сценариям и выбранный preset.

## Canonical VPS Layout

Для VPS действует безусловное правило верхнего уровня:

- `/projects` содержит только project roots;
- каждый проект живёт в `/projects/<project-root>/`;
- `_incoming` допускается только как подпапка проекта: `/projects/<project-root>/_incoming/`;
- temporary, intermediate и reconstructed repos допускаются только внутри соответствующего project root.

Запрещена плоская раскладка вспомогательных repo и служебных каталогов прямо в `/projects`.

Канонический release-facing reference по архитектуре, дереву проекта и workflow собран в:

- `docs/template-architecture-and-event-workflows.md`
- `RELEASE_NOTES.md`

## Подготовка после распаковки

```bash
cd factory-v2.4.4
bash POST_UNZIP_SETUP.sh
bash MATRIX_TEST.sh
bash CLEAN_VERIFY_ARTIFACTS.sh
```

`POST_UNZIP_SETUP.sh` теперь только обновляет execute-биты.
Generated projects больше не зависят от внешнего staging-контура для сценариев.

Если после self-tests нужен `PRE_RELEASE_AUDIT.sh` или сборка релиза, сначала очистите временные артефакты:

```bash
bash CLEAN_VERIFY_ARTIFACTS.sh
bash PRE_RELEASE_AUDIT.sh
```

Для работы с внешними границами без ручной сборки файлов:

```bash
bash GENERATE_BOUNDARY_ACTIONS.sh
bash VALIDATE_FACTORY_FEEDBACK.sh <working-project>
bash INGEST_FACTORY_FEEDBACK.sh <working-project> --dry-run
bash TRIAGE_INCOMING_LEARNINGS.sh --dry-run
```

`INGEST_FACTORY_FEEDBACK.sh` сначала прогоняет `VALIDATE_FACTORY_FEEDBACK.sh` и останавливает ingest на пустом или шаблонном `meta-feedback`, если не передан `--allow-incomplete`.

Для handoff в Codex:

```bash
python3 template-repo/scripts/create-codex-task-pack.py <working-project>
python3 template-repo/scripts/validate-codex-task-pack.py <working-project>
```

`validate-codex-task-pack.py` проверяет, что `codex-context.md`, `codex-task-pack.md`, `boundary-actions.md`, `done-checklist.md`, `task-launch.yaml` и `normalized-codex-handoff.md` не только созданы, но и согласованы с `active-scenarios.yaml`.
При формировании handoff в Codex явно фиксируйте, что приоритет у правил репозитория: `AGENTS`, runbook, scenario-pack и policy files repo.
Пользователю handoff выдаётся только одним цельным блоком для copy-paste в Codex, а не ссылкой на файл и не несколькими разрозненными блоками.
`template-repo/scripts/validate-handoff-response-format.py` дополнительно валидирует уже готовый markdown-ответ handoff и ловит file-based / multi-block handoff как process defect.

Для реального task-based routing используйте новый launch boundary.
Если вы уже находитесь внутри working project, запускайте:

```bash
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --dry-run
./scripts/launch-codex-task.sh --launch-source direct-task --task-text "проведи root-cause analysis ..." --dry-run
```

Если вы проверяете generated project из корня `factory-template`, используйте явный вызов script layer на целевом проекте:

```bash
python3 template-repo/scripts/bootstrap-codex-task.py <working-project> --launch-source direct-task --task-text "проведи root-cause analysis ..."
python3 template-repo/scripts/validate-codex-routing.py <working-project>
```

Проверка routing должна делаться только на новой задаче.
Нельзя считать старую уже открытую сессию Codex надежной единицей автоматической маршрутизации.

`VALIDATE_FACTORY_TEMPLATE_OPS.sh` теперь проверяет не только структуру `sources-pack-*`, но и semantic profile repo-артефактов, если они используются как reference/export layer:

- `sources-pack-core-20` обязан содержать сценарное ядро, runbook layer и policy presets;
- `core-hot-15` обязан содержать ровно 15 hot-файлов reference-профиля;
- `core-hot-15` и companion archive остаются repo-side export-профилями, а не обязательным daily UI upload flow;
- `core-cold-5` обязан содержать ровно 5 cold/reference файлов без дублей hot-set;
- `sources-pack-release-20` обязан содержать release-facing docs и release scripts;
- `sources-pack-bugfix-20` обязан содержать launcher, validator layer и feedback/handoff validators.

## Repo-First ChatGPT Project Rule

Для проектов ChatGPT теперь каноничен repo-first режим:

- сценарии не хранятся внутри ChatGPT Project как основной источник правды;
- на каждый запрос сначала открывается GitHub repo проекта;
- первое обязательное действие: открыть `template-repo/scenario-pack/00-master-router.md`, прочитать его и действовать строго по маршруту;
- если router ведёт в другие сценарии, читать уже их и только потом отвечать.

Для `factory-template` canonical repo:

- `mppcoder/factory-template`

Во время первичной настройки ChatGPT Project это правило нужно внести именно в поле `Instructions` до первого рабочего запроса.
В `Instructions` должен быть явно указан repo `mppcoder/factory-template`, обязательное чтение `template-repo/scenario-pack/00-master-router.md` и запрет на сценарии "из памяти" или из текста внутри Project.

Риски этого контура:

- если в ChatGPT Project останется старый текст про `Sources` или старый staging-workflow, агент может пойти по неверному workflow;
- если repo-first инструкция не обновлена после смены repo/path, модель может читать не тот репозиторий;
- нельзя заменять чтение `00-master-router.md` пересказом по памяти.

## AGENTS Canonical Sync Scheme

- root [AGENTS.md](/projects/factory-template/AGENTS.md) — persistent instruction для работы внутри самого `factory-template`;
- [template-repo/AGENTS.md](/projects/factory-template/template-repo/AGENTS.md) — canonical template source для downstream/battle repos;
- root `AGENTS.md` в боевом repo — materialized clone из `template-repo/AGENTS.md`, а не самостоятельный source of truth.

Для downstream repo разрешено менять только значение `SCENARIO_PACK_PATH`, если repo-local путь к scenario-pack отличается.

Канонический sync path для этого контура:

1. launcher создаёт initial root `AGENTS.md` через `template-repo/scripts/sync-agents.py`;
2. downstream refresh использует `workspace-packs/factory-ops/export-template-patch.sh`;
3. `workspace-packs/factory-ops/apply-template-patch.sh --apply-safe-zones` materializes generated root `AGENTS.md` в боевом repo;
4. `workspace-packs/factory-ops/check-template-drift.py` ловит отсутствие root clone и drift относительно `template-repo/AGENTS.md`.

Это не "магическое" обновление GitHub само по себе: sync происходит только как часть канонического template-sync/update flow внутри repo/tooling.

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

Эта рекомендация автоматически попадает в `_sources-export/factory-template/SUMMARY.md` и `_boundary-actions/factory-template-boundary-actions.md`, но для ежедневной работы ChatGPT Project должен опираться на GitHub repo, а не на отдельный Drive/Sources sync-контур.
Перезаливка `Sources` не является обязательным release-step и допускается только как compatibility fallback для проектов, которые ещё не переведены на чистый repo-first режим.

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
- `docs/template-architecture-and-event-workflows.md`

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

## Что нового в релизе 2.4.4
- canonical core-иерархия очищена от продуктовых/исторических имен в release-facing слоях;
- presets, workspace packs и example/reference contours переведены на универсальные factory names;
- `openclaw` вынесен из core-дерева в `optional-domain-packs/openclaw-reference`;
- launcher и preset application теперь принимают legacy preset names только как compatibility aliases;
- release docs, manifests, template metadata и examples синхронизированы под `factory-v2.4.4`.

## Базовый функционал ветки 2.4.4
- `factory-template` поддерживает greenfield, brownfield без repo и brownfield с repo в одном repo-first контуре;
- advisory/policy layer и executable routing layer остаются явным образом разделены;
- defect-capture, handoff, self-handoff, verification, release-followup и completion package описаны как обязательные контуры;
- generated projects продолжают получать единый template/versioning/documentation layer;
- release-facing docs и packaging layer теперь описывают не только инструменты, но и полный жизненный цикл выпуска релиза.

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
