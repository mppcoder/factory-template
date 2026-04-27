# Bug: `--skip-pull` is defeated by production `pull_policy: always`

Date: 2026-04-27

## Summary

During the approved 2.6 rollback drill, a local candidate image tag could not be deployed even with `deploy-local-vps.sh --skip-pull`.

## Evidence

The rollback drill tagged the already-pulled app image as a local candidate:

```text
factory-template-rollback-candidate:local
```

Deploy with `--skip-pull` still failed:

```text
app Error pull access denied for factory-template-rollback-candidate
```

Root cause: `deploy/compose.production.yaml` sets:

```yaml
pull_policy: always
```

That policy makes `docker compose up` try to pull the image even when the script skips the explicit `docker compose pull` step.

## Layer Classification

- Layer: production deploy script / compose production override.
- Defect class: runtime rollback drill blocker.
- Owner boundary: repo/template.

## Remediation

Make app pull policy configurable with a safe default:

```yaml
pull_policy: ${APP_PULL_POLICY:-always}
```

This preserves default production freshness while allowing explicit local rollback drills with `APP_PULL_POLICY=never`.

## Status

Captured and remediated in current runtime proof scope.
