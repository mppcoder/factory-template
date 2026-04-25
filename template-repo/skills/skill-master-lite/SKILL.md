---
name: skill-master-lite
description: Create or improve lightweight factory-template skills and prompt-like artifacts. Use when Codex is asked to draft a new repo skill, refine a skill trigger, reduce an overgrown prompt artifact, improve usefulness of scenario/runbook instructions, or prepare an artifact for the optional skill quality loop without introducing a full benchmark system.
---

# Skill Master Lite

Use this skill to turn a rough skill or prompt-like artifact into a small, triggerable, useful repo artifact. Keep the workflow lightweight and optional; this is an advanced factory-maintenance path, not a beginner default.

## Workflow

1. Identify the artifact type:
   - Codex skill: `template-repo/skills/<name>/SKILL.md`
   - Prompt-like artifact: scenario, runbook, handoff block, policy note, checklist, or task template.

2. Write the trigger contract first:
   - what task should activate the artifact;
   - what task should not activate it;
   - which repo rules remain higher priority.

3. Keep the body procedural:
   - include the minimum workflow another Codex instance needs;
   - move long examples or report shapes into `references/`;
   - do not add a full comparison repo, benchmark harness, or novice-facing mandatory step.

4. Add a usefulness check:
   - what output should be better after using this artifact;
   - what failure would prove the trigger is too broad, too narrow, or unclear;
   - which file should be tested with `skill-tester-lite`.

5. Hand off to `skill-tester-lite` when the user asks for validation, trigger QA, usefulness QA, or an improvement loop.

## Skill Shape

For a Codex skill, keep this structure unless the repo already has a stronger local convention:

```text
---
name: short-hyphen-name
description: What the skill does and exact situations when to use it.
---

# Human Title

Short purpose paragraph.

## Workflow
Numbered steps.

## Boundaries
What to avoid, what remains optional, what is out of scope.
```

Use only `name` and `description` in YAML frontmatter.

## Prompt-Like Artifact Shape

For scenarios, runbooks, handoffs, or policy prompts:

- state the decision point before the procedure;
- separate advisory text from executable routing;
- name required inputs, outputs, and verification;
- prefer one clear path plus explicit fallback over several equal-looking branches;
- add a short "not for beginner default path" note when the artifact is advanced-only.

## Improvement Checklist

Before finishing, check:

- Trigger: a future Codex instance can tell when to use the artifact.
- Usefulness: the artifact changes behavior, not just wording.
- Scope: it does not add a required novice step.
- Repo-first: it points to repo files and keeps scenario-pack/router precedence.
- Testability: at least one realistic test prompt can be written for `skill-tester-lite`.

## Output

When asked to create or improve an artifact, return:

- files changed;
- trigger/usefulness changes;
- optional QA suggestion if the user did not ask to run the loop yet.
