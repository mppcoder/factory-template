# Отчет о проверке результата

## Что проверяли
- Defect `bug-032`: upstream ChatGPT-generated handoff может прийти с англоязычными человекочитаемыми разделами.
- Defect-capture artifacts.
- Language-contract validator для `.chatgpt/codex-input.md`.
- Интеграцию validator в `validate-codex-task-pack.py`.
- Negative fixture для англоязычных `Goal` / `Hard constraints`.

## Статус defect-capture
- Bug report создан: `reports/bugs/bug-032-chatgpt-handoff-language-contract-gap.md`.
- Factory feedback создан: `reports/factory-feedback/feedback-032-chatgpt-handoff-language-contract-gap.md`.
- Статус remediation: fixed-in-current-scope.

## Что подтверждено
- `validate-handoff-language.py` пропускает текущий русскоязычный `.chatgpt/codex-input.md`.
- `validate-handoff-language.py` отклоняет англоязычный fixture с `Goal`, `Hard constraints`, `Do not hardcode`.
- `validate-codex-task-pack.py` успешно проходит с подключенным language validator.
- `validate-handoff-response-format.py` успешно проходит после расширения forbidden handoff headings.

## Команды проверки
- `python3 template-repo/scripts/validate-handoff-language.py .chatgpt/codex-input.md`: прошла.
- `printf 'Goal:\nImplement feature\n\nHard constraints:\nDo not hardcode latest model\n' | python3 template-repo/scripts/validate-handoff-language.py -`: упала ожидаемо.
- `python3 template-repo/scripts/validate-codex-task-pack.py .`: прошла.
- `python3 template-repo/scripts/validate-handoff-response-format.py .chatgpt/handoff-response.md`: прошла.
- `python3 template-repo/scripts/validate-codex-routing.py .`: прошла.
- `bash template-repo/scripts/verify-all.sh quick`: прошла.

## Итоговый вывод
- `bug-032` воспроизведен по пользовательскому сигналу и исправлен.
- Англоязычный upstream handoff теперь должен падать в repo validation до нормального closeout.
