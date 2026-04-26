# Реестр gap для brownfield: OpenClaw+

Дата: 2026-04-26

## GAP-001: входные корни не являются git repo

Severity: high

Evidence:
- `/root/.openclaw`: `fatal: not a git repository`
- `/root/openclaw-plus`: `fatal: not a git repository`

Impact:
- нет commit history;
- нет branch boundary;
- нельзя безопасно отличить source, generated state и ручные hotfixes;
- remediation без reconstruction может потерять рабочие изменения.

Decision:
- до любых изменений нужен source reconstruction plan.

Status: open

## GAP-002: package root содержит тяжелые generated/dependency зоны

Severity: medium

Evidence:
- `/root/openclaw-plus/.venvs`: `5.1G`
- `/root/openclaw-plus/wrappers`: `2.2G`
- всего package root: `7.3G`

Impact:
- naive archive/git import создаст шумный и тяжелый repo;
- dependency artifacts могут скрыть фактический source layer.

Decision:
- reconstruction должен явно исключать `.venvs/`, `node_modules/`, cache/pyc и другие generated artifacts.

Status: open

## GAP-003: присутствует много backup-файлов после ручных фиксов

Severity: medium

Evidence:
- множественные `/root/.openclaw/openclaw.json.bak*`
- backup-файлы в hooks, accounts, scripts, telemetry, wrappers

Impact:
- backup-файлы являются evidence для change history, но не обязательно source-of-truth;
- без triage можно восстановить устаревшую или конфликтующую версию.

Decision:
- создать отдельный backup triage pass: keep as evidence vs source candidate vs discard from source pack.

Status: open

## GAP-004: README не является достаточным source-of-truth

Severity: low

Evidence:
- `/root/openclaw-plus/README.md` содержит только одну строку про visible format.
- основная архитектура и known bugs находятся в отдельных файлах.

Impact:
- новый оператор не восстановит систему по README;
- source-of-truth нужно нормализовать через docs/runbooks.

Decision:
- использовать `ARCHITECTURE.md`, `RUNBOOK-*`, `KNOWN-BUGS.md`, validators и фактический runtime как primary evidence.

Status: open

## GAP-005: live validator обнаружил context bloat warning

Severity: medium

Evidence:
- `validators/run-final-acceptance.sh` завершился OK.
- `validators/live/28-token-memory-check.sh` выдал `[WARN] duplicated content detected (context bloat)`.

Impact:
- acceptance green не равен отсутствию runtime quality risk;
- warning может быть symptom of memory/log duplication.

Decision:
- до remediation создать отдельный structured defect report, если scope field test будет расширен до runtime quality fixes.

Status: open

## GAP-006: секреты и runtime state находятся вне repo boundary

Severity: high

Evidence:
- `/etc/openclaw-plus.env` существует и содержит integration secrets.
- `/root/.openclaw/credentials/`, `/root/.openclaw/identity/`, `/root/.openclaw/telegram/` существуют.

Impact:
- source pack нельзя собирать naive-copy;
- нужно явно отделить secret-bearing runtime state от reconstructable source.

Decision:
- все exports должны использовать redaction/allowlist; секреты не переносить в repo.

Status: open

## GAP-007: generated direct-task response не прошел response-format validator

Severity: medium

Evidence:
- `python template-repo/scripts/validate-handoff-response-format.py .chatgpt/direct-task-response.md` сначала вернул ошибку.
- Валидатор ожидал ровно один блок `## Handoff в Codex`, `## Применение в Codex UI` и `## Строгий launch mode (опционально)`.
- Сгенерированный direct-task response был оформлен как набор self-handoff секций и не соответствовал publishable response contract.

Impact:
- прямой visible self-handoff мог быть невалиден как user-facing handoff package;
- это reusable template/handoff formatting issue.

Decision:
- в текущем scope `.chatgpt/direct-task-response.md` нормализован вручную под validator contract.
- отдельный script-level remediation пока не выполнялась, потому что текущий field test не меняет template launcher/generator.

Status: fixed-in-current-scope for artifact; open for reusable generator remediation
