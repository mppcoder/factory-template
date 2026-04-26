# Карта изменений: OpenClaw+

Дата: 2026-04-26

## Известные change signals

Источник: filesystem evidence и `KNOWN-BUGS.md`.

## Runtime-изменения

Признаки ручных runtime изменений:
- множество `/root/.openclaw/openclaw.json.bak*`;
- backup hooks в `/root/.openclaw/hooks/pre-execution/`;
- session archives и `.deleted.*` files under `/root/.openclaw/agents/*/sessions/`;
- live sqlite state under `flows`, `tasks`, `memory`.

Решение:
- runtime changes пока не реконструировать как source;
- использовать как evidence для отдельных defect investigations;
- active source candidate брать только после redaction/review.

## Package-изменения

Признаки ручных package fixes:
- `KNOWN-BUGS.md` описывает install/runbook fixes и фактические обходы;
- backup-файлы в `accounts/`, `scripts/`, `telemetry/`, `wrappers/delegate-specialist-plugin/`;
- docs/runbooks содержат post-install audit notes;
- validators отражают фактические smoke/live checks.

Решение:
- active package files включать в source candidate allowlist;
- backup files вынести в evidence triage;
- generated dependency zones исключить.

## Карта рисков

| Риск | Где | Решение |
| --- | --- | --- |
| secret leakage | `/etc/openclaw-plus.env`, credentials/identity/telegram | redacted inventory only |
| oversized repo | `.venvs`, `node_modules` | denylist |
| source vs backup confusion | `*.bak*` | evidence triage |
| runtime mutation import | sqlite/jsonl/logs | denylist |
| docs drift | `README.md` слабый, `KNOWN-BUGS.md` богатый | использовать architecture/runbooks/known-bugs/validators |

## Следующий этап

После подтверждения allowlist/denylist можно собрать redacted source pack в dedicated project root внутри `/projects/<project-root>/...`.
