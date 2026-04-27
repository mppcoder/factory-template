# Bug: backup hook command is split before shell execution

Date: 2026-04-27

## Summary

During approved 2.6 runtime proof, `db-backup` failed before creating a dump.

## Evidence

Command:

```bash
docker compose --env-file deploy/.env \
  -f deploy/compose.yaml \
  -f deploy/compose.production.yaml \
  -f deploy/presets/app-db.yaml \
  -f deploy/presets/backup.yaml \
  run --rm db-backup
```

Observed output:

```text
BusyBox ... Usage: mkdir [-m MODE] [-p] DIRECTORY...
```

`docker compose config` showed the backup service command being split to:

```yaml
entrypoint:
  - /bin/sh
  - -lc
command:
  - mkdir
  - -p
  - /backups
```

With `/bin/sh -lc`, the shell command string became only `mkdir`, so `/backups` was not passed as the mkdir operand.

## Layer Classification

- Layer: production preset runtime hook.
- Defect class: compose command/entrypoint bug.
- Owner boundary: repo/template.

## Remediation

Use `/bin/sh -c` with a single command argument for the backup script.

## Status

Captured during runtime proof and remediated in current scope.
