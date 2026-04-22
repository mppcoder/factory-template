# Визуальная архитектура шаблона и event workflows

Этот документ собирает в одном месте две вещи:

1. визуальную архитектуру `factory-template`;
2. подробные workflow по ключевым событиям, которые инициируют запуск, развёртывание или доработку.

Он не заменяет `scenario-pack`, а помогает быстро увидеть карту контуров до погружения в конкретный сценарий.

## 1. Визуальная архитектура шаблона

### 1.1. Контуры системы

```text
                    ┌──────────────────────────────┐
                    │ ChatGPT Project              │
                    │ repo-first analysis layer    │
                    │ - classification             │
                    │ - scenario routing           │
                    │ - handoff preparation        │
                    └──────────────┬───────────────┘
                                   │
                                   │ handoff / repo-first guidance
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ factory-template repo                                                       │
│                                                                              │
│  README / runbooks / bootstrap / docs      -> operator & policy layer       │
│  template-repo/scenario-pack/              -> scenario routing layer         │
│  template-repo/project-presets.yaml        -> project presets                │
│  template-repo/policy-presets.yaml         -> policy presets                 │
│  template-repo/change-classes.yaml         -> change-class contract          │
│  template-repo/launcher.sh                 -> project generation entrypoint  │
│  template-repo/template/                   -> generated project scaffold      │
│  template-repo/scripts/                    -> validators / launcher scripts  │
│  template-repo/codex-routing.yaml          -> executable routing contract    │
│  working-project-examples/                 -> compatibility fixtures         │
│  reports/bugs + reports/factory-feedback/  -> defect/remediation memory      │
└──────────────────────────────┬───────────────────────────────────────────────┘
                               │
                               │ launcher copies template + scripts + presets
                               ▼
                   ┌──────────────────────────────┐
                   │ Generated project            │
                   │ - .chatgpt artifacts         │
                   │ - .codex profiles            │
                   │ - greenfield/brownfield docs │
                   │ - reports/tasks              │
                   └──────────────┬───────────────┘
                                  │
                                  │ new task launch
                                  ▼
                     ┌────────────────────────────┐
                     │ Codex executable layer     │
                     │ - launch-codex-task.sh     │
                     │ - bootstrap-codex-task.py  │
                     │ - resolve route            │
                     │ - --profile quick/build/...│
                     └────────────────────────────┘
```

### 1.2. Разделение advisory и executable слоёв

```text
advisory / policy layer
  AGENTS / runbooks / scenario-pack / ChatGPT Project instructions / .chatgpt guidance
  -> объясняет, как нужно работать
  -> не переключает model/profile/runtime сам по себе

executable routing layer
  .codex/config.toml named profiles
  codex-routing.yaml
  bootstrap-codex-task.py
  resolve-codex-task-route.py
  launch-codex-task.sh
  -> выбирает task class и profile на границе новой задачи
  -> фиксирует реальный launch в task-launch.yaml
```

### 1.3. Жизненный цикл шаблона

```text
template improvement inside factory-template
    -> scenario / docs / launcher / validators / template changes
    -> self-tests and verification
    -> commit/push
    -> downstream template sync
    -> battle repo update
    -> battle ChatGPT Project instruction refresh
```

## 2. Workflow событий

### 2.1. Развертывание проекта самого шаблона

Событие:
- новый операторский запуск `factory-template` как рабочего repo шаблона;
- новая среда;
- новая машина/VPS;
- проверка релизного архива или свежего clone.

Подробный workflow:

1. Получить repo или архив `factory-template`.
2. Открыть root repo и подтвердить canonical entry files:
   - `README.md`
   - `ENTRY_MODES.md`
   - `template-repo/scenario-pack/00-master-router.md`
3. Выполнить базовую подготовку:
   - `bash POST_UNZIP_SETUP.sh`
   - `bash MATRIX_TEST.sh`
   - `bash CLEAN_VERIFY_ARTIFACTS.sh`
4. Создать или открыть ChatGPT Project шаблона и внести repo-first instruction.
5. Открыть `/projects/factory-template` в VS Code / SSH.
6. Передать Codex стартовую задачу на self-tests, repo audit и controlled fixes.
7. При найденном defect сначала зафиксировать bug report/factory feedback.
8. После green verify использовать verified sync или отдельный release path.

