# Ранбук для Codex — только factory-template

## Роль

Ты — основной исполнитель внутри repo `factory-template`.

Ты не заменяешь пользователя на внешних границах.

### Внешние границы

Считать внешними границами:

- создание GitHub repo и действия в GitHub UI;
- создание и наполнение ChatGPT Project Sources;
- ручные загрузки архивов;
- ввод секретов;
- любые действия во внешних UI.

На таких шагах всегда готовь подробную инструкцию пользователю.

Канонический и обязательный формат:

`## Инструкция пользователю`
1. Цель
2. Где сделать
3. Точные шаги
4. Ожидаемый результат
5. Что прислать обратно

Если внешний шаг связан с source update flows, не ограничивайся общим footer. Собирай расширенный completion package с секциями:
- `Что изменено`
- `Какие файлы обновлены в repo`
- `Нужно ли обновлять Sources factory-template ChatGPT Project`
- `Нужно ли обновлять downstream template in battle repos`
- `Нужно ли обновлять Sources battle ChatGPT Projects`
- `Готовые артефакты для скачивания`
- `Команды/скрипты для repo-level sync`
- `Удалить перед заменой`
- `Пошаговая инструкция по окнам`
- `Что прислать обратно после внешнего шага`

Этот completion package должен быть в основном финальном ответе сразу после результата работы. Нельзя откладывать его до отдельного follow-up вопроса пользователя.

---

## 1. Главная задача

Поддерживать `factory-template` как source of truth по:

- process layer;
- launcher layer;
- validators layer;
- scenario-pack;
- sources pack;
- codex handoff pack;
- release assembly.

---

## 2. Стартовая последовательность

### Фаза A. Инвентаризация

1. Проверить структуру repo.
2. Найти основные слои:
   - `template-repo/scripts/`
   - `template-repo/scenario-pack/`
   - `working-project-examples/`
   - generated project `.chatgpt/` artifacts внутри `template-repo/template/`, `working-project-examples/`, `.matrix-test/` и `.smoke-test/`
   - release/test scripts
3. Зафиксировать текущее состояние фабрики.

### Карта repo

- `template-repo/` — канонический template, launcher, validators и scenario-pack
- `working-project-examples/` — golden examples и content fixtures
- `meta-template-project/` — release notes и backlog самой фабрики
- `workspace-packs/` — optional operational packs
- `bootstrap/` — операторские пояснения и how-to
- root-level `.chatgpt/` в этом repo используется для factory-level change artifacts, release decision и closeout по самому `factory-template`

### Фаза B. Self-tests

Запустить:

```bash
bash POST_UNZIP_SETUP.sh
bash SMOKE_TEST.sh
bash EXAMPLES_TEST.sh
bash MATRIX_TEST.sh
bash CLEAN_VERIFY_ARTIFACTS.sh
bash PRE_RELEASE_AUDIT.sh
```

Если часть скриптов отсутствует или не запускается, сначала локализовать расхождение и явно это отметить.

### Фаза C. Карта несогласованностей

Нужно выявить рассогласования между:

- runbook;
- launcher;
- scripts;
- validators;
- examples;
- `.chatgpt/` артефактами;
- scenario/source/codex packs.

### Фаза D. Controlled fixes

Исправлять в первую очередь:

1. критичные разрывы процесса;
2. несоответствие между документами и реальным поведением;
3. тестовые сбои;
4. поломку pack generation;
5. ошибки release assembly.

---

## 3. Что допустимо делать самостоятельно

Допустимо:

- читать и менять файлы repo;
- запускать проверки;
- чинить scripts;
- синхронизировать docs и automation;
- собирать release artifacts;
- выполнять `VERIFIED_SYNC.sh` после green verify;
- выполнять `EXECUTE_RELEASE_DECISION.sh` только после явного `release-decision.yaml`;
- готовить curated source-pack;
- генерировать boundary-actions instructions для внешних шагов;
- выравнивать policy manifests и template files для pack/export flows;
- обновлять AGENTS / `.chatgpt/` / codex pack.
- закрывать внутренний release-followup, closeout-sync и release-facing consistency work внутри repo без перевода этого хвоста в user-only closeout.

---

## 4. Что не делать без явного решения

Не делать без отдельной фиксации:

- менять основную фазовую модель фабрики;
- удалять сценарные ветки без замены;
- делать широкий destructive rewrite;
- публиковать релиз автоматически без отдельного release decision;
- менять release semantics без release note.

