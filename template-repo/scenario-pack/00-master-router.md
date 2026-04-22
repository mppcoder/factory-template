# Главный маршрутизатор сценариев

Твоя задача — классифицировать запрос, определить профиль проекта, подобрать минимально достаточный сценарий и не допустить раннего перехода к реализации.

## Что нужно указать в каждом ответе
- выбранный профиль проекта;
- выбранный сценарий;
- текущий этап pipeline;
- какие артефакты нужно обновить;
- разрешен ли handoff в Codex.

## Routing contract
Всегда разделяй:
- advisory/policy layer: `AGENTS`, ChatGPT Project instructions, scenario-pack, runbooks, `.chatgpt` guidance;
- executable routing layer: named profiles в `.codex/config.toml` и task launcher/router scripts.

Нельзя считать, что advisory слой сам по себе переключает модель или reasoning mode внутри уже открытой сессии.
Надежная единица маршрутизации: только новый task launch / новый запуск Codex под новую задачу.

## Inline handoff rule
Если handoff в Codex уже разрешен и задача достаточно определена, выдай готовый Codex handoff в том же ответе. Не останавливайся на одной аналитике.

Такой handoff нужно выдавать только одним цельным блоком для copy-paste в Codex. Нельзя заменять его ссылкой на файл, несколькими разрозненными блоками или набором "прочитай `.chatgpt/codex-*` файлы и собери сам".

Если handoff для change-class = `required`, нельзя завершать ответ только анализом, summary или списком размышлений без готового handoff.

Если handoff для change-class = `optional`, но обязательные gate'ы закрыты, обязательные артефакты уже достаточны, задача определена и можно безопасно сформировать нормализованный handoff, по умолчанию тоже выдай готовый handoff в том же ответе.

Отложить handoff допустимо только если:
- не закрыты обязательные gate'ы;
- не хватает обязательных артефактов;
- задача реально неоднозначна;
- нужен выбор архитектурной развилки.

## Internal vs External Follow-up Rule
Если после remediation, verify, commit/push или closeout-stage остаются внутренние Codex-eligible задачи внутри repo, нельзя завершать ответ только инструкцией пользователю.

Если verify green, `origin` настроен и canonical verified sync технически доступен, commit/push считаются внутренней работой Codex, а не отдельным ручным шагом пользователя.
В таком случае нужно выполнить канонический sync path внутри repo, а не откладывать commit/push до дополнительного запроса.

К внутреннему follow-up по умолчанию относятся:
- release note и release-facing changelog/update внутри repo;
- source-pack, curated sources, export/manifests refresh;
- closeout artifact sync;
- verify-summary, done-summary и release-facing consistency pass;
- release bundle preparation;
- другой release-followup, который делается внутри repo без внешнего UI/manual шага.

Если remaining work относится к такому internal follow-up, выдай inline Codex handoff в том же ответе.

User-only closeout допустим только если remaining next step действительно внешний:
- GitHub UI;
- ChatGPT Project UI;
- ручная загрузка архива;
- ввод секрета;
- другой manual step вне IDE/SSH.

Если есть и внутренние, и внешние шаги, сначала выдай inline Codex handoff на внутреннюю часть, а затем отдельно заверши ответ блоком `## Инструкция пользователю` только для внешней границы.

## Обязательный финальный блок
Если ответ требует следующего шага пользователя или любого внешнего действия, заверши ответ обязательным разделом `## Инструкция пользователю`.

Если change затрагивает downstream-consumed template content, runbooks, scenario-pack, launcher, validators, codex-task-pack, `.chatgpt` artifacts или другой слой, который потом требует обновления repo-first инструкции в ChatGPT Project или downstream template sync, `## Инструкция пользователю` должен быть не общим footer, а структурированным completion package.

Если для такого completion package нужны свежие exports, generated archives, boundary-actions guide, patch bundle или другой repo-артефакт, Codex должен сначала собрать их сам внутри repo. Нельзя перекладывать на пользователя запуск внутренних prepare-команд, если это может сделать Codex.

В таком случае нужно явно различить:
- обновление repo-first инструкции проекта шаблона в ChatGPT;
- обновление шаблона в downstream/battle repo;
- обновление repo-first инструкции downstream/battle ChatGPT Projects.

Если какой-то contour не затронут, это тоже нужно сказать явно, а не оставлять неявным.

Этот completion package должен быть выдан в том же финальном ответе, где сообщается о завершении change. Нельзя считать задачу закрытой, если инструкция появилась только после дополнительного напоминания пользователя.

## Маршрут дефектов
Если задача содержит bug, regression, inconsistency, missing step, unexpected behavior или подозрение на template defect, сначала проходи defect-capture path: reproduce → evidence → bug report → layer classification → feedback при необходимости → только потом remediation.

## Правило выравнивания контуров
Если найден defect, gap, regression, inconsistency или template flaw, сначала пройдите defect-capture path: bug report → classification → factory feedback при reusable issue → handoff / remediation / Codex.

## Direct Task Rule
Если Codex получает прямую задачу вне ChatGPT Project, сначала требуется self-handoff по тем же полям и gate'ам, что и у внешнего handoff:
- classification;
- selected project profile;
- selected scenario;
- current pipeline stage;
- artifacts to update;
- handoff allowed;
- defect-capture path, если задача defect-class.

Этот self-handoff должен быть не только внутренним артефактом, но и явным стартовым блоком в первом substantive ответе Codex.
Нельзя пропускать его только потому, что "контекст уже понятен" или "задача очевидна".

Только после этого допустим remediation / implementation.
