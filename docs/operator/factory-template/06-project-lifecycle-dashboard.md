# Панель жизненного цикла проекта

## Назначение

`project-lifecycle-dashboard` — это верхняя repo-native панель состояния проекта. Она отвечает на три вопроса:

- что происходит с проектом сейчас;
- какая доработка активна и где она застряла;
- какой следующий шаг безопасен, а какой является fallback.

Панель не является web app, daemon, SQLite database, Telegram bot или background worker. Это YAML state artifact плюс Markdown/CLI renderer и validator.

## Где лежат артефакты

- Canonical state: `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`.
- Handoff implementation register: `template-repo/template/.chatgpt/handoff-implementation-register.yaml`.
- Chat handoff index: `template-repo/template/.chatgpt/chat-handoff-index.yaml`.
- Renderer: `template-repo/scripts/render-project-lifecycle-dashboard.py`.
- Validator: `template-repo/scripts/validate-project-lifecycle-dashboard.py`.
- Register validator: `template-repo/scripts/validate-handoff-implementation-register.py`.
- Chat index validator: `template-repo/scripts/validate-chat-handoff-index.py`.
- Chat id allocator: `template-repo/scripts/allocate-chat-handoff-id.py`.
- Markdown output по умолчанию: `reports/project-lifecycle-dashboard.md`.
- ChatGPT mini card template: `template-repo/template/.chatgpt/visual-status-card.md.template`.
- Codex execution card template: `template-repo/template/.chatgpt/codex-execution-card.md.template`.

В generated/battle project canonical state живет в `.chatgpt/project-lifecycle-dashboard.yaml`. Он template-owned и безопасен для materialization downstream. Factory producer paths вроде `factory/producer/*` не должны попадать в root боевого проекта.

## Что показывает dashboard

- identity проекта: имя, профиль, lifecycle state, текущий mode;
- lifecycle phase: `idea / intake / spec / architecture / handoff / execution / verification / release / deploy / operate / improve`;
- active change: id, title, class, priority, status;
- stage gates: intake, classification, reuse/reality-check, spec, tech-spec, handoff, execution, verification, done;
- multi-step progress: текущая wave, completed tasks, blocked tasks, next task, final verification, archive readiness;
- handoff/orchestration: parent handoff, child tasks, selected profile/model/reasoning и route boundary;
- handoff implementation control: межчатовые ChatGPT handoff / Codex self-handoff задачи, их status, dependencies, blockers, stale evidence и closeout state;
- chat handoff index: стабильные номера и названия ChatGPT-чатов, где `kind` и `state` живут отдельно от UI title;
- release readiness: version, changelog, release notes, scorecard, verification state;
- deploy/runtime: signal из operator dashboard reports, если они есть;
- standards navigator: selected standards profile, lifecycle backbone version/status, standards gate summary, missing standards evidence, next safe standards action, monitoring status и `allowed_to_advance_phase`;
- software update governance: baseline, auto-update policy, update intelligence, findings, upgrade proposal status, next safe action, fallback и blockers;
- post-release improvement: incidents, feedback, learning proposals, backlog candidates;
- runbook packages: current phase, gates, blockers и next action для четырех entry paths;
- external actions ledger: только реальные user/manual/runtime/downstream действия;
- recommended next step и fallback next step.

## Stable ChatGPT Chat Titles

ChatGPT chat title должен быть стабильным на весь lifecycle задачи:

```text
<PROJECT_CODE>-CH-<NNNN> <task-slug>
```

Примеры:

```text
FT-CH-0010 dashboard-card-ui
FT-CH-0011 completion-report
```

В title нельзя добавлять `HO`, `OPEN`, `DONE`, `BLOCKED`, `VERIFIED`, `BUG`, `DECISION`, `RESEARCH` или другие status/kind tokens. Статусы живут только в repo state: `.chatgpt/chat-handoff-index.yaml`, handoff register и dashboard/card. Поэтому переход `open -> in_progress -> verified` не требует ручного переименования ChatGPT-чата.

