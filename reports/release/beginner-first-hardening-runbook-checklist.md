# Чеклист beginner-first hardening runbook

Date: 2026-05-07
Work item: FT-CX-0020 beginner-first-hardening
Runbook package: `docs/operator/runbook-packages/02-greenfield-product`

| ID | Status | Evidence |
|---|---|---|
| GF-000 | passed | `factory-template` verified; remote shell and `gh` auth available. |
| GF-005 | rehearsed | Factory ChatGPT UI remains the only user-owned intake start; not automated by Codex. |
| GF-010 | rehearsed | Trigger command remains `новый проект`; repo router entrypoint remains `template-repo/scenario-pack/00-master-router.md`. |
| GF-015 | rehearsed | Default-decision path preserved in user runbook and validator. |
| GF-020 | rehearsed | Recommendation-first intake boundaries preserved. |
| GF-030 | passed | `gh auth status` has repo write scope; VPS project root path available under `/projects`. |
| GF-040 | rehearsed | Handoff boundary validated by `validate-runbook-packages.py` and `validate-codex-task-pack.py`. |
| GF-050 | passed | Codex ran in repo-backed remote shell; no local-only handoff step used. |
| GF-060 | passed | Codex created repo/root/scaffold, initialized first feature workspace, ran verify, and synced. |
| GF-070 | passed | Generated repo contains repo-first `.chatgpt`, `AGENTS.md`, scenario-pack and handoff/boundary artifacts. |
| GF-080 | external | User-created battle ChatGPT Project remains external UI boundary. |
| GF-090 | external | User pastes prepared repo-first instruction in ChatGPT Project settings. |
| GF-100 | ready | First project is ready after user completes battle ChatGPT Project UI paste. |

## Доказательства валидаторов

- `python3 template-repo/scripts/validate-runbook-packages.py .` passed.
- `bash template-repo/scripts/verify-all.sh quick` passed.
- Generated project `/projects/beginner-first-rehearsal-20260507e`: `bash scripts/verify-all.sh quick` passed.
- Generated project `/projects/beginner-first-rehearsal-20260507e`: `python3 scripts/check-dod.py .` passed.

## Внешняя граница

Only ChatGPT Project UI remains user-owned:

- create the battle ChatGPT Project;
- open Project settings/instructions;
- paste the prepared repo-first instruction;
- save settings.

Public HTTPS / reverse-proxy remains a separate optional approval boundary and is not part of this checklist.
