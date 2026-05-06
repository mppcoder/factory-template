# Пользовательский ранбук: greenfield-product

Цель: создать новый боевой проект как `greenfield-product` / `greenfield-active`.
Старт нового боевого проекта происходит не в Codex. Канонический старт: ChatGPT Project шаблона фабрики `factory-template` -> новый чат -> команда `новый проект`.
Маркер границы: `Codex takeover point` наступает только на `GF-050`, когда пользователь вставляет generated handoff в выбранный Codex contour.

## Настройка только пользователем

Маркер слоя: `USER-ONLY SETUP`.
Пользователь делает только внешние действия: запускает factory-template ChatGPT intake, отвечает на опрос, вставляет стартовый Codex handoff, а после Codex automation создает ChatGPT Project боевого проекта, открывает Project settings/instructions, вставляет готовую repo-first instruction и сохраняет настройки.
Если проект идет на VPS, пользователь выбирает/подтверждает исходный Ubuntu LTS image как внешний setup-факт. Codex не устанавливает обновления автоматически: он фиксирует baseline, policy `manual-approved-upgrade`, watchlist/readiness и выносит любые upgrade decisions в отдельный approval gate.

Пользователь не создает GitHub repo, не выбирает slug/repo name вручную, не clone-ит repo, не добавляет `origin`, не делает initial commit/push, не создает VPS project root, не запускает launcher/wizard, не materialize-ит repo-first core, не запускает verify и sync.

## Автоматизация Codex

Маркер слоя: `CODEX-AUTOMATION`.
Codex получает стартовый handoff, сформированный ChatGPT Project шаблона фабрики после опроса. Codex нормализует slug/repo name, создает GitHub repo, готовит VPS project root, запускает factory launcher/wizard, materializes repo-first core, создает `.chatgpt`, `AGENTS`, scenario-pack, dashboard, project-knowledge, выполняет bootstrap/verify, делает initial commit/push/verified sync, готовит готовый текст repo-first instruction для боевого ChatGPT Project и готовит пошаговую инструкцию пользователю, куда этот текст вставить.

Codex готовит repo-first instruction для боевого ChatGPT Project. Пользователь создает ChatGPT Project в UI и вставляет готовый текст.
Codex не создает ChatGPT Project боевого проекта, не открывает Project settings/instructions, не вставляет instruction и не сохраняет настройки через browser/desktop UI automation как canonical path для новичка.

Допустимые contours: `vscode-remote-ssh-codex-extension` через `Codex extension / Codex chat` в VS Code Remote SSH или fallback `codex-app-remote-ssh`.

### GF-000. Проверить стартовое состояние

- Окно: Browser ChatGPT / VS Code Remote SSH / Codex app.
- Делает: Пользователь.
- Зачем: Убедиться, что factory-template уже готов и можно начинать intake в ChatGPT Project шаблона фабрики.
- Что нужно до начала: `factory-template` установлен и verified; доступен один Codex contour: Codex App Remote SSH или VS Code Remote SSH + Codex IDE extension.
- Где взять значения: Статус verified взять из последнего closeout factory-template; contour взять из factory-template setup runbook.
- Команды для копирования:

```text
Стартовое состояние:
- factory-template установлен и verified;
- открыт ChatGPT Project шаблона фабрики;
- доступен Codex contour: codex-app-remote-ssh или vscode-remote-ssh-codex-extension.
```

- Куда вставить: Можно вставить в заметки; в Codex не вставлять.
- Ожидаемый результат: Пользователь находится в ChatGPT Project шаблона фабрики `factory-template`.
- Если ошибка: Если Codex takeover еще невозможен, вернитесь в `../01-factory-template/01-user-runbook.md` и завершите setup до `FT-170`.
- Evidence: Factory-template ChatGPT Project открыт; contour готов или blocker понятен.
- Следующий шаг: `GF-005`.

### GF-005. Открыть новый чат в ChatGPT Project шаблона фабрики

- Окно: Browser ChatGPT Project `factory-template`.
- Делает: Пользователь.
- Зачем: Новый боевой проект стартует через factory ChatGPT intake, а не прямым сообщением Codex.
- Что нужно до начала: `GF-000`.
- Где взять значения: Project name: `factory-template`.
- Команды для копирования:

```text
ChatGPT UI path:
1. Открыть ChatGPT Project шаблона фабрики factory-template.
2. Нажать New chat / Новый чат.
3. Убедиться, что чат создан внутри factory-template Project.
```

- Куда вставить: Не в терминал; выполнить в Browser ChatGPT UI.
- Ожидаемый результат: Открыт новый пустой чат внутри ChatGPT Project шаблона фабрики.
- Если ошибка: Если открыт обычный ChatGPT chat вне Project, вернитесь в Project `factory-template` и создайте чат там.
- Evidence: Вверху/слева виден Project `factory-template`.
- Следующий шаг: `GF-010`.

