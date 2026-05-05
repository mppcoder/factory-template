# Release notes / заметки релиза

## Unreleased / не выпущено

### О чём этот инкремент

Repo-native Universal Codex Handoff Factory MVP: шаблон получает единый `FT-TASK` слой для Codex-задач, понятный русскоязычный handoff flow и проверяемый dashboard/queue контур без daemon, web app, Telegram/Slack bot или background worker.

Advanced automation increment: поверх Universal Task Control добавлен bounded GitHub Issue -> gate -> normalized Codex handoff -> branch/PR substrate, Symphony-compatible workflow spec, bounded runner skeleton, repo-reviewed curator proposal loop и full advanced automation refusal gates.

Advanced automation hardening increment: добавлены synthetic/local issue-autofix dry-run proof, permission/label trust model, worktree isolation policy, append-only audit ledger, rollback recovery policy, curator promotion path, downstream sync package и final safety/readiness reports без включения full autonomous mode по умолчанию.

### Что вошло

- `task-registry.yaml`, allocator, issue bridge, handoff generator, handoff validator, preview/prepare/status/queue commands.
- GitHub Issue templates для основных task classes: bug, feature, docs, research, audit, release, downstream sync и curator.
- Русскоязычные operator docs: architecture overview и one-paste flow `ChatGPT -> Codex -> GitHub -> VPS`.
- Lifecycle dashboard показывает Universal Task Control без false green.
- `verify-all quick` включает Universal Task Control smoke и negative fixtures в `tests/universal-task-control/`.
- Downstream materialization теперь покрывает generated root layout: `.chatgpt/task-registry.yaml`, `scripts/*`, `.github/ISSUE_TEMPLATE/*.yml`, `docs/operator/universal-task-control.md`, `reports/handoffs/` и `reports/release/`.
- `verify-all quick` включает temporary generated-project smoke для allocate -> preview -> prepare pack -> `ready_for_codex` -> queue -> dashboard validation без запуска Codex и без GitHub API.
- Для existing downstream sync зафиксировано правило: `.chatgpt/task-registry.yaml` нельзя слепо перезаписывать, если там есть user tasks/evidence.
- Root и downstream получают `issue-autofix.yml`, safe issue gate, handoff renderer, bounded runner shell, support issue forms, label manifest, support automation docs и `SECURITY.md`.
- `WORKFLOW.md` фиксирует Symphony-compatible contract: GitHub Issues + task registry, max concurrency 1, branch per issue/task, terminal states, no auto-merge, no `pull_request_target`, untrusted issue text as data only.
- `bounded-task-runner.py` работает как dry-run / one-task skeleton и отказывается от unsafe parallel execution до worktree isolation.
- `factory-curator.py` создает repo-reviewed proposals в `reports/curator/` без hidden self-learning и без auto-apply.
- Full advanced automation gates документируют, что сейчас разрешены только dry-run/gated issue dispatch, PR creation, human review and one-task runner mode; production deploy, secrets, security issue autofix and auto-merge запрещены.
- `verify-all quick` включает validators для issue-autofix support, Symphony workflow, bounded runner, factory curator and advanced automation gates.
- Synthetic issue-autofix fixtures cover eligible docs/change input and refusal paths for `security`, `external-secret`, `blocked`, high risk without approval, missing acceptance criteria, PR targets, command-injection-like text and secret-like content.
- `issue-autofix-smoke.py` proves gate -> handoff -> `run.yaml` -> bounded runner dry-run -> ledger without live GitHub mutation.
- Permission/label model, worktree isolation, audit ledger, rollback and curator promotion policies are documented for root and downstream-generated surfaces where applicable.
- New validators cover labels/trust model, worktree isolation, ledger, rollback and curator promotion; `verify-all quick` runs them.

### Что проверять