Где это описано сейчас:
- [README.md](/projects/factory-template/README.md:31)
- [factory_template_only_pack/01-runbook-dlya-polzovatelya-factory-template.md](/projects/factory-template/factory_template_only_pack/01-runbook-dlya-polzovatelya-factory-template.md:125)

Ограничение:
- до этого документа workflow был описан текстом, но без единой визуальной схемы контура.

### 2.2. Развертывание шаблона как нового greenfield-проекта

Событие:
- нужно создать новый проект с нуля на шаблоне.

Подробный workflow:

1. Запустить `template-repo/launcher.sh`.
2. Выбрать:
   - `project preset = product-dev`
   - `mode = greenfield`
   - change class и execution mode
3. Launcher создаёт working project и копирует:
   - template scaffold
   - `.chatgpt`
   - `.codex`
   - `scenario-pack`
   - scripts/presets/contracts
4. В новом project repo создать или открыть ChatGPT Project.
5. В `Instructions` внести repo-first правило:
   - сначала GitHub repo проекта
   - затем `template-repo/scenario-pack/00-master-router.md`
6. На каждый новый запрос ChatGPT Project сначала проходит `00-master-router.md`.
7. Для greenfield маршрута перейти в `04-discovery-new-project.md`.
8. Собрать:
   - problem statement
   - vision
   - scope v1
   - architecture options
9. После закрытия gate’ов сформировать handoff в Codex.
10. Для каждой новой Codex-задачи запускать task router через named profiles.

Где это описано сейчас:
- [ENTRY_MODES.md](/projects/factory-template/ENTRY_MODES.md:23)
- [template-repo/README.md](/projects/factory-template/template-repo/README.md:5)
- [bootstrap/02-как-создать-working-project.md](/projects/factory-template/bootstrap/02-%D0%BA%D0%B0%D0%BA-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-working-project.md:1)
- [template-repo/scenario-pack/04-discovery-new-project.md](/projects/factory-template/template-repo/scenario-pack/04-discovery-new-project.md:1)

### 2.3. Развертывание шаблона как нового brownfield-проекта без repo

Событие:
- есть существующая система, но нет нормализованного рабочего repo.

Подробный workflow:

1. Запустить `template-repo/launcher.sh`.
2. Выбрать:
   - `project preset = brownfield-dogfood-codex-assisted`
   - `mode = brownfield`
3. Создать working project и baseline artifacts.
4. Настроить repo-first ChatGPT Project для нового проекта.
5. На каждый запрос сначала проходить `00-master-router.md`.
6. Затем входить в `brownfield/00-brownfield-entry.md`.
7. Зафиксировать evidence-first режим:
   - не притворяться, что repo уже существует;
   - сначала собрать реальность системы.
8. Построить brownfield ядро:
   - `system-inventory.md`
   - `repo-audit.md` или явная фиксация отсутствия repo
   - `as-is-architecture.md`
   - `gap-register.md`
   - `reverse-engineering-summary.md`
9. Любой найденный gap переводить в defect/bug report до remediation.
10. После stabilisation и закрытия gate’ов формировать handoff в Codex.

Где это описано сейчас:
- [ENTRY_MODES.md](/projects/factory-template/ENTRY_MODES.md:32)
- [template-repo/README.md](/projects/factory-template/template-repo/README.md:12)
- [template-repo/scenario-pack/brownfield/00-brownfield-entry.md](/projects/factory-template/template-repo/scenario-pack/brownfield/00-brownfield-entry.md:1)
- [bootstrap/06-как-вести-brownfield-проект.md](/projects/factory-template/bootstrap/06-%D0%BA%D0%B0%D0%BA-%D0%B2%D0%B5%D1%81%D1%82%D0%B8-brownfield-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82.md:1)
- [bootstrap/13-как-проверять-результат-и-заполнять-brownfield-ядро.md](/projects/factory-template/bootstrap/13-%D0%BA%D0%B0%D0%BA-%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D1%8F%D1%82%D1%8C-%D1%80%D0%B5%D0%B7%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1%82-%D0%B8-%D0%B7%D0%B0%D0%BF%D0%BE%D0%BB%D0%BD%D1%8F%D1%82%D1%8C-brownfield-%D1%8F%D0%B4%D1%80%D0%BE.md:1)

### 2.4. Развертывание шаблона как нового brownfield-проекта с repo

Событие:
- есть существующий репозиторий, который нужно перевести на фабричный контур.

Подробный workflow:

