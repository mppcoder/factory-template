# Пользовательская спецификация

## Цель изменения
- Добавить для `factory-template` автоматический контур verified sync после успешного verify.
- Сохранить отдельный явный release/no-release decision.
- Автоматизировать publication layer только после явного release decision.

## Что должно получиться
- После успешного verify и при наличии diff выполняются auto commit и auto push.
- Если verify failed, ни commit, ни push, ни release не выполняются.
- Если release decision = `no-release`, ограничиться verified sync без tag и GitHub Release.
- Если release decision = `release`, после verified sync автоматически выполнить tag/release path или записать явный fallback report.

## Что не входит в объем
- Автоматический релиз после любого verify без отдельного решения.
- Параллельное выполнение git-команд.
- Хранение секретов в repo.
