# Release notes / заметки релиза

## 2.5 - GA No-Go (KPI evidence gap) - 2026-04-26

### Решение

`2.5` не объявляется GA. `G25-GA` заблокирован, потому что RC evidence зеленый, но full-KPI evidence не хватает для честного подтверждения порогов `docs/releases/2.5-success-metrics.md`.

### Что подтверждено

- RC closeout остается пригодным для downstream trial.
- Novice onboarding smoke и downstream upgrade UX evidence остаются полезными RC-артефактами.
- Открытых critical defects по текущим verification docs не выявлено.
- Repo-first routing для этого closeout соблюден: master router прочитан до implementation.

### Что блокирует GA

- нет timed first-success measurement для `M25-01`;
- нет controlled pilot completion rate для `M25-02`;
- нет manual intervention count для `M25-03`;
- нет downstream safe-sync success-rate population для `M25-04`;
- нет aggregate handoff rework-loop register для `M25-06`.

Blocker report: `reports/bugs/2026-04-26-25-ga-readiness-gap.md`.

## 2.5 - RC Closeout Candidate (not GA) - 2026-04-23

### О чём этот контур

Линия `2.5` остается dual-track программой:

- `2.5-A` — engineering hardening;
- `2.5-B` — beginner-first productization (UI-friendly и безопасный downstream UX).

Этот блок фиксирует не только framing, но и фактический RC closeout для downstream + novice acceptance.

### Что вошло в RC closeout

- human-readable downstream upgrade отчет: `workspace-packs/factory-ops/upgrade-report.py`;
- safe apply теперь сохраняет rollback state и backup для materialized safe-зон;
- safe apply дополнительно поддерживает full-project snapshot режим (`--with-project-snapshot`);
- rollback path: `workspace-packs/factory-ops/rollback-template-patch.sh --check|--rollback`;
- rollback path поддерживает full snapshot restore (`--restore-project-snapshot`) для mixed manual sessions;
- `check-template-drift.py` поддерживает human-readable отчет (`--format human`) и строгий режим (`--strict`);
- novice acceptance fixtures: `onboarding-smoke/run-novice-e2e.sh` + `onboarding-smoke/ACCEPTANCE_REPORT.md`;
- novice acceptance теперь включает post-bootstrap long-flow (`fill_smoke_artifacts` + `validate-evidence/quality/handoff/check-dod`);
- consolidated verify path (`template-repo/scripts/verify-all.sh ci`) теперь включает novice onboarding smoke перед `SMOKE/EXAMPLES/MATRIX`.

### Evidence RC verification / подтверждение RC

- `UPGRADE_SUMMARY.md` — dry-run/apply/rollback UX summary на реальном novice brownfield downstream;
- `onboarding-smoke/ACCEPTANCE_REPORT.md` — greenfield novice + brownfield novice сценарии зеленые;
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
- `workspace-packs/vscode-codex-bootstrap` заменяет dogfood naming в canonical workspace bootstrap слое;
- `optional-domain-packs/openclaw-reference` закрепляет `OpenClaw` как optional reference-case, а не как часть core factory tree;
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
