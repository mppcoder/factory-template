# Repo-first правило сценариев для Codex

Работай строго repo-first.

## Настройка пути сценариев
Используй единую настройку:

`SCENARIO_PACK_PATH=template-repo/scenario-pack`

Для проекта `factory-template` это значение является значением по умолчанию.

Для боевых проектов на основе шаблона:
- сохрани это же значение, если структура repo не менялась;
- если папка сценариев перенесена, сначала обнови только `SCENARIO_PACK_PATH` на фактический repo-local path;
- не угадывай путь к сценариям “по памяти”.

## Обязательное первое действие на каждый новый запрос
1. Открой `${SCENARIO_PACK_PATH}/00-master-router.md`.
2. Прочитай его.
3. Дальше действуй строго по маршруту, который он задаёт.
4. Если router отправляет в другие repo-файлы, сначала прочитай их, затем продолжай работу.
5. Не начинай реализацию до прохождения этого шага.

## Правило доступа к GitHub repo
Если ChatGPT или Codex должен читать или менять GitHub repo `mppcoder/factory-template`, primary path — GitHub connector, repo tool или authenticated `gh`.
Публичные `github.com` / `raw.githubusercontent.com` URL не являются default path для ChatGPT/Codex, если connector/tool доступен.
Public URL fallback допустим только при явном blocker: connector unavailable, no permission, repo not installed in connector, authenticated repo tool unavailable или пользователь явно попросил public URL. При fallback обязательно назови blocker.

## Что фиксировать в первом содержательном ответе
- номер запроса Codex (`FT-CX-....`) или exact allocator blocker;
- карточку проекта из repo renderer;
- выбранный профиль проекта;
- выбранный сценарий;
- текущий этап pipeline;
- артефакты для обновления;
- разрешен ли handoff.

## Правило маршрутизации
Всегда разделяй:
- advisory/policy layer;
- executable routing layer.

Нельзя считать, что advisory-тексты сами переключают модель, профиль или reasoning mode внутри уже открытой сессии.

Надёжная единица маршрутизации — только новый task launch.

## Правило прямой задачи
Если задача пришла без внешнего handoff, сначала сделай self-handoff по repo rules, а уже потом переходи к remediation / implementation.

## Правило handoff
Если handoff уже допустим и задача достаточно определена, выдавай один цельный inline handoff block для copy-paste.

## Правило примеров для вставки
Если предлагаешь написать, вставить или отправить конкретный пример текста, этот пример всегда должен быть в fenced code block для копирования.
Нельзя давать готовый текст для вставки только inline, в кавычках или пересказом.

## Запрещено
- отвечать до чтения `${SCENARIO_PACK_PATH}/00-master-router.md`;
- пересказывать сценарии из памяти вместо чтения repo;
- подменять repo rules текстом из ChatGPT Project;
- считать уже открытую сессию Codex надёжным механизмом автопереключения профиля под новую задачу.
