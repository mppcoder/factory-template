# Русское ядро фабрики проектов v2.5.4

Это стабилизационный релиз фабрики проектов для связки:

- **ChatGPT Project** — сценарии, интервью, анализ, нормализация.
- **Codex** — исполнение по подготовленному handoff.
- **Repo** — единственный источник правды по документам и изменениям.

Следующая линия `2.5` уже оформлена как отдельная release-программа: не только hardening процесса, но и beginner-first productization с UI-friendly контуром и безопасной эволюцией downstream-репозиториев.

Release truth source: `docs/releases/release-scorecard.yaml`.
Current 2.5 stage: `release publication / release artifact assembly`.
Status: `2.5.4 Package Ready`.
GA-ready: `true`.

## Канонические entry modes

Шаблон сейчас поддерживает 3 канонических режима запуска и сопровождения:

1. Новый проект с нуля
   Основа: `greenfield` steady-state путь для нового продукта или сервиса.
   Типовой вход: `greenfield-product`.

2. Перевод на шаблон имеющегося проекта без репо
   Основа: transitional `brownfield` intake/reconstruction path для live-системы, где нет нормализованного исходного repo.
   Типовой вход: `brownfield-without-repo`.
   Обязательный выход: canonical repo плюс conversion в `greenfield-product` или documented blocker.

3. Перевод на шаблон имеющегося проекта с репо
   Основа: transitional `brownfield` audit/adoption path для уже существующего репозитория или инженерного контура.
   Типовые входы: `brownfield-with-repo-modernization`, `brownfield-with-repo-integration`, `brownfield-with-repo-audit`.
   Обязательный выход: active profile `greenfield-product` или documented blocker.

Во всех трех случаях для generated project используется один и тот же базовый repo-first контур:

- прямое чтение `scenario-pack` из GitHub repo

Различается не workflow core, а стартовый маршрут, lifecycle state и ownership layer. Brownfield не является финальным типом проекта: успешное принятие существующего проекта заканчивается `project_preset: greenfield-product`, `recommended_mode: greenfield`, `lifecycle_state: greenfield-converted`.

`factory-template` следует тем же lifecycle rules, что и боевые проекты. Его продукт — сама фабрика проектов; дополнительное отличие только в `factory-producer-owned` layer: template generation, release, packaging, registry, downstream sync, reference packs и archives.

## Beginner-first entry через guided launcher

Для первого запуска больше не нужно вручную помнить preset-термины.
Используйте единый guided launcher:

```bash
python3 template-repo/scripts/factory-launcher.py
```

Launcher ведет по трем маршрутам:
- `greenfield` - steady-state product development с нуля;
- `brownfield` - transitional adoption существующего проекта или системы с выходом в greenfield;
- `continue` - уже созданный flow, planning workspace или operator next step.

По ответам launcher автоматически сопоставляет корректный `project preset`, показывает next-step recommendation и вызывает существующие fallback scripts: `first-project-wizard.py`, `preflight-vps-check.py`, `init-feature-workspace.sh`, `operator-dashboard.py`.
Старые команды остаются рабочими прямыми входами.

Отдельная инструкция для первого запуска:
- `docs/guided-launcher.md`
- `docs/first-project.md`

## Канонический VPS layout

Для VPS действует безусловное правило верхнего уровня:

- `/projects` содержит только project roots;
- каждый проект живёт в `/projects/<project-root>/`;
- `_incoming` допускается только как подпапка проекта: `/projects/<project-root>/_incoming/`;
- temporary, intermediate, reconstructed и helper repos для intake/adoption/reconstruction должны жить только внутри repo целевого `greenfield-product`: `/projects/<target-greenfield-project>/...`.

Запрещена плоская раскладка вспомогательных repo и служебных каталогов прямо в `/projects`, включая создание промежуточных repo как соседних project roots.

Канонический release-facing reference по архитектуре, дереву проекта и workflow собран в:

- `docs/template-architecture-and-event-workflows.md`
- `RELEASE_NOTES.md`
- `docs/releases/2.5-roadmap.md`
- `docs/releases/2.5-success-metrics.md`

