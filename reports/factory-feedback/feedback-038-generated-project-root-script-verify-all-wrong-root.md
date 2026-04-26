# FEEDBACK-038: Generated root scripts должны работать из `root/scripts`

Дата: 2026-04-26

## Наблюдение

Скрипты, которые живут в `template-repo/scripts`, после materialization также попадают в generated project root `scripts`. Если script вычисляет root только как `../..`, он ломается в generated contour.

## Правило

Root detection для materialized scripts должен различать:

- `template-repo/scripts/*`;
- root-level `scripts/*`.

## Current remediation

`verify-all.sh` получил dual root detection и generated-project quick verify mode.

## Follow-up

При следующих изменениях стоит проверить другие root-level copied scripts на аналогичное предположение о расположении.

## Status

Captured and fixed for `verify-all.sh`.

