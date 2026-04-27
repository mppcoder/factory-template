# Factory Feedback: downstream sync v3 needs multi-cycle proof

Источник: `reports/bugs/2026-04-27-downstream-multi-cycle-sync-gap.md`.

## Почему это reusable factory issue

Downstream/battle repos используют общий factory ops sync contract. Если фабрика доказывает только один safe/advisory/manual pass, downstream operator не получает repo-controlled evidence для более реального сценария: несколько sync циклов, ручные project-owned edits между ними, advisory review и rollback после накопленного состояния.

## Требуемое изменение

- Закрепить multi-cycle downstream sync validator в factory ops.
- Проверять safe-generated/safe-clone apply отдельно от advisory-review/manual-project-owned.
- Проверять rollback metadata после нескольких циклов.
- Проверять `converted_greenfield`, где brownfield history становится protected history, а не template starter content.
- Явно классифицировать production VPS field-pilot docs/scripts/reports и runtime boundaries.

## Принятое исправление

- `validate-downstream-multi-cycle-sync.py` создает synthetic downstream fixture и прогоняет multi-cycle proof.
- `factory-sync-manifest.yaml` добавляет safe deploy templates/scripts, advisory field-pilot docs/report и manual-only runtime/secrets boundaries.
- `MATRIX_TEST.sh` включает proof в representative matrix.
- `docs/downstream-upgrade-policy.md` и release report фиксируют operator boundary.

## Acceptance

- Project-owned edits остаются защищены.
- Advisory-review не применяется автоматически.
- Rollback работает после нескольких циклов.
- Brownfield history сохраняется после conversion.
- Real VPS deploy, secrets, `.factory-runtime/` и `deploy/.env` остаются вне automatic sync.
