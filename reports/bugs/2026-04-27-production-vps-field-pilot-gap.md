# Bug report: production VPS field pilot gap

Дата: 2026-04-27

## Summary

Production VPS deploy path имел безопасные presets и dry-run, но не имел отдельного field pilot runbook/report mode, который честно разделяет dry-run evidence и реальный VPS proof.

## Evidence

- `docs/deploy-on-vps.md` описывал deploy, backups, health checks и rollback, но не давал цельного field pilot сценария `starter -> app-db -> reverse-proxy-tls -> backup -> healthcheck -> rollback drill`.
- Не было `docs/production-vps-field-pilot.md`.
- Не было `reports/release/production-vps-field-pilot-report.md`.
- `deploy-dry-run.sh`, `operator-dashboard.py` и `validate-operator-env.py` не умели писать dedicated field pilot report.
- Acceptance требовал не выдавать dry-run за production proof, но отдельного отчета для этого boundary не было.

## Impact

- Оператор мог принять локальный dry-run за завершенный production proof.
- DNS, firewall, Docker Compose, env secrets и backup restore checklist не были собраны в одном field pilot gate.
- Rollback drill был описан минимально, но не был зафиксирован как обязательный field pilot этап.
- Project Knowledge Done Loop не был явно применен к production VPS field pilot decisions/downstream impact/done evidence.

## Layer classification

- Advisory/policy layer: VPS docs, field pilot runbook, release report, TEST/CURRENT state.
- Executable routing/validation layer: deploy scripts, operator dashboard, env validator, quick verify smoke.
- Downstream-consumed template content: yes. Deploy scripts and docs are consumed by generated/downstream projects.

## Remediation

- Add dedicated field pilot runbook and release report.
- Add field pilot markdown report mode to dry-run/operator/env scripts.
- Keep starter as default and production presets opt-in.
- Add DNS/firewall/Docker/env/backup restore checklist and rollback drill.
- Add quick verify smoke for production report mode using fake Docker Compose only.
- Record Project Knowledge Done Loop decisions, rollback/backup выводы, downstream impact and done evidence in the release report.

## Status

Fixed in current scope as repo-controlled dry-run/report evidence. Real VPS deploy remains pending external approval/runtime access.
