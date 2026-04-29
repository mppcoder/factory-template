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
- Renderer: `template-repo/scripts/render-project-lifecycle-dashboard.py`.
- Validator: `template-repo/scripts/validate-project-lifecycle-dashboard.py`.
- Register validator: `template-repo/scripts/validate-handoff-implementation-register.py`.
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
- release readiness: version, changelog, release notes, scorecard, verification state;
- deploy/runtime: signal из operator dashboard reports, если они есть;
- standards navigator: selected standards profile, lifecycle backbone version/status, standards gate summary, missing standards evidence, next safe standards action, monitoring status и `allowed_to_advance_phase`;
- software update governance: baseline, auto-update policy, update intelligence, findings, upgrade proposal status, next safe action, fallback и blockers;
- post-release improvement: incidents, feedback, learning proposals, backlog candidates;
- runbook packages: current phase, gates, blockers и next action для четырех entry paths;
- external actions ledger: только реальные user/manual/runtime/downstream действия;
- recommended next step и fallback next step.

## Beginner visual surfaces / визуальные поверхности для новичка

Для новичка dashboard проявляется в трех местах:

- `ChatGPT mini card` — короткий readout в ChatGPT Project: проект, фаза, активная задача, статус, готово, блокеры, требуется ли действие пользователя и следующий безопасный шаг.
- `Codex execution card` — короткий readout в Codex App / VS Code Codex extension: route receipt, выбранный профиль/model/reasoning, текущая wave/task, completed/remaining steps, blockers, next internal action и external action boundary.
- `reports/project-lifecycle-dashboard.md` — полная Markdown доска состояния, которую можно открыть в VS Code Markdown Preview или GitHub preview.

Связь слоев:

- `project-lifecycle-dashboard` — source/full board;
- `ChatGPT mini card` — короткий readout для пульта управления;
- `Codex execution card` — ход исполнения для пульта исполнения;
- `orchestration-cockpit-lite` — detailed artifact для parent handoff и child tasks;
- `operator-dashboard` — runtime/deploy detail.

Карточки не являются отдельным state. Renderer выводит их из того же dashboard YAML. Если данных не хватает, карточка показывает `unknown` или `pending`, а не зеленый статус.

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
- blocked, снятые, implemented-but-not-verified и stale задачи должны оставаться видимыми до closeout;
- silent deletion запрещен: неактуальные задачи закрываются как `not_applicable` или `archived` с reason/evidence.

Dashboard рендерит раздел `## Handoff implementation control`:

- `Queued / ready` — очередь реализации; prerequisite/blocker tasks поднимаются выше обычных ready tasks;
- `Blocked by dependencies` — задачи, которые имеют незакрытые `depends_on`;
- `Blockers / prerequisite tasks` — задачи, которые разблокируют другие items;
- `In progress` — текущие работы;
- `Implemented but not verified` — код/доки сделаны, но verification evidence еще нет;
- `Not applicable / archived` — явно снятые или архивированные задачи;
- `Stale items without recent evidence` — открытые items без свежего evidence/update.

Priority считается детерминированно: base priority `critical > high > medium > low`, затем +1 level если item блокирует хотя бы одну незакрытую задачу и еще +1 level если блокирует несколько. Blocked item не должен отображаться как ready.

Codex closeout behavior:

- найти соответствующий item в `.chatgpt/handoff-implementation-register.yaml`;
- обновить `status`;
- добавить `evidence`;
- если задача породила новый self-handoff, добавить новый item;
- если задача неактуальна, не удалять ее, а выполнить deactivation path: `status: not_applicable`, `closeout_reason`, evidence или `accepted_reason`;
- обновить `reports/project-lifecycle-dashboard.md`.

Dashboard может показывать `selected_profile`, `selected_model` и reasoning как readout из handoff/register. Это не auto-switch: уже открытая Codex-сессия не меняет route/model/reasoning из-за YAML или advisory text.

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

python3 template-repo/scripts/render-project-lifecycle-dashboard.py \
  --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml \
  --format codex-card \
  --stdout
```

Для generated project из его root:

```bash
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
python3 scripts/validate-handoff-implementation-register.py .chatgpt/handoff-implementation-register.yaml
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
