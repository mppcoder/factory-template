# Bug report: Project Knowledge Done Loop gap

Дата: 2026-04-27

## Summary

Feature closeout мог завершаться без явного чтения `user-spec`, `tech-spec` и `decisions.md`, без Project Knowledge update proposal, без archive evidence и без downstream impact note.

## Evidence

- `template-repo/scenario-pack/16-done-closeout.md` требовал обновлять `project-knowledge/` и `work/completed/`, но не задавал проверяемый artifact contract для feature workspace.
- До remediation не было `template-repo/scripts/close-feature-workspace.py`.
- До remediation не было `template-repo/scripts/validate-project-knowledge-update.py`.
- `/done` в `pavel-molyanov/molyanov-ai-dev` читает `user-spec`, `tech-spec`, `decisions.md`, обновляет Project Knowledge и архивирует feature; factory-template не имел сопоставимого machine-checkable loop.

## Impact

- Decisions могли остаться только в чате или рабочем workspace.
- Project Knowledge update мог быть пропущен или выполнен неявно.
- Feature archive мог не содержать done evidence.
- Downstream sync/review effect оставался незафиксированным.
- Для `feature-execution-lite` final verification и artifact-eval evidence могли не попасть в done evidence.

## Layer classification

- Advisory/policy layer: docs and Project Knowledge templates.
- Executable routing/validation layer: closeout script, validator, DoD/verify integration.
- Downstream-consumed template content: yes, because `template-repo/template/project-knowledge/*` and `work-templates/decisions.md.template` changed.

## Remediation

- Add factory-native closeout script.
- Add validator for done report, decisions, Project Knowledge proposal, archive/blocker and downstream impact note.
- Add `feature-execution-lite` evidence checks and artifact-eval link/justification.
- Add smoke fixture to `verify-all.sh quick`.
- Document beginner-facing loop.

## Status

Fixed in current scope.
