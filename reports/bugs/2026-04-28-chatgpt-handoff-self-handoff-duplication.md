# ChatGPT handoff self-handoff duplication ambiguity

Date: 2026-04-28

## Summary

Repo guidance used `self-handoff` terminology too broadly and could make Codex appear to rewrite a ChatGPT-generated handoff before execution. For `launch_source: chatgpt-handoff`, Codex should execute the incoming handoff and may only emit a short route/handoff receipt. `self-handoff` must be reserved for direct user tasks without external handoff and for incidental defects that become a separate task boundary.

## Severity

Medium. The defect can confuse launch semantics and make the operator think Codex replaced the ChatGPT source-of-truth handoff with a newly generated one.

## Reproduction / evidence

- `template-repo/scenario-pack/15-handoff-to-codex.md` says normalized routing fields apply to "любого handoff или self-handoff" without clearly naming the ChatGPT handoff receipt boundary.
- `CURRENT_FUNCTIONAL_STATE.md` says direct task uses "такой же нормализованный self-handoff, как и handoff из ChatGPT Project", which blurs the distinction.
- User-observed behavior: after pasting a ChatGPT handoff, Codex printed a "Self-handoff" style route block before execution, making it look like handoff duplication.

## Expected behavior

- `chatgpt-handoff`: Codex executes the pasted handoff. A visible first response may contain only `handoff receipt` / `route receipt` fields confirming route, stage, artifacts and defect-capture path.
- `direct-task`: Codex creates and shows `self-handoff` before implementation.
- Incidental defect: Codex creates `self-handoff` only if the defect becomes a separate task boundary or needs explicit current-route continuation.

## Actual behavior

Guidance allowed or encouraged calling the ChatGPT handoff acceptance block `self-handoff`, which implies a replacement handoff and duplicates the ChatGPT-generated source.

## Layer classification

- advisory/policy layer: scenario-pack terminology and operator-facing process docs.
- executable routing layer: unchanged; `launch_source` remains `chatgpt-handoff` or `direct-task`.
- generated handoff layer: generated ChatGPT handoff text must tell Codex to emit route receipt, not self-handoff, for `chatgpt-handoff`.

## Remediation plan

1. Add an explicit ChatGPT handoff acceptance rule to `00-master-router.md`.
2. Update `15-handoff-to-codex.md` to distinguish `handoff receipt` from `self-handoff`.
3. Update direct-task scenario to say it does not apply to ChatGPT handoff.
4. Update generated handoff response text so pasted ChatGPT handoff is not treated as a self-handoff replacement.
5. Update release-facing state/evidence and artifact eval expectations.

## Verification plan

1. Run Artifact Eval for `master-router` and `direct-task-self-handoff`.
2. Run `validate-codex-task-pack.py`.
3. Run `validate-human-language-layer.py`.
4. Run `bash template-repo/scripts/verify-all.sh quick`.

## Factory feedback

Required. This is a reusable template/process terminology defect in the handoff contract.

Factory feedback report: `reports/factory-feedback/feedback-041-chatgpt-handoff-self-handoff-duplication.md`
