# Bug: downstream project could inherit FT index identity

## Где найдено
`factory-template` bootstrap path for generated downstream projects.

## В каком сценарии или шаге
`template-repo/launcher.sh` copies `template-repo/template/.chatgpt/*` before downstream identity materialization.

## Что ожидалось
Every generated project receives its own `PROJECT_CODE` at creation time. ChatGPT ids use `<PROJECT_CODE>-CH-<NNNN>`, Codex work ids use `<PROJECT_CODE>-CX-<NNNN>`, and CH/CX counters are independent repo-local counters starting at `1`.

## Что произошло фактически
The template seed contained `project_code: FT` in:
- `template-repo/template/.chatgpt/chat-handoff-index.yaml`;
- `template-repo/template/.chatgpt/codex-work-index.yaml`.

The launcher copied those files into downstream repos without a dedicated index identity generation step, so a downstream repo could keep factory-only `FT` identity.

## Impact
Duplicate `FT-CH-*` and `FT-CX-*` names could appear across unrelated projects, breaking handoff traceability and making repo-local ChatGPT/Codex reservations ambiguous.

## Classification
- defect_layer: `factory-template`
- reusable_issue: `true`
- affected_layer: `bootstrap / template / validators / docs`

## Remediation
Add bootstrap-time index generation and validation:
- choose one `PROJECT_CODE` during project creation;
- materialize `.chatgpt/chat-handoff-index.yaml` with `project_code: <PROJECT_CODE>`, `next_chat_number: 1`, `items: []`;
- materialize `.chatgpt/codex-work-index.yaml` with `project_code: <PROJECT_CODE>`, `next_codex_work_number: 1`, `items: []`;
- validate project identity against repo config and reject downstream `FT` identity unless the project is `factory-template`.

## Verification
- `python3 template-repo/scripts/validate-chat-handoff-index.py template-repo/template/.chatgpt/chat-handoff-index.yaml`
- `python3 template-repo/scripts/validate-codex-work-index.py template-repo/template/.chatgpt/codex-work-index.yaml`
- `python3 template-repo/scripts/validate-project-index-identity.py <generated-project-root>`
- `bash template-repo/scripts/verify-all.sh quick`