- `python3 template-repo/scripts/validate-task-registry.py template-repo/template/.chatgpt/task-registry.yaml`
- `python3 template-repo/scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0001-codex-handoff.md`
- `python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`
- `bash template-repo/scripts/verify-all.sh quick`
- `reports/downstream-materialization/smoke-report.md`
- `python3 template-repo/scripts/validate-issue-autofix-support.py .`
- `python3 template-repo/scripts/validate-symphony-workflow.py .`
- `python3 template-repo/scripts/validate-bounded-runner.py .`
- `python3 template-repo/scripts/validate-factory-curator.py .`
- `python3 template-repo/scripts/validate-advanced-automation-gates.py .`
- `python3 template-repo/scripts/issue-autofix-smoke.py .`
- `python3 template-repo/scripts/validate-issue-autofix-labels.py .`
- `python3 template-repo/scripts/validate-worktree-isolation-policy.py .`
- `python3 template-repo/scripts/validate-automation-run-ledger.py .`
- `python3 template-repo/scripts/validate-automation-rollback.py .`
- `python3 template-repo/scripts/validate-curator-promotion-flow.py .`

## 2.5.8 - 2026-04-30

### О чём этот релиз

Patch release для Windows beginner onboarding: `WINDOWS_INSTALL_LATEST.md` выровнен по настоящей executable boundary. До запуска installer пользователь делает только PowerShell 7, download/verify/unzip latest package и запуск `windows-bootstrap/install-windows.ps1`; SSH/VPS setup остается автоматизацией installer; дальнейшая работа после handoff принадлежит Codex.

### Что вошло

- Pre-executable section теперь содержит только: PowerShell 7, latest package download, SHA256 verification, unzip и запуск executable path.
- Ручная настройка SSH до запуска installer не требуется и не описывается как отдельный user step.
- Installer-owned section описывает prompts и automation: `ssh.exe`/`scp.exe`/`ssh-keygen.exe` checks, existing SSH key check, public key install, remote repo install, quick verification and Codex prompt copy.
- Post-handoff section описывает Codex-owned работу: открыть router, пройти repo-first route, проверить git status и продолжать задачу внутри VPS repo.
- Archive + manifest + SHA256 fallback path: `factory-v2.5.8.zip`, `factory-v2.5.8.manifest.yaml`, `factory-v2.5.8.zip.sha256`.
- `FactoryTemplateSetup.exe` остается future signed wrapper boundary; готовый exe этот релиз не публикует.
- Npm install/download не поддерживается.

### Что проверять

- `python3 windows-bootstrap/tests/validate-windows-bootstrap.py .`
- `bash template-repo/scripts/verify-all.sh quick`
- `bash RELEASE_BUILD.sh _incoming/factory-v2.5.8.zip`
- `sha256sum -c _incoming/factory-v2.5.8.zip.sha256`
- `python3 template-repo/scripts/validate-release-package.py _incoming/factory-v2.5.8.zip --checksum _incoming/factory-v2.5.8.zip.sha256 --manifest _incoming/factory-v2.5.8.manifest.yaml`

## 2.5.7 - 2026-04-30

### О чём этот релиз

Patch release для Windows beginner onboarding: порядок в `WINDOWS_INSTALL_LATEST.md` исправлен так, чтобы пользователь сначала видел подготовительные шаги, затем скачивал/проверял latest package, и только потом отдельно запускал `windows-bootstrap/install-windows.ps1`.

### Что вошло

- Latest release download block только скачивает ZIP/manifest/SHA256, проверяет checksum, распаковывает и сохраняет путь к installer.
- Запуск `windows-bootstrap/install-windows.ps1` вынесен в отдельный шаг.
- Archive + manifest + SHA256 fallback path: `factory-v2.5.7.zip`, `factory-v2.5.7.manifest.yaml`, `factory-v2.5.7.zip.sha256`.
- `FactoryTemplateSetup.exe` остается future signed wrapper boundary; готовый exe этот релиз не публикует.
- Npm install/download не поддерживается.

## 2.5.6 - 2026-04-30

### О чём этот релиз

Patch release для Windows beginner onboarding: добавлен один файл `WINDOWS_INSTALL_LATEST.md` со ссылками и copy-paste PowerShell блоками, который скачивает latest GitHub Release без фиксированного номера версии.

### Что вошло

