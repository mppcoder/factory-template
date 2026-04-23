# Ранбук для пользователя — только factory-template

## 0. Цель

Этот ранбук описывает работу **только с проектом шаблона фабрики проектов**.

Единая визуальная архитектура шаблона и сводные workflows по ключевым событиям собраны в:

- `docs/template-architecture-and-event-workflows.md`

Цель проекта:

- развивать сам шаблон;
- исправлять баги фабрики;
- улучшать launcher / validators / scenario-pack / export/reference packs / codex handoff;
- собирать новые релизные версии фабрики.

## 0.1. Три канонических режима шаблона

Шаблон должен явно поддерживать:

1. новый проект с нуля;
2. перевод на шаблон имеющегося проекта без репо;
3. перевод на шаблон имеющегося проекта с репо.

Текущее соответствие в фабрике:

- новый проект с нуля → `greenfield` + типовой профиль `greenfield-product`
- имеющийся проект без репо → `brownfield` + типовой профиль `brownfield-without-repo`
- имеющийся проект с репо → `brownfield` + типовые профили `brownfield-with-repo-modernization`, `brownfield-with-repo-integration`, `brownfield-with-repo-audit`

Важно:

- для generated projects repo-first контур остается единым
- не нужно поддерживать разные проектные инструкции под каждый entry mode
- различие задается через entry path, preset и сценарный маршрут

## 0.2. Первый запуск для новичка (wizard-first)

Для первого проекта используйте wizard, а не ручной ввод preset-терминов:

```bash
python3 template-repo/scripts/first-project-wizard.py
```

Wizard в понятной форме:
- спрашивает, что у вас уже есть;
- спрашивает, что вы хотите запустить;
- показывает, что система сделает дальше;
- сам выбирает нужный preset и запускает preflight VPS-проверку.

Отдельный документ для первого прохода:
- `docs/first-project.md`

---

## 1. Целевой контур

На VPS используется один основной каталог:

```text
/projects/factory-template/
```

Корень `/projects` должен содержать только project roots. Для `factory-template` канонический вид такой:

```text
/projects/
└── factory-template/
    ├── _incoming/
    ├── template-repo/
    ├── factory_template_only_pack/
    └── ...
```

`_incoming` — это подпапка проекта, а не соседний верхнеуровневый каталог.
В `/projects` нельзя держать `_release`, `_artifacts`, temporary repo, intermediate repo или reconstructed repo как отдельные соседние папки.
Source of truth для проекта — только `factory-template`.

---

## 2. Что делаете вы

Вы делаете только внешние действия:

1. создаете и поддерживаете GitHub-репозиторий шаблона;
2. создаете ChatGPT Project шаблона;
3. поддерживаете короткую repo-first инструкцию в ChatGPT Project;
4. загружаете архивы/входящие материалы в `_incoming`;
5. подтверждаете risky-внешние действия;
6. принимаете release/no-release решение.

После successful verify verified sync теперь может выполняться автоматически: commit/push делаются без отдельного ручного GitHub UI шага, если verify green и в repo есть diff.
Если основной verify уже green, а потом остался только low-risk follow-up вроде `.gitignore` или небольшого closeout/docs cleanup, фабрика может использовать lightweight follow-up verify path и тоже выполнить auto commit/push без отдельного ручного подтверждения.

---

## 3. Что делает Codex

Codex делает внутреннюю работу по шаблону:

1. распаковка/инициализация;
2. self-tests;
3. анализ багов фабрики;
4. реализация улучшений;
5. обновление scenario-pack / export/reference packs / codex-task-pack;
6. smoke / audit / matrix / examples;
7. подготовка release bundle;
8. формирование для вас инструкций на внешние действия.

К этой внутренней работе также относятся release-facing и closeout follow-up внутри repo:
- release notes и changelog;
- export/reference packs refresh;
- export / manifests refresh;
- closeout artifacts;
- verify / done / release-facing consistency pass.

Пользовательские инструкции нужны только на внешних границах, а не вместо такого внутреннего follow-up.

Выбор модели/режима теперь нужно проверять только на новой задаче и новом запуске Codex.
Не рассчитывайте, что старая уже открытая сессия сама переключит profile по типу следующей задачи.

ChatGPT Project для `factory-template` не должен хранить сценарии как основной источник правды.
Внутри проекта должна лежать только короткая инструкция: сначала открыть GitHub repo `mppcoder/factory-template`, затем `template-repo/scenario-pack/00-master-router.md`, затем идти по маршруту из него.

Формат таких инструкций канонический и обязательный:

`## Инструкция пользователю`
1. Цель
2. Где сделать
3. Точные шаги
4. Ожидаемый результат
5. Что прислать обратно

