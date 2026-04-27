# Отчет downstream multi-cycle sync

Дата проверки: 2026-04-27.

## Вердикт

`passed`: downstream sync v3 выдержал synthetic multi-cycle proof без перезаписи project-owned зон.

## Проверенные циклы

1. Первичная template sync: safe-generated/safe-clone drift был обнаружен и применен controlled apply.
2. Ручные project-owned edits: live `work/`, advisory `project-knowledge/`, `deploy/.env`, `.factory-runtime/` и local field-pilot transcript получили ручные маркеры.
3. Safe-generated update: template-owned `.chatgpt/examples`, `work-templates`, root `AGENTS.md`, deploy preset и deploy script применились.
4. Advisory review: production VPS field pilot docs/report и `project-knowledge/project.md` появились только как review-only targets и не были применены автоматически.
5. Rollback: rollback metadata version 3 был создан после нескольких циклов, `--rollback --restore-project-snapshot` восстановил pre-apply snapshot.
6. Brownfield conversion: `converted_greenfield` сохранил real brownfield history, safe-зоны продолжили обновляться.

## Evidence / проверочные факты

- Cycle 1 generated safe targets: `5`.
- Cycle 3 generated safe targets: `5`.
- Cycle 3 advisory targets: `docs/deploy-on-vps.md, docs/production-vps-field-pilot.md, project-knowledge/project.md, reports/release/production-vps-field-pilot-report.md`.
- Rollback tracked safe files: `.chatgpt/examples/done-report.example.md, AGENTS.md, deploy/presets/starter.yaml, scripts/deploy-dry-run.sh, work-templates/user-spec.md.template`.
- Brownfield lifecycle status: `converted_greenfield`.
- Brownfield preview items protected: `2`.

## Production VPS field-pilot boundary / граница field pilot

- Safe/template-owned apply: `deploy/.env.example`, compose files, deploy presets, `scripts/deploy-dry-run.sh`, `scripts/deploy-local-vps.sh`, `scripts/operator-dashboard.py`, `scripts/validate-operator-env.py`, `scripts/preflight-vps-check.py`.
- Review-only: `docs/deploy-on-vps.md`, `docs/production-vps-field-pilot.md`, `reports/release/production-vps-field-pilot-report.md`.
- Manual-only/protected: `deploy/.env`, `.factory-runtime/`, local field-pilot transcripts, backup/rollback runtime transcripts, real VPS approval boundary and secrets.

## Честное ограничение

Это synthetic repo-controlled proof. Он не заменяет реальный production VPS deploy, backup restore test или rollback drill: эти действия требуют отдельного user approval, доступа к VPS и ручного secrets/runtime boundary.
