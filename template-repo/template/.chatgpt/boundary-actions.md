# Действия на границе

## Для пользователя

Каноническая финальная секция ответа пользователю называется `Инструкция пользователю` и должна использовать структуру:
1. Цель
2. Где сделать
3. Точные шаги
4. Ожидаемый результат
5. Что прислать обратно

- Создать или открыть ChatGPT Project для этого рабочего проекта.
- В ChatGPT Project должен действовать repo-first режим: сначала GitHub repo, затем 00-master-router.md. Сценарии не должны пересказываться из памяти.
- Активные стартовые сценарии: `00-master-router.md`; уточняются по `.chatgpt/active-scenarios.yaml`.
- Проверить, что Codex получает актуальные `codex-input.md`, `codex-context.md`, `codex-task-pack.md` и `boundary-actions.md`.

## Модель влияния

- `impact.factory_sources` — Обновление repo-first инструкции проекта шаблона в ChatGPT только если изменились canonical repo/path/entrypoint или короткая instruction text; иначе по умолчанию не требуется
- `impact.downstream_template_sync` — Обновление шаблона в боевых repo
- `impact.downstream_project_sources` — Обновление repo-first инструкции боевых ChatGPT Projects только для legacy/hybrid fallback; для чистого repo-first режима по умолчанию не требуется
- `impact.manual_archive_required` — Нужен готовый архив или каталог для ручной загрузки
- `impact.delete_before_replace` — Перед заменой нужно удалить старую repo-first инструкцию, если она конфликтует с новой

## Пакет завершения для изменений repo-first инструкций

Если change затрагивает scenario-pack, launcher, validators, runbooks, codex-task-pack, `.chatgpt` artifacts или другой downstream-consumed template content, сначала определи, есть ли реальные внешние действия пользователя.

Compact default:
- если внешних действий нет, финальный ответ должен сказать `Внешних действий не требуется.` и дать fully-done continuation outcome;
- если внешние действия есть, `## Инструкция пользователю` перечисляет только то, что пользователь реально должен сделать снаружи Codex;
- не перечисляй contour'ы со статусом `не требуется`, если пользователь явно не запросил полный audit-style register или это не release/security approval.

Для реальных внешних действий пользовательский boundary output должен включать:

1. Что изменено
2. Какие файлы обновлены в repo
3. Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project
   По умолчанию: нет, если canonical repo/path/entrypoint/instruction text не менялись
4. Нужно ли обновлять downstream template in battle repos
5. Нужно ли обновлять repo-first инструкции battle ChatGPT Projects
   По умолчанию: нет для чистого repo-first режима; да только для legacy/hybrid fallback
6. Готовые артефакты для скачивания
7. Команды/скрипты для repo-level sync
8. Удалить перед заменой
9. Пошаговая инструкция по окнам
10. Что прислать обратно после внешнего шага

Отдельно обязателен compact outcome:
- `Внешние действия: нет`, если действий нет;
- или `Реестр внешних действий`, если есть хотя бы одно действие.

В реестре для каждого actionable contour нужно явно указать:
- `Рекомендация`: `требуется`, `рекомендуется`, `опционально` или `только legacy/hybrid fallback`;
- `Причина`: почему именно такой статус;
- `Действие пользователя`: точная команда или UI-шаг;
- `Когда выполнять`: сейчас, при следующем downstream sync, только для legacy/hybrid fallback или не выполнять.

`Реестр внешних действий` — это actionable ledger, а не audit table всех возможных contour'ов.
Если все строки имеют `действие не требуется`, не выводи реестр; используй `Внешние действия: нет` или `Внешних действий не требуется.`

Обязательно различайте три контура:
- Обновление repo-first инструкции проекта шаблона в ChatGPT
- Обновление шаблона в боевых repo
- Обновление repo-first инструкции боевых ChatGPT Projects

Если contour не затронут, не добавляй его в пользовательскую инструкцию.
Для contour `Обновление repo-first инструкции проекта шаблона в ChatGPT` canonical default — `нет`, если canonical repo/path/entrypoint/instruction text не менялись.
Для contour `Обновление repo-first инструкции боевых ChatGPT Projects` canonical default — `нет`, если downstream уже живет в чистом repo-first режиме.

