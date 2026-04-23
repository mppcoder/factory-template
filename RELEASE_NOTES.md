# Release Notes

## 2.5 - Program Framing (planned, not released) - 2026-04-23

### О чём этот контур

Это не опубликованный release note для тега, а канонический framing следующей линии `2.5`.
Линия `2.5` определена как dual-track программа:

- `2.5-A` — engineering hardening;
- `2.5-B` — beginner-first productization (UI-friendly и безопасный для downstream evolution UX).

### Что нормализовано

- единый roadmap: `docs/releases/2.5-roadmap.md`;
- единые success metrics с порогами MVP/full: `docs/releases/2.5-success-metrics.md`;
- release-facing документы обновлены так, чтобы `2.5` не трактовался как "ещё один process-hardening-only релиз".

### Gate-фокус следующих handoff

1. `H25-01`: hardening backlog и risk register.
2. `H25-02`: beginner onboarding flow и UI contracts.
3. `H25-03`: safe defaults и compatibility для downstream.
4. `H25-04`: MVP DoD подтвержден по порогам.
5. `H25-05`: full 2.5 DoD и release closeout.

### Определение готовности

- `MVP 2.5` требует закрытия hardening + beginner контуров в минимально достаточном наборе и достижения MVP-порогов.
- `Full 2.5` требует закрытия всех фаз roadmap и full-порогов метрик из `docs/releases/2.5-success-metrics.md`.

## 2.4.4 - 2026-04-22

### О чём этот релиз

Релиз `2.4.4` приводит `factory-template` к семантически чистой универсальной иерархии.
Главная цель релиза: убрать product-specific naming из canonical core/release-facing слоя, синхронизировать presets, manifests и docs tree, а domain-specific reference-cases отделить от core без потери compatibility.

### Что вошло

- canonical preset naming переведён на универсальные factory names:
  - `greenfield-product`
  - `brownfield-without-repo`
  - `brownfield-with-repo-modernization`
  - `brownfield-with-repo-integration`
  - `brownfield-with-repo-audit`
- `workspace-packs/vscode-codex-bootstrap` заменяет dogfood naming в canonical workspace bootstrap слое;
- `optional-domain-packs/openclaw-reference` закрепляет `OpenClaw` как optional reference-case, а не как часть core factory tree;
- release docs, manifests, template metadata, examples и `.chatgpt` closeout artifacts синхронизированы под `2.4.4`;
- launcher/runtime сохраняют compatibility aliases для legacy preset names, чтобы переход не ломал existing downstream flows.
- cleanup path теперь также убирает `.factory-runtime`, чтобы pre-release audit не наследовал stale runtime reports между verify/release циклами.
- verified-sync/release automation теперь устойчиво обрабатывает non-ASCII git paths, встречающиеся в repo bootstrap/docs слоях.

### Архитектурные изменения в документации

- canonical release-facing tree теперь явно отделяет:
  - core factory layers;
  - universal template source;
  - greenfield;
  - brownfield with repo;
  - brownfield without repo;
  - optional domain references;
- release-facing naming больше не закрепляет dogfood/openclaw как canonical структуру фабрики;
- advisory/policy layer и executable routing layer по-прежнему описаны раздельно, но теперь это согласовано с новой физической и логической иерархией.

### Что важно для downstream

- для downstream/battle repos canonical docs и presets теперь должны использовать новые neutral names;
- legacy preset names допускаются только как compatibility aliases и не считаются release-facing canon;
- optional domain references должны жить вне core naming и не маскироваться под обязательный factory layer;
- обновление `Sources` по-прежнему не требуется по умолчанию и используется только как compatibility fallback, если такой contour ещё сохранён.

### Проверка и выпуск

Релизный пакет рассчитан на прохождение:

- `bash VALIDATE_FACTORY_TEMPLATE_OPS.sh`
- `bash SMOKE_TEST.sh`
- `bash EXAMPLES_TEST.sh`
- `bash MATRIX_TEST.sh`
- `bash CLEAN_VERIFY_ARTIFACTS.sh`
- `bash PRE_RELEASE_AUDIT.sh`
- `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
- `bash VALIDATE_RELEASE_DECISION.sh`
- `bash VALIDATE_RELEASE_NOTES_SOURCE.sh`

### Ограничения

- semantic quality проверки по-прежнему частично эвристические;
- публикация GitHub Release зависит от доступности и авторизации `gh`;
- release-facing reference layer остаётся живым каноном и требует синхронного обновления при следующих process changes;
- compatibility aliases пока сохраняются, поэтому legacy names ещё могут встречаться в historical registry data и migration notes.
