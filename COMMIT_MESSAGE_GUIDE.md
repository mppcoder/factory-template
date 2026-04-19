# Commit Message Guide

## Принцип

Сообщение коммита для `factory-template` должно быстро отвечать на два вопроса:

1. какой слой изменён;
2. что именно сделано.

Формат:

```text
<тип>: <краткое действие в repo>
```

Примеры типов:

- `fix`
- `docs`
- `release`
- `policy`
- `test`
- `refactor`
- `feat`

## Рекомендуемые шаблоны

### Docs

```text
docs: align runbooks with current repo topology
docs: add release-facing operator checklist
docs: refresh release note template
```

### Fix

```text
fix: align versioning layer with release metadata
fix: clean release audit flow after self-tests
fix: remove legacy CURRENT_STATE references
```

### Policy

```text
policy: add factory-template ops policy manifest
policy: validate curated sources pack composition
policy: define boundary-actions settings for repo
```

### Test

```text
test: add ops policy validation to matrix runner
test: extend prerelease audit with release-layer docs
test: verify curated sources pack export flow
```

### Release

```text
release: prepare factory-template release layer
release: sync release-facing docs and verify summary
release: finalize notes for factory-template publish
```

### Refactor

```text
refactor: move sources-pack export to declarative policy
refactor: extract boundary-actions generator template
```

### Feature

```text
feat: add curated sources pack exporter
feat: add boundary-actions generator for external steps
feat: add release checklist and verify summary
```

## Как выбирать тип

- `fix`: когда устраняется defect, drift или inconsistency
- `docs`: когда меняется только documentation layer
- `policy`: когда меняется manifest, preset, pack composition, routing rule
- `test`: когда меняется validator, audit, runner или verify coverage
- `release`: когда change в первую очередь про release readiness
- `refactor`: когда структура улучшается без изменения целевого поведения
- `feat`: когда появляется новый repo capability

## Практическое правило

Если change затрагивает несколько слоёв, выбирайте тип по главному результату:

- если главное — устранить поломку, используйте `fix`
- если главное — добавить новый workflow, используйте `feat`
- если главное — подготовить publish/release, используйте `release`
- если главное — синхронизировать документацию, используйте `docs`
