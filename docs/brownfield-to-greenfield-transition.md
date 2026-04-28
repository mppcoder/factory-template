# Переход из brownfield в greenfield

Brownfield is a temporary adoption state for existing projects. It is not a final project class.

Successful adoption ends when the active project profile is:

```yaml
project_preset: greenfield-product
recommended_mode: greenfield
```

and stage state records:

```yaml
lifecycle_state: greenfield-converted
```

## Без репозитория

Use this path when there is an existing system or files, but no normalized repo.

1. Create `/projects/<project-slug>/`.
2. Put incoming materials only inside `/projects/<project-slug>/_incoming/`.
3. Capture evidence:
   `brownfield/system-inventory.md`, `brownfield/as-is-architecture.md`,
   `brownfield/gap-register.md`, `.chatgpt/evidence-register.md`,
   `.chatgpt/reality-check.md`.
4. Reconstruct or identify the canonical repo:
   `brownfield/reverse-engineering-plan.md`,
   `brownfield/reverse-engineering-summary.md`,
   `brownfield/decision-log.md`, temporary `reconstructed-repo/` or equivalent
   inside the target `greenfield-product` repo root.
5. Move canonical product code into the final project layout, retire temporary
   reconstruction workspace from active paths, then run the with-repo audit/adoption
   cycle.
6. Convert to `greenfield-product`.

Temporary, intermediate, reconstructed and helper repos are never separate siblings in
`/projects`; they are project-local workspaces under `/projects/<target-greenfield-project>/...`.

Done requires conversion or an explicit blocker.

## С репозиторием

Use this path when an existing repo can remain the canonical project root.

1. Keep the existing repo as root whenever possible.
2. Materialize repo-first core:
   `AGENTS.md`, `.chatgpt/`, `.codex/`, `template-repo/scenario-pack/`,
   presets, routing files, `template-repo/tree-contract.yaml`,
   `template-repo/mode-parity.yaml`.
3. Capture audit/adoption evidence:
   `brownfield/system-inventory.md`, `brownfield/repo-audit.md`,
   `brownfield/as-is-architecture.md`, `brownfield/gap-register.md`,
   `brownfield/change-map.md`, `brownfield/risks-and-constraints.md`,
   `.chatgpt/reality-check.md`, `.chatgpt/conflict-report.md`.
4. Normalize only safe structural drift. Do not overwrite product code.
5. Convert when repo-first core, scenario-pack, defect-capture, self-handoff,
   project smoke/tests, protected project-owned zones and risk decisions are ready.
6. Keep `brownfield/` as historical evidence.

## Gate'ы conversion

- `repo_first_core_present`
- `master_router_present`
- `scenario_pack_accessible`
- `active_project_profile_updated_to_greenfield_product`
- `lifecycle_state_greenfield_converted`
- `greenfield_required_artifacts_present`
- `brownfield_evidence_archived_or_referenced`
- `project_owned_zones_protected`
- `template_owned_zones_marked`
- `sync_manifest_safe_for_downstream`
- `validators_green`

Validators:

```bash
python3 template-repo/scripts/validate-brownfield-transition.py <project> --without-repo
python3 template-repo/scripts/validate-brownfield-transition.py <project> --with-repo
python3 template-repo/scripts/validate-greenfield-conversion.py <project> --require-converted
```
