# Bug: chat-title-allocation-github-confirmation-gate-regression

Date: 2026-05-07
Status: verified

## Symptom

ChatGPT Project first substantive answer can still show the exact allocator blocker:

```text
Нужно выделить номер через repo chat-handoff-index / allocator.
```

instead of a materialized stable title such as `FT-CH-.... <task-slug>`.

A separate repeated symptom appeared in the same contour: the assistant sometimes asks for conversational confirmation before using GitHub access to allocate the number, for example asking whether it may use GitHub before reading the repo/index or attempting connector-safe reservation.

## Impact

- The user does not get the stable copyable ChatGPT task title in the first answer.
- The ChatGPT Project first-answer path can stop at a free-form confirmation question even though repo/project instructions already require authenticated repo-first GitHub connector access.
- The allocator blocker and the confirmation question both delay the required binary first-answer outcome: materialized allocation or exact confirmed blocker.

## Root Cause

The first-answer allocation protocol did not include an explicit no-conversational-confirmation gate.

Existing rules required repo-first reads, repo-local allocator attempt, GitHub connector write fallback, and confirm fetch/readback. They did not explicitly say that repo-first instructions are prior authorization for the configured authenticated GitHub connector/repo tool, nor did they forbid a model-level "можно ли использовать GitHub?" question before attempting the available connector path.

## Boundary

Repo instructions cannot disable a platform-level OAuth / connector authorization prompt.

Allowed blocker:
- `external_auth_blocker` when the platform itself requires OAuth/connector authorization or connector installation before the tool can be used;
- `write_auth_blocker` when the connector can read but no write action is exposed, write is rejected, or confirm fetch/readback fails.

Forbidden behavior:
- asking a free-form model-level confirmation question such as "подтвердите доступ к GitHub", "разрешите использовать GitHub", "do you confirm GitHub access" or "please grant/confirm access" before the repo-first read/allocation attempt.

## Relation To Prior Bugs

- `FT-CH-0016`: earlier title allocator blocker regression.
- `FT-CH-0018`: allocator write-path regression.
- `FT-CH-0020`: allocator blocker still returned when connector write fallback should be used.
- `reports/bugs/2026-05-07-chat-title-allocation-runtime-enforcement-gap.md`: prior runtime enforcement gap report for connector-safe reservation.

## Expected Behavior

First substantive ChatGPT Project answer must:

1. read `template-repo/scenario-pack/00-master-router.md`;
2. read `.chatgpt/chat-handoff-index.yaml`;
3. use repo-local allocator if executable;
4. otherwise, when GitHub connector write path is exposed, use that write path directly to append one canonical item and bump `next_chat_number`;
5. confirm fetch/readback of the updated index;
6. show the stable materialized title in an однострочный fenced `text` code block;
7. ask no conversational confirmation in between.

If the platform/OAuth layer blocks tool access, show `external_auth_blocker` and the exact allocator blocker. If the write action is not exposed or cannot be confirmed, show `write_auth_blocker` and the exact allocator blocker. If write action exposed and confirm fetch succeeds, the exact allocator blocker is forbidden.

## Remediation

- Router, handoff scenario and operator docs now state that repo-first instruction authorizes configured GitHub connector for required read/index/allocation attempts.
- Router, handoff scenario and operator docs now forbid conversational confirmation before GitHub read/index read/allocation attempt.
- Validator now requires the no-confirmation / OAuth boundary wording in canonical sources.
- Validator now detects confirmation questions before materialized allocation or explicit `external_auth_blocker` / `write_auth_blocker`.
- Added negative fixture `tests/chatgpt-first-answer-contract/negative/github-access-confirmation-before-allocation.md`.
- Added positive fixture `tests/chatgpt-first-answer-contract/positive/github-connector-no-confirmation-materialized.md`.

## Verification Target

- `python3 template-repo/scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml`
- `python3 template-repo/scripts/validate-chatgpt-first-answer-contract.py .`
- `python3 template-repo/scripts/validate-handoff-implementation-register.py .chatgpt/handoff-implementation-register.yaml`
- `bash template-repo/scripts/verify-all.sh quick`
- `bash template-repo/scripts/verify-all.sh`

## Verification Result

Passed in `HIR-015` closeout.
