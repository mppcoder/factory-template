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

Canonical flow:

1. Browser ChatGPT Project готовит один большой handoff.
2. VS Code Remote SSH открывает repo на VPS.
3. Codex extension в этом Remote SSH window получает handoff.
4. Repo-native orchestrator создает child subtask specs.
5. Codex CLI sessions запускаются на VPS/repo context отдельно по `quick / build / deep / review`.
6. Parent report собирает результат и blockers.

`Codex App / Cloud Director` допускается как optional, not default. Cloud delegation нельзя описывать как default path; она возможна только по явному выбору пользователя и если repo/security boundary это разрешает.

Already-open live session не является надежным auto-switch mechanism. Child session не наследует parent route by default: каждый child subtask обязан явно фиксировать `selected_profile`, `selected_model`, `selected_reasoning_effort`, `selected_plan_mode_reasoning_effort` и `selected_scenario`.

Связанные artifacts:

- `docs/operator/factory-template/04-vps-remote-ssh-full-handoff-orchestration.md`
- `template-repo/scripts/orchestrate-codex-handoff.py`
- `template-repo/scripts/validate-codex-orchestration.py`