## Установка с нуля и fallback archive

Canonical path для установки с нуля — GitHub clone/download или опубликованный release artifact `factory-v2.5.4.zip`.
Npm path не поддерживается: в repo нет `package.json` и npm packaging contract.

## Установка с Windows для новичка

Для полного новичка на Windows рекомендованный вход теперь находится в:

```text
windows-bootstrap/
```

Release-facing имя будущего wrapper artifact: `FactoryTemplateSetup.exe`. В текущем portable repo environment exe не собирается и не выдается за готовый signed installer; MVP executable path — прозрачный PowerShell script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\windows-bootstrap\install-windows.ps1
```

Bootstrapper проверяет `ssh.exe`/`scp.exe`, по возможности находит `git.exe` и `code.exe`, спрашивает VPS host/IP, SSH username и port, создает `/projects/factory-template/_incoming`, рекомендует GitHub clone/download из `mppcoder/factory-template`, поддерживает fallback archive upload `factory-v2.5.4.zip` + manifest + SHA256, запускает remote quick verification и сохраняет install log/next-step report.

Пользователь вручную делает только внешние действия: создает/оплачивает VPS, вводит passwords/secrets, авторизует GitHub при необходимости, создает ChatGPT Project в browser и подтверждает risky external/destructive actions. Npm install path для установки `factory-template` не поддерживается.

Fallback для ручной загрузки:

```bash
mkdir -p /projects/factory-template/_incoming
# загрузите factory-v2.5.4.zip, factory-v2.5.4.manifest.yaml и factory-v2.5.4.zip.sha256 в _incoming
cd /projects/factory-template/_incoming
sha256sum -c factory-v2.5.4.zip.sha256
rm -rf /projects/factory-template/factory-v2.5.4
unzip -q factory-v2.5.4.zip -d /projects/factory-template
cd /projects/factory-template/factory-v2.5.4
bash POST_UNZIP_SETUP.sh
python3 template-repo/scripts/validate-release-package.py ../_incoming/factory-v2.5.4.zip --checksum ../_incoming/factory-v2.5.4.zip.sha256 --manifest ../_incoming/factory-v2.5.4.manifest.yaml
bash template-repo/scripts/verify-all.sh quick
```

Archive contract: внутри zip должен быть один root `factory-v2.5.4/`; sidecar manifest `factory-v2.5.4.manifest.yaml` и checksum `factory-v2.5.4.zip.sha256` лежат рядом с archive.

## Подготовка после распаковки

```bash
cd factory-v2.5.4
bash POST_UNZIP_SETUP.sh
bash tests/onboarding-smoke/run-novice-e2e.sh
bash MATRIX_TEST.sh
bash CLEAN_VERIFY_ARTIFACTS.sh
```

`POST_UNZIP_SETUP.sh` теперь только обновляет execute-биты.
Generated projects больше не зависят от внешнего staging-контура для сценариев.

Если после self-tests нужен `PRE_RELEASE_AUDIT.sh` или сборка релиза, сначала очистите временные артефакты:

```bash
bash CLEAN_VERIFY_ARTIFACTS.sh
bash PRE_RELEASE_AUDIT.sh
```

Для работы с внешними границами без ручной сборки файлов:

```bash
bash GENERATE_BOUNDARY_ACTIONS.sh
bash VALIDATE_FACTORY_FEEDBACK.sh <working-project>
bash INGEST_FACTORY_FEEDBACK.sh <working-project> --dry-run
bash TRIAGE_INCOMING_LEARNINGS.sh --dry-run
```

`INGEST_FACTORY_FEEDBACK.sh` сначала прогоняет `VALIDATE_FACTORY_FEEDBACK.sh` и останавливает ingest на пустом или шаблонном `meta-feedback`, если не передан `--allow-incomplete`.

Для handoff в Codex:

```bash
python3 template-repo/scripts/create-codex-task-pack.py <working-project>
python3 template-repo/scripts/validate-codex-task-pack.py <working-project>
```

`validate-codex-task-pack.py` проверяет, что `codex-context.md`, `codex-task-pack.md`, `boundary-actions.md`, `done-checklist.md`, `task-launch.yaml` и `normalized-codex-handoff.md` не только созданы, но и согласованы с `active-scenarios.yaml`.
При формировании handoff в Codex явно фиксируйте, что приоритет у правил репозитория: `AGENTS`, runbook, scenario-pack и policy files repo.
Пользователю handoff выдаётся только одним цельным блоком для copy-paste в Codex, а не ссылкой на файл и не несколькими разрозненными блоками.
`template-repo/scripts/validate-handoff-response-format.py` дополнительно валидирует уже готовый markdown-ответ handoff и ловит file-based / multi-block handoff как process defect.

Для VS Code Codex extension используйте dual-path:
- `manual-ui (default)`: новый чат/окно Codex, ручной выбор model/reasoning в picker, затем вставка handoff;
- `launcher-first strict mode (optional)`: когда нужен executable launch boundary для automation, reproducibility и shell-first работы.

Новый чат + вставка handoff и новый task launch через executable launcher — не одно и то же.
Уже открытая live session не является надежным auto-switch механизмом.

Для strict launch path используйте новый launch boundary.
Если вы уже находитесь внутри working project, запускайте:

```bash
./scripts/launch-codex-task.sh --launch-source chatgpt-handoff --task-file .chatgpt/codex-input.md --dry-run
./scripts/launch-codex-task.sh --launch-source direct-task --task-text "проведи root-cause analysis ..." --dry-run
```

Если вы проверяете generated project из корня `factory-template`, используйте явный вызов script layer на целевом проекте:

```bash
python3 template-repo/scripts/bootstrap-codex-task.py <working-project> --launch-source direct-task --task-text "проведи root-cause analysis ..."
python3 template-repo/scripts/validate-codex-routing.py <working-project>
```

Проверка routing должна делаться только на новой задаче.
Нельзя считать старую уже открытую сессию Codex надежной единицей автоматической маршрутизации.

Model availability auto-check добавляет отдельную live Codex catalog проверку поверх repo-configured mapping:

```bash
python3 template-repo/scripts/check-codex-model-catalog.py .
python3 template-repo/scripts/check-codex-model-catalog.py . --json
python3 template-repo/scripts/check-codex-model-catalog.py . --write-proposal
```

`template-repo/codex-model-routing.yaml` хранит task class -> selected_profile -> selected_model / selected_reasoning_effort / selected_plan_mode_reasoning_effort. Live catalog берется из `codex debug models`, когда CLI доступен; если catalog недоступен, validator предупреждает и не делает automatic promotion mapping. Новый model ID в live catalog сначала попадает в proposal, исчезновение настроенной model и неподдерживаемый reasoning считаются routing risk, а sticky picker в VS Code или handoff, вставленный в уже открытую сессию, остаются manual boundary issues.

## Full handoff cockpit / панель полного handoff

Для больших ChatGPT handoff поверх Plan №5 runner добавлен beginner-first productization слой:

- `docs/operator/factory-template/05-orchestration-cockpit-lite.md` — как читать parent status, child tasks, blockers, deferred user actions, placeholder replacements и next action;
- `template-repo/template/.chatgpt/parent-orchestration-plan.yaml.template` — шаблон нормализации большого handoff в `codex-orchestration/v1`;
- `template-repo/template/.chatgpt/orchestration-cockpit.yaml` — lightweight status artifact;
- `template-repo/scripts/validate-parent-orchestration-plan.py`, `validate-orchestration-cockpit.py`, `explain-codex-route.py`, `validate-route-explain.py`, `validate-beginner-handoff-ux.py` — targeted проверки.

Этот слой не добавляет web app, daemon, SQLite, Telegram notifications или обязательный cloud director. Его задача проще: один handoff, понятная parent orchestration, наблюдаемые child tasks, честные boundaries и ясный closeout.

## Панель жизненного цикла проекта

Для общего состояния проекта добавлен repo-native lifecycle dashboard:

- `docs/operator/factory-template/06-project-lifecycle-dashboard.md` — как читать “что происходит сейчас”, blockers, next action, release/deploy/runtime state и improvement queue;
- `docs/operator/factory-template/07-beginner-visual-dashboard-ux.md` — beginner-first объяснение трех визуальных поверхностей;
- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` — canonical state artifact для generated проектов;
- `template-repo/template/.chatgpt/handoff-implementation-register.yaml` — register незакрытых ChatGPT handoff / Codex self-handoff задач с dependencies, evidence, replacement/superseded links и closeout status;
- `template-repo/scripts/render-project-lifecycle-dashboard.py` — Markdown/CLI renderer;
- `template-repo/scripts/validate-project-lifecycle-dashboard.py` — schema/status/evidence/boundary validator.
- `template-repo/scripts/validate-handoff-implementation-register.py` — validator register, который ловит false green, неизвестные dependencies, blocked-as-ready, несколько active handoff в одной group и secret-like content.

