# Чек-лист завершения

- [ ] Проверить, что задача выполнена
- [ ] Обновить verification-report.md
- [ ] Обновить done-report.md
- [ ] Обновить CURRENT_FUNCTIONAL_STATE.md
- [ ] Проверить, нужен ли feedback в фабрику
- [ ] Если был найден defect, создать или обновить bug report
- [ ] Проверить `.chatgpt/task-launch.yaml`
- [ ] Проверить `.chatgpt/normalized-codex-handoff.md`
- [ ] Если `origin` настроен и verify green, прогнать `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
- [ ] Если prereqs green и diff допустим, прогнать `bash VERIFIED_SYNC.sh` до финального closeout
- [ ] Если verified sync не выполнен, явно зафиксировать реальный blocker и не помечать change как `done`
- [ ] Перед финальным ответом выполнить `git status --short --branch`
- [ ] Если branch ahead или рабочее дерево dirty, выполнить sync/push или явно назвать blocker
- [ ] В финальном ответе указать commit hash / sync status или `no-op`

## Классификация влияния

- [ ] impact.factory_sources
- [ ] impact.downstream_template_sync
- [ ] impact.downstream_project_sources
- [ ] impact.manual_archive_required
- [ ] impact.delete_before_replace

## Пакет завершения для изменений repo-first инструкций

- [ ] Что изменено
- [ ] Какие файлы обновлены в repo
- [ ] Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project
- [ ] По умолчанию: нет, если canonical repo/path/entrypoint/instruction text не менялись
- [ ] Нужно ли обновлять downstream template in battle repos
- [ ] Нужно ли обновлять repo-first инструкции battle ChatGPT Projects
  По умолчанию: нет для чистого repo-first режима; да только для legacy/hybrid fallback
- [ ] Готовые артефакты для скачивания
- [ ] Команды/скрипты для repo-level sync
- [ ] Удалить перед заменой
- [ ] Пошаговая инструкция по окнам
- [ ] Что прислать обратно после внешнего шага
- [ ] Пакет завершения выдан в том же финальном ответе, без дополнительного напоминания пользователя
- [ ] Если есть ожидающий внешний шаг, финальный ответ действительно заканчивается блоком `## Инструкция пользователю`
- [ ] Если ожидающего внешнего шага нет, финальный ответ явно говорит, что внешних действий не требуется
