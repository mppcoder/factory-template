# Guided launcher UX gap

## Дата
2026-04-25

## Сценарий
`2.5-ga/guided-launcher-ux`

## Класс
feature-onboarding-ux / template defect

## Что обнаружено
`template-repo/scripts/factory-launcher.py` уже был единым entrypoint для выбора `greenfield`, `brownfield` и `continue`, но beginner path после создания проекта всё ещё требовал помнить отдельные команды:

- `bash scripts/init-feature-workspace.sh --feature-id first-feature`
- `python3 scripts/factory-launcher.py --mode continue`
- отдельный operator/dashboard запуск для deploy dry-run

Из-за этого launcher оставался хорошей оболочкой над scripts, но не закрывал полный guided path одной основной командой.

## Ожидаемое поведение
Новичок может пройти первый проект одной основной командой:

```bash
python3 template-repo/scripts/factory-launcher.py --guided
```

Путь должен последовательно покрывать:

1. выбор режима;
2. preflight;
3. создание проекта;
4. проверку `project-knowledge`;
5. создание workspace первой задачи;
6. показ следующего шага оператора;
7. опциональный deploy dry-run.

## Фактическое поведение до исправления
Проект создавался, но после этого launcher печатал рекомендацию и завершался, если пользователь заранее не знал флаг `--init-feature-workspace` или отдельную команду `--mode continue`.

## Слой дефекта
factory-template reusable UX layer.

## Решение в текущем scope
Исправляется в текущей remediation-задаче:

- добавить `--guided`, `--continue`, `--status`;
- сделать `--guided` полным beginner path;
- расширить novice smoke на guided greenfield, brownfield without repo, brownfield with repo и continue-flow;
- обновить документацию и verification evidence.

## Статус
fixed-in-current-scope после прохождения smoke и `verify-all.sh ci`.