1. Запустить `template-repo/launcher.sh`.
2. Выбрать один из preset’ов:
   - `legacy-modernization`
   - `integration-project`
   - `audit-only`
3. Создать working project baseline.
4. Настроить repo-first ChatGPT Project для целевого проекта.
5. На каждый запрос проходить `00-master-router.md`.
6. Затем пройти:
   - `brownfield/00-brownfield-entry.md`
   - `brownfield/01-system-inventory.md`
   - `brownfield/02-repo-audit.md`
7. Зафиксировать архитектуру “как есть” и карту изменений:
   - `brownfield/as-is-architecture.md`
   - `brownfield/change-map.md`
   - `brownfield/gap-register.md`
8. Любой gap/дефект оформить до remediation planning.
9. Если задача дошла до remediation, handoff в Codex должен идти уже по нормализованным полям.
10. Новые Codex-задачи запускать только через launcher/router boundary.

Где это описано сейчас:
- [ENTRY_MODES.md](/projects/factory-template/ENTRY_MODES.md:43)
- [template-repo/README.md](/projects/factory-template/template-repo/README.md:15)
- [template-repo/scenario-pack/brownfield/00-brownfield-entry.md](/projects/factory-template/template-repo/scenario-pack/brownfield/00-brownfield-entry.md:1)
- [template-repo/scenario-pack/brownfield/01-system-inventory.md](/projects/factory-template/template-repo/scenario-pack/brownfield/01-system-inventory.md:1)
- [template-repo/scenario-pack/brownfield/02-repo-audit.md](/projects/factory-template/template-repo/scenario-pack/brownfield/02-repo-audit.md:1)

### 2.5. Доработка шаблона и развернутых на шаблоне боевых проектов

Событие:
- найден defect или process gap в шаблоне;
- нужно улучшить launcher/scenario-pack/validators;
- нужно перенести улучшение в downstream template и battle repos.

Подробный workflow:

1. Обнаружить проблему в `factory-template` или в working project на шаблоне.
2. Зафиксировать defect-capture:
   - bug report
   - classification
   - factory feedback при reusable issue
3. Если change требует ChatGPT Project analysis, пройти repo-first сценарный анализ.
4. Реализовать изменение в `factory-template`.
5. Пройти verify:
   - smoke
   - matrix
   - pre-release audit
   - release-facing consistency pass
6. Синхронизировать release-facing docs и completion artifacts внутри repo.
7. Закоммитить и запушить изменение в `factory-template`.
8. Подготовить completion package по трём контурам:
   - обновление repo-first инструкции проекта шаблона в ChatGPT
   - обновление шаблона в downstream/battle repo
   - обновление repo-first инструкции downstream/battle ChatGPT Projects
9. Для downstream sync при необходимости использовать patch/export workflow.
10. После внешнего обновления battle repos повторить verify уже на стороне downstream.

Где это описано сейчас:
- [factory_template_only_pack/01-runbook-dlya-polzovatelya-factory-template.md](/projects/factory-template/factory_template_only_pack/01-runbook-dlya-polzovatelya-factory-template.md:212)
- [bootstrap/07-как-обновлять-template-repo-через-meta-template.md](/projects/factory-template/bootstrap/07-%D0%BA%D0%B0%D0%BA-%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%8F%D1%82%D1%8C-template-repo-%D1%87%D0%B5%D1%80%D0%B5%D0%B7-meta-template.md:1)
- [bootstrap/19-как-работает-цикл-доработки-фабрики.md](/projects/factory-template/bootstrap/19-%D0%BA%D0%B0%D0%BA-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82-%D1%86%D0%B8%D0%BA%D0%BB-%D0%B4%D0%BE%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8-%D1%84%D0%B0%D0%B1%D1%80%D0%B8%D0%BA%D0%B8.md:1)
- [factory_template_only_pack/templates/factory-template-boundary-actions.template.md](/projects/factory-template/factory_template_only_pack/templates/factory-template-boundary-actions.template.md:16)

## 3. Итог оценки покрытия

До добавления этого документа repo содержал:
- хороший scenario-pack и runbook layer;
- хорошие входные маршруты по greenfield/brownfield;
- частичное описание operator lifecycle;
- но не содержал одного цельного документа с визуальной архитектурой шаблона и подробными workflows по всем пяти событиям.

Теперь этот gap закрыт как reference layer. Канонические детали реализации по-прежнему остаются в `scenario-pack`, runbooks, launcher и validator scripts.
