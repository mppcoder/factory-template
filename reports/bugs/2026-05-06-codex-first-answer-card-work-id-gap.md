# Bug: Codex first answer can hide project card and request number

Date: 2026-05-06

## User report

`в ответе кодекса в factory-template не видно карточки проекта и номера тикета запроса`

## Reproduction / Evidence

- `template-repo/scenario-pack/17-direct-task-self-handoff.md` required a visible self-handoff, but did not require top-level `Номер запроса Codex` or `Карточка проекта` blocks.
- `template-repo/scripts/codex_task_router.py::render_direct_task_response()` included `codex_work_id` and `codex_work_title` only inside the large handoff text block.
- `.chatgpt/direct-task-response.md` generated before the fix started with `## Применение в Codex UI`, so the operator did not get a glanceable request ticket or project card at the top of the Codex response.
- `template-repo/template/.chatgpt/codex-execution-card.md.template` showed route fields, but no visible request identity line.

## Expected

The first substantive Codex direct-task answer must show:

- `Номер запроса Codex` as a one-line fenced text block with the materialized `FT-CX-.... <task-slug>` title, or an exact allocator blocker.
- `Карточка проекта` from the repo renderer before route receipt, self-handoff, analysis or remediation.

## Actual

Codex request identity existed in repo state, but it was easy to miss because it was buried inside the handoff block. The project card was required for final closeout, but not for the starting direct-task response.

## Layer classification

- advisory/policy layer: `00-master-router.md`, `17-direct-task-self-handoff.md`, `AGENTS.md`, operator docs.
- executable routing layer: `bootstrap-codex-task.py`, `codex_task_router.py`, `render-project-lifecycle-dashboard.py`, `validate-codex-routing.py`.
- dashboard/rendering layer: Codex execution card template.

## Remediation

Require and generate top-level Codex request number and project card blocks for direct-task responses, validate the generated response, and expose current request identity in the Codex execution card.
