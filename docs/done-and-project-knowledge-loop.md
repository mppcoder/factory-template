# Цикл done и Project Knowledge

Этот loop закрывает feature так, чтобы решения не исчезали вместе с рабочей папкой.

Обычный `/done` в `molyanov-ai-dev` делает четыре полезные вещи: читает `user-spec`, `tech-spec` и `decisions.md`, обновляет Project Knowledge, архивирует feature в `work/completed/` и сообщает результат. Factory-template сохраняет эту идею, но делает ее проверяемой через отдельные closeout artifacts и validator.

## Зачем это новичку

Feature work почти всегда содержит маленькие решения: почему выбран один путь, что оказалось не нужно, где появилось ограничение, какую проверку реально выполнили. Если оставить это только в чате или commit message, следующий участник начнет заново.

Поэтому closeout разделяет два слоя:
- `work/features/<feature>/decisions.md` хранит решения конкретной задачи;
- `project-knowledge/` хранит только устойчивые знания, которые пригодятся будущим задачам.

Не каждое решение нужно переносить в Project Knowledge. Но каждый closeout должен явно сказать: перенос нужен или не нужен, и почему.

## Closeout в factory-template

Команда:

```bash
python3 template-repo/scripts/close-feature-workspace.py work/features/<feature-id>
```

Она читает:
- `specs/user-spec.md`;
- `specs/tech-spec.md`;
- `decisions.md`;
- advanced evidence из `logs/`, если feature использовала `feature-execution-lite`.

Затем создает в feature workspace:
- `done-report.md` — summary, прочитанные источники, decisions, evidence и archive result;
- `project-knowledge-update-proposal.md` — что нужно перенести в `project-knowledge/` или почему перенос не требуется;
- `downstream-impact.md` — нужен ли downstream review/sync;
- `closeout-blocker.md`, если архивирование заблокировано.

После успешного closeout workspace переносится в:

```text
work/completed/<feature-id>/
```

## Proposal для Project Knowledge

Proposal не переписывает `project-knowledge/` молча. Он делает следующий шаг явным:
- `status: required` — есть устойчивый вывод или follow-up candidate;
- `status: not_required` — перенос не нужен, но причина записана.

Так future maintainer видит, что decisions были просмотрены, а не потеряны.

## Evidence для Feature Execution Lite

Если feature использовала `feature-execution-lite`, closeout проверяет:
- `logs/execution-plan.md`;
- `logs/checkpoint.yaml`;
- task waves в `tasks/T-*.md`;
- entries в `decisions.md` с `execution_wave`, `review_rounds` и `boundary`;
- `final_verification.status: passed`.

Если feature меняла reusable artifact, scenario-pack, skill, policy или advanced execution template, приложите artifact-eval evidence:

```bash
python3 template-repo/scripts/close-feature-workspace.py \
  work/features/<feature-id> \
  --artifact-eval-report tests/artifact-eval/reports/<report>.md
```

Если artifact eval не нужен, `done-report.md` должен явно сказать `status: not_required` и дать причину.

## Validator для closeout

Проверка одного закрытого workspace:

```bash
python3 template-repo/scripts/validate-project-knowledge-update.py . \
  --workspace work/completed/<feature-id>
```

Validator требует:
- `done-report.md`;
- непустой `decisions.md`;
- `project-knowledge-update-proposal.md` со статусом `required` или `not_required`;
- `downstream-impact.md`;
- archive в `work/completed/` или явный `closeout-blocker.md`;
- для `feature-execution-lite` — execution-plan, checkpoint, task waves, final verification и artifact-eval evidence link/justification.

`verify-all.sh quick` запускает smoke fixture и проверяет реальный archive/proposal/evidence path во временной директории.
