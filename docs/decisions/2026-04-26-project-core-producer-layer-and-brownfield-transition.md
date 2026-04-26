# ADR: Project core, producer layer and brownfield transition

## Статус

Accepted

## Дата

2026-04-26

## Контекст

The factory currently describes greenfield and brownfield generated project contours, but brownfield can be read as a permanent project class. The same discussion also risks making `factory-template` look like it has a special development workflow.

## Решение

All projects use one lifecycle core: repo-first instructions, scenario routing, `.chatgpt` state, defect capture, handoff, verification, done/closeout, versioning and project knowledge.

`factory-template` is a normal `greenfield-product` project whose product is the project factory. It additionally has a factory producer layer for template generation, release, packaging, registry, downstream sync, reference packs and archives.

`brownfield-without-repo` and brownfield-with-repo presets are transitional adoption states, not final product classes.

Successful brownfield adoption ends by switching the active project profile to:

```yaml
project_preset: greenfield-product
recommended_mode: greenfield
```

and the stage state to:

```yaml
lifecycle_state: greenfield-converted
```

Brownfield artifacts remain as historical evidence, audit records and migration records after conversion. They are no longer active mode drivers.

## Lifecycle-состояния

- `greenfield-active`
- `brownfield-without-repo-intake`
- `brownfield-without-repo-reconstruction`
- `brownfield-with-repo-audit`
- `brownfield-with-repo-adoption`
- `brownfield-to-greenfield-conversion`
- `greenfield-converted`

## Следствия для ownership

- Template releases update only template-owned zones.
- Project-owned product code, specs and history are protected from template sync.
- Factory producer paths are excluded from battle project sync.
- Brownfield evidence, audit and reconstruction zones are protected during transition and become historical evidence after conversion.

## Последствия

- Validators must distinguish project preset, active mode and lifecycle state.
- Brownfield completion requires conversion to greenfield-product or an explicit blocker.
- Converted projects receive future template releases as greenfield products while preserving brownfield history.
- Factory-template and downstream projects share lifecycle rules; their difference is ownership and producer responsibilities, not workflow.
