# Smoke для artifact eval

Этот каталог хранит sample specs и static reports для optional advanced Artifact Eval Harness.

## Назначение

- `specs/` — machine-readable `artifact-eval/v1` specs.
- `reports/` — deterministic reports, сгенерированные из sample specs.
- quick verify запускает smoke в `/tmp` и валидирует static reports.

Beginner path этот каталог не использует.

## Plan №3 coverage

P3-S3 расширил набор beyond samples:

- master router и direct task self-handoff;
- normalized Codex handoff response;
- done closeout external actions ledger;
- downstream sync boundary;
- production VPS proof boundary;
- skill-tester-lite и feature-execution-lite.

Negative fixtures проверяют multi-block/file-based handoff, old live session auto-switch claims, dry-run production overclaim и done without final verification.