### GF-010. Написать команду `новый проект`

- Окно: Новый чат в ChatGPT Project шаблона фабрики.
- Делает: Пользователь.
- Зачем: Запустить scenario-pack intake для нового проекта.
- Что нужно до начала: `GF-005`.
- Где взять значения: Команда фиксированная.
- Команды для копирования:

```text
новый проект
```

- Куда вставить: В поле сообщения нового чата ChatGPT Project шаблона фабрики.
- Ожидаемый результат: ChatGPT Project по repo-first instruction сначала читает `template-repo/scenario-pack/00-master-router.md` и начинает default-decision intake.
- Если ошибка: Если ChatGPT не начинает опрос, проверьте, что чат открыт внутри Project `factory-template`, а repo-first instruction активна.
- Evidence: ChatGPT отвечает вопросом выбора default-decision mode.
- Следующий шаг: `GF-015`.

### GF-015. Выбрать режим default decisions

- Окно: Новый чат в ChatGPT Project шаблона фабрики.
- Делает: Пользователь.
- Зачем: Чтобы новичку не приходилось принимать все решения с пустого листа, если фабрика может предложить безопасную рекомендацию.
- Что нужно до начала: `GF-010`.
- Где взять значения: Режим выбирает пользователь; beginner-friendly default — принять safe recommendations и спрашивать только реальные choices.
- Команды для копирования:

```text
Использовать рекомендуемые решения по умолчанию на основе лучших доступных практик, концепции и масштаба проекта?

Да, используй рекомендуемые решения по умолчанию; спрашивай меня только там, где реально нужен мой выбор.
```

- Куда вставить: Ответом в чат ChatGPT Project шаблона фабрики.
- Ожидаемый результат: ChatGPT Project фиксирует `default_decision_mode: global-defaults`, `confirm-each-default` или `manual`.
- Если ошибка: Если ChatGPT Project задает expert-only вопросы без recommendation/default/override path, попросите его продолжить в `per-question-default mode`.
- Evidence: В чате зафиксирован выбранный `default_decision_mode`.
- Следующий шаг: `GF-020`.

### GF-020. Пройти опрос ChatGPT Project

- Окно: Новый чат в ChatGPT Project шаблона фабрики.
- Делает: Пользователь.
- Зачем: ChatGPT Project должен собрать данные до формирования Codex handoff, но показывать safe defaults там, где фабрика может рекомендовать решение.
- Что нужно до начала: `GF-015`.
- Где взять значения: Название и идею придумывает пользователь; остальные решения ChatGPT Project предлагает recommendation-first на основе repo-policy, best-practice, project-scale и readiness из factory-template runbook/checklist.
- Команды для копирования:

```text
Опрос recommendation-first:
- название проекта: пользовательское, без default кроме подсказки;
- краткая идея: пользовательская;
- slug/repo name default: slug из названия проекта по naming rules;
- GitHub repo visibility default: private, если пользователь не просит public/open-source;
- VPS root path default: /projects/<slug>;
- starter preset default: starter/minimal production-ready baseline;
- Codex contour default: VS Code Remote SSH + Codex extension, fallback Codex App Remote SSH если так настроено;
- verification mode default: quick; full только для release/deploy/matrix contour;
- ChatGPT Project instruction: Codex подготовит default text после automation;
- blockers: подписка, GitHub connection, VPS, SSH, Codex takeover, paid/security/destructive confirmations.

Формат каждого решения:
Вопрос: Где создать репозиторий?
Рекомендация по умолчанию: GitHub repo в аккаунте пользователя, slug из названия проекта.
Почему: это соответствует repo-first flow фабрики и позволяет Codex создать repo/origin/first push.
Ответ:
- Enter / "по умолчанию" — принять рекомендацию;
- или напишите свой вариант.
```

- Куда вставить: Ответами в чат ChatGPT Project шаблона фабрики.
- Ожидаемый результат: ChatGPT Project знает project name, project type, readiness state, Codex contour, blockers, `accepted_defaults`, `overridden_defaults`, `default_source_basis`, `uncertainty_notes` и `decisions_requiring_user_confirmation`.
- Если ошибка: Если есть blocker по подписке/GitHub/VPS/SSH/Codex takeover, не переходите к handoff; закройте blocker по factory-template setup runbook. Проверка handoff: no hidden forced defaults for risky actions.
- Evidence: В чате есть ответы на опрос, принятые defaults и overrides.
- Следующий шаг: `GF-030`.

### GF-030. Проверить readiness по runbook/checklist

