# Release notes / заметки релиза

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