Номер выделяется repo-first через index/allocator и считается занятым только после materialized/reserved write в `.chatgpt/chat-handoff-index.yaml`. Если следующий номер неизвестен или repo write не подтвержден в repo/GitHub index, его нельзя придумывать; нужно сказать:

```text
Нужно выделить номер через repo chat-handoff-index / allocator.
```

Project Instructions могут показать пользователю только уже зарезервированный stable title или allocator blocker. Они не могут надежно auto-rename ChatGPT UI, просканировать все названия чатов проекта или гарантировать следующий свободный номер без repo write. Переименование ChatGPT UI остается one-time manual action при создании чата, если нет отдельного поддержанного API/tool.

Fallback contract: сначала попытка через repo-local allocator; если repo-local allocator недоступен в ChatGPT connector context, но доступен GitHub connector write path, ChatGPT делает connector update `.chatgpt/chat-handoff-index.yaml`, затем confirm fetch/readback. Connector fallback должен быть connector-safe reservation patch: append one item and bump `next_chat_number`; не делай ручной full-file rewrite без сверки текущего counter, canonical `status_chain` и confirm fetch/readback. repo-first instruction authorizes configured GitHub connector, поэтому не спрашивай conversational confirmation перед чтением repo/index или allocation attempt. GitHub write-access request gate сохраняет ChatGPT write-access request mechanism: structured write-access request — not a conversational confirmation. Если write action not exposed, но platform/connector может запросить write scope, сначала сделай structured write-access request для записи `.chatgpt/chat-handoff-index.yaml`, затем retry connector-safe reservation after grant. platform-level OAuth / connector authorization prompt остается внешней границей: если он блокирует действие, назови `external_auth_blocker`; если write action exposed отсутствует или write rejected, назови `write_auth_blocker`. blocker нельзя выводить, когда GitHub connector write path доступен и confirm fetch подтверждает update. Если write action exposed and confirm fetch succeeds, exact allocator blocker запрещен. Exact blocker допустим только если `write_access_request_attempted` завершился как `request unavailable/rejected`, request rejected, materialized write failed after request, write action truly absent with no platform request path, write rejected или confirm fetch failed.

Важно: `FT-CH-....` в первом ответе не является предложением. Это ссылка на уже созданный item в repo index. Если handoff так и не запустили в Codex, номер остается занятым; следующая задача должна получить новый номер, а старую запись нужно явно закрыть как `superseded`, `not_applicable` или `archived`, если она больше не нужна.

Инвариант first substantive answer: до route receipt, анализа или handoff должен быть один из двух видимых outcomes - materialized allocation or allocator blocker. Первое допустимое состояние - materialized allocation confirmed, затем stable title block. Второе допустимое состояние - repo write не подтвержден или allocation unavailable, затем exact allocator blocker.

третье состояние запрещено: no allocation attempted / no blocker / answer continues. Если ChatGPT не показал `FT-CH-....` и не показал allocator blocker, это ошибка первого ответа `allocation-not-attempted`. Пользователь должен остановить route и запустить repo allocator или передать Codex remediation, а не продолжать с примерным номером.

Значение title/blocker в первом ответе должно быть оформлено как отдельный однострочный fenced `text` code block: так ChatGPT UI показывает copy button, и пользователь может скопировать его одним кликом. Внутри code block должна быть ровно одна строка: stable title или exact allocator blocker.

Первый substantive ответ ChatGPT в новом task-чате должен начинаться с:

````markdown
## Название чата для копирования
```text
<stable chat title или allocator blocker>
```

## Карточка проекта
<compact project card>
````

`Карточка проекта` берется из `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --format chatgpt-card --stdout`, `reports/project-status-card.md` или compact block в `reports/project-lifecycle-dashboard.md`. Этот блок обязателен для ChatGPT-ответов так же, как для Codex closeout.