- `WINDOWS_INSTALL_LATEST.md` ведет нового пользователя от PowerShell 7 до запуска `windows-bootstrap/install-windows.ps1`.
- Download block использует GitHub API `releases/latest`, находит `factory-v*.zip`, manifest и SHA256 asset без hard-coded версии.
- ZIP проверяется через SHA256 перед распаковкой.
- Installer ищется рекурсивно как `windows-bootstrap/install-windows.ps1`, поэтому пользователю не нужно угадывать имя папки `factory-vX.Y.Z`.
- В инструкции явно описаны defaults: `SSH username=root`, `SSH port=22`, `TargetRoot=/projects/factory-template`, `IncomingDir=/projects/factory-template/_incoming`.
- SSH key login остается default-yes path; существующий ключ проверяется до изменения VPS `authorized_keys`.
- Archive + manifest + SHA256 fallback path: `factory-v2.5.6.zip`, `factory-v2.5.6.manifest.yaml`, `factory-v2.5.6.zip.sha256`.
- `FactoryTemplateSetup.exe` остается future signed wrapper boundary; готовый exe этот релиз не публикует.
- Npm install/download не поддерживается.

### Что проверять

- `python3 windows-bootstrap/tests/validate-windows-bootstrap.py .`
- `bash template-repo/scripts/verify-all.sh quick`
- `bash RELEASE_BUILD.sh _incoming/factory-v2.5.6.zip`
- `sha256sum -c _incoming/factory-v2.5.6.zip.sha256`
- `python3 template-repo/scripts/validate-release-package.py _incoming/factory-v2.5.6.zip --checksum _incoming/factory-v2.5.6.zip.sha256 --manifest _incoming/factory-v2.5.6.manifest.yaml`

## 2.5.5 - 2026-04-30

### О чём этот релиз

Patch release для Windows beginner bootstrapper: существующий SSH key теперь проверяется до изменения VPS `authorized_keys`, чтобы не просить пароль без необходимости.

### Что вошло

- Installer проверяет существующий key login через `ssh -o BatchMode=yes -i <key>`.
- Если ключ уже работает, `authorized_keys` не меняется и VPS password не запрашивается.
- Если private key есть, но `.pub` потерян, public key восстанавливается через `ssh-keygen.exe -y`.
- Если public key пришлось добавить на VPS, installer повторно проверяет key login после update.
- Archive + manifest + SHA256 fallback path: `factory-v2.5.5.zip`, `factory-v2.5.5.manifest.yaml`, `factory-v2.5.5.zip.sha256`.
- `FactoryTemplateSetup.exe` остается future signed wrapper boundary; готовый exe этот релиз не публикует.
- Npm install/download не поддерживается.

### Что проверять

- `python3 windows-bootstrap/tests/validate-windows-bootstrap.py .`
- `bash template-repo/scripts/verify-all.sh quick`
- `bash RELEASE_BUILD.sh _incoming/factory-v2.5.5.zip`
- `sha256sum -c _incoming/factory-v2.5.5.zip.sha256`
- `python3 template-repo/scripts/validate-release-package.py _incoming/factory-v2.5.5.zip --checksum _incoming/factory-v2.5.5.zip.sha256 --manifest _incoming/factory-v2.5.5.manifest.yaml`

## 2.5.4 - 2026-04-30

### О чём этот релиз

Patch release для Windows beginner bootstrapper: добавлен SSH key setup, чтобы пользователь не вводил VPS password на каждом `ssh/scp` шаге.

### Что вошло

- Installer по умолчанию спрашивает: `Set up SSH key login to avoid repeated password prompts? [Y/n]`.
- Создается или используется `%USERPROFILE%\\.ssh\\factory-template-vps-ed25519`.
- Public key добавляется в VPS `~/.ssh/authorized_keys`; пароль нужен один раз, если key login еще не настроен.
- После этого installer использует `ssh.exe -i` и `scp.exe -i`.
- Если пользователь пропускает key setup, installer предупреждает, что password prompts могут повторяться.
- Archive + manifest + SHA256 fallback path: `factory-v2.5.4.zip`, `factory-v2.5.4.manifest.yaml`, `factory-v2.5.4.zip.sha256`.
- `FactoryTemplateSetup.exe` остается future signed wrapper boundary; готовый exe этот релиз не публикует.
- Npm install/download не поддерживается.

### Что проверять

- `python3 windows-bootstrap/tests/validate-windows-bootstrap.py .`
- `bash template-repo/scripts/verify-all.sh quick`
- `bash RELEASE_BUILD.sh _incoming/factory-v2.5.4.zip`
- `sha256sum -c _incoming/factory-v2.5.4.zip.sha256`
- `python3 template-repo/scripts/validate-release-package.py _incoming/factory-v2.5.4.zip --checksum _incoming/factory-v2.5.4.zip.sha256 --manifest _incoming/factory-v2.5.4.manifest.yaml`