Dashboard агрегирует task/stage state, feature execution progress, orchestration cockpit, handoff implementation register, release readiness и runtime signals. Он не заменяет cockpit или operator dashboard и не добавляет heavy runtime. Advisory route text может быть показан как readout, но не считается auto-switch mechanism для уже открытой Codex-сессии.

Для новичка есть 3 визуальные поверхности:
- ChatGPT mini card — коротко показывает проект, фазу, активную задачу, статус, готово, блокеры, действие пользователя и следующий шаг;
- Codex execution card — показывает route receipt, текущую wave/task, progress, blockers, next internal action и verify/sync boundary;
- Markdown dashboard — полный отчет `reports/project-lifecycle-dashboard.md`.

## Standards navigator / контроль жизненного цикла по стандартам

Поверх lifecycle dashboard добавлен lightweight standards navigator:

- registry: `template-repo/standards/lifecycle-standards-registry.yaml`;
- phase map: `template-repo/standards/lifecycle-stage-map.yaml`;
- generated gates: `template-repo/template/.chatgpt/standards-gates.yaml`;
- validator: `template-repo/scripts/validate-standards-gates.py`;
- offline watchlist: `template-repo/scripts/check-standards-watchlist.py`.

Default profile для одного разработчика: `solo_lightweight`. Для commercial/production-critical проекта профиль эскалируется до `commercial_production`. Слой использует ISO/IEC/IEEE 12207, Scrum Guide/Kanban-lite, ISO 25010, NIST SSDF, OWASP ASVS, WCAG, DORA и AI safety overlay как evidence map, но не заявляет formal certification/compliance.

