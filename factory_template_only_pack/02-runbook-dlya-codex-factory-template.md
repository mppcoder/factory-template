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
- root-level `.chatgpt/` в этом repo не является обязательным слоем

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
- готовить curated source-pack;
- генерировать boundary-actions instructions для внешних шагов;
- выравнивать policy manifests и template files для pack/export flows;
- обновлять AGENTS / `.chatgpt/` / codex pack.

---

## 4. Что не делать без явного решения

Не делать без отдельной фиксации:

- менять основную фазовую модель фабрики;
- удалять сценарные ветки без замены;
- делать широкий destructive rewrite;
- публиковать релиз автоматически;
- менять release semantics без release note.

---

## 5. Когда вернуть задачу в ChatGPT Project

Возвращать handoff в ChatGPT Project, если:

- надо выбрать архитектурную развилку;
- есть несколько равновесных стратегий;
- меняется философия использования фабрики;
- изменение затрагивает и шаблон, и downstream-проекты;
- нужен глубокий сравнительный анализ.

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