- Окно: ChatGPT Project шаблона фабрики / docs operator runbook.
- Делает: Пользователь и ChatGPT Project.
- Зачем: Handoff нельзя формировать, если Codex takeover еще невозможен.
- Что нужно до начала: `GF-020`.
- Где взять значения: Readiness сверяется по `../01-factory-template/03-checklist.md` и выбранному contour.
- Команды для копирования:

```text
Readiness checklist:
- factory-template verified;
- Codex contour выбран;
- remote shell доступен;
- GitHub connection доступен;
- VPS/SSH готовы;
- нет blocker по подписке, secret, approval или Codex takeover.
```

- Куда вставить: Ответить в ChatGPT Project шаблона фабрики, если он спрашивает readiness.
- Ожидаемый результат: Если readiness green, ChatGPT Project переходит к handoff. Если нет, пользователь возвращается в factory-template setup runbook.
- Если ошибка: Если readiness uncertain, не вставляйте handoff в Codex; сначала выполните `../01-factory-template/01-user-runbook.md`.
- Evidence: ChatGPT Project фиксирует readiness state и выбранный Codex contour.
- Следующий шаг: `GF-040`.

### GF-040. Получить стартовый Codex handoff

- Окно: ChatGPT Project шаблона фабрики.
- Делает: ChatGPT Project; пользователь копирует результат.
- Зачем: Codex должен получить структурированный handoff, а не raw project name.
- Что нужно до начала: `GF-030` green или documented blocker отсутствует.
- Где взять значения: Handoff формирует ChatGPT Project после опроса.
- Команды для копирования:

```text
Проверить handoff:
- один цельный блок;
- содержит project name;
- содержит slug proposal;
- содержит project type;
- содержит default_decision_mode;
- содержит accepted_defaults;
- содержит overridden_defaults;
- содержит uncertainty_notes и unresolved decisions/blockers;
- содержит readiness state;
- содержит выбранный Codex contour;
- содержит boundary: GitHub repo/root/verify/sync делает Codex;
- содержит Язык ответа Codex: русский.
```

- Куда вставить: Пока не вставлять; скопировать весь handoff для `GF-050`.
- Ожидаемый результат: Есть один цельный стартовый Codex handoff.
- Если ошибка: Если handoff разбит на части или не содержит boundary, попросите ChatGPT Project сформировать один цельный handoff.
- Evidence: Handoff block готов.
- Следующий шаг: `GF-050`.

### GF-050. Вставить handoff в Codex

- Окно: Новый Codex chat/window в выбранном contour.
- Делает: Пользователь.
- Зачем: Передать выполнение Codex после ChatGPT intake.
- Что нужно до начала: `GF-040`; доступен выбранный Codex contour.
- Где взять значения: Handoff из `GF-040`.
- Команды для копирования:

```text
Открыть новый Codex chat/window в выбранном contour.
Если picker доступен, вручную выбрать model/reasoning из handoff.
Вставить один цельный handoff из ChatGPT Project шаблона фабрики.
REMOTE_CONTEXT_MARKER: Codex должен быть открыт в VS Code Remote SSH window или Codex app remote thread на VPS.
GF-050 continuity: один handoff запускает всю Codex automation до closeout или blocker.
Do not paste into local Codex: локальный Codex не создает VPS project root и не выполняет remote verify/sync.
No hidden second shell step: после handoff Codex сам делает repo/root/scaffold/verify/sync.
```

- Куда вставить: В Codex App Remote SSH thread или VS Code Remote SSH Codex chat.
- Ожидаемый результат: Codex выводит handoff receipt и начинает automation; `GF-050` continuity соблюдено без дополнительного ручного shell шага.
- Если ошибка: Если Codex открыт не в remote context, вернитесь к factory-template setup runbook; если handoff разделился, откройте новый chat/window и вставьте одним блоком.
- Evidence: Codex handoff receipt.
- Следующий шаг: `GF-060`.

### GF-060. Дождаться Codex automation

- Окно: Codex App Remote SSH или VS Code Remote SSH Codex chat.
- Делает: Codex.
- Зачем: Вся внутренняя работа по боевому проекту выполняется Codex.
- Что нужно до начала: `GF-050`.
- Где взять значения: Codex берет значения из ChatGPT-generated handoff.
- Команды для копирования:

```text
Codex выполняет:
- slug/repo naming;
- GitHub repo creation;
- VPS project root;
- launcher/wizard;
- repo-first core;
- .chatgpt, AGENTS, scenario-pack, dashboard, project-knowledge;
- bootstrap/verify;
- initial commit/push/verified sync.
```

