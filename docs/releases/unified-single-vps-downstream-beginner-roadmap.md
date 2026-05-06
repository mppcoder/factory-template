# Единый roadmap: single VPS -> downstream proof -> первый проект новичка

## Карта источников

- `template-repo/scenario-pack/00-master-router.md`: routing, handoff receipt and execution mode boundary.
- `.chatgpt/chat-handoff-index.yaml`: `FT-CH-0011` closure and chat numbering source.
- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`: lifecycle, module gate and runbook package dashboard source.
- `template-repo/template/.chatgpt/standards-gates.yaml`: module/standards-inspired baseline evidence.
- `docs/architecture/vps-project-hosting-topologies.md`: canonical VPS topology standard.
- `docs/operator/single-big-vps-dev-runtime-architecture.md`: operator shortcut for the supported single-host topology.
- `docs/downstream-application-proof.md`: downstream app proof scenario and false-pass boundary.
- `docs/operator/runbook-packages/`: beginner runbooks and takeover boundaries.

## Текущее состояние

- Stage 0: `FT-CH-0011 single-vps-dev-runtime-host` is closed as `verified` by explicit user confirmation on `2026-05-06`; the number remains reserved and `next_chat_number` stays `15`.
- Stage 0.5: Module Gate Baseline is materialized. Lifecycle, Core, Security, Quality, WebSec, Ops and UI/A11y have repo evidence; AI remains `not_applicable` because this template does not declare runtime AI-output behavior.
- Stage 1: `single-host` is the default supported topology for solo/beginner operators when one large VPS hosts `/projects/*` dev workspaces and `/srv/*-prod` runtime copies with hard separation.
- Stage 2: downstream/battle proof is prepared but not passed. There is no selected downstream repo and no real `APP_IMAGE` in this repo.
- Stage 3: beginner-first path remains Windows PC -> VPS -> VS Code Remote SSH + Codex extension or Codex app remote -> Codex takeover -> first greenfield project.

## Порядок зависимостей

1. Stage 0: close `FT-CH-0011` and state/dashboard drift.
2. Stage 0.5: close module gate baseline with evidence, accepted reason, not applicable reason or blocker.
3. Stage 1: materialize single big VPS architecture.
4. Stage 2: prepare downstream/battle proof path and block false pass.
5. Stage 3: harden beginner-first Windows-to-first-project flow.
6. Stage 4: render dashboard, run validators, sync, and publish closeout.

Do not reverse Stage 2 and Stage 3 unless the user explicitly changes priority.

## Внешние блокеры

Downstream/battle app proof pass requires:

- downstream repo path;
- real `APP_IMAGE`;
- approved VPS/staging target;
- secrets outside repo;
- approval for deploy, restore and rollback;
- sanitized transcript.

Without those inputs, the correct status is `ready_for_external_pilot` or `blocked_external_inputs`, not `passed`.

## Валидаторы

- `python3 template-repo/scripts/validate-chat-handoff-index.py .chatgpt/chat-handoff-index.yaml`
- `python3 template-repo/scripts/validate-standards-gates.py .`
- `python3 template-repo/scripts/validate-project-lifecycle-dashboard.py template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`
- `python3 template-repo/scripts/validate-runbook-packages.py .`
- `python3 template-repo/scripts/validate-downstream-application-proof.py reports/release/downstream-application-proof-report.md`
- `bash template-repo/scripts/verify-all.sh quick`

## Fallback path / запасной путь

If real downstream inputs are absent, keep the proof report blocked, preserve the false-pass guard and continue beginner-first hardening. Internal repo work should proceed without asking the user to type "continue"; only ChatGPT Project UI, secret entry, paid/security/destructive approvals and real downstream selection remain external.
