# Bug report: mode parity gap

## Статус
Исправлено в рамках текущей remediation-задачи.

## Дата
2026-04-25

## Обнаружено в
- `template-repo/template/work`
- `template-repo/project-presets.yaml`
- `onboarding-smoke/run-novice-e2e.sh`

## Симптом
Контракт задачи требовал доказать, что template, greenfield, brownfield-without-repo и brownfield-with-repo имеют одинаковый core layer, включая `work/features` и `work/completed`.

До remediation в template skeleton был `work/active` и `work/completed`, но не было явного `work/features`, хотя `template-repo/scripts/init-feature-workspace.sh` использует `work/features` как default workspace path.

## Воспроизведение
1. Проверить `template-repo/template/work`.
2. Сравнить список директорий с требуемым core capability `work/features and work/completed`.
3. Проверить `template-repo/scripts/init-feature-workspace.sh`, где default `BASE_DIR="work/features"`.

## Ожидаемое поведение
Generated project должен иметь оба core пути:
- `work/features`
- `work/completed`

## Фактическое поведение
Template skeleton материализовал:
- `work/active`
- `work/completed`

`work/features` появлялся только как runtime target при запуске feature workspace script.

## Классификация слоя
- defect layer: `factory-template`
- affected contour: generated project template skeleton
- reusable issue: yes
- downstream impact: template-consumed generated tree

## Исправление
- добавлен `template-repo/template/work/features/.gitkeep`;
- `template-repo/tree-contract.yaml` расширен на `work/features`;
- `template-repo/mode-parity.yaml` закрепил `work_features_and_completed` как обязательный core capability;
- `template-repo/project-presets.yaml` теперь перечисляет общий parity core в каждом canonical preset;
- `template-repo/scripts/validate-mode-parity.py` проверяет этот контракт;
- `onboarding-smoke/run-novice-e2e.sh` покрывает все canonical presets.

## Проверка
- `python3 template-repo/scripts/validate-mode-parity.py .`
- `python3 template-repo/scripts/validate-tree-contract.py .`
- `bash onboarding-smoke/run-novice-e2e.sh`
