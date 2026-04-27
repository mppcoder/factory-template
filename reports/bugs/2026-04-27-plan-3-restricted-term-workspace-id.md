# Bug: P3-S4 workspace id used a restricted historical term

Date: 2026-04-27

## Summary

During P3-S3/P3-S4 verification, `bash template-repo/scripts/verify-all.sh quick` failed at `validate-tree-contract` because the new completed feature workspace id used a historical/product-specific restricted term.

## Evidence

Command:

```bash
bash template-repo/scripts/verify-all.sh quick
```

Observed failure:

```text
TREE CONTRACT НЕ ПРОЙДЕН
- naming: термин 'dogfood' найден вне compatibility/optional allowlist: work/completed/plan-3-eval-dogfood
```

## Layer Classification

- Layer: factory repo work archive / release-facing evidence.
- Defect class: naming contract violation.
- Scope: incidental defect found during current P3-S3/P3-S4 implementation.
- Owner boundary: repo.

## Remediation

Rename the feature evidence from `plan-3-eval-dogfood` to `plan-3-eval-adoption` and replace active release-facing wording with neutral `adoption` language.

## Prevention

For future feature ids, avoid historical/product-specific terms that tree contract keeps only in compatibility/archive allowlists.
