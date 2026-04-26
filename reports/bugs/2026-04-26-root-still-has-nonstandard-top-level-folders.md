# Root still has nonstandard top-level folders after ownership remediation

Date: 2026-04-26
Status: fixed-in-scope
Layer: factory-template / tree contract / physical root UX
Scenario: defect-capture -> structural remediation

## Summary

Previous lifecycle and ownership remediation fixed the conceptual contract: `factory-template` is a `greenfield-product` whose product is the factory, with an additional `factory-producer-owned` layer. That remediation did not physically normalize the repository root.

The root still exposed historical and factory-only top-level folders:

| old_path | current purpose | ownership class | target_path | move/wrapper/delete/archive | risk | references_to_update |
| --- | --- | --- | --- | --- | --- | --- |
| `.dogfood-bootstrap/` | historical dogfood bootstrap project | historical-archive | `factory/producer/archive/legacy-bootstrap/` | move/archive, no active wrapper | medium | tree contract, language exceptions, release history |
| `factory_template_only_pack/` | operator runbooks, routing notes, source guidance, boundary template | factory-producer-owned / docs | `docs/operator/factory-template/`, `factory/producer/ops/templates/` | move | high | README, source profiles, validators, pre-release audit, docs |
| `meta-template-project/` | historical meta project for factory evolution | project-owned / historical-archive | `project-knowledge/factory/template-evolution/`, `docs/releases/factory-template-release-notes.md`, `reports/factory-feedback/*` | dissolve | high | version checks, source profiles, triage/ingest tools, docs |
| `onboarding-smoke/` | onboarding smoke harness and acceptance report | project-core tests | `tests/onboarding-smoke/` | move | medium | verify-all, KPI validator, README, release docs |
| `optional-domain-packs/` | optional domain reference cases | factory-producer-owned reference | `factory/producer/reference/domain-packs/` | move | low | tree contract, docs, release notes |
| `packaging/` | source/export profile packaging | factory-producer-owned packaging | `factory/producer/packaging/` | move | medium | source export scripts, README, policy validators |
| `registry/` | factory version, release and project registry | factory-producer-owned registry | `factory/producer/registry/` | move | medium | release scripts, phase/version checks, docs |
| `working-project-examples/` | release/reference examples and matrix fixtures | factory-producer-owned reference | `factory/producer/reference/examples/` | move | high | matrix tests, example tests, docs, feedback |
| `workspace-packs/` | downstream sync and workspace operational packs | factory-producer-owned extensions | `factory/producer/extensions/workspace-packs/` | move | high | sync scripts, README, policies, release docs |

## Evidence

- `python3 template-repo/scripts/validate-tree-contract.py .` passed before remediation even though legacy top-level folders were present.
- `template-repo/tree-contract.yaml` listed `.dogfood-bootstrap`, `factory_template_only_pack`, `meta-template-project`, `onboarding-smoke`, `optional-domain-packs`, `packaging`, `registry`, `working-project-examples`, and `workspace-packs` under `contours.factory_root.allowed_top_level`.
- `find . -maxdepth 2 -type d | sort` showed the same folders as visible root-level peers of `docs/`, `reports/`, `template-repo/`, and `work/`.
- `rg "factory_template_only_pack|meta-template-project|\\.dogfood-bootstrap|workspace-packs|optional-domain-packs|working-project-examples|onboarding-smoke|packaging/|registry/" .` found active references in release scripts, validators, docs, source profiles, matrix tests and factory sync manifests.

## Defect

The advisory and machine-readable lifecycle/ownership contract says the project is standard lifecycle core plus a bounded factory-producer layer, but the physical root still looks like a collection of historical subprojects and factory-only packs. This creates UX and architecture drift: users see legacy names as canonical root concepts, and validators encode that drift as allowed structure.

## Classification

- Defect type: structural / repo UX / contract drift.
- Scope: fixed in the current physical root normalization task.
- Reusable factory issue: yes, because downstream sync and generated project validation must exclude factory-producer-owned content.

## Remediation

Move factory-producer-owned and historical content under `factory/producer/*`, dissolve `meta-template-project/` into normal project zones, move smoke harness under `tests/`, shrink `allowed_top_level`, and teach validators to reject legacy active root paths.
