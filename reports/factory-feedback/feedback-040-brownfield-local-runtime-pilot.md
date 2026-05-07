# Feedback 040: OpenClaw brownfield без repo до local runtime pilot

Updated UTC: 2026-05-07T04:27:59Z

## Классификация

```yaml
feedback_type: reusable_scenario_feedback
source_project: OpenClaw
source_repo: mppcoder/openclaw
route: brownfield-without-repo-to-greenfield
severity: medium
status: incorporated
```

## Наблюдение

The real OpenClaw pilot started from non-standard VPS folders rather than a
clean repo:

- patched runtime distribution: `/root/.openclaw`;
- overlay customization layer: `/root/openclaw-plus`;
- final active repo: `/projects/openclaw/reconstructed-repo`.

The route worked after Codex treated the two folders as brownfield inputs,
created a repo, pushed it to GitHub, built a real image and closed a local prod
runtime proof. This is distinct from public HTTPS/nginx proof.

## Требуемое поведение template

- Brownfield-without-repo intake must offer a folder-without-repo option.
- Non-standard VPS paths must be accepted as intake candidates, not active
  source roots.
- Runtime distribution patches must be reviewed before promotion.
- Local prod runtime proof may be closed if deploy, healthcheck, backup,
  restore, rollback, secrets boundary and sanitized transcript evidence exist.
- Public HTTPS/reverse-proxy must remain optional future work unless explicitly
  approved and verified.

## Внесенные артефакты

- `docs/operator/runbook-packages/04-brownfield-without-repo-to-greenfield/`
- `docs/operator/downstream-battle-external-pilot-runbook.md`
- `docs/releases/unified-single-vps-downstream-beginner-roadmap.md`
- `reports/release/downstream-local-runtime-pilot-summary.md`