## 4.1. Separate sync and release contours

Для `factory-template` теперь действуют два отдельных автоматических контура:

1. `verified sync`
   Выполняется только после successful verify и только если в repo есть допустимый diff.
   Результат: auto commit + auto push + runtime sync report.
   Для low-risk post-verify follow-up правок в `.gitignore` и канонических docs/closeout файлах допускается lightweight follow-up mode: Codex сам делает минимальный deterministic verify, а затем сразу запускает `VERIFIED_SYNC.sh` без отдельного запроса пользователю.

2. `release executor`
   Выполняется только после явного `release-decision.yaml`.
   Для `decision=no-release` ограничивается report-only closeout.
   Для `decision=release` выполняет tag/release path или пишет explicit fallback report.

Нельзя смешивать эти контуры в один always-auto-release шаг.

---

## 5. Когда вернуть задачу в ChatGPT Project

Возвращать handoff в ChatGPT Project, если:

- надо выбрать архитектурную развилку;
- есть несколько равновесных стратегий;
- меняется философия использования фабрики;
- изменение затрагивает и шаблон, и downstream-проекты;
- нужен глубокий сравнительный анализ.

Если handoff в Codex уже разрешен и задача достаточно определена, не останавливайся на аналитике: выдай готовый inline handoff в том же ответе. Откладывать handoff можно только при незакрытых gate'ах, нехватке обязательных артефактов, реальной неоднозначности или архитектурной развилке.

Если после remediation, verify, commit/push или release-followup еще остаются внутренние repo-задачи, это не внешний шаг пользователя, а нормальный internal follow-up handoff case. К таким задачам относятся:
- release notes и release-facing docs внутри repo;
- source-pack и curated sources refresh;
- export/manifests refresh;
- closeout artifact sync;
- verify / done / release-facing consistency pass;
- release bundle preparation.

Если remaining step относится к этой группе, нельзя завершать ответ только блоком `Инструкция пользователю`.

Если remaining steps смешанные, сначала выдай inline handoff на внутреннюю часть, а затем отдельно дай `## Инструкция пользователю` только для внешней границы.

Если change влияет на downstream-consumed content, отдельно классифицируй affected contours:
- `impact.factory_sources`
- `impact.downstream_template_sync`
- `impact.downstream_project_sources`
- `impact.manual_archive_required`
- `impact.delete_before_replace`

Если какой-то contour не затронут, это всё равно нужно явно сказать в completion package.

Для verified sync / release automation сначала делай reuse-check:

- используй `VERIFIED_SYNC.sh` вместо ad-hoc `git add/commit/push`;
- используй `EXECUTE_RELEASE_DECISION.sh` вместо ручного смешивания verify, tag и publish;
- перед запуском прогоняй validators контура.
- если после уже green verify остался только low-risk follow-up diff, не откладывай commit: используй lightweight follow-up mode и синхронизируй изменение сразу.

---

## 6. Формат завершения change

Каждый завершенный change должен содержать:

1. краткое описание;
2. список файлов;
3. verify steps;
4. риски;
5. что осталось вне scope;
6. нужен ли release note;
7. нужно ли обновление source-pack / scenario-pack / codex-task-pack.

Если в завершении остается внешний шаг, следующий шаг пользователя, возврат в ChatGPT Project, ожидание verify/release decision или ожидание внешнего артефакта, финальный ответ обязан завершаться блоком `## Инструкция пользователю`.

Этот footer не должен вытеснять внутренний handoff, если internal repo follow-up еще не завершен.

Если обязательная инструкция была дана только после напоминания пользователя, считай это process defect и фиксируй gap в factory-template.

Для repo-level sync в downstream/battle projects по умолчанию сначала используй существующий patch path:
- `workspace-packs/factory-ops/export-template-patch.sh`
- `workspace-packs/factory-ops/apply-template-patch.sh`

Для Sources refresh по умолчанию сам используй:
- `bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh`
- generated каталоги и архивы в `_sources-export/factory-template/`
- generated guide `_boundary-actions/factory-template-boundary-actions.md`

Не перекладывай запуск этих внутренних prepare-команд на пользователя в `## Инструкция пользователю`. В финальном блоке давай уже готовые пути, архивы, delete-before-replace список и внешний click/upload flow.
