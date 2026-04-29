# Factory feedback 044: handoff_shape validator drift

Date: 2026-04-29

## Reusable issue

When a validator is introduced for a specialized advanced path, it can accidentally become the global contract for simpler paths. Here, parent orchestration UX markers were required for every beginner handoff, so the repo could not cleanly express a single-agent default.

## Recommended factory rule

Any reusable handoff validator should first read a normalized shape/type field, then apply only the requirements for that shape.

For Codex handoff routing, the normalized field is:

```yaml
handoff_shape:
  allowed_values:
    - single-agent-handoff
    - parent-orchestration-handoff
```

## Regression protection

- Positive fixture for `single-agent-handoff`.
- Positive fixture for `parent-orchestration-handoff`.
- Negative fixture for missing `handoff_shape`.
- Negative fixture for large/multi-child task marked single-agent.
- Negative fixture for small cohesive task marked parent orchestration.
