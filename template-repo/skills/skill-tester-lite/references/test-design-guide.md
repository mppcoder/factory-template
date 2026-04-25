# Test Design Guide

Use this guide for the optional advanced QA loop:

```text
create -> test -> improve trigger/usefulness
```

The loop is for improving factory-template itself. It is not a required step for beginners using the template.

## Test Surface

Test only the surface that matters for reuse:

- trigger fit: when the skill or prompt should activate;
- trigger rejection: when it should stay silent;
- usefulness: what behavior becomes better after using it;
- boundary safety: repo-first, routing, beginner-path, and defect-capture constraints.

## Minimal Case Set

Use 2-4 cases:

1. Positive obvious case: should trigger.
2. Positive edge case: should trigger but needs careful interpretation.
3. Negative adjacent case: should not trigger even though words overlap.
4. Regression case: checks a known repo boundary, if one exists.

For prompt-like artifacts, replace "trigger" with "route/use": should this scenario, runbook, or handoff rule be applied?

## Scoring

Use a simple result per case:

```text
PASS | FAIL | UNCLEAR
```

Judge three dimensions:

- selection: was the right artifact chosen;
- execution: were the required steps concrete enough;
- restraint: did it avoid adding mandatory work outside the requested scope.

## Improvement Heuristics

If positive cases fail:

- add concrete trigger phrases to the description or opening rule;
- make the first workflow step more decisive;
- name the artifact classes it covers.

If negative cases fail:

- add exclusions to boundaries;
- remove broad wording from the description;
- split unrelated capabilities into another artifact.

If usefulness fails:

- add expected output shape;
- add a tiny checklist;
- move long background text into a reference file.

If beginner-path safety fails:

- mark the workflow as optional advanced mode;
- remove it from quick-start paths;
- link it from maintenance or quality sections only.

## Factory-Template Example

Target: `template-repo/skills/skill-master-lite/SKILL.md`

Positive prompt:

```text
Create a new lightweight Codex skill for validating factory-template handoff blocks.
```

Expected: `skill-master-lite` should trigger because the request is to create a repo skill.

Negative prompt:

```text
I am starting my first project from the factory template. What command do I run?
```

Expected: `skill-master-lite` should not trigger. The beginner path should stay with `docs/first-project.md` or `docs/guided-launcher.md`.

Usefulness check:

```text
After using the skill, the new artifact should have a clear trigger contract, boundaries, and a testable QA surface.
```
