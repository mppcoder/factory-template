# Сводка локального runtime-пилота OpenClaw

Updated UTC: 2026-05-07T04:27:59Z

## Статус

```yaml
pilot_project: OpenClaw
downstream_repo: mppcoder/openclaw
repo_path: /projects/openclaw/reconstructed-repo
route: brownfield-without-repo-to-greenfield
target_lifecycle: greenfield-converted
local_prod_runtime_proof: passed
source_hardening: completed_baseline
operator_readiness: completed_baseline
public_https: not_claimed
factory_template_downstream_proof_status: external_local_runtime_pilot_evidence_only
```

## Карта evidence

- OpenClaw repo was created as `mppcoder/openclaw` and pushed to `main`.
- Non-standard source folders were handled as brownfield inputs:
  `/root/.openclaw` as patched runtime distribution and `/root/openclaw-plus`
  as overlay customization source.
- Active repo root is `/projects/openclaw/reconstructed-repo`.
- Real local `APP_IMAGE` is `openclaw:1236c7fcc0fe`.
- Runtime root is `/srv/openclaw-prod`.
- Secrets remain outside repo in `/etc/openclaw-prod.env`.
- Deploy, localhost healthcheck, backup, disposable restore and rollback drill
  passed.
- Source-like runtime patches were promoted into active repo source.
- Repo self-sufficiency runbook, report and validator were added.

## Обратная связь для factory-template

This pilot validates a reusable route:

```text
non-standard VPS folders / no repo
-> bounded brownfield intake
-> reconstructed repo under /projects/<project>/reconstructed-repo
-> GitHub repo creation/sync
-> greenfield-converted lifecycle
-> real APP_IMAGE build
-> local prod runtime proof
-> source hardening
-> operator readiness
```

It also confirms the false-pass boundary:

- local prod runtime proof can pass without public HTTPS;
- public HTTPS/nginx proof must remain a separate optional runtime boundary;
- `factory-template` must not claim full downstream/battle public endpoint proof
  from local-only evidence.

## Follow-up, внесенный в template

- Brownfield-without-repo runbook now explicitly supports non-standard VPS
  folders as intake candidates.
- Downstream pilot runbook now separates local runtime proof closure from public
  HTTPS/reverse-proxy proof.
- Unified roadmap now records OpenClaw as external local runtime pilot evidence,
  not as full public downstream proof pass.