## 2.5.3 - 2026-04-30

### О чём этот релиз

Patch release для Windows beginner bootstrapper UX: PowerShell 7 recommendation, safe default prompt values and `factory-v2.5.3` fallback artifact names.

### Что вошло

- `windows-bootstrap/install-windows.ps1` рекомендует PowerShell 7 (`pwsh`) и показывает `winget install --id Microsoft.PowerShell --source winget`.
- Installer предлагает safe defaults: `SSH username=root`, `SSH port=22`, `TargetRoot=/projects/factory-template`, `IncomingDir=/projects/factory-template/_incoming`.
- `VPS host/IP` остается обязательным ручным вводом без default.
- Archive + manifest + SHA256 fallback path: `factory-v2.5.3.zip`, `factory-v2.5.3.manifest.yaml`, `factory-v2.5.3.zip.sha256`.
- `FactoryTemplateSetup.exe` остается future signed wrapper boundary; готовый exe этот релиз не публикует.
- Npm install/download не поддерживается.

### Что проверять

- `python3 windows-bootstrap/tests/validate-windows-bootstrap.py .`
- `bash template-repo/scripts/verify-all.sh quick`
- `bash RELEASE_BUILD.sh _incoming/factory-v2.5.3.zip`
- `sha256sum -c _incoming/factory-v2.5.3.zip.sha256`
- `python3 template-repo/scripts/validate-release-package.py _incoming/factory-v2.5.3.zip --checksum _incoming/factory-v2.5.3.zip.sha256 --manifest _incoming/factory-v2.5.3.manifest.yaml`

## 2.5.2 - 2026-04-30

### О чём этот релиз

Patch release для публикации downloadable `factory-template` artifact с Windows beginner bootstrapper MVP из commit `02c517fcad5562412c1f06e682251f71e0e7babf`.

### Что вошло

- В release package включен `windows-bootstrap/`: PowerShell entrypoint `install-windows.ps1`, remote bash installer, prompts, README, build boundary для будущего `FactoryTemplateSetup.exe` и targeted validator.
- Recommended install path остается GitHub clone/download из `mppcoder/factory-template`.
- `windows-bootstrap/install-windows.ps1` является текущим executable MVP path для новичка на Windows.
- `FactoryTemplateSetup.exe` зафиксирован только как future signed wrapper boundary; готовый exe этот релиз не публикует.
- Archive + manifest + SHA256 остаются fallback path: `factory-v2.5.2.zip`, `factory-v2.5.2.manifest.yaml`, `factory-v2.5.2.zip.sha256`.
- Npm install/download не поддерживается: в repo нет `package.json` и npm packaging contract.

### Что проверять

- `python3 windows-bootstrap/tests/validate-windows-bootstrap.py .`
- `bash template-repo/scripts/verify-all.sh quick`
- `bash RELEASE_BUILD.sh _incoming/factory-v2.5.2.zip`
- `sha256sum -c _incoming/factory-v2.5.2.zip.sha256`
- `python3 template-repo/scripts/validate-release-package.py _incoming/factory-v2.5.2.zip --checksum _incoming/factory-v2.5.2.zip.sha256 --manifest _incoming/factory-v2.5.2.manifest.yaml`

## 2.5.1 - 2026-04-29

### О чём этот релиз

Patch release для проверяемой установки `factory-template` с нуля. Изменение release-facing: пакет теперь собирается как archive + manifest + SHA256 и имеет отдельный validator для уже собранного zip.

### Что вошло

- `RELEASE_BUILD.sh` расширен без замены builder path: собирает `factory-v2.5.1.zip`, `factory-v2.5.1.manifest.yaml` и `factory-v2.5.1.zip.sha256`.
- Добавлен `template-repo/scripts/validate-release-package.py` для проверки single root folder, forbidden/transient paths, embedded/sidecar manifest, checksum и required files.
- Release artifact refresh: install ZIP теперь содержит ASCII-only archive paths; `bootstrap/*.md` нормализуются внутри staging archive, чтобы обычные GUI/Windows archive tools не падали на filename encoding.
- Release artifact refresh: install ZIP больше не включает transient `.tmp-run/` smoke trees и проходит portable path-length gate (`max_archive_path_length: 180`).
- User/Codex install-from-scratch runbooks описывают canonical GitHub clone/download или release artifact path и fallback manual upload через `/projects/factory-template/_incoming`.
- Npm path явно не заявляется: в repo нет `package.json` и npm packaging contract.