Рекомендуемый snippet для Project Instructions:

```text
В первом substantive ответе нового task chat сначала покажи:
1. `Название чата для копирования`;
2. `Карточка проекта`.

Stable title имеет формат `<PROJECT_CODE>-CH-<NNNN> <task-slug>` и разрешен только после materialized/reserved write в repo index.
Title/blocker под `Название чата для копирования` выводи как отдельный однострочный fenced `text` code block, чтобы ChatGPT UI показал copy button и пользователь мог скопировать значение одним кликом.
Инвариант first substantive answer: до route receipt, анализа или handoff должен быть один из двух видимых outcomes - materialized allocation or allocator blocker.
Если repo write не подтвержден, не придумывай номер и скажи: `Нужно выделить номер через repo chat-handoff-index / allocator.`
третье состояние запрещено: no allocation attempted / no blocker / answer continues.
Если нет `FT-CH-....` и нет allocator blocker, это ошибка первого ответа `allocation-not-attempted`; останови route и не продолжай с примерным номером.
Status/kind tokens в title запрещены; статусы показывай только в project card и repo dashboard.
```

При первом substantive ответе в новом task chat handoff обязан получить номер из repo counter и ссылаться на него:

```bash
python3 template-repo/scripts/allocate-chat-handoff-id.py \
  --index .chatgpt/chat-handoff-index.yaml \
  --kind handoff \
  --description "short task name"
```

Эта команда должна выполниться без `--dry-run` до показа `FT-CH-....` пользователю. `--dry-run` может использоваться только для диагностики и не резервирует номер.

Codex self-handoff использует отдельный counter и не расходует ChatGPT `FT-CH` номера:

```bash
python3 template-repo/scripts/allocate-codex-work-id.py \
  --index .chatgpt/codex-work-index.yaml \
  --kind self_handoff \
  --description "short self handoff task"
```

В executable path `bootstrap-codex-task.py` записывает `kind: handoff` в `.chatgpt/chat-handoff-index.yaml` только для `chatgpt-handoff`. Для `direct-task` он записывает `kind: self_handoff` в `.chatgpt/codex-work-index.yaml`. Поэтому `FT-CH-....` означает ChatGPT task chat, а `FT-CX-....` означает Codex remediation/direct work.

Первый substantive ответ Codex для direct task должен начинаться с видимой пары:

````markdown
## Номер запроса Codex
```text
<PROJECT_CODE>-CX-<NNNN> <task-slug>
```

## Карточка проекта
<compact project card>
````

`FT-CX-....` разрешен только после materialized write в `.chatgpt/codex-work-index.yaml`. Если write не подтвержден, Codex должен показать exact blocker:

```text
Нужно выделить номер через repo codex-work-index / allocator.
```

Карточка проекта для этого блока берется из repo renderer (`--format chatgpt-card --stdout`) так же, как финальная closeout-card. Если renderer недоступен, это blocker, а не повод заменить карточку пересказом.

Поиск:

- по номеру: `FT-CH-0010`;
- по Codex work номеру: `FT-CX-0010`;
- по slug: `dashboard-card-ui`;
- незавершенная работа ищется в dashboard/card, а не по status token в title.

## Beginner visual surfaces / визуальные поверхности для новичка

Для новичка dashboard проявляется в трех местах:

- `ChatGPT mini card` — короткий readout в ChatGPT Project: проект, compact lifecycle chain, module readiness chain и активные handoff/task status lines.
- `Codex execution card` — короткий readout в Codex App / VS Code Codex extension: request identity, route receipt, выбранный профиль/model/reasoning, текущая wave/task, completed/remaining steps, blockers, next internal action и external action boundary.
- `reports/project-lifecycle-dashboard.md` — полная Markdown доска состояния, которую можно открыть в VS Code Markdown Preview или GitHub preview.

Связь слоев:

- `project-lifecycle-dashboard` — source/full board;
- `ChatGPT mini card` — короткий readout для пульта управления;
- `Codex execution card` — ход исполнения для пульта исполнения;
- `orchestration-cockpit-lite` — detailed artifact для parent handoff и child tasks;
- `operator-dashboard` — runtime/deploy detail.

Карточки не являются отдельным state. Renderer выводит их из dashboard YAML и repo index. Если данных не хватает, карточка показывает `unknown` или `pending`, а не зеленый статус.

Если `external_actions_ledger` не пуст, ChatGPT card не может писать “от пользователя требуется: ничего”. Если Codex card пишет `executed`, `completed`, `passed` или `done`, у этого claim должна быть execution evidence или accepted reason.

## Как читать “что происходит сейчас”

Сначала смотрите раздел `Сейчас`, затем `Активное изменение` и `Следующий шаг`.

Если stage gate отмечен `passed`, `completed`, `done`, `ready` или `archived`, у него должен быть `evidence` или `accepted_reason`. Иначе это false green, validator остановит dashboard.

Если `final_verification.status` не `passed`, feature нельзя архивировать в `work/completed/`, даже если часть задач уже `done`.

## Связь с cockpit-lite

`orchestration-cockpit-lite` показывает состояние одного большого parent handoff: child tasks, route receipt, blockers, deferred user actions и placeholder replacements.

`project-lifecycle-dashboard` стоит уровнем выше. Он агрегирует cockpit как один источник, но не заменяет его:

- cockpit отвечает “как идет этот parent handoff”;
- lifecycle dashboard отвечает “где сейчас проект от идеи до release/deploy/operate/improve”.

## Контроль реализации handoff / Handoff implementation control

`.chatgpt/handoff-implementation-register.yaml` фиксирует doработка/bug задачи, которые появились в ChatGPT handoff или были созданы Codex как self-handoff. Это отдельный lifecycle register, а не KPI: `.chatgpt/handoff-rework-register.yaml` остается только счетчиком rework loops.

Зачем нужен register:

- задача может родиться в отдельном ChatGPT-чате и иначе потеряться между сессиями;
- пользователь должен видеть, что handoff уже выдан, но реализация еще не закрыта;
- blocked, replaced/superseded, снятые, implemented-but-not-verified и stale задачи должны оставаться видимыми до closeout;
- silent deletion запрещен: неактуальные задачи закрываются как `not_applicable`, `superseded` или `archived` с reason/evidence.
- если в одном ChatGPT-чате по той же задаче создан новый handoff, старый handoff списывается через replacement path, а не остается активным.

Dashboard рендерит раздел `## Handoff implementation control`:

- `Queued / ready` — очередь реализации; prerequisite/blocker tasks поднимаются выше обычных ready tasks;
- `Blocked by dependencies` — задачи, которые имеют незакрытые `depends_on`;
- `Blockers / prerequisite tasks` — задачи, которые разблокируют другие items;
- `In progress` — текущие работы;
- `Implemented but not verified` — код/доки сделаны, но verification evidence еще нет;
- `Not applicable / superseded / archived` — явно снятые, замененные или архивированные задачи;
- `Stale items without recent evidence` — открытые items без свежего evidence/update.

Priority считается детерминированно: base priority `critical > high > medium > low`, затем +1 level если item блокирует хотя бы одну незакрытую задачу и еще +1 level если блокирует несколько. Blocked item не должен отображаться как ready.

Codex closeout behavior:

- найти соответствующий item в `.chatgpt/handoff-implementation-register.yaml`;
- обновить `status`;
- добавить `evidence`;
- если задача породила новый self-handoff, добавить новый item;
- если создается новый handoff по той же задаче в текущем чате, проверить `handoff_group`, списать старые active items как `superseded`, заполнить `superseded_by`, `replacement_reason`, evidence, а у нового item заполнить `replaces`;
- если задача неактуальна, не удалять ее, а выполнить deactivation path: `status: not_applicable`, `closeout_reason`, evidence или `accepted_reason`;
- обновить `reports/project-lifecycle-dashboard.md`.
- вставить свежую compact project card в финальный ответ пользователю в разделе `Карточка проекта`; карточка должна быть получена через `render-project-lifecycle-dashboard.py --format chatgpt-card --stdout` и содержать lifecycle chain, `Модули:` и `В работе:`.
- compact card не является историческим журналом: раздел `В работе:` показывает текущую chat/self-handoff задачу и незакрытые задачи; verified/archived/superseded старые задачи остаются в полном `reports/project-lifecycle-dashboard.md`, но не шумят в compact card.
- compact card не должен превращать stale/unregistered index seeds в активную очередь: незакрытая строка без `handoff_register_item_id` скрывается из compact `В работе:`, если это не текущая/latest задача; такие записи нужно списывать в `not_applicable`/`superseded` с evidence или accepted reason.
- compact card выводится без лишних пустых строк. Длинные lifecycle/module/task строки должны переноситься renderer-ом на читаемых границах, чтобы карточка оставалась удобной в ChatGPT answer pane.

Replacement identity:

- `handoff_group` — стабильный идентификатор задачи внутри чата/цепочки handoff;
- `handoff_revision` — номер версии handoff в этой группе;
- `replaces` — какие старые handoff items заменяет новый handoff;
- `superseded_by` — каким новым item списан старый handoff;
- `replacement_reason` — почему старый handoff заменен, например broken single-block shape, уточнение scope или переработка после вопроса пользователя.

Dashboard может показывать `selected_profile`, `selected_model` и reasoning как readout из handoff/register. Это не auto-switch: уже открытая Codex-сессия не меняет route/model/reasoning из-за YAML или advisory text.

Register item может ссылаться на stable chat identity:

- `chat_id`;
- `chat_title`;
- `task_slug`;
- `chat_state`;
- `chat_index_item_id`.

`chat_title` остается стабильным и не является источником статуса. `chat_state`/status chain читаются из repo state, а не из названия ChatGPT-чата.

## Связь с operator-dashboard

`operator-dashboard.py` остается runtime/deploy панелью: env, preset, dry-run, deploy reports, Docker Compose и next deploy step.

Lifecycle dashboard не выполняет deploy и не обещает runtime automation. Он только показывает runtime/deploy state и evidence boundary. Dry-run/report evidence не считается real production proof.

## Связь со standards navigator

`standards_navigator` — обязательный readout/control block для lifecycle standards gates. Он не заменяет dashboard, а добавляет к нему нормативную карту:

- какой standards profile выбран: `solo_lightweight`, `commercial_production` или `custom`;
- какая lifecycle backbone version используется;
- какие standards обязательны для текущей фазы;
- какие gates passed/pending/missing/blocking;
- какая evidence отсутствует;
- можно ли продвигать фазу без false green.

Dashboard validator блокирует production/commercial claim с одним `solo_lightweight`, security/accessibility/quality green без evidence, AI readiness без `ai_safety_gate`, stale standard overclaim и certification/compliance claim без evidence.

Это не formal certification. Dashboard может говорить, что проект использует standards-inspired gates или mapped evidence, но не должен заявлять ISO/NIST/OWASP/WCAG/DORA/OpenAI compliance/certification.

## Module Readiness Line

Compact card показывает standards-inspired readiness по модулям:

```text
Модули:
✅ Lifecycle → 🟡 Core → 🟡 Security → 🕒 UI/A11y → 🕒 Quality → 🕒 WebSec → 🕒 Ops → ⏸ AI
```

Это readout готовности evidence gates, а не заявление о compliance/certification. Значки:

- `✅` — passed/completed/verified только с evidence или accepted_reason;
- `🟡` — in progress или частично готово;
- `🕒` — required, но pending/not started;
- `🔴` — blocked/failed или missing required evidence;
- `⏸` — not applicable только с accepted_reason.

