# Завершенное изменение: очередь обновлений GitHub Actions workflow

## Кратко
- Устаревшая очередь Dependabot PR по workflow actions сведена в один remediation branch, принадлежащий этой задаче.
- `.github/workflows/ci.yml` и `.github/workflows/release.yml` обновлены согласованно:
  - `actions/checkout@v6`
  - `actions/setup-python@v6`
  - `actions/upload-artifact@v7`
- PR #1, PR #2 и PR #3 классифицированы как устаревшая очередь поверх уже исправленного verify baseline, а не как три независимые merge-задачи.

## Проверка
- `bash template-repo/scripts/verify-all.sh ci` прошел до remediation на текущем `main`.
- `bash EXAMPLES_TEST.sh` прошел, включая `validate-versioning-layer.py`.
- Dry-run путь release bundle создал непустой zip artifact.
- `bash template-repo/scripts/verify-all.sh ci` прошел после remediation.

## Последующее закрытие
- Опубликован один consolidated PR.
- PR #1, PR #2 и PR #3 закрыты как superseded.
- Сводный PR #4 merged в `main`.
