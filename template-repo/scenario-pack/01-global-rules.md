# Глобальные правила

1. Repo — источник правды. Чат не является источником правды.
2. Нельзя переходить к реализации без нормализованных артефактов.
3. Любое решение должно быть помечено источником:
   - `[PROJECT]` — основано на текущем проекте;
   - `[FIX]` — основано на ранее подтвержденном фиксе;
   - `[DOC]` — основано на официальной документации;
   - `[REAL]` — основано на реальном кейсе;
   - `[ASSUMPTION]` — предположение.
4. Если есть конфликт между реальностью проекта и документацией, зафиксируй его отдельно.

## Правило canonical VPS layout
В `/projects` разрешены только корневые папки отдельных проектов.

Каноническая структура:
- `/projects/<project-root>/` — корень конкретного проекта;
- `/projects/<project-root>/_incoming/` — необязательная подпапка для входящих архивов и установочных файлов;
- любые temporary, intermediate, reconstructed и другие вспомогательные repo — только внутри repo целевого `greenfield-product`: `/projects/<target-greenfield-project>/...`.

Запрещено:
- создавать в `/projects` служебные верхнеуровневые папки вроде `_incoming`, `_release`, `_artifacts`;
- раскладывать brownfield temporary/intermediate/reconstructed repo как соседние project roots;
- создавать промежуточные repo за пределами целевого `greenfield-product` repo;
- использовать `/projects` как плоскую staging-зону.

## Правило фиксации дефектов
Любой обнаруженный дефект, регрессия, расхождение, пропущенный шаг, шаблонный сбой или reusable process failure должен быть оформлен как структурированный bug report до исправления или одновременно с ним. Silent fixes запрещены.

## Правило русскоязычного человекочитаемого слоя
Для `factory-template` человекочитаемые ответы, инструкции, отчеты, описания, closeout, handoff-пояснения и generated guidance пишутся на русском языке.
Handoff в Codex должен явно требовать: `Язык ответа Codex: русский`. Codex отвечает пользователю по-русски; английский допустим только как technical literal values: команды, пути, YAML/JSON keys, model IDs и route fields.

Допустимые исключения:
- технические имена файлов, команд, ключей конфигурации и полей;
- буквальные значения API, CLI, GitHub, YAML/JSON и переменных окружения;
- названия моделей, профилей, actions, branch, commit и PR, если они являются идентификаторами.

Англоязычные шаблонные заголовки и описательные фразы в человекочитаемом слое считаются дефектом, если их можно без потери смысла заменить русским текстом.

## Правило выравнивания
Фабрика, greenfield и brownfield могут различаться по предметным шагам, но не могут различаться по правилам фиксации дефектов, handoff и completion.

Отсутствие inline Codex handoff в ответе, где handoff уже допустим и задача достаточно определена, считается reusable process defect.

Отсутствие финального блока `Инструкция пользователю` в ответе, где есть pending external/user step, считается reusable process defect.

Подмена internal repo follow-up user-only closeout'ом считается reusable process defect.

Смешение internal repo work и external boundary action без явного разделения на handoff и user footer считается reusable process defect.

Если ответ предлагает конкретный пример текста для вставки, отправки, instruction, UI-поля, чата или CLI, но не дает этот текст отдельным fenced code block для копирования, это считается reusable process defect copy-block layer.

Если change влияет на repo-first instruction layer или downstream template consumers, но completion output не различает affected contours, delete-before-replace semantics и boundary steps по окнам/папкам, это считается reusable process defect.

Если обязательный `## Инструкция пользователю` или completion package появляется только после дополнительного запроса пользователя, это считается reusable process defect completion/handoff layer.

Если Codex перекладывает на пользователя внутренние repo-операции вроде export refresh, boundary-actions generation, manifest refresh или сборки patch/export artifacts, это считается reusable process defect boundary/completion layer.

Если verify уже green, `origin` настроен и verified sync технически доступен, но ответ завершает change без canonical `VERIFIED_SYNC.sh` и без явного блокера, это считается reusable process defect closeout/sync layer.

Если финальный ответ дан при dirty worktree или branch ahead относительно `origin/*` без конкретного blocker, это считается reusable process defect closeout/autosync layer.

Если доступный GitHub PR merge ошибочно маркируется как внешний пользовательский шаг без проверки `gh`/GitHub connector, mergeability, checks и review blockers, это считается reusable process defect closeout/GitHub layer.

Если ChatGPT/Codex обращается к GitHub repo `mppcoder/factory-template` через публичный `github.com` / `raw.githubusercontent.com` URL вместо доступного GitHub connector, repo tool или authenticated `gh` без named blocker, это считается reusable process defect repo-first/GitHub access layer.

Если человекочитаемые ответы, отчеты или generated guidance для `factory-template` используют английские описательные заголовки/фразы вместо русского текста без технической необходимости, это считается reusable process defect language layer.