Если change затрагивает runbook layer, scenario-pack, launcher, validators, codex-task-pack или другой downstream-consumed template content, инструкции должны быть расширены до completion package для трёх контуров:
- обновление repo-first инструкции проекта шаблона в ChatGPT;
- обновление шаблона в downstream/battle repo;
- обновление repo-first инструкции downstream/battle ChatGPT Projects.

Для manual replacement обязательно должны быть перечислены:
- что удалить перед заменой;
- что загрузить вместо этого;
- какой архив или каталог уже готов для скачивания/загрузки.

Если для этих внешних шагов нужны exports, generated archives, boundary-actions guide или patch bundle, Codex должен подготовить их заранее сам внутри repo. Пользователь не должен запускать внутренние repo-команды только для того, чтобы собрать артефакт, который фабрика умеет собрать автоматически.

Важно:
- для `factory-template` и для downstream repo-first Projects обновление `Sources` не требуется по умолчанию;
- curated packs и `hot15` остаются только compatibility/reference слоем;
- использовать их нужно только там, где legacy/hybrid contour ещё сознательно сохранён как fallback.

Нельзя считать ChatGPT Project источником сценариев. Источник правды всегда находится в repo.

---

## 4. Порядок запуска

## Шаг 1. Подготовить внешние сущности

Создайте:

- GitHub repo `factory-template`
- ChatGPT Project `Factory Template`

## Шаг 2. Настроить поле Instructions в ChatGPT Project

Этот шаг нужен, чтобы ChatGPT Project сразу работал в repo-first режиме и не воспринимал сценарии внутри Project как основной источник правды.
Выполните его до первого рабочего запроса, bootstrap-запуска или сценарного прохода через ChatGPT Project.

В поле `Instructions` вставьте канонический текст:

```text
Работаем по проекту factory-template.

В этом ChatGPT Project сценарии не хранятся.
На каждый запрос сначала иди в GitHub repo `mppcoder/factory-template`.

Первое обязательное действие на каждый запрос:
1. открыть главный сценарий `template-repo/scenario-pack/00-master-router.md`;
2. прочитать его;
3. действовать строго по нему;
4. если главный сценарий направляет в другие сценарии, читать и исполнять уже их;
5. только после этого формировать ответ.

Запрещено:
- отвечать до чтения главного сценария;
- пересказывать сценарии из памяти вместо чтения repo;
- описывать сценарии внутри ChatGPT Project;
- придумывать свой workflow, если маршрут уже задан в `00-master-router.md`.

Главное правило:
сначала GitHub repo `mppcoder/factory-template`,
потом `template-repo/scenario-pack/00-master-router.md`,
потом выполнение маршрута из него,
и только потом ответ.
```

После этого для каждой новой задачи используйте launcher/profile flow и проверяйте routing по `.chatgpt/task-launch.yaml`.

Проверьте после сохранения:

- в `Instructions` явно указан repo `mppcoder/factory-template`;
- первым обязательным чтением указан `template-repo/scenario-pack/00-master-router.md`;
- в проекте не осталось старого текста про `Sources`, staging-first поток или хранение сценариев внутри ChatGPT Project.

## Шаг 3. Подготовить VPS

```bash
mkdir -p /projects/factory-template/_incoming
```

Если каталог проекта ещё не создан, сначала создайте `/projects/factory-template`.

Загрузите в `/projects/factory-template/_incoming` архив фабрики и дополнительные входящие артефакты.

После распаковки и первого `bash POST_UNZIP_SETUP.sh` дополнительных действий по внешнему staging-контуру больше не требуется.

После распаковки можно запустить preflight-проверку:

```bash
cd /projects/factory-template
python3 template-repo/scripts/preflight-vps-check.py --project-slug my-first-project
```

Если вы создаете первый рабочий проект из шаблона, используйте wizard-first вход:

```bash
python3 template-repo/scripts/first-project-wizard.py
```

## Шаг 4. Открыть VS Code по SSH

Откройте в VS Code именно папку:

```text
/projects/factory-template
```

Если репо еще не распаковано — сначала откройте `/projects/factory-template/_incoming`, дайте Codex распаковать материалы внутрь `/projects/factory-template`, затем переключитесь на `/projects/factory-template`.

## Шаг 5. Стартовый промпт для Codex

```text
Работаем только по проекту шаблона фабрики проектов.
Твоя зона ответственности — сам repo factory-template.
Не выходи за внешние границы: GitHub, ChatGPT Project UI, ручные загрузки, секреты, внешние UI.
Во всех таких местах готовь для меня точные пошаговые инструкции.
Сначала:
1. проверь структуру repo,
2. прогони self-tests,
3. зафиксируй текущее состояние,
4. найди несогласованности между runbook, scripts, examples, validators и scenario-pack,
5. подготовь план controlled fixes.
```

