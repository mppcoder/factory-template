# chg-20260425-language-layer-cleanup

## Summary / сводка
- Закрыт полный cleanup для `bug-033`: active source-facing слой нормализован под русский человекочитаемый язык.
- Добавлены documented archival exceptions для historical reports, old completed work, legacy packs и fixture evidence.
- Добавлен validator `template-repo/scripts/validate-human-language-layer.py` и подключен в `template-repo/scripts/verify-all.sh quick`.

## Updated artifacts / обновленные артефакты
- `template-repo/language-archive-exceptions.yaml`
- `docs/language-layer-policy.md`
- `template-repo/scripts/validate-human-language-layer.py`
- active docs/release artifacts/skills/template handoff files
- `reports/bugs/bug-033-repo-wide-english-human-layer-residue.md`
- `reports/factory-feedback/feedback-033-repo-wide-english-human-layer-residue.md`

## Verification / проверка
- `python3 template-repo/scripts/validate-human-language-layer.py .`
- `active findings: 0`
- `archival exception findings: 171`

## Notes / заметки
- Archival exceptions не означают, что английский “исчез из истории”. Они фиксируют границу: старый evidence text сохраняется, а active source-facing слой должен проходить validator.
