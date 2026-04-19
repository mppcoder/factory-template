# Сценарий: завершение minimal evidence pack

## Цель
Подтвердить, что собран минимальный evidence pack и можно переходить от чистого аудита к controlled stabilization.

## Что должно быть зафиксировано
- дерево файлов или хотя бы рабочий fs-tree;
- сервисы/systemd/nginx/docker при наличии;
- базовые API probe или smoke-факты;
- схема БД или явная фиксация, что доступ к ней отсутствует;
- ключевые логи;
- reverse engineering summary.

## Выходы
- обновлённый `.chatgpt/evidence-register.md`
- обновлённый `brownfield/reverse-engineering-summary.md`
- решение: остаёмся в `hybrid` или можно готовить переход в `codex-led`
