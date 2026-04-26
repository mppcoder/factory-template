# BUG-038: generated project `scripts/verify-all.sh` вычислял ROOT как `/projects`

Дата: 2026-04-26

## Кратко

В generated project repo `/projects/openclaw-brownfield` запуск `bash scripts/verify-all.sh` из root-level copied scripts contour вычислял `ROOT` как `/projects`, а затем искал `/projects/CLEAN_VERIFY_ARTIFACTS.sh`.

## Reproduction

```bash
cd /projects/openclaw-brownfield
bash scripts/verify-all.sh
```

До исправления результат:

```text
bash: /projects/CLEAN_VERIFY_ARTIFACTS.sh: No such file or directory
```

## Root cause

`template-repo/scripts/verify-all.sh` предполагал, что script path всегда `template-repo/scripts/verify-all.sh` и вычислял root через `../..`. После materialization в generated root `scripts/verify-all.sh` правильный root находится на один уровень выше.

## Impact

- Fresh generated project repo не мог использовать root-level `scripts/verify-all.sh`.
- Closeout мог ошибочно классифицировать verify как невозможный или внешний manual recovery step.
- FP-02 project repo pack оставался недопроверенным.

## Remediation

- `verify-all.sh` теперь определяет root по расположению script:
  - `root/scripts/verify-all.sh` -> root на один уровень выше;
  - `root/template-repo/scripts/verify-all.sh` -> root на два уровня выше.
- Для generated project без factory-only shell scripts добавлен generated-project quick verify contour.
- В `/projects/openclaw-brownfield` заполнены недостающие quality artifacts, после чего `bash scripts/verify-all.sh` прошел.

## Verification

- `bash scripts/verify-all.sh` в `/projects/openclaw-brownfield`: passed.
- `bash template-repo/scripts/verify-all.sh` в `/projects/factory-template`: будет проверено full verify перед sync.

## Status

Fixed in current scope.

