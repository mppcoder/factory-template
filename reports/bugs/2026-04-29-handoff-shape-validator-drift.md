# Defect capture: handoff_shape validator drift

Date: 2026-04-29

## Summary

Beginner handoff UX validation treated parent orchestration markers as mandatory for every handoff. That made the desired default `single-agent-handoff` path fail the same scorecard that should protect it.

## Evidence

- `template-repo/scripts/validate-beginner-handoff-ux.py` required `defer-to-final-closeout`, `deferred_user_actions`, `placeholder_replacements` and `owner_boundary` unconditionally.
- `tests/beginner-handoff-ux/positive/handoff.md` only represented a parent/full orchestration handoff.
- No positive fixture covered a small cohesive single-agent handoff.
- No negative fixture caught a large multi-child task mistakenly marked as single-agent, or a small cohesive task mistakenly marked as parent orchestration.

## Layer classification

- advisory/policy layer: scenario-pack did not require explicit `handoff_shape`.
- executable routing layer: `codex-routing.yaml` and route explanation did not expose handoff shape.
- validator/test layer: beginner UX validator was not shape-aware.
- docs/operator layer: full orchestration wording did not clearly say parent orchestration is not the default for every task.

## Remediation

- Add normalized `handoff_shape` with allowed values `single-agent-handoff` and `parent-orchestration-handoff`.
- Make `single-agent-handoff` the default for cohesive one-route tasks.
- Add hard triggers and soft scoring for parent orchestration.
- Make validators and fixtures shape-aware.

## Status

Fixed in current scope.
