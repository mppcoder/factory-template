# Контракт дерева factory-template

`template-repo/tree-contract.yaml` является machine-readable source для дерева фабрики, template base skeleton и generated projects.
Документ ниже объясняет тот же контракт для оператора.

## Контуры

Контракт описывает пять контуров:

- `factory_root` — корень `mppcoder/factory-template`;
- `template_base` — базовый skeleton в `template-repo/template`;
- `generated_greenfield` — проект, созданный с preset `greenfield-product`;
- `generated_brownfield_without_repo` — evidence-first проект с preset `brownfield-without-repo`;
- `generated_brownfield_with_repo` — проект с существующим repo и presets `brownfield-with-repo-modernization`, `brownfield-with-repo-integration`, `brownfield-with-repo-audit`.

Проверка:

```bash
python3 template-repo/scripts/validate-tree-contract.py .
```

Для generated project validator определяет contour по `.chatgpt/project-profile.yaml`.

## Канонический factory root

Корень фабрики содержит release-facing и operator-facing слой:

```text
factory-template/
├── README.md
├── ENTRY_MODES.md
├── FACTORY_MANIFEST.yaml
├── CURRENT_FUNCTIONAL_STATE.md
├── TEST_REPORT.md
├── docs/
├── reports/
├── template-repo/
├── workspace-packs/
├── optional-domain-packs/
├── working-project-examples/
└── factory_template_only_pack/
```

`/projects` на VPS содержит только project roots. Временные входящие материалы должны жить внутри конкретного project root, например `/projects/<project-root>/_incoming/`.

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

Различие между greenfield и brownfield не в другом наборе сценариев, а в selected preset, active route и обязательных смысловых артефактах.

Greenfield обязательно опирается на:

- `greenfield/vision.md`
- `greenfield/problem-statement.md`
- `greenfield/scope-v1.md`
- `greenfield/architecture-options.md`
- `greenfield/initial-task-list.md`

Brownfield без repo обязательно опирается на:

- `brownfield/system-inventory.md`
- `brownfield/repo-audit.md`
- `brownfield/as-is-architecture.md`
- `brownfield/gap-register.md`
- `brownfield/reverse-engineering-summary.md`
- `meta-feedback/factory-bug-report.md`
- `meta-feedback/factory-task.md`

Brownfield с repo обязательно опирается на:

- `brownfield/system-inventory.md`
- `brownfield/repo-audit.md`
- `brownfield/as-is-architecture.md`
- `brownfield/gap-register.md`
- `brownfield/change-map.md`
- `brownfield/risks-and-constraints.md`

## Optional и reference layers

Optional/reference layers допустимы только как явно помеченные дополнительные контуры:

- `optional-domain-packs/` — предметные reference cases, не core;
- `workspace-packs/` — operational tooling для downstream sync, patch export и rollback;
- `working-project-examples/` — examples и fixtures;
- `factory_template_only_pack/` — operator/runbook слой для самой фабрики.

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

Validator не запрещает project-owned code внутри `src/` и других рабочих каталогов generated project. Контракт фиксирует factory-owned scaffold и границы core/optional/compatibility layers.