### Что проверять

- `bash RELEASE_BUILD.sh`
- `sha256sum -c factory-v2.5.1.zip.sha256`
- `python3 template-repo/scripts/validate-release-package.py <archive> --checksum <sha256> --manifest <manifest>`
- `python3` zip inspection: `NON_ASCII_COUNT=0`
- `python3` zip inspection: `TMP_RUN_COUNT=0`, `MAX_PATH_LEN <= 180`
- Распаковка в temp, `bash POST_UNZIP_SETUP.sh`, targeted package validation и `bash template-repo/scripts/verify-all.sh quick`.

## Не выпущено - handoff implementation control

- Добавлен repo-native register `.chatgpt/handoff-implementation-register.yaml` для ChatGPT handoff / Codex self-handoff задач, которые нельзя терять между чатами.
- Project Lifecycle Dashboard теперь показывает handoff implementation control cards: queued/ready, blocked by dependencies, prerequisite blockers, in progress, implemented but not verified, stale без свежего evidence и closed/not applicable.
- Validator `validate-handoff-implementation-register.py` ловит green status без evidence, `not_applicable` без reason/evidence, unknown dependencies, blocked item ошибочно показанный как ready и secret-like content.
- Если новый handoff заменяет старый handoff той же задачи в текущем чате, старый item списывается как `superseded` с `superseded_by`, `replacement_reason` и evidence; validator запрещает несколько active handoff в одной `handoff_group`.
- Register не заменяет `.chatgpt/handoff-rework-register.yaml`: rework register остается KPI по rework loops, новый register отвечает за lifecycle реализации handoff/self-handoff задач.
- Handoff route/model/reasoning остаются readout: dashboard/register не обещают auto-switch внутри уже открытой Codex-сессии.
- Cleanup fix: `_artifacts` теперь очищается перед release audit, чтобы stale generated release/source packs не ломали `PRE_RELEASE_AUDIT`.

## Не выпущено - runbook package layer

- Intake UX стал recommendation-first: после команды `новый проект` пользователь выбирает `default_decision_mode`, затем ChatGPT Project предлагает safe defaults, объясняет их и дает override path.
- Generated intake/handoff state теперь должен фиксировать `default_decision_mode`, accepted defaults, overrides, default source basis, uncertainty notes и decisions requiring explicit confirmation.
- Greenfield path теперь явно выглядит так: `новый проект` -> выбор default-decision mode -> recommendation-first опрос -> generated Codex handoff.
- Brownfield packages получили аналогичный default-decision layer: keep existing repo/no overwrite/evidence-first audit для with-repo и `_incoming` plus reconstruction inside target root для without-repo.
- Validators блокируют отсутствие default-decision state, forced defaults без override path и silent default для risky/paid/destructive/security/privacy/legal/secret decisions.
- Runbook packages теперь переписаны как beginner zero-to-Codex-ready flow: user-only setup заканчивается remote Codex takeover, а install/clone/bootstrap/verify/dashboard/sync выполняет Codex.
- `factory-template` user-runbook получил copy-paste шаги `FT-000`..`FT-180`: ChatGPT, GitHub, VS Code, Codex app/CLI, Timeweb VPS Ubuntu 24.04, SSH key/config, `ssh factory-vps`, два Codex contours, `FT-170` one-block handoff takeover и `FT-180` диагностику.
- Codex-runbook теперь явно автоматизирует VPS preflight, system packages, Node/npm/Codex CLI, GitHub CLI, `/projects/factory-template`, clone `mppcoder/factory-template`, targeted/quick verify, dashboard update и verified sync.
- Validator `validate-runbook-packages.py` теперь ловит abstract-only package regressions: отсутствие `USER-ONLY SETUP`, `CODEX-AUTOMATION`, takeover point, beginner step cards и обязательных factory setup steps.
- Чеклист factory-template теперь является таблицей-зеркалом user-runbook и не содержит process/meta checks; dashboard показывает `current_step`, `active_contour`, `takeover_ready` и `checklist_path`.
- Greenfield package boundary исправлен: пользователь больше не создает GitHub repo, не добавляет `origin`, не делает first push и не запускает launcher/verify. Codex делает это сам и готовит текст repo-first инструкции для ChatGPT Project.
- Greenfield package теперь не стартует напрямую в Codex: новый боевой проект начинается в ChatGPT Project шаблона фабрики командой `новый проект`; после scenario-pack опроса ChatGPT Project формирует стартовый Codex handoff.
- Greenfield ChatGPT Project boundary уточнен: Codex готовит repo-first instruction и пошаговую UI-инструкцию, а пользователь сам создает боевой ChatGPT Project, открывает Project settings/instructions, вставляет готовый текст и сохраняет настройки.
- Добавлен полный слой `docs/operator/runbook-packages/` для четырех входов: сам `factory-template`, чистый `greenfield-product`, brownfield with repo -> greenfield и brownfield without repo -> greenfield.
- Каждый package разделяет Browser ChatGPT Project, VS Code Remote SSH, Codex chat, terminal fallback, GitHub/external UI, secrets и approvals.
- Brownfield packages закрепляют продуктовую логику: brownfield является только transitional path, а done требует conversion в `greenfield-product` / `greenfield-converted` или explicit documented blocker.
- Добавлен validator `validate-runbook-packages.py` и quick verify coverage для package existence, command/path lint, dashboard contract, archive/cleanup wording, handoff language contract и запрета fake auto-switch claims.
- Lifecycle dashboard получил `runbook_packages` readout с phase, gates, blockers и next action без добавления web app/daemon/SQLite/Telegram stack.
- Lifecycle dashboard для `02-greenfield-product` теперь фиксирует `chatgpt_project_ui_owner: user`, `repo_first_instruction_prepared_by: codex` и `repo_first_instruction_pasted_by: user`.
- Source manifest получил отдельный `sources-pack-runbook-packages` для полного package export.