## Optional skills quality loop для skills

Для развития самого `factory-template` доступен облегченный advanced-контур для skills и prompt-like artifacts:

```text
создал -> протестировал -> улучшил trigger/usefulness
```

Он нужен, когда команда улучшает reusable template artifacts: `template-repo/skills/*`, scenario-pack, handoff/runbook/policy тексты или task templates.
Это не beginner default path и не обязательный шаг для первого проекта.

Основные артефакты:

- `template-repo/skills/skill-master-lite/SKILL.md` — создать или улучшить компактный skill/prompt artifact;
- `template-repo/skills/skill-tester-lite/SKILL.md` — проверить trigger, usefulness и границы применения;
- `docs/skills-quality-loop.md` — короткий operator guide с примером на artifact из `factory-template`.

`VALIDATE_FACTORY_TEMPLATE_OPS.sh` теперь проверяет не только структуру `sources-pack-*`, но и semantic profile repo-артефактов, если они используются как reference/export layer:

- `sources-pack-core-20` обязан содержать сценарное ядро, runbook layer и policy presets;
- `core-hot-15` обязан содержать ровно 15 hot-файлов reference-профиля;
- `core-hot-15` и companion archive остаются repo-side export-профилями, а не обязательным daily UI upload flow;
- `core-cold-5` обязан содержать ровно 5 cold/reference файлов без дублей hot-set;
- `sources-pack-release-20` обязан содержать release-facing docs и release scripts;
- `sources-pack-bugfix-20` обязан содержать launcher, validator layer и feedback/handoff validators.

## Repo-first правило для ChatGPT Project

Для проектов ChatGPT теперь каноничен repo-first режим:

- сценарии не хранятся внутри ChatGPT Project как основной источник правды;
- на каждый запрос сначала открывается GitHub repo проекта;
- первое обязательное действие: открыть `template-repo/scenario-pack/00-master-router.md`, прочитать его и действовать строго по маршруту;
- если router ведёт в другие сценарии, читать уже их и только потом отвечать.

Для `factory-template` canonical repo:

- `mppcoder/factory-template`

Во время первичной настройки ChatGPT Project это правило нужно внести именно в поле `Instructions` до первого рабочего запроса.
В `Instructions` должен быть явно указан repo `mppcoder/factory-template`, обязательное чтение `template-repo/scenario-pack/00-master-router.md` и запрет на сценарии "из памяти" или из текста внутри Project.

Риски этого контура:

- если в ChatGPT Project останется старый текст про `Sources` или старый staging-workflow, агент может пойти по неверному workflow;
- если repo-first инструкция не обновлена после смены repo/path, модель может читать не тот репозиторий;
- нельзя заменять чтение `00-master-router.md` пересказом по памяти.

## Каноническая sync-схема AGENTS

- root [AGENTS.md](/projects/factory-template/AGENTS.md) — persistent instruction для работы внутри самого `factory-template`;
- [template-repo/AGENTS.md](/projects/factory-template/template-repo/AGENTS.md) — canonical template source для downstream/battle repos;
- root `AGENTS.md` в боевом repo — materialized clone из `template-repo/AGENTS.md`, а не самостоятельный source of truth.

Для downstream repo разрешено менять только значение `SCENARIO_PACK_PATH`, если repo-local путь к scenario-pack отличается.

Канонический sync path для этого контура:

1. launcher создаёт initial root `AGENTS.md` через `template-repo/scripts/sync-agents.py`;
2. downstream refresh использует `factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh`;
3. `factory/producer/extensions/workspace-packs/factory-ops/factory-sync-manifest.yaml` разделяет impact на `template-owned-safe`, `template-owned-clone`, `template-owned-advisory`, `project-owned`, brownfield history и excluded `factory-producer-owned`;
4. `factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh --apply-safe-zones` materializes только generated safe-tier files в боевом repo;
5. `factory/producer/extensions/workspace-packs/factory-ops/check-template-drift.py` ловит отсутствие root clone и tiered drift относительно template source.

Human-readable upgrade/rollback операторский маршрут:

```bash
bash factory/producer/extensions/workspace-packs/factory-ops/export-template-patch.sh <factory-root> <downstream-root> --dry-run
python3 factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py <factory-root> <downstream-root> --format markdown --output UPGRADE_SUMMARY.md
bash factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --apply-safe-zones
bash factory/producer/extensions/workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --apply-safe-zones --with-project-snapshot
bash factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --check
bash factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback
bash factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback --restore-project-snapshot
```

Это не "магическое" обновление GitHub само по себе: sync происходит только как часть канонического template-sync/update flow внутри repo/tooling.

Policy detail: `docs/downstream-upgrade-policy.md`.

Состав archive pack и direct profile теперь берётся из единого declarative manifest:

- `factory/producer/packaging/sources/sources-profiles.yaml`

Phase recommendation теперь тоже декларативна:

- `controlled-fixes` -> `sources-pack-core-20.tar.gz`
- `release` -> `sources-pack-release-20.tar.gz`
- `bugfix-drift` -> `sources-pack-bugfix-20.tar.gz`

Автоопределение фазы теперь считается из `git status` и правил в `factory-template-ops-policy.yaml`.

Для `release` одной правки release-файлов недостаточно:

- detector смотрит на changed paths;
- и отдельно проверяет checked intent signals в `RELEASE_CHECKLIST.md`.

Для `bugfix-drift` тоже нужен не только file drift:

- detector смотрит на bug/validator changed paths;
- и отдельно проверяет intent signals внутри `reports/bugs/*.md`.

Проверить текущую рекомендацию можно так:

```bash
bash DETECT_FACTORY_TEMPLATE_PHASE.sh
bash PHASE_DETECTION_TEST.sh
```

