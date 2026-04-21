# Пользовательская спецификация

## Цель изменения
- Сделать source-update completion package нормой completion/handoff layer.
- Обязать Codex явно различать factory Sources, downstream repo sync и downstream ChatGPT Project Sources.
- Требовать delete-before-replace, ready artifacts и window-by-window instructions для manual external steps.

## Что должно получиться
- После relevant change completion output явно показывает, какие external update contours затронуты.
- Для manual replacement есть точный список `Удалить перед заменой`.
- Для repo-level sync и Sources refresh указаны готовые артефакты и точные скрипты.

## Что не входит в объем
- Автоматическое управление GitHub UI или ChatGPT UI.
- Новый entry-mode matrix.
- Автопубликация релиза.
