# Матрица mode parity

Эта матрица — человекочитаемое дополнение к `template-repo/mode-parity.yaml`.
YAML-манифест остается machine-readable контрактом; документ объясняет смысл core слоя и допустимых отличий.

## Core слой возможностей

Каждый generated project mode должен нести один и тот же core layer:

| Capability | Template base | Greenfield | Brownfield without repo | Brownfield with repo |
| --- | --- | --- | --- | --- |
| `repo_first_instructions` | yes | yes | yes | yes |
| `scenario_pack_access` | yes | yes | yes | yes |
| `agents_materialization` | yes | yes | yes | yes |
| `chatgpt_task_artifacts` | yes | yes | yes | yes |
| `codex_handoff_pack` | yes | yes | yes | yes |
| `defect_capture_path` | yes | yes | yes | yes |
| `versioning_documentation_layer` | yes | yes | yes | yes |
| `project_knowledge_layer` | yes | yes | yes | yes |
| `work_features_and_completed` | yes | yes | yes | yes |
| `verify_done_checklist` | yes | yes | yes | yes |
| `downstream_sync_metadata` | yes | yes | yes | yes |

## Обязательные core artifacts

Обязательный набор core artifacts общий для всех generated presets:

- repo-first entry: `AGENTS.md`, `template-repo/scenario-pack/00-master-router.md`
- `.chatgpt` task layer: `project-profile.yaml`, `task-index.yaml`, `task-state.yaml`, `stage-state.yaml`, `active-scenarios.yaml`
- handoff layer: `codex-input.md`, `direct-task-self-handoff.md`, `normalized-codex-handoff.md`, `task-launch.yaml`
- defect layer: `.chatgpt/bugflow-status.yaml`, `reports/bugs`, `reports/learnings`, `reports/factory-feedback`, `meta-feedback/factory-bug-report.md`
- docs/versioning layer: `VERSION.md`, `CHANGELOG.md`, `CURRENT_FUNCTIONAL_STATE.md`, `README.md`, `docs/architecture.md`, `docs/codex-workflow.md`
- project knowledge: `project-knowledge/README.md` and topic files
- work lifecycle: `work/features`, `work/completed`, `work-templates/*`
- verify/done: `.chatgpt/verification-report.md`, `.chatgpt/done-checklist.md`, `.chatgpt/done-report.md`
- downstream sync metadata: `project-presets.yaml`, `policy-presets.yaml`, `compatibility-aliases.yaml`, `codex-routing.yaml`, `codex-model-routing.yaml`, `template-repo/tree-contract.yaml`, `template-repo/mode-parity.yaml`

## Допустимые отличия

| Mode | Preset | Допустимый mode-specific layer | Почему это разрешено |
| --- | --- | --- | --- |
| Template base | n/a | Содержит greenfield и brownfield starter folders | Template является source skeleton, поэтому содержит все стартовые поверхности. |
| Greenfield | `greenfield-product` | `greenfield/*`, `.chatgpt/discovery-summary.md` | Новому проекту нужны discovery artifacts до появления evidence. |
| Brownfield without repo | `brownfield-without-repo` | evidence-first brownfield artifacts плюс reverse-engineering plan/summary | Нормализованного repo еще нет, поэтому reconstruction и incoming evidence являются first-class слоем. |
| Brownfield with repo modernization | `brownfield-with-repo-modernization` | repo audit, change map, risks, conflict report | Работа с существующим repo требует audit и modernization boundaries до правок. |
| Brownfield with repo integration | `brownfield-with-repo-integration` | integration docs, reality check, tech spec | Риск integration живет в dependencies, versions и external contracts. |
| Brownfield with repo audit | `brownfield-with-repo-audit` | gap register, evidence register, done report | Audit mode может завершиться findings без обязательного implementation handoff. |

## Проверка

Команда:

```bash
python3 template-repo/scripts/validate-mode-parity.py .
```

Validator проверяет, что:

- all generated modes list the identical `core_capabilities`;
- mode-specific differences are declared and justified in `template-repo/mode-parity.yaml`;
- every canonical preset is mapped to exactly one parity mode;
- every canonical preset carries the shared required artifacts in `template-repo/project-presets.yaml`;
- template/source paths exist for core and mode-specific artifacts;
- generated projects can be validated against the same manifest after scaffold creation.
