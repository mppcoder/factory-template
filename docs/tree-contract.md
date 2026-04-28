# Контракт дерева factory-template

`template-repo/tree-contract.yaml` является machine-readable source для дерева фабрики, template base skeleton и generated projects.
Документ ниже объясняет тот же контракт для оператора.

## Контуры

Контракт описывает общий lifecycle core и несколько контуров:

- `factory_root` — корень `mppcoder/factory-template`;
- `template_base` — базовый skeleton в `template-repo/template`;
- `generated_greenfield` — проект, созданный с preset `greenfield-product`;
- `generated_brownfield_without_repo` — compatibility label для transitional intake/reconstruction с preset `brownfield-without-repo`;
- `generated_brownfield_with_repo` — compatibility label для transitional audit/adoption с presets `brownfield-with-repo-modernization`, `brownfield-with-repo-integration`, `brownfield-with-repo-audit`;
- `converted_greenfield` — steady-state после успешного brownfield adoption.

Инвариант: all projects = project lifecycle core + type-specific owned layer.

`factory-template` — обычный `greenfield-product`, чей продукт — фабрика проектов. Отличие от боевого greenfield проекта только в дополнительном `factory-producer-owned` layer: template generation, release, packaging, registry, downstream sync, reference packs и archives.

Проверка:

```bash
python3 template-repo/scripts/validate-tree-contract.py .
```

Для generated project validator определяет contour по `.chatgpt/project-profile.yaml`.

## Канонический factory root

Корень фабрики содержит release-facing и operator-facing слой:

```text
factory-template/
├── AGENTS.md
├── README.md
├── VERSION.md
├── CHANGELOG.md
├── CURRENT_FUNCTIONAL_STATE.md
├── .chatgpt/
├── .codex/
├── docs/
├── project-knowledge/
├── reports/
├── scripts/
├── src/
├── tasks/
├── tests/
├── work/
├── work-templates/
├── brownfield/
├── greenfield/
├── template-repo/
├── deploy/
└── factory/
    └── producer/
        ├── ops/
        ├── release/
        ├── packaging/
        ├── registry/
        ├── sync/
        ├── reference/
        ├── extensions/
        └── archive/
```

`/projects` на VPS содержит только project roots. Временные входящие материалы должны жить внутри конкретного project root, например `/projects/<project-root>/_incoming/`.
Все temporary, intermediate, reconstructed и helper repos для intake/adoption/reconstruction должны находиться внутри repo целевого `greenfield-product`, например `/projects/<target-greenfield-project>/...`. Создавать такие промежуточные repo как соседние project roots прямо в `/projects` запрещено.

## Контракт именования

`project_name` и `project_slug` - разные поля:

- `project_name` - человекочитаемое имя. Можно писать по-русски, по-английски, с пробелами и пунктуацией.
- `project_slug` - технический идентификатор: lowercase Latin, цифры и дефис.

Канонические правила slug:

- regex: `^[a-z0-9][a-z0-9-]{1,62}$`;
- максимум 63 символа;
- без leading/trailing hyphen;
- repeated hyphens схлопываются при генерации и запрещены в user-provided slug;
- empty slug - blocker, silent fallback в `new-project` запрещен;
- reserved/generic slugs (`new-project`, `project`, `test`, `demo`, `example`, `factory-template`, `template-repo`) требуют явного override marker.

Примеры deterministic mapping:

- `Краб — CRM для ремонта` -> `krab-crm-remonta`;
- `AI Factory` -> `ai-factory`;
- `Мой первый проект!!!` -> `moy-pervyy-proekt`.

Локальный repo path в production VPS layout: `/projects/<project_slug>`. Если launcher запущен в выбранной parent directory, создается `./<project_slug>`.
GitHub repo должен называться `<github_owner>/<project_slug>`. Local repo basename и GitHub repo name должны совпадать с `project_slug` exactly.

Brownfield naming: final/canonical repo называется по target product slug, а не по transition stage. Launcher/validator не должны автоматически добавлять `-brownfield` или `-greenfield`; temporary, incoming, reconstructed и helper repos живут внутри `/projects/<project_slug>/...`.

GitHub owner берется из `--github-owner` или config. Если owner не задан, допустимо использовать authenticated `gh`/GitHub connector user только когда это однозначно. Если owner ambiguous, это blocker. Default visibility для создаваемого GitHub repo - `private`.

## Базовый template skeleton

`template-repo/template` — это scaffold, который materialize-ится в generated project:

```text
template-repo/template/
├── AGENTS source создается launcher-ом из template-repo/AGENTS.md
├── README.md
├── VERSION.md
├── CHANGELOG.md
├── CURRENT_FUNCTIONAL_STATE.md
├── .chatgpt/
├── .codex/
├── brownfield/
├── greenfield/
├── docs/
├── meta-feedback/
├── project-knowledge/
├── reports/
├── scripts/              # добавляется launcher-ом из template-repo/scripts
├── src/
├── tasks/
├── tests/
├── work/
└── work-templates/
```

Файл `AGENT.md` запрещен. Канонический downstream instruction file называется `AGENTS.md` и создается через `template-repo/scripts/sync-agents.py`.

## Контуры generated projects

Все generated projects получают общий repo-first scaffold:

