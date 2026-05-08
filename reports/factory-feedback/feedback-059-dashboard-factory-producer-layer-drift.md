# Factory feedback 059: dashboard factory producer layer drift

Источник: `reports/bugs/2026-05-08-dashboard-factory-producer-layer-drift.md`

## Reusable issue

Root-specific factory facts can be hidden when a generated-project dashboard template is rendered as the `factory-template` project card.

## Expected factory behavior

- Generated projects keep `factory_producer_owned_layer: false`.
- `factory-template` root readout derives producer ownership from `FACTORY_MANIFEST.yaml`.
- Dashboard/card renderer must not turn optional `factory/producer/*` into downstream core.

## Suggested validation

Run the project lifecycle dashboard renderer and confirm the factory card shows producer layer `True` while generated template defaults remain false.
