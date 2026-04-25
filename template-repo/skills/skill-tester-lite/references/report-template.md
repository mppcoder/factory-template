# Lite QA Report Template

Use this template when a persistent QA note is useful. Keep reports short; the loop is intentionally lightweight.

```markdown
# Lite QA Report: <artifact>

Date: YYYY-MM-DD
Target: <path>
Artifact type: skill | prompt-like
Tester: Codex

## Goal
What behavior should improve?

## Cases

| Case | Prompt / situation | Expected | Result | Notes |
| --- | --- | --- | --- | --- |
| positive-obvious | ... | trigger/use | PASS | ... |
| positive-edge | ... | trigger/use | PASS/FAIL/UNCLEAR | ... |
| negative-adjacent | ... | do not trigger/use | PASS/FAIL/UNCLEAR | ... |
| regression-boundary | ... | preserve boundary | PASS/FAIL/UNCLEAR | ... |

## Findings
- ...

## Improvements Applied
- ...

## Remaining Risk
- ...
```

If the QA reveals a defect in repo process, create the bug report at the defect-capture path required by the task or router before remediation.
