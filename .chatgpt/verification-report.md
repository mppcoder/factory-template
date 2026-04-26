# Отчет о проверке результата

## Что проверяли
- Исправление остановки closeout перед внутренним brownfield follow-up.
- Исправление отсутствия обязательной пользовательской инструкции в generated direct-task / closeout guidance.
- Source-candidate map и reconstruction boundary для `/root/.openclaw` и `/root/openclaw-plus`.
- Продвижение field pilot roadmap до FP-02 evidence completion.
- Исправление преждевременного FP-02 pass до создания project repo.
- Создание локального project repo `/projects/openclaw-brownfield`.
- Совместимость новых generator/validator правил с существующими routing и handoff validators.

## Статус defect-capture
- Bug report создан: `reports/bugs/bug-035-closeout-stopped-before-internal-followup-and-user-instruction.md`.
- Factory feedback создан: `reports/factory-feedback/feedback-035-closeout-stopped-before-internal-followup-and-user-instruction.md`.
- Bug report создан: `reports/bugs/bug-036-fp02-marked-passed-before-repo-creation.md`.
- Factory feedback создан: `reports/factory-feedback/feedback-036-fp02-marked-passed-before-repo-creation.md`.
- Статус remediation: fixed-in-current-scope.

## Что подтверждено
- `source-candidate-map` является internal Codex-eligible follow-up, а не ручным пользовательским шагом.
- `/root/openclaw-plus` является основным source candidate root.
- `/root/.openclaw` допускается только как limited candidate root после redaction/review.
- `reports/release/field-pilot-scenarios/02-brownfield-without-repo.md` переведен в `passed` на sanitized OpenClaw+ кейсе.
- `/projects/openclaw-brownfield` создан как локальный project repo и зафиксирован commit `4a58c8d`.
- `/projects/openclaw-brownfield/src/openclaw-plus` содержит sanitized reconstruction из `/root/openclaw-plus`.
- Raw `/root/.openclaw` и raw `/etc/openclaw-plus.env` не перенесены.
- Общий field pilot status стал `partial-field-evidence`, `1/5`; FP-01/FP-03/FP-04/FP-05 не помечались как пройденные.
- Generated/dependency zones исключены через denylist: `.venvs`, `node_modules`, `__pycache__`, `var`, logs, sqlite, jsonl.
- `render_direct_task_response` теперь генерирует publishable direct-task response с `## Handoff в Codex`, continuation rule и closeout instruction rule.
- `validate-codex-routing.py` закрепляет запрет остановки на self-handoff и требование `## Инструкция пользователю` / `Внешних действий не требуется.`.
- `create-codex-task-pack.py` и `validate-codex-task-pack.py` закрепляют brownfield source-candidate follow-up как internal repo work.

## Команды проверки
- `python template-repo/scripts/validate-codex-routing.py .`: прошла.
- `python template-repo/scripts/validate-handoff-response-format.py .chatgpt/direct-task-response.md`: прошла.
- `python template-repo/scripts/validate-codex-task-pack.py .`: прошла.
- `python template-repo/scripts/validate-evidence.py .`: прошла.
- `python template-repo/scripts/validate-brownfield-transition.py .`: прошла.
- `python template-repo/scripts/validate-quality.py .`: прошла.
- `python template-repo/scripts/validate-human-language-layer.py .`: прошла.
- `python scripts/validate-brownfield-transition.py .` в `/projects/openclaw-brownfield`: прошла.
- `python scripts/validate-evidence.py .` в `/projects/openclaw-brownfield`: прошла.
- `python scripts/validate-codex-task-pack.py .` в `/projects/openclaw-brownfield`: прошла.
- `git -C /projects/openclaw-brownfield status --short --branch`: clean on `main`.
- `bash template-repo/scripts/verify-all.sh` в `/projects/factory-template`: прошла, `VERIFY-ALL ПРОЙДЕН (full)`.

## Итоговый вывод
- Оба заявленных дефекта исправлены в source-of-truth repo.
- Source-candidate map и reconstruction boundary подготовлены.
- Недостающий repo creation step выполнен: `/projects/openclaw-brownfield`, commit `4a58c8d`.
- Runtime OpenClaw не изменялся.
