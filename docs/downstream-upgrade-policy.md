# Политика downstream upgrade

This policy defines how downstream/battle repos consume updates from `factory-template`.

## Source of truth

- `factory-template` remains the canonical template source.
- Downstream root `AGENTS.md` is a materialized clone of `template-repo/AGENTS.md`.
- Downstream operators should use `workspace-packs/factory-ops/export-template-patch.sh` to create a preview bundle before any apply step.

## Sync tiers

The sync contract is declared in `workspace-packs/factory-ops/factory-sync-manifest.yaml`.

| Tier | Meaning | Apply behavior |
| --- | --- | --- |
| `safe` | Template-owned files that can be generated into a patch bundle. | `apply-template-patch.sh --apply-safe-zones` may copy generated files and records rollback metadata. |
| `advisory` | Template references that may be useful but can conflict with local workflow choices. | Preview and patch only; apply manually after review. |
| `manual-only` | Project-specific lifecycle content. | Impact signal only; never generated for automatic apply. |

## Bundle metadata

Each export writes:

- `bundle-metadata.json`: bundle schema, template version, contract version, tier counts, and generated safe-file count.
- `preview-changes.json`: per-file tier, target, status, and whether it will be generated for apply.
- `safe-changed-files.txt`: exact generated targets that safe apply may copy.
- `patch-summary.md`: human-readable operator summary.

The static bundle schema source lives in `workspace-packs/factory-ops/sync-bundle-version.json`.

## Operator flow

```bash
bash workspace-packs/factory-ops/export-template-patch.sh <factory-root> <downstream-root> --dry-run
bash workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --check
bash workspace-packs/factory-ops/apply-template-patch.sh <downstream-root>/_factory-sync-export --apply-safe-zones --with-project-snapshot
python3 workspace-packs/factory-ops/upgrade-report.py <factory-root> <downstream-root> --format markdown --output UPGRADE_SUMMARY.md
```

Use `--with-project-snapshot` whenever a human has edited files during the same upgrade session.

## Rollback flow

```bash
bash workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --check
bash workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback
bash workspace-packs/factory-ops/rollback-template-patch.sh <downstream-root>/_factory-sync-export --rollback --restore-project-snapshot
```

`--rollback` restores only tracked safe-tier generated files. `--rollback --restore-project-snapshot` restores the full snapshot created during apply and is the safer path for mixed manual sessions.

## Safety rules

- Advisory and manual-only changes must not be copied by `apply-template-patch.sh`.
- Missing optional safe zones are reported as `optional-missing-project`, not as a hard failure.
- Before manual copying from advisory/manual-only patches, inspect local project intent and current work state.
- If a safe apply overwrites local edits unexpectedly, capture a bug report before remediation.
