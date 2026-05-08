# Маршрутизация моделей и режимов — только для factory-template

## Базовая схема

Для `factory-template` нужен явный task-based routing layer на границе новой задачи.

Надежная единица выбора модели/режима:
- новый task launch;
- новый запуск Codex под новую задачу;
- `--profile` или эквивалентный override layer.

Advisory слой:
- `AGENTS`
- ChatGPT Project instructions
- scenario-pack
- runbooks

Executable слой:
- `.codex/config.toml` named profiles
- `template-repo/codex-routing.yaml`
- `./scripts/resolve-codex-task-route.py`
- `./scripts/bootstrap-codex-task.py`
- `./scripts/launch-codex-task.sh`

Достаточно 4 профилей:

- `quick`
- `build`
- `deep`
- `review`

## Goal-first layer

Перед выбором сценария и исполнением новая задача нормализуется в `goal_contract`.
Это advisory/template layer, а не executable profile switch.

`goal first` фиксирует:
- `normalized_goal`;
- DoD и evidence;
- scope/non-goals;
- safety/budget boundaries;
- feedback tools;
- proxy-signal denylist.

Goal-first не меняет `task_class`, `selected_profile`, model или reasoning сам по себе.
Эти поля остаются результатом task-based routing и live catalog validation.

`Codex /goal runtime` optional. После обновления CLI проверяйте:

```bash
codex --version
codex features list
```

Если `goals` отображается как experimental/off by default, его можно использовать как рабочий runtime только по явному user/operator выбору. Нельзя считать, что advisory text или уже открытая Codex session включили `/goal`.

---

## 1. Профили

### quick

Подходит для:
- docs/triage/search;
- lightweight inventory;
- short repo lookup;
- low-risk docs follow-up.

Рекомендуемый профиль:

- модель: `gpt-5.4-mini`
- reasoning: `low`

### build

Использовать для обычной реализации.

Подходит для:
- feature/fix;
- remediation;
- scripts/docs sync;
- launcher/validator updates;
- обычные repo changes.

Рекомендуемый профиль:

- модель: `gpt-5.5`
- reasoning: `medium`

### deep

Использовать для тяжелого анализа.

Подходит для:

- несогласованности runbook ↔ scripts ↔ examples;
- RCA сложного тестового сбоя;
- сравнения нескольких сценарных веток;
- reverse analysis downstream feedback into template.
- классификации internal repo follow-up vs external boundary step при спорном closeout.

Рекомендуемый профиль:

- модель: `gpt-5.5`
- reasoning: `high`

### review

Использовать для review/tests/cleanup.

Подходит для:

- review;
- tests;
- cleanup;
- final verification;
- release-facing consistency pass.

Рекомендуемый профиль:

- модель: `gpt-5.5`
- reasoning: `high`

---

## 2. Правила маршрутизации

### Правило 1

Не проверять routing в старой уже открытой сессии.

### Правило 2

Не считать один static profile в `~/.codex/config.toml` умным task router.

### Правило 3

Каждая новая задача должна идти через новый launcher/router run.

### Правило 4

ChatGPT handoff и direct task обязаны использовать один vocabulary: `quick / build / deep / review`.

### Правило 5

Direct task сначала проходит self-handoff и только потом remediation.

### Правило 6

Broad migration/architecture task не запускается одним гигантским goal. Сначала `scrappy`, затем PRD/spec, затем clean implementation.

---

## 3. Практический протокол

1. Пройти router/scenario layer.
2. Запустить `./scripts/launch-codex-task.sh --launch-source ...`.
3. Проверить `.chatgpt/task-launch.yaml`.
4. Убедиться, что `selected_profile / selected_model / selected_reasoning_effort` совпали с ожиданием.
5. Только после этого считать routing подтвержденным.

---

## 4. Что внедрять сразу

Сразу внедрить:

- `.codex/config.toml` с профилями `quick / build / deep / review`;
- executable launcher/router scripts;
- launch logging в `.chatgpt/task-launch.yaml`;
- self-handoff standard для direct task.

Этого достаточно, чтобы routing был не advisory, а executable.

---

## 5. VPS Remote SSH-first orchestration

Для больших handoff default path — `VPS Remote SSH-first`, а не Codex App/Cloud Director.

Default UX для full orchestration handoff — one-paste autopilot: оператор вставляет parent handoff в Codex один раз, а parent Codex сам запускает repo-native orchestrator после validation gate. `orchestrate-codex-handoff.py --execute` является parent Codex execution path; ручной shell-запуск оператора остается troubleshooting / strict fallback.

Canonical flow:

1. Browser ChatGPT Project готовит один большой handoff.
2. VS Code Remote SSH открывает repo на VPS.
3. Codex extension в этом Remote SSH window получает handoff.
4. Repo-native orchestrator создает child subtask specs.
5. Codex CLI sessions запускаются на VPS/repo context отдельно по `quick / build / deep / review`.
6. Parent report собирает результат и blockers.

`Codex App / Cloud Director` допускается как optional, not default. Cloud delegation нельзя описывать как default path; она возможна только по явному выбору пользователя и если repo/security boundary это разрешает.

Already-open live session не является надежным auto-switch mechanism. Child session не наследует parent route by default: каждый child subtask обязан явно фиксировать `selected_profile`, `selected_model`, `selected_reasoning_effort`, `selected_plan_mode_reasoning_effort` и `selected_scenario`.

Большой handoff дополнительно использует `user_actions_policy: defer-to-final-closeout`: пользовательские действия, реальные external values, runtime approvals и downstream/battle inputs переносятся в конец parent plan. До этого child sessions работают на repo-local задачах; где возможно, используются temporary placeholders, а parent report обязан вывести `deferred_user_actions` и `placeholder_replacements`.

Связанные artifacts:

- `docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md`
- `template-repo/scripts/orchestrate-codex-handoff.py`
- `template-repo/scripts/validate-codex-orchestration.py`
