# Пользовательская спецификация

## Цель изменения
- Добавить для `factory-template` lightweight follow-up mode поверх существующего verified sync.
- Разрешить auto commit/push для low-risk post-verify cleanup изменений без отдельного ручного подтверждения.
- Сохранить verify-first модель и отдельный release decision contour без изменений.

## Что должно получиться
- После уже зафиксированного green verify low-risk `.gitignore` и docs/closeout follow-up правки тоже auto commit/push через `VERIFIED_SYNC.sh`.
- Lightweight follow-up не должен захватывать code/scripts/policy changes вне allowlist.
- Commit message для lightweight follow-up не должен повторно использовать title предыдущего большого change.

## Что не входит в объем
- Автоматический релиз после любого verify без отдельного решения.
- Ослабление verify требований для non-lightweight изменений.
- Хранение секретов в repo.