## Для handoff

- Handoff в Codex сейчас не является обязательным для выбранного профиля.
- `apply_mode: manual-ui (default)` — основной user-facing путь для интерактивной работы через VS Code Codex extension.
- Для ручного применения через UI откройте новый чат/окно Codex, вручную выберите `selected_model=gpt-5.5` и `selected_reasoning_effort=high` в picker, затем вставьте handoff.
- `strict_launch_mode: optional` — используйте launch command из `.chatgpt/task-launch.yaml`, если нужна automation, reproducibility, shell-first или scripted launch.
- `новый чат + вставка handoff` и `новый task launch через executable launcher` — не одно и то же.
- Уже открытая live session является только non-canonical fallback и не должна подаваться как надежный auto-switch path.
- `AGENTS`, ChatGPT Project instructions, scenario-pack и `.chatgpt` guidance являются advisory layer; profile/model выбирает executable launcher/router.
- `selected_profile` — это исполнимая граница маршрутизации; `selected_model` и `selected_reasoning_effort` описывают repo-configured mapping этого profile, а не auto-switch от текста handoff.
- Model availability auto-check выполняется через `scripts/check-codex-model-catalog.py` / `codex debug models`; если catalog недоступен или stale, не утверждайте, что selected_model точно live-available.
- Если новый model появляется в live catalog, сначала создайте proposal через `--write-proposal`; promotion существующего profile требует ручного review.
- Проверяемая фиксация реального выбора хранится в `.chatgpt/task-launch.yaml`.
- При исполнении handoff приоритет у правил repo: `AGENTS`, runbook, scenario-pack, policy files и других канонических файлов этого репозитория.
- Общие рабочие инструкции применять только там, где они не конфликтуют с repo rules и старшими системными ограничениями среды.
- Если выбран `hybrid` или `codex-led`, передать Codex актуальный `codex-task-pack.md`.
- После возврата из Codex обновить verification-report.md, done-report.md и CURRENT_FUNCTIONAL_STATE.md.
- Если handoff уже разрешен и задача достаточно определена, его нужно выдать inline в том же ответе, а не ограничиваться аналитикой.
- Формат handoff для пользователя: только один цельный блок для вставки в Codex.
- Нельзя заменять handoff ссылкой на файл, несколькими разрозненными блоками или инструкцией собрать handoff из `codex-input.md`, `codex-context.md`, `codex-task-pack.md`.
- Если remaining work еще остается внутренним repo follow-up, handoff не должен исчезать из-за будущего user footer.
- Release-followup, source-pack refresh, export refresh, closeout-sync и release-facing consistency pass внутри repo считаются внутренней работой Codex.
- Brownfield source-candidate map, reconstruction allowlist/denylist, change-map и reverse-engineering summary внутри repo тоже считаются внутренней работой Codex.
- Если такой внутренний follow-up уже назван и route текущей live-сессии совместим, Codex продолжает выполнение в этом task и не завершает ответ просьбой пользователя вручную написать "продолжай".
- Перед финальным ответом Codex обязан выполнить `git status --short --branch`; dirty worktree или branch ahead без конкретного blocker означает, что closeout еще не завершен.
- Если `origin` настроен, verify green и sync технически доступен, Codex выполняет `VALIDATE_VERIFIED_SYNC_PREREQS.sh` и `VERIFIED_SYNC.sh` сам; commit/push нельзя оставлять пользователю.
- Финальный ответ по внутренне закрытому repo change должен назвать commit hash / sync status или `no-op`.
- Человекочитаемые заголовки, инструкции, отчеты и closeout-тексты должны быть на русском языке; английский допустим только для технических идентификаторов, команд, файлов, ключей конфигурации и literal values.
- Upstream ChatGPT-generated handoff в `.chatgpt/codex-input.md` тоже должен быть на русском в человекочитаемом слое; англоязычные разделы `Goal`, `Hard constraints`, `Required implementation`, `Verification commands`, `Completion requirements` считаются language-contract defect.
- Codex обязан отвечать пользователю на русском языке. Английский допустим только для technical literal values: команды, пути, ключи конфигурации, model IDs и route fields.
- Troubleshooting sticky state:
  - если пользователь открыл случайную или уже существующую Codex chat-сессию и просто вставил handoff, profile/model/reasoning могли не переключиться;
  - для интерактивного процесса сначала закройте устаревшую сессию, откройте новую и вручную проверьте picker;
  - если нужна строгая boundary-гарантия, выполните optional strict launch command через `./scripts/launch-codex-task.sh`;
  - если после этого route все еще выглядит устаревшим, проверить именованный profile в local Codex config и сверить `selected_model` с live `codex debug models`.

