# Физическая нормализация root tree

Date: 2026-04-26
Status: accepted

## Контекст

The lifecycle and ownership contract now treats `factory-template` as a `greenfield-product` whose product is the factory. The factory has one additional owned layer: `factory-producer-owned`. The physical root still exposed factory-only and historical folders as first-class project roots, which made the visual tree contradict the accepted architecture.

## Решение

There is no separate `factory-template` workflow outside the standard project lifecycle. The root model is:

- standard project lifecycle core;
- plus a bounded `factory/producer/` namespace for factory-producer-owned release, packaging, registry, sync, reference, extension and archive content.

Factory-producer-owned content must live under `factory/producer/*` unless a file is an intentional root operator entrypoint. Historical names cannot remain as active root paths. Compatibility may be provided only by temporary root wrappers for operator scripts, not by keeping full legacy folders at root.

## Финальная карта переносов

| old_path | new_path | rule |
| --- | --- | --- |
| `.dogfood-bootstrap/` | `factory/producer/archive/legacy-bootstrap/` | historical archive only |
| `factory_template_only_pack/*.md` | `docs/operator/factory-template/` | human/operator docs |
| `factory_template_only_pack/templates/` | `factory/producer/ops/templates/` | producer operator templates |
| `factory_template_only_pack/06-codex-config-factory-template.toml` | `factory/producer/ops/codex-config-factory-template.toml` | producer operator config |
| `meta-template-project/RELEASE_NOTES.md` | `docs/releases/factory-template-release-notes.md` | release history |
| `meta-template-project/incoming-learnings/` | `reports/factory-feedback/incoming-learnings/` | feedback intake |
| `meta-template-project/scenario-audits/` | `reports/factory-feedback/scenario-audits/` | feedback/audit evidence |
| `meta-template-project/templates/` | `work-templates/factory-feedback/` | reusable feedback templates |
| remaining `meta-template-project/*` | `project-knowledge/factory/template-evolution/` | project knowledge/history |
| `onboarding-smoke/` | `tests/onboarding-smoke/` | smoke harness |
| `optional-domain-packs/` | `factory/producer/reference/domain-packs/` | optional reference packs |
| `packaging/` | `factory/producer/packaging/` | producer packaging |
| `registry/` | `factory/producer/registry/` | producer registry |
| `working-project-examples/` | `factory/producer/reference/examples/` | release/reference examples and matrix fixtures |
| `workspace-packs/` | `factory/producer/extensions/workspace-packs/` | producer extensions and downstream sync tooling |

## Compatibility wrappers / совместимость

The only allowed root compatibility wrappers are intentional executable UX entrypoints such as `MATRIX_TEST.sh`, `PRE_RELEASE_AUDIT.sh`, `VERIFIED_SYNC.sh` and related release shell commands. No full legacy folder remains at repository root.

## Последствия

- `template-repo/tree-contract.yaml` must reject old root folders except intentionally documented root wrappers.
- Generated greenfield/brownfield projects must not receive `factory/producer/*`.
- Downstream sync manifests and source profiles must reference the new producer namespace.
- Documentation must describe advisory/policy routing separately from executable launch routing.
