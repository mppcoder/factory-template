# Инвентаризация prompt-артефактов для GPT-5.5

Дата: 2026-04-28
Scope: `factory-template`

## Карта источников (source map)

Проверено 177 candidate files в обязательных prompt-like зонах:
- `.chatgpt/*`
- `template-repo/template/.chatgpt/*`
- `template-repo/scenario-pack/**/*.md`
- `template-repo/tasks/codex/*.md`
- `template-repo/template/tasks/codex/*.md`
- `template-repo/skills/**/*.md`
- `docs/operator/**/*`
- `bootstrap/**/*`
- `template-repo/template/docs/**/*`
- `tests/artifact-eval/specs/*.yaml`
- `template-repo/codex-routing.yaml`
- `template-repo/template/.codex/config.toml`
- scripts that render/generate handoff, route explanation, ChatGPT source packs and prompt/task packs

`rg` audit found 119 prompt-like files with routing, handoff, model, instruction or Codex markers. These are audit candidates, not automatic defects.

## Группы prompt-артефактов

| Group | Files / examples | Migration decision |
| --- | --- | --- |
| Active `.chatgpt` task artifacts | `.chatgpt/codex-input.md`, `.chatgpt/codex-context.md`, `.chatgpt/codex-task-pack.md`, reports | Update to current GPT-5.5 migration task. |
| Template `.chatgpt` prompts | `template-repo/template/.chatgpt/codex-input.md`, `codex-task-pack.md` | Convert placeholders to outcome-first prompt shape. |
| Handoff generators | `template-repo/scripts/create-codex-task-pack.py`, `codex_task_router.py` | Add GPT-5.5 prompt baseline to generated packs. |
| Routing config | `template-repo/codex-routing.yaml`, `template-repo/codex-model-routing.yaml`, `.codex/config.toml` | Preserve mapping; no silent quick promotion. |
| Scenario-pack | `00-master-router.md`, `15-handoff-to-codex.md`, `17-direct-task-self-handoff.md` | Mostly current; preserve hard invariants. |
| Skills | `skill-master-lite`, `skill-tester-lite` | Compatible; no broad rewrite needed. |
| Operator docs | `docs/operator/factory-template/*` | Compatible; routing/runbook language already separates advisory/executable. |
| Artifact eval | `tests/artifact-eval/specs/*` | Add GPT-5.5 prompt-contract spec. |

## Остаточные упоминания старых моделей

Allowed / intentional:
- `gpt-5.4-mini` remains `quick` profile in `template-repo/codex-routing.yaml` and related routing docs.
- `gpt-5.3`, `gpt-5.4`, `gpt-5.2` appear in model catalog compatibility fixtures/config, not as silent target promotion.

Cleanup applied:
- Default fallback literals in generated handoff response changed from `gpt-5.4` to `gpt-5.5` where the build/default prompt path was implied.

## Аудит запрещенных prompt-паттернов

`think step by step` and `as an AI` appear only inside validator/spec negative markers after remediation. Static `current date:` prompt instructions were not found in critical prompt surfaces.
