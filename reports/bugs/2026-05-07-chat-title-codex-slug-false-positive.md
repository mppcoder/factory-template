# Bug: chat title validator rejected legitimate codex slug

## Где найдено
`factory-template` ChatGPT handoff allocator / validator path.

## В каком сценарии или шаге
While materializing `FT-CH-0022 per-project-unique-chatgpt-codex-indexes`, the repo-local allocator rejected the new item before writing it.

## Что ожидалось
A task slug may contain product/domain words such as `chatgpt` or `codex` when they describe the work. The title validator should reject status/kind tokens in titles, but should not reject legitimate lowercase task slug words.

## Что произошло фактически
`validate-chat-handoff-index.py` treated `CODEX` as a forbidden title status token after tokenizing the canonical title, so `per-project-unique-chatgpt-codex-indexes` failed validation even though the canonical title matched `<PROJECT_CODE>-CH-<NNNN> <task-slug>`.

## Impact
ChatGPT/Codex index work could not reserve its own ChatGPT title through the repo-local allocator. Operators would be pushed toward manual edits or false allocator blockers for valid task names.

## Classification
- defect_layer: `factory-template`
- reusable_issue: `true`
- affected_layer: `validators / allocator / docs / smoke tests`

## Remediation
- Removed `CODEX` from the forbidden status-token list for ChatGPT chat titles.
- Kept actual status/kind tokens forbidden in title text.
- Added smoke coverage that allocates `per-project-unique-chatgpt-codex-indexes`.
- Updated the operator doc so `CODEX` is not documented as a forbidden status token.

## Verification
- `python3 template-repo/scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml`
- `bash template-repo/scripts/verify-all.sh quick`
