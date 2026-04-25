# Первый проект: путь для новичка

Этот документ - главный вход для первого запуска.

Вместо ручного выбора внутренних preset-терминов используйте guided launcher:

```bash
python3 template-repo/scripts/factory-launcher.py
```

Он покрывает:
- новый проект с нуля;
- старт с существующим проектом или системой;
- продолжение уже созданного flow до planning/deploy next step.

Прямой wizard остается fallback-командой:

```bash
python3 template-repo/scripts/first-project-wizard.py
```

Wizard задаст 3 понятных вопроса:
1. Что у вас уже есть.
2. Что вы хотите запустить.
3. Что система сделает дальше.

После ответов wizard:
- сам подбирает правильный режим (`greenfield` или `brownfield`) и нужный preset;
- показывает короткое объяснение выбора;
- запускает VPS preflight в человекочитаемом виде;
- создает проект через существующий launcher без ломки текущей архитектуры.

## Отдельный запуск preflight

Если хотите проверить VPS заранее:

```bash
python3 template-repo/scripts/preflight-vps-check.py --project-slug my-first-service
```

Проверка показывает:
- что уже в порядке;
- где есть риск;
- что исправить конкретной командой.

## Как wizard сопоставляет ответы

- Только идея, без кода -> `greenfield-product`
- Есть проект и repo -> один из путей:
  - модернизация -> `brownfield-with-repo-modernization`
  - интеграции -> `brownfield-with-repo-integration`
  - аудит -> `brownfield-with-repo-audit`
- Есть система, но repo нет -> `brownfield-without-repo`

## Что появится в созданном проекте

В проекте сразу будет слой долгоживущих знаний:
- `project-knowledge/README.md`
- `project-knowledge/project.md`
- `project-knowledge/architecture.md`
- `project-knowledge/deployment.md`

Этот слой нужен, чтобы фиксировать устойчивые решения и не терять контекст между задачами.

## Defect capture: что мешало раньше

До wizard-first потока у новичка были типовые блокеры:
- старт требовал знать внутренние имена preset и change-class заранее;
- не было понятного preflight отчета по VPS layout;
- не было прозрачного объяснения, что система сделает после ответов.

Текущий guided launcher закрывает эти блокеры единым входом поверх существующих preset/scenario механизмов.

Подробно:
- `docs/guided-launcher.md`
