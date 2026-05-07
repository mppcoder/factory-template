# Проекты, созданные из фабрики

<!--
Подсказка: сюда заносятся production-проекты, созданные из фабрики.
Для test-прогонов используйте статус `test` или режим `FACTORY_REGISTRY_MODE=skip`.

Формат записи:
- дата: 2026-04-14
  проект: Название проекта
  slug: slug-project  # canonical project_slug: local repo basename and GitHub repo name must match exactly
  версия_фабрики: 2.3.6
  режим: greenfield|brownfield
  статус_записи: production|test
  project_preset: greenfield-product|brownfield-with-repo-modernization|brownfield-with-repo-integration|brownfield-with-repo-audit|brownfield-without-repo
  change_class: small-fix|feature|refactor|migration|brownfield-audit
  execution_mode: manual|hybrid|codex-led
  reserved_slug_override: false
  примечание: свободный комментарий
-->
- дата: 2026-04-14
  проект: Проект дефектов
  slug: proj-defect
  версия_фабрики: 2.3.7
  режим: greenfield
  статус_записи: production
  project_preset: product-dev
  change_class: feature
  execution_mode: hybrid
  примечание: создан через launcher
- дата: 2026-04-14
  проект: Проект дефектов
  slug: proj-defect
  версия_фабрики: 2.3.7
  режим: greenfield
  статус_записи: production
  project_preset: product-dev
  change_class: feature
  execution_mode: hybrid
  примечание: создан через launcher
- дата: 2026-04-14
  проект: Проект дефектов
  slug: proj-defect
  версия_фабрики: 2.3.7
  режим: greenfield
  статус_записи: production
  project_preset: product-dev
  change_class: feature
  execution_mode: hybrid
  примечание: создан через launcher
- дата: 2026-04-14
  проект: Проект дефектов
  slug: proj-defect
  версия_фабрики: 2.3.7
  режим: greenfield
  статус_записи: production
  project_preset: product-dev
  change_class: feature
  execution_mode: hybrid
  примечание: создан через launcher
- дата: 2026-04-15
  проект: Тестовый проект
  slug: test-align
  версия_фабрики: 2.3.7
  режим: greenfield
  статус_записи: production
  project_preset: product-dev
  change_class: small-fix
  execution_mode: manual
  примечание: создан через launcher
- дата: 2026-04-15
  проект: Тестовый проект
  slug: test-align
  версия_фабрики: 2.3.7
  режим: greenfield
  статус_записи: production
  project_preset: product-dev
  change_class: small-fix
  execution_mode: manual
  примечание: создан через launcher
- дата: 2026-04-15
  проект: GF Demo
  slug: gf-demo
  версия_фабрики: 2.4.0-versioning-layer
  режим: greenfield
  статус_записи: production
  project_preset: product-dev
  change_class: feature
  execution_mode: hybrid
  примечание: создан через launcher
- дата: 2026-04-15
  проект: BF Demo
  slug: bf-demo
  версия_фабрики: 2.4.0-versioning-layer
  режим: brownfield
  статус_записи: production
  project_preset: legacy-modernization
  change_class: brownfield-audit
  execution_mode: manual
  примечание: создан через launcher
- дата: 2026-04-17
  проект: Dogfood Brownfield Shell
  slug: dogfood-brownfield-shell
  версия_фабрики: 2.4.0
  режим: brownfield
  статус_записи: production
  project_preset: audit-only
  change_class: brownfield-audit
  execution_mode: manual
  примечание: создан через launcher
- дата: 2026-04-26
  проект: OpenClaw Brownfield
  slug: openclaw-brownfield
  версия_фабрики: 2.5.0
  режим: brownfield
  статус_записи: production
  project_preset: brownfield-without-repo
  change_class: brownfield-stabilization
  execution_mode: hybrid
  примечание: создан через launcher; локальный git repo зафиксирован commit `4a58c8d`
- дата: 2026-04-26
  проект: Greenfield Test
  slug: greenfield-test
  версия_фабрики: 2.5.0
  режим: greenfield
  статус_записи: production
  project_preset: greenfield-product
  change_class: feature
  execution_mode: codex-led
  примечание: создан через launcher; GitHub repo `mppcoder/greenfield-test`, latest commit `cca68d5`
- дата: 2026-05-07
  проект: Beginner First Rehearsal
  slug: beginner-first-rehearsal-20260507
  версия_фабрики: 2.5.0
  режим: greenfield
  статус_записи: production
  project_preset: greenfield-product
  change_class: feature
  execution_mode: codex-led
  reserved_slug_override: false
  примечание: создан через launcher
- дата: 2026-05-07
  проект: Beginner First Rehearsal
  slug: beginner-first-rehearsal-20260507
  версия_фабрики: 2.5.0
  режим: greenfield
  статус_записи: production
  project_preset: greenfield-product
  change_class: feature
  execution_mode: codex-led
  reserved_slug_override: false
  примечание: создан через launcher
- дата: 2026-05-07
  проект: Beginner First Rehearsal B
  slug: beginner-first-rehearsal-20260507b
  версия_фабрики: 2.5.0
  режим: greenfield
  статус_записи: production
  project_preset: greenfield-product
  change_class: feature
  execution_mode: codex-led
  reserved_slug_override: false
  примечание: создан через launcher
- дата: 2026-05-07
  проект: Beginner First Rehearsal C
  slug: beginner-first-rehearsal-20260507c
  версия_фабрики: 2.5.0
  режим: greenfield
  статус_записи: production
  project_preset: greenfield-product
  change_class: feature
  execution_mode: codex-led
  reserved_slug_override: false
  примечание: создан через launcher
- дата: 2026-05-07
  проект: Beginner First Rehearsal D
  slug: beginner-first-rehearsal-20260507d
  версия_фабрики: 2.5.0
  режим: greenfield
  статус_записи: production
  project_preset: greenfield-product
  change_class: feature
  execution_mode: codex-led
  reserved_slug_override: false
  примечание: создан через launcher
- дата: 2026-05-07
  проект: Beginner First Rehearsal E
  slug: beginner-first-rehearsal-20260507e
  версия_фабрики: 2.5.0
  режим: greenfield
  статус_записи: production
  project_preset: greenfield-product
  change_class: feature
  execution_mode: codex-led
  reserved_slug_override: false
  примечание: создан через launcher
