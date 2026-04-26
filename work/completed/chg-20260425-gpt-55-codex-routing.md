# chg-20260425-gpt-55-codex-routing

## Summary
- Updated Codex handoff model recommendations for GPT-5.5.
- Kept `quick` on `gpt-5.4-mini` for lightweight tasks.
- Moved `build`, `deep`, and `review` to `gpt-5.5`.

## Updated Artifacts
- `template-repo/codex-routing.yaml`
- `template-repo/scripts/codex_task_router.py`
- `template-repo/template/.codex/config.toml`
- `factory/producer/extensions/workspace-packs/vscode-codex-bootstrap/codex/global-codex-config.example.toml`
- `docs/operator/factory-template/03-mode-routing-factory-template.md`
- `factory/producer/ops/codex-config-factory-template.toml`
- `factory/producer/archive/legacy-bootstrap/dogfood-brownfield-shell-p1/.codex/config.toml`
- `.chatgpt/direct-task-source.md`
- `.chatgpt/direct-task-self-handoff.md`
- `.chatgpt/direct-task-response.md`
- `.chatgpt/normalized-codex-handoff.md`
- `.chatgpt/task-launch.yaml`
- `.chatgpt/verification-report.md`
- `.chatgpt/done-report.md`
- `CURRENT_FUNCTIONAL_STATE.md`

## Evidence
- Local `codex debug models` includes `gpt-5.5`.
- Official OpenAI release note: `https://openai.com/index/introducing-gpt-5-5/`.

## Verification
- `python3 template-repo/scripts/validate-codex-routing.py .`
- `python3 template-repo/scripts/validate-codex-task-pack.py .`
