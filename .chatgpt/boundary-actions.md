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
- Активные стартовые сценарии: еще не определены.
- Проверить, что Codex получает актуальные `codex-input.md`, `codex-context.md`, `codex-task-pack.md` и `boundary-actions.md`.

## Модель влияния

- `impact.factory_sources` — Обновление repo-first инструкции проекта шаблона в ChatGPT только если изменились canonical repo/path/entrypoint или короткая instruction text; иначе по умолчанию не требуется
- `impact.downstream_template_sync` — Обновление шаблона в боевых repo
- `impact.downstream_project_sources` — Обновление repo-first инструкции боевых ChatGPT Projects только для legacy/hybrid fallback; для чистого repo-first режима по умолчанию не требуется
- `impact.manual_archive_required` — Нужен готовый архив или каталог для ручной загрузки
- `impact.delete_before_replace` — Перед заменой нужно удалить старую repo-first инструкцию, если она конфликтует с новой

## Пакет завершения для изменений repo-first инструкций

Если change затрагивает scenario-pack, launcher, validators, runbooks, codex-task-pack, `.chatgpt` artifacts или другой downstream-consumed template content, пользовательский boundary output должен включать:

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

Обязательно различайте три контура:
- Обновление repo-first инструкции проекта шаблона в ChatGPT
- Обновление шаблона в боевых repo
- Обновление repo-first инструкции боевых ChatGPT Projects

Если contour не затронут, это нужно явно написать.
Для contour `Обновление repo-first инструкции проекта шаблона в ChatGPT` canonical default — `нет`, если canonical repo/path/entrypoint/instruction text не менялись.
Для contour `Обновление repo-first инструкции боевых ChatGPT Projects` canonical default — `нет`, если downstream уже живет в чистом repo-first режиме.

## Для handoff

- Handoff в Codex сейчас не является обязательным для выбранного профиля.
- `apply_mode: manual-ui (default)` — основной user-facing путь для интерактивной работы через VS Code Codex extension.
- Для ручного применения через UI откройте новый чат/окно Codex, вручную выберите `selected_model=gpt-5.5` и `selected_reasoning_effort=medium` в picker, затем вставьте handoff.
- `strict_launch_mode: optional` — используйте launch command из `.chatgpt/task-launch.yaml`, если нужна automation, reproducibility, shell-first или scripted launch.
- `новый чат + вставка handoff` и `новый task launch через executable launcher` — не одно и то же.
- Уже открытая live session является только non-canonical fallback и не должна подаваться как надежный auto-switch path.
- `AGENTS`, ChatGPT Project instructions, scenario-pack и `.chatgpt` guidance являются advisory layer; profile/model выбирает executable launcher/router.
- `selected_profile` — это исполнимая граница маршрутизации; `selected_model` и `selected_reasoning_effort` описывают repo-configured mapping этого profile, а не auto-switch от текста handoff.
- Model availability auto-check выполняется через `scripts/check-codex-model-catalog.py` / `codex debug models`; если catalog недоступен или stale, не утверждайте, что selected_model точно live-available.
- Если новый model появляется в live catalog, сначала создайте proposal через `--write-proposal`; promotion существующего profile требует manual review.
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
- Человекочитаемые заголовки, инструкции, отчеты и closeout-тексты должны быть на русском языке; английский допустим только для технических идентификаторов, команд, файлов, ключей конфигурации и literal values.
- Troubleshooting sticky state:
  - если пользователь открыл случайную или уже существующую Codex chat-сессию и просто вставил handoff, profile/model/reasoning могли не переключиться;
  - для интерактивного процесса сначала закройте устаревшую сессию, откройте новую и вручную проверьте picker;
  - если нужна строгая boundary-гарантия, выполните optional strict launch command через `./scripts/launch-codex-task.sh`;
  - если после этого route все еще выглядит устаревшим, проверить именованный profile в local Codex config и сверить `selected_model` с live `codex debug models`.

## Для внешних границ

- GitHub PR merge не считать внешним шагом автоматически. Если `gh` или GitHub connector доступен, PR относится к текущей задаче, checks green, PR mergeable и нет required human approval/conflict/неясной merge strategy, Codex должен сам выполнить ready/merge/delete-branch/local sync.
- GitHub UI считать внешним шагом только при конкретном блокере: нет авторизации, нет прав, required human review/approval, red/pending checks, конфликт, release/security approval или другое действие, которое нельзя безопасно выполнить инструментами Codex.
- Внешние UI / секреты не выполнять автоматически из Codex.
- Все внешние действия фиксировать отдельной пошаговой инструкцией для пользователя с финальным блоком `Инструкция пользователю`.
- `Инструкция пользователю` не должна подменять внутренний handoff, если internal repo follow-up еще не завершен.
- Если внешнего шага нет, финальный ответ все равно должен явно сказать, что внешних действий не требуется.
- Для обновления factory ChatGPT Project сначала сам подготовьте точный repo-first instruction text; этот шаг выполняет Codex внутри repo до пользовательского блока.
- Для downstream repo sync сначала используйте `workspace-packs/factory-ops/export-template-patch.sh` и `workspace-packs/factory-ops/apply-template-patch.sh`.
- Для downstream repo instruction layer source-of-truth хранится в `template-repo/AGENTS.md`, а Codex в battle repo должен читать materialized root `AGENTS.md`.
- Не перекладывайте на пользователя запуск внутренних repo-команд вроде `GENERATE_BOUNDARY_ACTIONS.sh`, если эти шаги может выполнить Codex.
- Если замена может создать устаревшие дубликаты, добавляйте точный раздел `Удалить перед заменой`.

Если closeout полностью внутренний и `Инструкция пользователю` не нужна, используйте явную формулировку вроде:
- `Внешних действий не требуется.`
- `Следующий пользовательский шаг отсутствует; change закрыт полностью внутри repo.`
