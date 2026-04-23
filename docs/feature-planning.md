# Resumable Feature Planning (beginner-first)

Этот поток помогает пройти путь от сырой идеи до понятного списка задач без потери контекста.

## Что решает поток
- Можно начать интервью сегодня и продолжить завтра.
- Черновая идея превращается в `user-spec`.
- `user-spec` превращается в простой `tech-spec`.
- Фича раскладывается на маленькие задачи `T-xxx`.

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

## Что создаётся в workspace
- `interview-state.yaml` — текущее состояние интервью и stage.
- `specs/user-spec.md` — понятная продуктовая спецификация.
- `specs/tech-spec.md` — технический план простым языком.
- `tasks/T-001.md ...` — маленькие задачи с критериями приемки.
- `tasks/index.md` — индекс сгенерированных задач.

## Resume-семантика
- Любое прерывание безопасно: состояние сохраняется в `interview-state.yaml`.
- Повторный запуск `resume-setup.py` не теряет заполненные ответы.
- Если обязательные вопросы заполнены, flow автоматически предлагает следующий шаг (`generate-user-spec.py`).

## Ограничения текущей версии
- Генерация опирается на структурированные ответы интервью и не заменяет живой review.
- Скрипты формируют readable draft; финальное уточнение содержания остается за командой.

## Связанные артефакты
- `.chatgpt/interview-state.yaml.template`
- `template-repo/scripts/resume-setup.py`
- `template-repo/scripts/init-feature-workspace.sh`
- `template-repo/scripts/generate-user-spec.py`
- `template-repo/scripts/decompose-feature.py`
- `template-repo/template/work-templates/user-spec.md.template`
- `template-repo/template/work-templates/tech-spec.md.template`
- `template-repo/template/work-templates/tasks/task.md.template`
