# chg-20260426-project-core-producer-layer-and-brownfield-transition

## Статус

completed

## Дата

2026-04-26

## Defect capture

- Bug report: `reports/bugs/2026-04-26-brownfield-must-convert-to-greenfield.md`
- ADR: `docs/decisions/2026-04-26-project-core-producer-layer-and-brownfield-transition.md`

## Что изменено

- `factory-template` закреплен как обычный `greenfield-product`, чей продукт — project factory, с дополнительным `factory-producer-owned` layer.
- Brownfield без repo и brownfield с repo закреплены как transitional adoption states, а не финальные project classes.
- Успешный brownfield adoption теперь требует conversion в `greenfield-product` / `greenfield-converted` или documented blocker.
- Добавлены lifecycle states, ownership classes, conversion gates и validators.
- Sync manifest защищает project-owned/brownfield history и исключает factory producer paths из battle sync.
- Launcher/wizard/preflight и docs больше не описывают brownfield как steady-state project type.

## Проверка

- `python3 template-repo/scripts/validate-tree-contract.py .` — pass.
- `python3 template-repo/scripts/validate-mode-parity.py .` — pass.
- `python3 template-repo/scripts/validate-brownfield-transition.py .` — pass.
- `python3 template-repo/scripts/validate-greenfield-conversion.py .` — pass.
- generated brownfield-without-repo smoke — pass.
- `bash template-repo/scripts/verify-all.sh quick` — pass.
- `bash MATRIX_TEST.sh` — pass.
- `bash template-repo/scripts/verify-all.sh ci` — pass.
- `bash PRE_RELEASE_AUDIT.sh` — pass.

## Физические moves

Физических переносов каталогов не выполнялось.
