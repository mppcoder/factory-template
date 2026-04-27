# Цикл learning patch

`learning-patch-loop` закрывает маленький, но дорогой пробел: reusable bug не должен теряться после defect-capture. Для каждого явно reusable bug нужен либо proposal, который можно перенести в фабрику/Project Knowledge, либо честная причина `not_required`.

Это не автоматическое изменение `project-knowledge/` и не замена defect-capture. Это легкий evolve layer поверх уже существующих reports.

## Когда нужен

Используйте loop, если bug или gap:

- повторится в других downstream/battle repo;
- относится к scenario-pack, handoff, validator, template, docs или closeout process;
- требует нового reusable rule, template или validator;
- уже привел к factory feedback.

Не используйте loop для разового project-owned bug без reusable вывода. В таком случае укажите `learning_patch_status: not_required` и краткое обоснование.

## Где фиксировать

В новом bug report можно добавить machine-readable строки:

```yaml
reusable: true
learning_patch_status: required
```

Затем создать proposal:

```text
reports/learnings/<bug-id>-learning-patch.md
```

Если reusable learning не нужен:

```yaml
reusable: true
learning_patch_status: not_required
learning_patch_reason: "Разовый project-owned сбой без reusable изменения фабрики."
```

## Предложение

Шаблон находится здесь:

```text
template-repo/template/reports/learnings/learning-patch-proposal.md.template
```

Минимально proposal должен содержать:

- `source_bug`: путь к source bug report;
- `status`: `proposed` или `not_required`;
- `target_surface`: куда должен попасть reusable вывод;
- `proposed_change`: что изменить, если status `proposed`;
- `verification`: как проверить будущую доработку;
- `justification`: причина для `not_required`.

`status: applied`, `done` или `completed` запрещены в proposal: learning patch не должен утверждать, что изменение уже применено, пока отдельная remediation задача не закрыла verify.

## Проверка

```bash
python3 template-repo/scripts/validate-learning-patch-loop.py .
```

Validator проверяет:

- все явно reusable bug reports имеют proposal или `not_required` reason;
- proposal не пустой и ссылается на source bug;
- proposal не overclaim'ит applied/done/completed;
- fake proposal с placeholder-only текстом не проходит.

Historical bug reports без machine-readable reusable marker не переинтерпретируются автоматически. Это нужно, чтобы не ломать архивные reports, но новые reusable bug reports должны использовать этот контракт.

## Связь с Done Loop

Project Knowledge Done Loop отвечает за closeout feature workspaces. Learning patch loop отвечает за reusable defect learning. Если feature closeout нашел reusable bug, он должен оставить bug report и learning proposal или `not_required` reason; сам Project Knowledge не переписывается молча.
