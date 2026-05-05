# Universal Task Control: контракт downstream materialization

## Назначение

Этот контракт фиксирует, какие части Universal Task Control должны попадать в generated downstream project из `factory-template`, какие остаются factory-only, и какие пути считаются canonical после генерации.

Главное разделение:

- factory self-improvement path: `template-repo/template/.chatgpt/task-registry.yaml`;
- generated project path: `.chatgpt/task-registry.yaml`.

Любой downstream-facing script, doc или dashboard должен работать от root generated repo без префикса `template-repo/template/`.

## Обязательный downstream payload

| Область | Factory source | Generated path | Contract |
|---|---|---|---|
| Task registry | `template-repo/template/.chatgpt/task-registry.yaml` | `.chatgpt/task-registry.yaml` | Materialize initial registry with example task terminal `not_applicable`; downstream tasks live here. |
| Dashboard source | `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` | `.chatgpt/project-lifecycle-dashboard.yaml` | Include `universal_task_control` section, no false green, registry path `.chatgpt/task-registry.yaml`. |
| Dashboard renderer | `template-repo/scripts/render-project-lifecycle-dashboard.py` | `scripts/render-project-lifecycle-dashboard.py` | Render generated dashboard/card from generated root. |
| Registry validator | `template-repo/scripts/validate-task-registry.py` | `scripts/validate-task-registry.py` | Validate generated `.chatgpt/task-registry.yaml`. |
| Task id allocator | `template-repo/scripts/allocate-task-id.py` | `scripts/allocate-task-id.py` | Allocate/append generated task ids without touching factory state. |
| Issue bridge | `template-repo/scripts/issue-to-task-registry.py` | `scripts/issue-to-task-registry.py` | Convert sanitized local issue drafts; no GitHub API required. |
| Handoff preview | `template-repo/scripts/preview-task-handoff.py` | `scripts/preview-task-handoff.py` | Write preview/handoff under generated `reports/handoffs/`. |
| Task pack wrapper | `template-repo/scripts/prepare-task-pack.py` | `scripts/prepare-task-pack.py` | Prepare preview, handoff, validation and optional `ready_for_codex` transition. |
| Status transition | `template-repo/scripts/update-task-status.py` | `scripts/update-task-status.py` | Update generated registry and optional generated dashboard counters. |
| Queue renderer | `template-repo/scripts/render-task-queue.py` | `scripts/render-task-queue.py` | Render generated queue to `reports/task-queue.md` or stdout. |
| Handoff generator | `template-repo/scripts/task-to-codex-handoff.py` | `scripts/task-to-codex-handoff.py` | Produce one copy-paste `codex-task-handoff`. |
| Handoff validator | `template-repo/scripts/validate-codex-task-handoff.py` | `scripts/validate-codex-task-handoff.py` | Validate generated handoff before Codex launch. |
| Issue templates | `.github/ISSUE_TEMPLATE/*.yml` | `.github/ISSUE_TEMPLATE/*.yml` | Local downstream issues plus upstream factory feedback form must materialize with privacy/consent wording. |
| Operator docs | `template-repo/template/docs/operator/*.md` | `docs/operator/*.md` | Explain downstream task lifecycle in Russian. |
| Reports placeholders | `template-repo/template/reports/*` plus launcher-created dirs | `reports/*` | Generated project must have `reports/handoffs/`, `reports/bugs/`, `reports/factory-feedback/`, `reports/release/` and `reports/task-queue.md` target path available on demand. |

## Canonical generated-команды

Generated projects must support these commands from repo root:

```bash
python3 scripts/validate-task-registry.py .chatgpt/task-registry.yaml
python3 scripts/allocate-task-id.py --registry .chatgpt/task-registry.yaml
python3 scripts/allocate-task-id.py --registry .chatgpt/task-registry.yaml --append-draft --title "..." --task-class docs --source-kind manual --source-ref ""
python3 scripts/update-task-status.py --registry .chatgpt/task-registry.yaml --dashboard .chatgpt/project-lifecycle-dashboard.yaml --task-id FT-TASK-0002 --status ready_for_handoff --reason "Task route is clear." --sync-dashboard --write
python3 scripts/preview-task-handoff.py --registry .chatgpt/task-registry.yaml --task-id FT-TASK-0002 --output reports/handoffs/FT-TASK-0002-preview.md
python3 scripts/prepare-task-pack.py --registry .chatgpt/task-registry.yaml --dashboard .chatgpt/project-lifecycle-dashboard.yaml --task-id FT-TASK-0002 --mark-ready-for-codex --sync-dashboard --write
python3 scripts/validate-codex-task-handoff.py reports/handoffs/FT-TASK-0002-codex-handoff.md
python3 scripts/render-task-queue.py --registry .chatgpt/task-registry.yaml --output reports/task-queue.md
```

Factory-facing commands with `template-repo/template/.chatgpt/task-registry.yaml` remain valid only inside `factory-template` self-improvement tasks.

## Правило sync для существующих downstream projects

When updating an existing downstream project, never blindly overwrite `.chatgpt/task-registry.yaml`. It may contain user tasks, statuses, evidence and external-action boundaries. Sync must be a merge or migration:

- preserve existing `tasks`, `next_task_number`, evidence and status history;
- add new allowed classes/statuses only when compatible;
- update scripts/docs/templates independently from registry state;
- write a migration report before changing task registry semantics.

## Factory-only артефакты

The following stay factory-only by default:

- `tests/universal-task-control/*` positive/negative fixtures;
- factory readouts under `reports/universal-task-control-*.md`;
- factory release evidence and upstream feedback reports;
- root factory `docs/operator/factory-template/*` docs, except when a downstream-specific variant is placed under `template-repo/template/docs/operator/`.

Generated-project smoke may create temporary copies of fixtures, but it must not materialize factory test fixtures into every project unless a future contract explicitly opts in.

## Privacy и consent boundaries

Downstream Issue Forms and local issue bridge must preserve these rules:

- no secrets, tokens, passwords, private keys or raw private logs in issue drafts;
- local downstream issues are project work, not automatic upstream factory reports;
- upstream factory feedback requires explicit user intent and sanitized content;
- public external reports require review and consent;
- risky, paid, destructive, security-sensitive, deploy or release actions require explicit approval.

## Критерии приемки

Downstream materialization is complete when:

- a generated project contains `.chatgpt/task-registry.yaml`, Universal Task Control scripts, Issue Forms, docs and report target directories;
- generated commands work from generated repo root with `.chatgpt/task-registry.yaml`;
- dashboard/card show Universal Task Control with `.chatgpt/task-registry.yaml` and no false green;
- generated smoke validates allocate -> preview -> prepare pack -> `ready_for_codex` -> queue without mutating factory state;
- `verify-all quick` includes a temporary generated-project smoke for this path.
