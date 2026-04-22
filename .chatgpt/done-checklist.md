# Чек-лист завершения

- [ ] Проверить, что задача выполнена
- [ ] Обновить verification-report.md
- [ ] Обновить done-report.md
- [ ] Обновить CURRENT_FUNCTIONAL_STATE.md
- [ ] Проверить, нужен ли feedback в фабрику
- [ ] Если был найден defect, создать или обновить bug report
- [ ] Если найден unresolved incidental defect, подготовить self-handoff и зафиксировать route decision
- [ ] Если для incidental defect нужен другой route, подготовить готовый handoff для нового Codex task/chat
- [ ] Если для incidental defect нужен deep research, подготовить ChatGPT-ready research bug report/prompt
- [ ] Проверить `.chatgpt/task-launch.yaml`
- [ ] Проверить `.chatgpt/normalized-codex-handoff.md`
- [ ] Если `origin` настроен и verify green, прогнать `bash VALIDATE_VERIFIED_SYNC_PREREQS.sh`
- [ ] Если prereqs green и diff допустим, прогнать `bash VERIFIED_SYNC.sh` до финального closeout
- [ ] Если verified sync не выполнен, явно зафиксировать реальный blocker и не помечать change как `done`

## Impact classification

- [ ] impact.factory_sources
- [ ] impact.downstream_template_sync
- [ ] impact.downstream_project_sources
- [ ] impact.manual_archive_required
- [ ] impact.delete_before_replace

## Completion Package For Repo-First Instruction Changes

- [ ] Что изменено
- [ ] Какие файлы обновлены в repo
- [ ] Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project
- [ ] Нужно ли обновлять downstream template in battle repos
- [ ] Нужно ли обновлять repo-first инструкции battle ChatGPT Projects
- [ ] Готовые артефакты для скачивания
- [ ] Команды/скрипты для repo-level sync
- [ ] Удалить перед заменой
- [ ] Пошаговая инструкция по окнам
- [ ] Что прислать обратно после внешнего шага
- [ ] Completion package выдан в том же финальном ответе, без дополнительного напоминания пользователя
- [ ] Если есть pending external step, финальный ответ действительно заканчивается блоком `## Инструкция пользователю`
- [ ] Если найден incidental defect, финальный ответ явно говорит: same-chat fallback / recommended new Codex task / deep research