- Куда вставить: Не вставлять; это контроль ожидания.
- Ожидаемый результат: Codex сообщает адрес созданного repo, project root, verify result, commit/push status и готовит пошаговую инструкцию пользователю для ChatGPT Project UI.
- Если ошибка: Если Codex фиксирует blocker, выполнить только названное внешнее действие: permission, approval, secret, paid/dangerous confirmation или ChatGPT Project UI.
- Evidence: Codex closeout с адресом созданного repo, project root, verify result и sync status.
- Следующий шаг: `GF-070`.

### GF-070. Получить готовую repo-first instruction и UI-инструкцию

- Окно: Codex chat/window.
- Делает: Codex; пользователь копирует результат.
- Зачем: Боевой ChatGPT Project должен получить точную instruction под созданный repo, а ChatGPT Project UI остается действием пользователя.
- Что нужно до начала: `GF-060` green или documented blocker снят.
- Где взять значения: Codex final closeout.
- Команды для копирования:

```text
Скопировать готовую repo-first instruction из финального ответа Codex.
Скопировать пошаговую инструкцию Codex: где в ChatGPT Project UI открыть settings/instructions, куда вставить текст и как сохранить.
Не редактировать адрес repo, project root, scenario entrypoint и language contract вручную.
```

- Куда вставить: Пока не вставлять; сохранить для `GF-090`.
- Ожидаемый результат: Готовый instruction block и UI-инструкция скопированы.
- Если ошибка: Если instruction отсутствует, попросите Codex выдать готовый блок для ChatGPT Project боевого проекта.
- Evidence: Готовый repo-first instruction block и пошаговая UI-инструкция.
- Следующий шаг: `GF-080`.

### GF-080. Создать ChatGPT Project боевого проекта

- Окно: Browser ChatGPT.
- Делает: Пользователь.
- Зачем: Это внешний UI; Codex не создает ChatGPT Project.
- Что нужно до начала: `GF-070`.
- Где взять значения: Название проекта из опроса; repo-first instruction из Codex.
- Команды для копирования:

```text
ChatGPT UI path:
1. Открыть ChatGPT.
2. Projects -> New project.
3. Название: имя боевого проекта из опроса.
4. Создать project.
5. Не передавать создание Project в Codex: это ручное действие в ChatGPT UI.
```

- Куда вставить: Не в терминал; выполнить в Browser ChatGPT UI.
- Ожидаемый результат: ChatGPT Project боевого проекта создан.
- Если ошибка: Если UI не создает project, отправьте Codex screenshot/error text без секретов.
- Evidence: Новый ChatGPT Project боевого проекта существует.
- Следующий шаг: `GF-090`.

### GF-090. Вставить готовую repo-first instruction и сохранить настройки

- Окно: Browser ChatGPT Project settings/instructions.
- Делает: Пользователь.
- Зачем: Перевести дальнейшую работу в собственный ChatGPT Project боевого проекта.
- Что нужно до начала: `GF-080`; готовый instruction block из `GF-070`.
- Где взять значения: Instruction block подготовил Codex.
- Команды для копирования:

```text
Открыть ChatGPT Project боевого проекта.
Открыть Project settings/instructions.
Вставить в ChatGPT Project боевого проекта ровно готовую repo-first instruction, которую подготовил Codex.
Сохранить настройки.
```

- Куда вставить: Browser ChatGPT -> боевой Project -> Settings/Instructions.
- Ожидаемый результат: Project instructions сохранены и указывают на созданный repo/root/scenario-pack.
- Если ошибка: Если instruction слишком длинная или UI не сохраняет, попросите Codex подготовить короткую совместимую версию.
- Evidence: Instruction сохранена.
- Следующий шаг: `GF-100`.

### GF-100. Боевой проект готов

- Окно: Browser ChatGPT Project боевого проекта.
- Делает: Пользователь.
- Зачем: Завершить bootstrap flow и перейти к работе уже через боевой Project.
- Что нужно до начала: `GF-090`.
- Где взять значения: Новый Project и repo-first instruction уже созданы.
- Команды для копирования:

```text
Дальнейшие задачи по боевому проекту задавать в его собственном ChatGPT Project.
Factory-template ChatGPT Project остается каналом создания/обновления проектов, а не постоянным каналом работы внутри каждого боевого проекта.
```

- Куда вставить: Можно сохранить в заметки; не вставлять в Codex.
- Ожидаемый результат: Боевой проект готов к дальнейшей работе через собственный ChatGPT Project.
- First project ready proof: первый проект считается готовым только если есть repo URL, VPS project root, verify result, commit/push or sync blocker, готовая repo-first instruction и сохраненная инструкция в battle ChatGPT Project.
- Если ошибка: Если новый Project не читает repo-first instruction, вернитесь к `GF-090` и проверьте сохранение instruction.
- Evidence: Первый новый чат в боевом Project следует repo-first instruction.
- Следующий шаг: `STOP`.