## Не выпущено - Plan №6 orchestration productization

- Добавлен beginner-first слой для full handoff UX поверх Plan №5: cockpit-lite, parent plan normalization, route explanation, UX scorecard и safe synthetic rehearsal.
- Cockpit показывает parent handoff id, child tasks, selected profile/model/reasoning, status, blockers, deferred user actions, placeholder replacements и next action без web app, daemon, SQLite, Telegram stack или background-worker promises.
- Parent plan template and validator wrapper make a large ChatGPT handoff checkable as `codex-orchestration/v1` before child session artifacts are written.
- Route explanation is deterministic keyword/rule-based, names evidence and live catalog boundary, and does not claim semantic classifier or advisory auto-switch.
- Beginner full handoff UX scorecard checks one copy-paste block, no file-based handoff, no hidden second operator shell step, no fake auto-switch claims, owner boundaries, Russian human-readable layer and final continuation outcome.
- Safe rehearsal remains synthetic/repo-local: no secrets, no real VPS mutation and no real downstream/battle app proof claim.

## Не выпущено - Plan №5 internal hardening

- Добавлен VPS Remote SSH-first Full Handoff Orchestration Layer: operator runbook, dry-run parent runner, per-subtask session files and parent report.
- Добавлено правило `user_actions_policy: defer-to-final-closeout`: пользовательские действия и реальные external values уходят в конец parent plan, а временные заглушки фиксируются в финальных напоминаниях о замене.
- Codex App/Cloud Director закреплен как optional path, not default; default workflow остается VS Code Remote SSH to VPS plus repo-native Codex CLI sessions.
- Добавлены validators и fixtures для explicit child routing, one-block handoff, secret boundary and curated/reference pack quality.
- Добавлен sync fallback evidence report без изменения stable sync logic.
- Добавлен domain scenario acceptance template beyond parity smoke; real downstream pilots остаются future external contour.

## Не выпущено - post-2.5 planning

- Добавлены roadmaps `2.5.1` и `2.6`: `2.5.1` ограничен stabilization/bugfix/docs/field proof, а `2.6` получает production VPS runtime proof, расширенный Artifact Eval Harness, adoption `feature-execution-lite` и runtime/source-hygiene backlog.
- Добавлен `docs/releases/post-2.5-gap-register.md`, который отделяет completed repo-controlled/synthetic proof от pending external runtime proof.
- Зафиксировано сравнение с `pavel-molyanov/molyanov-ai-dev`: что уже адаптировано, что полезно для 2.6 и что намеренно не переносится из Claude-specific execution model.
- Новый release-ready статус не объявлен: `docs/releases/release-scorecard.yaml` остается source of truth для `2.5.0 GA Ready`.

