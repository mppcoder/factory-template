# Resumable feature planning / возобновляемое планирование feature

Этот поток помогает пройти путь от сырой идеи до понятного списка задач без потери контекста.

## Что решает поток
- Можно начать интервью сегодня и продолжить завтра.
- Черновая идея превращается в `user-spec`.
- `user-spec` превращается в простой `tech-spec` с привязкой к пользовательским намерениям.
- Фича раскладывается на маленькие задачи `T-xxx`, каждая задача хранит ссылку на `US-*` anchor.

## Быстрый старт

1. Инициализируйте workspace фичи:
```bash
bash template-repo/scripts/init-feature-workspace.sh --feature-id feat-my-first-flow --title "Мой первый flow" --idea "Хочу упростить планирование"
```

2. Заполняйте интервью постепенно (можно в несколько подходов):
```bash
python3 template-repo/scripts/resume-setup.py --workspace template-repo/work/features/feat-my-first-flow --answer problem="Теряем контекст между сессиями"
python3 template-repo/scripts/resume-setup.py --workspace template-repo/work/features/feat-my-first-flow --answer users="Новички команды"
```

3. Сгенерируйте user-spec из интервью:
```bash
python3 template-repo/scripts/generate-user-spec.py --workspace template-repo/work/features/feat-my-first-flow
```

4. Сгенерируйте tech-spec и задачи:
```bash
python3 template-repo/scripts/decompose-feature.py --workspace template-repo/work/features/feat-my-first-flow
```

5. Проверьте traceability после генерации:
```bash
python3 template-repo/scripts/validate-spec-traceability.py --workspace template-repo/work/features/feat-my-first-flow
```

## Что создаётся в workspace
- `interview-state.yaml` — текущее состояние интервью и stage.
- `specs/user-spec.md` — что хочет пользователь, с `User Intent Anchors`.
- `specs/tech-spec.md` — как агент реализует user-spec, с `User Intent Binding`, `Decisions`, `User-Spec Deviations`, `Acceptance Criteria`, `Audit Wave Lite` и `Final Verification`.
- `tasks/T-001.md ...` — маленькие задачи с критериями приемки, ссылкой на пользовательский intent и `Verify-smoke` / `Verify-user`.
- `tasks/index.md` — индекс сгенерированных задач.
- `decisions.md` — журнал важных решений, deviations и verification после выполнения задач.

## Resume-семантика
- Любое прерывание безопасно: состояние сохраняется в `interview-state.yaml`.
- Повторный запуск `resume-setup.py` не теряет заполненные ответы.
- Если обязательные вопросы заполнены, flow автоматически предлагает следующий шаг (`generate-user-spec.py`).
- `generate-user-spec.py` и `decompose-feature.py` запускают lightweight traceability audit после генерации. Если нужно отладить черновик без audit, есть флаг `--skip-traceability-audit`.

## Зачем нужен traceability слой

`US-001`, `US-002` и другие anchors — это короткие метки пользовательских требований. Они помогают увидеть, почему техническое решение или задача вообще существует.

Если технический план расходится с user-spec, это не запрещено, но отклонение нужно записать в `User-Spec Deviations` как `DEV-001 | anchor=US-xxx | decision=... | reason=... | validation=... | approval=pending`. Так review видит не только решение, но и причину, риск и способ проверки.

После утверждения tech-spec pending deviation нужно заменить на `approval=approved`. Validator специально ловит approved документы, в которых deviation остался неутверждённым.

`decisions.md` нужен не для бюрократии. Это короткая память feature: что реально решили, чем проверили, были ли deviations, и нужно ли перенести устойчивый вывод в `project-knowledge/`.

## Ограничения текущей версии
- Генерация опирается на структурированные ответы интервью и не заменяет живой review.
- Скрипты формируют readable draft; финальное уточнение содержания остается за командой.
- Validator проверяет структуру, anchors и явные deviation records. Он не заменяет продуктовое решение и не пытается угадать скрытый смысл текста.

## Связанные артефакты
- `.chatgpt/interview-state.yaml.template`
- `template-repo/scripts/resume-setup.py`
- `template-repo/scripts/init-feature-workspace.sh`
- `template-repo/scripts/generate-user-spec.py`
- `template-repo/scripts/decompose-feature.py`
- `template-repo/scripts/validate-spec-traceability.py`
- `template-repo/template/work-templates/user-spec.md.template`
- `template-repo/template/work-templates/tech-spec.md.template`
- `template-repo/template/work-templates/tasks/task.md.template`
- `template-repo/template/work-templates/decisions.md.template`
- `docs/spec-traceability.md`
