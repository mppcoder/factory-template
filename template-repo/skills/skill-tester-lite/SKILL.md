---
name: skill-tester-lite
description: Test factory-template skills and prompt-like artifacts with lightweight trigger and usefulness checks. Use when Codex is asked to validate a skill, test whether a skill should trigger, evaluate prompt/scenario usefulness, compare expected vs actual behavior on small examples, or run the optional create-test-improve loop for advanced template maintenance.
---

# Skill Tester Lite

Use this skill to run a small QA loop for skills and prompt-like artifacts. The goal is not a benchmark platform; the goal is to catch unclear triggers, weak usefulness, and missing repo-first boundaries before an artifact becomes reusable.

## Workflow

1. Select the target artifact and classify it:
   - `skill`: `template-repo/skills/<name>/SKILL.md`
   - `prompt-like`: scenario, runbook, handoff, policy note, checklist, task template.

2. Read the target artifact and, if needed, `references/test-design-guide.md`.

3. Define the expected behavior:
   - trigger-positive cases;
   - trigger-negative cases;
   - usefulness expectation;
   - repo boundary or beginner-path constraint.

4. Run a lightweight desk test:
   - use 2-4 realistic prompts or task fragments;
   - judge whether the artifact would be selected correctly;
   - judge whether following it would improve the output or routing.

5. Record findings:
   - use `references/report-template.md` when a durable report is requested;
   - otherwise include a short inline result with pass/fail and recommended edits.

6. Improve the artifact only when requested or when the current task includes remediation. Keep edits minimal and re-check the changed trigger/usefulness surface.

## References

- Read `references/test-design-guide.md` when designing cases or scoring trigger/usefulness.
- Read `references/report-template.md` when writing a persistent QA report.

## Pass Criteria

A target passes the lite loop when:

- positive trigger cases are clearly in scope;
- negative trigger cases are clearly out of scope;
- expected output is more useful than a generic response;
- beginner default path is not made heavier;
- repo-first and executable-routing boundaries remain explicit where relevant.

## Boundaries

- Do not require this loop for first-time users or ordinary generated projects.
- Do not build a full benchmark harness unless the user explicitly asks for one.
- Do not treat advisory text as an executable profile/model switch.
- Do not hide a defect: if testing reveals a repo process bug, follow the repo defect-capture path.