## Не выпущено - архитектура brownfield transition

- `factory-template` теперь описан как обычный `greenfield-product`, чей продукт — project factory, с дополнительным factory producer layer.
- Brownfield без repo и brownfield с repo закреплены как transitional adoption paths, а не финальные project classes.
- Успешный brownfield adoption должен завершаться active profile `greenfield-product`, recommended mode `greenfield` и lifecycle state `greenfield-converted`.
- Добавлены validators для brownfield transition и greenfield conversion; они подключены к quick verify и matrix.
- Sync manifest защищает brownfield history/project-owned zones и исключает factory-producer-owned paths из battle project sync.

## Не выпущено - physical root normalization

- Старые factory-only и historical top-level folders убраны из root: `.dogfood-bootstrap`, `factory_template_only_pack`, `meta-template-project`, `onboarding-smoke`, `optional-domain-packs`, `packaging`, `registry`, `working-project-examples`, `workspace-packs`.
- Factory-producer-owned слой теперь физически ограничен `factory/producer/*`: `ops`, `packaging`, `registry`, `sync`, `reference`, `extensions`, `archive`, `release`.
- Smoke harness перенесен в `tests/onboarding-smoke/`, а validator tree contract теперь запрещает старые active root paths и блокирует `factory/producer/*` в generated/battle projects.

## Не выпущено - language contract для handoff

- Generated handoff теперь явно содержит `Язык ответа Codex: русский`.
- Codex handoff instructs: отвечать пользователю по-русски, английский оставлять только для technical literal values.
- Validators блокируют англоязычные labels `Repo:`, `Goal:`, `Entry point:`, `Scope:` в copy-paste handoff.

## 2.5.0 - 2026-04-26

### Решение release

`2.5` объявляется GA-ready. `G25-GA` закрыт после добавления измеримых full-KPI evidence для всех `M25-*` метрик.

### Что подтверждено для GA

- `M25-01`: novice path фиксирует time-to-first-success ниже `25` минут.
- `M25-02`: controlled pilot checklist фиксирует `9/9`, `100%`.
- `M25-03`: manual intervention count равен `0`.
- `M25-04`: downstream safe-sync report фиксирует `6/6`, `100%`.
- `M25-05`: открытых critical defects в текущем verification scope нет.
- `M25-06`: handoff rework loops не превышают `1`.
- `M25-07`: release-facing docs синхронизированы с scorecard.
- `M25-08`: repo-first routing соблюден.

### Что добавлено

- `docs/releases/2.5-ga-kpi-evidence.md`;
- `reports/release/2.5-controlled-pilot-checklist.md`;
- `reports/release/2.5-downstream-safe-sync-report.md`;
- `.chatgpt/handoff-rework-register.yaml`;
- `template-repo/scripts/validate-25-ga-kpi-evidence.py`.

Blocker report `reports/bugs/2026-04-26-25-ga-readiness-gap.md` закрыт как remediated.

## 2.5 - RC Closeout Candidate (not GA) - 2026-04-23

### О чём этот контур

Линия `2.5` остается dual-track программой:

- `2.5-A` — engineering hardening;
- `2.5-B` — beginner-first productization (UI-friendly и безопасный downstream UX).

Этот блок фиксирует не только framing, но и фактический RC closeout для downstream + novice acceptance.

### Что вошло в RC closeout

- human-readable downstream upgrade отчет: `factory/producer/extensions/workspace-packs/factory-ops/upgrade-report.py`;
- safe apply теперь сохраняет rollback state и backup для materialized safe-зон;
- safe apply дополнительно поддерживает full-project snapshot режим (`--with-project-snapshot`);
- rollback path: `factory/producer/extensions/workspace-packs/factory-ops/rollback-template-patch.sh --check|--rollback`;
- rollback path поддерживает full snapshot restore (`--restore-project-snapshot`) для mixed manual sessions;
- `check-template-drift.py` поддерживает human-readable отчет (`--format human`) и строгий режим (`--strict`);
- novice acceptance fixtures: `tests/onboarding-smoke/run-novice-e2e.sh` + `tests/onboarding-smoke/ACCEPTANCE_REPORT.md`;
- novice acceptance теперь включает post-bootstrap long-flow (`fill_smoke_artifacts` + `validate-evidence/quality/handoff/check-dod`);
- consolidated verify path (`template-repo/scripts/verify-all.sh ci`) теперь включает novice onboarding smoke перед `SMOKE/EXAMPLES/MATRIX`.

