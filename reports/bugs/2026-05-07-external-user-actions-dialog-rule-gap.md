# Bug: external user actions lacked mandatory dialog and copy-block contract

- id: `bug-2026-05-07-external-user-actions-dialog-rule-gap`
- detected: `2026-05-07`
- source: direct user report / requested rule hardening
- owner_boundary: repo template, scenario-pack, generated task-pack guidance and runbook package contract
- external_boundary: user-facing UI/manual actions, secrets, approvals and ChatGPT Project UI steps
- severity: medium

## Symptom

Closeout rules already required `## Инструкция пользователю` for real external actions, but did not explicitly require a dialog-style scenario with step explanations, choices and inline copy blocks.

As a result, a future closeout could technically satisfy the section name while still telling a beginner to follow a file path or link instead of giving the exact text/command/handoff to copy.

## Expected behavior

Whenever external user action remains:

- final output uses `## Инструкция пользователю`;
- each action is explained as a compact dialog scenario: goal, window/service, exact steps, recommended option and fallback where relevant, expected result and what to send back;
- any text, command, URL, handoff or repo-first instruction the user must copy is emitted as a fenced code block in the answer;
- file links or repo paths may be evidence only, not the primary copy mechanism.

## Reproduction

1. Reach a closeout that requires a ChatGPT Project UI paste, external approval, secret entry or manual GitHub UI step.
2. Emit `## Инструкция пользователю`.
3. Point the user to a file/path for the text to copy instead of providing the text inline.
4. The old contract had no targeted validator fragment that failed this response shape.

## Layer classification

- scenario-pack/router closeout contract;
- generated `.chatgpt/boundary-actions.md`;
- generated `.chatgpt/done-checklist.md`;
- beginner runbook package contract;
- validators for task-pack and runbook package source.

## Fix direction

Add an explicit external-action dialog rule to source guidance and validators:

- router final-block rule;
- boundary-actions guidance;
- done-checklist closeout checks;
- runbook package contract and greenfield closeout;
- validator fragments for `validate-codex-task-pack.py` and `validate-runbook-packages.py`.