```text
<project-root>/
├── AGENTS.md
├── README.md
├── VERSION.md
├── CHANGELOG.md
├── CURRENT_FUNCTIONAL_STATE.md
├── .chatgpt/
├── .codex/
├── brownfield/
├── greenfield/
├── docs/
├── meta-feedback/
├── project-knowledge/
├── reports/
├── scripts/
├── src/
├── tasks/
├── tests/
├── template-repo/scenario-pack/
├── work/
├── work-templates/
├── change-classes.yaml
├── policy-presets.yaml
├── project-presets.yaml
├── compatibility-aliases.yaml
├── codex-routing.yaml
├── codex-model-routing.yaml
└── template-repo/tree-contract.yaml
```

Различие между greenfield и brownfield не в другом lifecycle core, а в selected preset, active route, lifecycle state и ownership layer.

Greenfield обязательно опирается на:

- `greenfield/vision.md`
- `greenfield/problem-statement.md`
- `greenfield/scope-v1.md`
- `greenfield/architecture-options.md`
- `greenfield/initial-task-list.md`

Brownfield без repo — transitional intake/reconstruction path. Он обязательно опирается на:

- `brownfield/system-inventory.md`
- `brownfield/repo-audit.md`
- `brownfield/as-is-architecture.md`
- `brownfield/gap-register.md`
- `brownfield/reverse-engineering-summary.md`
- `meta-feedback/factory-bug-report.md`
- `meta-feedback/factory-task.md`

Exit gate: создать или определить canonical repo root, пройти with-repo audit/adoption cycle, затем переключить active profile на `greenfield-product`, либо зафиксировать blocker.

Brownfield с repo — transitional audit/adoption path. Он обязательно опирается на:

- `brownfield/system-inventory.md`
- `brownfield/repo-audit.md`
- `brownfield/as-is-architecture.md`
- `brownfield/gap-register.md`
- `brownfield/change-map.md`
- `brownfield/risks-and-constraints.md`

Exit gate: repo-first core установлен, scenario-pack работает, defect-capture/handoff работают, project tests/smoke checks проходят, protected project-owned zones записаны, risks/constraints resolved or accepted, затем active profile переключается на `greenfield-product`.

После conversion:

- `.chatgpt/project-profile.yaml` содержит `project_preset: greenfield-product` и `recommended_mode: greenfield`;
- `.chatgpt/stage-state.yaml` содержит `lifecycle_state: greenfield-converted`;
- `greenfield/vision.md`, `problem-statement.md`, `scope-v1.md`, `architecture-options.md`, `initial-task-list.md` отражают уже нормализованный продукт;
- `brownfield/` остается historical evidence/archive и не управляет active mode.

## Ownership-классы

Machine-readable taxonomy живет в `template-repo/tree-contract.yaml`.

- `project-core` — общий lifecycle core;
- `template-owned-safe` и `template-owned-clone` — controlled sync zones;
- `template-owned-advisory` — diff/review only;
- `project-owned` — продуктовый код, specs, history и decisions, never overwrite;
- `brownfield-evidence-owned`, `brownfield-reconstruction-owned`, `brownfield-audit-owned` — protected transition/history zones;
- `factory-producer-owned` — factory-only producer layer, excluded from battle sync;
- `historical-archive` — retained evidence/release history;
- `transient-generated` — ignored runtime/test/build output.

## Optional и reference layers

Optional/reference layers допустимы только как явно помеченные дополнительные контуры:

- `factory/producer/reference/domain-packs/` — предметные reference cases, не core;
- `factory/producer/extensions/workspace-packs/` — operational tooling для downstream sync, patch export и rollback;
- `factory/producer/reference/examples/` — examples и fixtures;
- `docs/operator/factory-template/` — operator/runbook слой для самой фабрики.
- `factory/producer/archive/` — исторические архивы и legacy bootstrap evidence.

Эти слои не должны становиться canonical generated project root structure без отдельного решения и обновления `tree-contract.yaml`.

## Запрещенная historical naming

В primary UX запрещено показывать исторические или продуктовые имена как нормальные route/preset names.

Запрещено в primary UX:

- `product-dev`
- `legacy-modernization`
- `integration-project`
- `audit-only`
- `brownfield-dogfood-codex-assisted`

Запрещено создавать новые core paths с historical/product-specific terms вроде `dogfood` или `openclaw`.
Исключения разрешены только там, где они явно перечислены в `template-repo/tree-contract.yaml`:

- `template-repo/compatibility-aliases.yaml` — compatibility-only alias map;
- historical archive paths;
- optional domain reference paths;
- explicit compatibility wrapper paths.

## Слой compatibility

Старые aliases живут только в `template-repo/compatibility-aliases.yaml`.
`template-repo/project-presets.yaml` содержит только canonical presets.

Launcher и `apply-project-preset.py` читают compatibility aliases как входную совместимость, но generated beginner UX и docs должны показывать только canonical names.

## Область validator

`validate-tree-contract.py` проверяет:

- обязательные paths для каждого contour;
- отсутствие запрещенных paths;
- отсутствие `preset_aliases` в active `project-presets.yaml`;
- наличие explicit compatibility aliases layer;
- отсутствие legacy aliases в primary UX files;
- отсутствие новых forbidden path terms вне allowlist.
- отсутствие legacy/factory-only folders как active root paths;
- размещение factory-producer-owned content только под `factory/producer/*`;
- отсутствие `factory/producer/*` в generated/battle projects.
- canonical naming: project path basename equals `project_slug`, origin repo name equals `project_slug`, slug matches policy, reserved slug has explicit override marker, brownfield/helper repos не создаются sibling roots под `/projects`.

Validator не запрещает project-owned code внутри `src/` и других рабочих каталогов generated project. Контракт фиксирует factory-owned scaffold и границы core/optional/compatibility layers.
