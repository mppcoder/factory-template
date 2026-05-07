# Bug: FT-CX-0012 stayed active after beginner-first replacement

Date: 2026-05-07

## Reproduction

1. Render the compact project card:
   `python3 template-repo/scripts/render-project-lifecycle-dashboard.py --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml --format chatgpt-card --stdout`
2. Inspect the generated dashboard:
   `sed -n '1,180p' reports/project-lifecycle-dashboard.md`
3. Inspect Codex work state:
   `rg -n "FT-CX-0012|FT-CX-0020|FT-CX-0025" .chatgpt/codex-work-index.yaml`

## Evidence

- `FT-CX-0012 continue-after-unified-roadmap` remained `blocked` even after `FT-CX-0020 beginner-first-hardening` and `FT-CX-0025 rehearsal-project-ui-completion-confirmation` closed the current beginner-first product contour.
- The compact card therefore showed a red active blocker although no current repo task was blocked.
- The markdown dashboard also displayed template seed `task-state.yaml` / `stage-state.yaml` values when rendering the factory dashboard from `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml`.

## Layer Classification

- Primary layer: `.chatgpt` state / Codex work index closeout.
- Secondary layer: dashboard renderer context resolution for template-dashboard rendering in the factory repo.
- Reusable risk: downstream or factory dashboards can show seed template state instead of root repo state when rendering from a template-owned dashboard path.

## Remediation

- Reclassified `FT-CX-0012` as `superseded` by `FT-CX-0020`.
- Added root `.chatgpt/task-state.yaml` for the factory repo closeout state.
- Updated the renderer to prefer root `.chatgpt` state when rendering the factory template dashboard path.
- Moved dashboard lifecycle readout to `release -> deploy` while keeping Release itself pending as a future approval boundary.

## Factory Feedback

Renderer context must not let template seed artifacts override root project state for the factory repo status card. Template seed files remain useful for generated projects, but factory readouts should prefer root `.chatgpt` state when it exists.