## Для внешних границ

- GitHub PR merge не считать внешним шагом автоматически. Если `gh` или GitHub connector доступен, PR относится к текущей задаче, checks green, PR mergeable и нет required human approval/conflict/неясной merge strategy, Codex должен сам выполнить ready/merge/delete-branch/local sync.
- GitHub repo/remote creation не считать внешним шагом автоматически. Если `gh` или GitHub connector доступен с write permissions, owner/name однозначны и repo можно безопасно создать или использовать, Codex должен сам создать GitHub repo, добавить `origin` и выполнить первый push.
- Просьба пользователю "создай repo на GitHub и пришли URL" допустима только при конкретном blocker: нет авторизации, нет прав, неоднозначный owner/name, repo name conflict без безопасного решения или требуется человеческое security/release approval.
- GitHub UI считать внешним шагом только при конкретном блокере: нет авторизации, нет прав, required human review/approval, red/pending checks, конфликт, release/security approval или другое действие, которое нельзя безопасно выполнить инструментами Codex.
- Внешние UI / секреты не выполнять автоматически из Codex.
- Все внешние действия фиксировать отдельной пошаговой инструкцией для пользователя с финальным блоком `Инструкция пользователю`.
- Финальный блок должен содержать только реальные внешние действия пользователя.
- Если внешних действий нет, не пиши таблицу contour'ов; напиши `Внешних действий не требуется.`
- Если external actions есть, используй compact `Реестр внешних действий` со строками только для actionable contour'ов.
- Если GitHub repo creation действительно заблокирован, `Инструкция пользователю` должна явно указать owner/repo, целевой visibility, точную команду или UI-шаг, ожидаемый remote URL, команду проверки и что прислать обратно.
- `Инструкция пользователю` не должна подменять внутренний handoff, если internal repo follow-up еще не завершен.
- Если внешнего шага нет, финальный ответ все равно должен явно сказать, что внешних действий не требуется.
- Каждый финальный ответ обязан содержать continuation outcome: либо `## Инструкция пользователю` с точным действием для продолжения, либо явную фразу `Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью.`
- Если существует будущий roadmap stage, но он не actionable сейчас, назови его как future boundary и отдельно скажи, что текущий scope закрыт полностью.
- Если roadmap/readout содержит несколько возможных следующих веток, финальный ответ обязан назвать рекомендованную ветку и fallback-ветку; `Следующий пользовательский шаг отсутствует` закрывает только текущий scope и не заменяет next-roadmap recommendation.
- Для обновления factory ChatGPT Project сначала сам подготовьте точный repo-first instruction text; этот шаг выполняет Codex внутри repo до пользовательского блока.
- Для downstream repo sync сначала используйте `factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh` и `factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh`.
- Для downstream repo instruction layer source-of-truth хранится в `template-repo/AGENTS.md`, а Codex в battle repo должен читать materialized root `AGENTS.md`.
- Не перекладывайте на пользователя запуск внутренних repo-команд вроде `GENERATE_BOUNDARY_ACTIONS.sh`, если эти шаги может выполнить Codex.
- Если замена может создать устаревшие дубликаты, добавляйте точный раздел `Удалить перед заменой`.

Если closeout полностью внутренний и `Инструкция пользователю` не нужна, используйте явную формулировку вроде:
- `Внешних действий не требуется.`
- `Следующий пользовательский шаг отсутствует; задачи текущего scope выполнены полностью.`
- `Рекомендованный следующий roadmap шаг: P4-S5/P4-S6 при наличии real downstream/battle app; иначе Plan №5 / hardening contour.`
