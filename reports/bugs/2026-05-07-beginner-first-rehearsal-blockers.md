# Beginner-first rehearsal exposed first-project blockers

Date: 2026-05-07
Work item: FT-CX-0020 beginner-first-hardening

## Summary

Repo-backed rehearsal of `Windows PC -> VPS -> VS Code Remote SSH / Codex app remote -> factory-template -> first greenfield project` exposed reusable template blockers that prevent a beginner from reaching the first verified project without Codex remediation.

## Reproduction

Run a real greenfield rehearsal from `/projects` with GitHub repo creation enabled:

```bash
python3 /projects/factory-template/template-repo/scripts/factory-launcher.py \
  --template-repo-root /projects/factory-template/template-repo \
  --mode greenfield \
  --guided \
  --project-name "Beginner First Rehearsal" \
  --project-slug beginner-first-rehearsal-20260507 \
  --yes \
  --skip-preflight \
  --create-github-repo \
  --github-owner mppcoder \
  --github-visibility private
```

## Findings

- `git user.name` / `git user.email` absent on clean VPS blocked initial commit before GitHub repo creation.
- Generated project validators looked for `template-repo/template/work-templates/*` and missed generated-root `work-templates/*`.
- Generated project did not materialize `.chatgpt/boundary-actions.md` and `.chatgpt/handoff-response.md`.
- Generated `task-launch.yaml` omitted `selected_plan_mode_reasoning_effort`.
- `tools/fill_smoke_artifacts.py` overwrote compliant `handoff-response.md` with an older minimal handoff block.
- Launcher copied `scripts/__pycache__` into generated repos and generated projects lacked `.gitignore`.

## Remediation

- `template-repo/launcher.sh` derives local git identity from `gh api user` when GitHub repo creation is requested, without mutating global git config.
- `template-repo/scripts/verify-all.sh` now includes `first-project-github-identity-smoke`.
- `validate-feature-execution-lite.py` and `validate-spec-traceability.py` accept generated-root `work-templates/*`.
- Generated template `.chatgpt` now includes the required handoff/boundary task-pack artifacts and routing defaults.
- `tools/fill_smoke_artifacts.py` preserves the current handoff-response UX contract.
- Generated template now has `.gitignore`, and launcher removes `__pycache__` / `*.pyc` from copied scripts.

## Evidence

- Final real rehearsal repo: `https://github.com/mppcoder/beginner-first-rehearsal-20260507e`.
- Final project root: `/projects/beginner-first-rehearsal-20260507e`.
- Generated quick verify: `bash scripts/verify-all.sh quick` passed.
- Generated sync: commit `68cd156` pushed to `origin/main`.
- Factory quick verify: `bash template-repo/scripts/verify-all.sh quick` passed after adding the git identity smoke.