### Evidence RC verification / подтверждение RC

- `UPGRADE_SUMMARY.md` — dry-run/apply/rollback UX summary на реальном novice brownfield downstream;
- `tests/onboarding-smoke/ACCEPTANCE_REPORT.md` — greenfield novice + brownfield novice сценарии зеленые;
- `TEST_REPORT.md` — обновлен под beginner-first acceptance и downstream hardening, а не только process/docs polish.

### Статус готовности

- `2.5` как GA-релиз не объявлен;
- RC candidate готов для downstream trial;
- переход к GA возможен только после дальнейшего подтверждения KPI из `docs/releases/2.5-success-metrics.md`.

## 2.4.4 - 2026-04-22

### О чём этот релиз

Релиз `2.4.4` приводит `factory-template` к семантически чистой универсальной иерархии.
Главная цель релиза: убрать product-specific naming из canonical core/release-facing слоя, синхронизировать presets, manifests и docs tree, а domain-specific reference-cases отделить от core без потери compatibility.

### Что вошло

- canonical preset naming переведён на универсальные factory names:
  - `greenfield-product`
  - `brownfield-without-repo`
  - `brownfield-with-repo-modernization`
  - `brownfield-with-repo-integration`
  - `brownfield-with-repo-audit`
- `factory/producer/extensions/workspace-packs/vscode-codex-bootstrap` заменяет dogfood naming в canonical workspace bootstrap слое;
- `factory/producer/reference/domain-packs/openclaw-reference` закрепляет `OpenClaw` как optional reference-case, а не как часть core factory tree;
- release docs, manifests, template metadata, examples и `.chatgpt` closeout artifacts синхронизированы под `2.4.4`;
- launcher/runtime сохраняют compatibility aliases для legacy preset names, чтобы переход не ломал existing downstream flows.
- cleanup path теперь также убирает `.factory-runtime`, чтобы pre-release audit не наследовал stale runtime reports между verify/release циклами.
- verified-sync/release automation теперь устойчиво обрабатывает non-ASCII git paths, встречающиеся в repo bootstrap/docs слоях.

### Архитектурные изменения в документации

- canonical release-facing tree теперь явно отделяет:
  - core factory layers;
  - universal template source;
  - greenfield;
  - brownfield with repo;
  - brownfield without repo;
  - optional domain references;
- release-facing naming больше не закрепляет dogfood/openclaw как canonical структуру фабрики;
- advisory/policy layer и executable routing layer по-прежнему описаны раздельно, но теперь это согласовано с новой физической и логической иерархией.

### Что важно для downstream

- для downstream/battle repos canonical docs и presets теперь должны использовать новые neutral names;
- legacy preset names допускаются только как compatibility aliases и не считаются release-facing canon;
- optional domain references должны жить вне core naming и не маскироваться под обязательный factory layer;
- обновление `Sources` по-прежнему не требуется по умолчанию и используется только как compatibility fallback, если такой contour ещё сохранён.

### Проверка и выпуск

Релизный пакет рассчитан на прохождение:

- `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- `bash SMOKE_TEST.sh`
- `bash EXAMPLES_TEST.sh`
- `bash MATRIX_TEST.sh`
- `bash CLEAN_VERIFY_ARTIFACTS.sh`
- `bash PRE_RELEASE_AUDIT.sh`
- `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
- `bash VALIDATE_RELEASE_DECISION.sh`
- `bash VALIDATE_RELEASE_NOTES_SOURCE.sh`

### Ограничения

- semantic quality проверки по-прежнему частично эвристические;
- публикация GitHub Release зависит от доступности и авторизации `gh`;
- release-facing reference layer остаётся живым каноном и требует синхронного обновления при следующих process changes;
- compatibility aliases пока сохраняются, поэтому legacy names ещё могут встречаться в historical registry data и migration notes.