Security, UI/A11y, Quality, WebSec, Ops и AI нельзя показывать зелеными без evidence или accepted_reason. AI может быть `⏸`, если проект не использует AI behavior и причина записана в repo.

## Связь с software update governance

`software_update_governance` показывает controlled update state, а не выполняет обновления. Source artifacts:

- `.chatgpt/software-inventory.yaml`;
- `.chatgpt/software-update-watchlist.yaml`;
- `.chatgpt/software-update-readiness.yaml`;
- `reports/software-updates/README.md`.

Блок обязан различать Ubuntu/VPS image release, later package update state, runtime stack и production-critical dependency state. Default policy: `manual-approved-upgrade`; auto-install без approval запрещен. Переход на новую Ubuntu LTS является отдельным migration/upgrade project, а не silent maintenance step.

## Связь с runbook packages

`runbook_packages` показывает четыре проверяемых пакета:

- `01-factory-template`;
- `02-greenfield-product`;
- `03-brownfield-with-repo-to-greenfield`;
- `04-brownfield-without-repo-to-greenfield`.

Для каждого package dashboard фиксирует текущую phase, gates, blockers, next action и owner boundary. Это readout/control tower слой, а не отдельная automation runtime.

## Routing boundary

Dashboard может показывать `selected_profile`, `selected_model`, `selected_reasoning_effort` и route explanation. Это readout, а не переключатель.

Advisory layer (`AGENTS`, scenario-pack, handoff text, docs) не переключает model/profile/reasoning внутри уже открытой Codex-сессии. Надежная executable boundary — новый task launch или ручной выбор model/reasoning в picker нового Codex chat/window.

## Команды

```bash
python3 template-repo/scripts/validate-project-lifecycle-dashboard.py \
  template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml

python3 template-repo/scripts/validate-handoff-implementation-register.py \
  template-repo/template/.chatgpt/handoff-implementation-register.yaml

python3 template-repo/scripts/validate-chat-handoff-index.py \
  template-repo/template/.chatgpt/chat-handoff-index.yaml

python3 template-repo/scripts/validate-standards-gates.py \
  template-repo/template/.chatgpt/standards-gates.yaml

python3 template-repo/scripts/check-standards-watchlist.py --root .

python3 template-repo/scripts/render-project-lifecycle-dashboard.py \
  --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml \
  --format markdown-full \
  --output reports/project-lifecycle-dashboard.md

python3 template-repo/scripts/render-project-lifecycle-dashboard.py \
  --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml \
  --format chatgpt-card \
  --stdout

python3 template-repo/scripts/allocate-chat-handoff-id.py \
  --index template-repo/template/.chatgpt/chat-handoff-index.yaml \
  --project-code FT \
  --kind handoff \
  --description "dashboard card ui"

python3 template-repo/scripts/render-project-lifecycle-dashboard.py \
  --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml \
  --format codex-card \
  --stdout
```

Для generated project из его root:

```bash
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
python3 scripts/validate-handoff-implementation-register.py .chatgpt/handoff-implementation-register.yaml
python3 scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml
python3 scripts/render-project-lifecycle-dashboard.py --format markdown-full --output reports/project-lifecycle-dashboard.md
python3 scripts/render-project-lifecycle-dashboard.py --format chatgpt-card --stdout
python3 scripts/render-project-lifecycle-dashboard.py --format codex-card --stdout
```

Обычный пользователь не обязан запускать эти команды вручную в one-paste flow: это внутренняя работа Codex при closeout/verify.

## Owner boundaries

Dashboard использует те же границы, что orchestration layer:

- `internal-repo-follow-up`;
- `external-user-action`;
- `runtime-action`;
- `downstream-battle-action`;
- `model-mapping-blocker`;
- `secret-boundary-blocker`.

`external_actions_ledger` не является audit table. Туда попадают только actionable user/manual/runtime/downstream шаги, которые реально требуют внешнего действия.