Эта рекомендация автоматически попадает в `_sources-export/factory-template/SUMMARY.md` и `_boundary-actions/factory-template-boundary-actions.md`, но для ежедневной работы ChatGPT Project должен опираться на GitHub repo, а не на отдельный Drive/Sources sync-контур.
Перезаливка `Sources` не является обязательным release-step и допускается только как compatibility fallback для проектов, которые ещё не переведены на чистый repo-first режим.

Состав curated packs и параметры boundary-инструкций задаются декларативно в:

- `factory-template-ops-policy.yaml`
- `factory/producer/ops/templates/factory-template-boundary-actions.template.md`

Короткие release-facing operator docs:

- `RELEASE_CHECKLIST.md`
- `VERIFY_SUMMARY.md`
- `RELEASE_NOTE_TEMPLATE.md`
- `COMMIT_MESSAGE_GUIDE.md`
- `docs/releases/sources-pack-usage.md`

Короткая карта поддерживаемых режимов:

- `ENTRY_MODES.md`
- `docs/tree-contract.md`
- `docs/template-architecture-and-event-workflows.md`

Примечание по git sync в этом окружении:

- `git commit`, `git push`, `git fetch` и смену `origin` выполняйте последовательно
- если обычный `git push origin main` ведет себя нестабильно, используйте прямой SSH push на `git@github.com:mppcoder/factory-template.git`
- если нужен canonical verified path, используйте `bash VERIFIED_SYNC.sh`
- если после уже пройденного green verify остался только low-risk follow-up вроде `.gitignore` или небольших docs/closeout правок, `bash VERIFIED_SYNC.sh` может сам перейти в lightweight follow-up mode и закоммитить их без отдельного ручного подтверждения
- если нужен release path после отдельного решения, используйте `bash EXECUTE_RELEASE_DECISION.sh`

Для нового automation contour доступны validators:

- `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
- `bash VALIDATE_RELEASE_DECISION.sh`
- `bash VALIDATE_RELEASE_NOTES_SOURCE.sh`
- `bash VALIDATE_RELEASE_REPORT.sh`

## Что входит в релиз
- `template-repo/` — шаблон нового рабочего проекта.
- `project-knowledge/factory/template-evolution/` — историческая knowledge-зона развития фабрики, не отдельный root workflow.
- `factory/producer/reference/examples/` — примеры greenfield и brownfield проектов.
- `factory/producer/extensions/workspace-packs/factory-ops/` — optional operational-слой для drift, patch export и hooks.
- `factory/producer/registry/` — журнал версий фабрики и происхождения проектов.

## Что не должно попадать в релиз
- тестовые рабочие проекты;
- временные каталоги smoke/matrix прогонов;
- логи и служебные следы локальной сборки.

## Что нового в релизе 2.5.4
- Windows bootstrapper теперь по умолчанию предлагает настроить SSH key login без постоянного ввода пароля;
- installer создает или использует `%USERPROFILE%\\.ssh\\factory-template-vps-ed25519`;
- public key добавляется в VPS `~/.ssh/authorized_keys`, после чего installer использует `ssh.exe -i` и `scp.exe -i`;
- пароль VPS нужен один раз для установки public key, если passwordless SSH еще не настроен;
- fallback archive имена синхронизированы под `factory-v2.5.4.zip` + manifest + SHA256.

## Что нового в релизе 2.5.3
- Windows bootstrapper теперь явно рекомендует PowerShell 7 (`pwsh`) и показывает команду установки через `winget`;
- installer предлагает safe defaults: `SSH username=root`, `SSH port=22`, `TargetRoot=/projects/factory-template`, `IncomingDir=/projects/factory-template/_incoming`;
- fallback archive имена синхронизированы под `factory-v2.5.3.zip` + manifest + SHA256;
- `VPS host/IP` остается обязательным ручным вводом без default;
- `FactoryTemplateSetup.exe` по-прежнему future signed wrapper boundary, готовый exe не публикуется;
- npm path явно не заявляется, потому что repo не содержит `package.json`.

## Что нового в релизе 2.5.2
- release artifact включает Windows beginner bootstrapper MVP: `windows-bootstrap/install-windows.ps1`, remote installer, prompts, README и validator;
- GitHub clone/download из `mppcoder/factory-template` остается recommended install path;
- `windows-bootstrap/install-windows.ps1` является текущим executable MVP path для Windows-новичка;
- `FactoryTemplateSetup.exe` остается future signed wrapper boundary и не публикуется как готовый exe;
- fallback archive публикуется как `factory-v2.5.2.zip` + manifest + SHA256;
- npm path явно не заявляется, потому что repo не содержит `package.json`.

## Что нового в релизе 2.5.1
- release package assembly теперь создает archive, sidecar manifest и SHA256 checksum;
- install-from-scratch runbooks описывают canonical GitHub/release artifact path и fallback manual upload через `/projects/factory-template/_incoming`;
- package validator проверяет single root folder, forbidden paths, manifest, checksum и required files;
- npm path явно не заявляется, потому что repo не содержит `package.json`.

## Что нового в релизе 2.5.0
- `G25-GA` закрыт как passed на основании измеримых `M25-*` evidence;
- novice onboarding smoke теперь фиксирует duration и manual intervention count по каждому сценарию;
- добавлен consolidated KPI evidence: `docs/releases/2.5-ga-kpi-evidence.md`;
- добавлен validator `validate-25-ga-kpi-evidence.py`, который не дает включить `ga_ready: true` без измеримых артефактов;
- release docs, manifests, template metadata и examples синхронизированы под `factory-v2.5.0`.

## Программа релиза 2.5 (release truth)
- Release truth source: `docs/releases/release-scorecard.yaml`;
- Current 2.5 stage: `release publication / release artifact assembly`;
- Status: `2.5.4 Package Ready`;
- GA-ready: `true`;
- канонический план зафиксирован в `docs/releases/2.5-roadmap.md`;
- success metrics и пороги MVP/full 2.5 зафиксированы в `docs/releases/2.5-success-metrics.md`;
- трек `2.5-A` закрепляет engineering hardening (валидаторы, устойчивость, безопасные default paths);
- трек `2.5-B` закрепляет beginner-first productization (UI-friendly entry path, понятный onboarding, снижение порога входа);
- выпуск `2.5` закрыт как полный только после совместного подтверждения `2.5-A` и `2.5-B`.
- `G25-GA` прошел на `2026-04-26`, потому что full-KPI evidence добавлен и валидируется.

## Как читать release truth

Начинайте с `docs/releases/release-scorecard.yaml`. Это machine-readable release state, который используют pre-release и CI gates. Roadmap/current-state/README/checklist объясняют то же состояние для человека; `TEST_REPORT.md` фиксирует verification evidence и не должен считаться отдельным release-status source.

## Базовый функционал ветки 2.5
- `factory-template` поддерживает greenfield, brownfield без repo и brownfield с repo в одном repo-first контуре;
- advisory/policy layer и executable routing layer остаются явным образом разделены;
- defect-capture, handoff, self-handoff, verification, release-followup и completion package описаны как обязательные контуры;
- generated projects продолжают получать единый template/versioning/documentation layer;
- release-facing docs и packaging layer теперь описывают не только инструменты, но и полный жизненный цикл выпуска релиза.

## Известные ограничения
- quality-валидация остаётся эвристической, а не семантической;
- advisory/back-sync слой по-прежнему рассчитан на контролируемое применение, а не на безусловный sync всех зон;
- содержательное наполнение `user-spec`, `tech-spec`, `reality-check` требует сценарного слоя и участия пользователя.
- auto GitHub Release publication выполняется только при явном `release-decision.yaml` и доступном `gh auth`.


## Стандарт versioning/documentation layer

Во всех контурах используются одинаковые файлы:
- `VERSION.md`
- `CHANGELOG.md`
- `CURRENT_FUNCTIONAL_STATE.md`
- `.chatgpt/project-origin.md`

Это правило действует для фабрики, шаблона, greenfield-проектов и brownfield transition-проектов. После успешного transition бывший brownfield проект обслуживается как `greenfield-product`.