---

## 5. Основной цикл работы

Рабочий цикл всегда один:

```text
внешний сигнал → ChatGPT Project → решение/спецификация → Codex-исполнение → verify → verified sync → release/no-release
```

Где:

- `verified sync` = auto commit + auto push только после green verify;
- `release/no-release` = отдельное явное решение;
- auto release path включается только после `release=yes`.

### Типовые внешние сигналы

- найден баг фабрики;
- надо улучшить launcher;
- надо обновить validators;
- надо собрать новый source-pack;
- надо изменить архитектуру фабрики;
- надо подготовить новый релиз;
- надо сравнить поведение шаблона с боевыми reference/production проектами.

---

## 6. Что сначала отдавать в ChatGPT Project

Сначала в ChatGPT Project:

- спорные архитектурные решения;
- изменение философии фабрики;
- новые сценарные ветки;
- release strategy;
- сравнение нескольких вариантов устройства шаблона;
- анализ, что надо вынести из реальных проектных контуров обратно в фабрику.

## 7. Что сразу отдавать в Codex

Сразу в Codex:

- правка markdown и yaml/json/toml/sh;
- обновление launcher/validators;
- приведение структуры в порядок;
- синхронизация `template-repo/scenario-pack/`, `template-repo/scripts/`, `working-project-examples/` и generated project artifacts;
- self-tests и локальные проверки;
- сбор release bundle;
- подготовка curated sources pack;
- генерация boundary-инструкций на GitHub / ChatGPT Project / uploads.

Для каждой новой задачи:
- не продолжайте старую уже открытую сессию Codex как будто она сама поменяет модель/режим;
- запускайте новую задачу через подготовленный launcher/profile flow;
- проверяйте routing по `.chatgpt/task-launch.yaml`, а не по догадке о текущей сессии.

---

## 8. Жесткие правила

1. Не открывать один Codex-сеанс на весь `/projects`.
2. Не смешивать входящие архивы и сам repo.
3. Не публиковать релиз без локального verify-пакета.
4. Не менять одновременно сценарную логику и validators без повторного полного прогона self-tests.
5. Любое изменение фабрики, влияющее на downstream-проекты, должно иметь release note.
6. После `SMOKE_TEST.sh` / `EXAMPLES_TEST.sh` / `MATRIX_TEST.sh` перед `PRE_RELEASE_AUDIT.sh` запускать `bash CLEAN_VERIFY_ARTIFACTS.sh`.
7. Перед `git`/GitHub-фиксацией сверяться с `VERIFY_SUMMARY.md` и `RELEASE_CHECKLIST.md`.
8. Для любого release/no-release решения использовать `RELEASE_NOTE_TEMPLATE.md` как базовый шаблон релизной заметки.
9. Git-зависимые шаги (`commit`, `push`, `fetch`, смена `origin`) выполнять последовательно, не параллелить.
10. Если `git push origin main` ведет себя нестабильно, использовать прямой SSH push на `git@github.com:mppcoder/factory-template.git`.
11. Если verify failed, не запускать `VERIFIED_SYNC.sh` и `EXECUTE_RELEASE_DECISION.sh`.
12. Если release decision = `no-release`, не создавать tag и не публиковать GitHub Release.

---

## 9. Критерий успеха

Схема считается внедренной, если:

1. Codex самостоятельно ведет внутреннюю работу по `factory-template`;
2. вы не сопровождаете вручную каждую команду терминала;
3. ChatGPT Project используется как сценарный и исследовательский слой;
4. repo-first инструкция уже внесена в поле `Instructions` ChatGPT Project и указывает на `mppcoder/factory-template` и `template-repo/scenario-pack/00-master-router.md`;
5. все внешние действия сведены к коротким инструкциям;
6. новый релиз фабрики собирается воспроизводимо.

Если Codex, ChatGPT Project или boundary-step заканчиваются ожиданием вашего действия, ответ без финального блока `Инструкция пользователю` считается неполным.

---

## 10. Минимальная operator-панель и deploy path

Для сценария, где нужен максимально простой и безопасный deploy на одном VPS, используйте новый минимальный контур:

1. Понять текущее состояние:

```bash
python3 template-repo/scripts/operator-dashboard.py
```

2. Запустить безопасный dry-run:

```bash
bash template-repo/scripts/deploy-dry-run.sh
```

3. Запустить one-button-ish deploy (dry-run внутри обязателен и запускается автоматически):

```bash
bash template-repo/scripts/deploy-local-vps.sh --yes
```

4. Проверить краткий verify summary:

```bash
python3 template-repo/scripts/operator-dashboard.py --verify-summary
```

Подробные инструкции:
- `docs/operator-next-step.md`
- `docs/deploy-on-vps.md`
