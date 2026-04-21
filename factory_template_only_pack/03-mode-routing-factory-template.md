# Маршрутизация моделей и режимов — только для factory-template

## Базовая схема

Для `factory-template` не нужен тяжелый routing как для brownfield shell.

Достаточно 4 профилей:

- `default-dev`
- `fast-routine`
- `heavy-analysis`
- `release-verify`

---

## 1. Профили

### default-dev

Использовать по умолчанию.

Подходит для:

- обычной правки repo;
- синхронизации docs и scripts;
- стандартных улучшений;
- работы по готовому spec.

Рекомендуемый профиль:

- модель: `gpt-5.4`
- reasoning: `medium`

### fast-routine

Использовать для механических подзадач.

Подходит для:

- docs only;
- rename only;
- export packs;
- dry-run и повторные recheck'и repo-side export/reference artifacts;
- mechanical cleanup;
- простых validator runs;
- repeated no-op/recheck runs для `VALIDATE_*` и `VERIFIED_SYNC.sh`.
- post-verify lightweight follow-up changes вроде `.gitignore` и небольших docs/closeout cleanup.
- сбор completion package для source-update instructions по уже известному impact model.

Рекомендуемый профиль:

- модель: `gpt-5.4-mini`
- reasoning: `low` или `medium`

### heavy-analysis

Использовать для тяжелого анализа.

Подходит для:

- несогласованности runbook ↔ scripts ↔ examples;
- RCA сложного тестового сбоя;
- сравнения нескольких сценарных веток;
- reverse analysis downstream feedback into template.
- классификации internal repo follow-up vs external boundary step при спорном closeout.

Рекомендуемый профиль:

- модель: `gpt-5.4`
- reasoning: `high`

### release-verify

Использовать для финального контрольного прохода.

Подходит для:

- final audit;
- diff review;
- release bundle review;
- complete self-test pass review;
- `EXECUTE_RELEASE_DECISION.sh` и publish/fallback review;
- release-followup, source-pack refresh и closeout consistency pass как внутренней repo-работы.
- final review операторских инструкций для factory ChatGPT Project, downstream repo sync и battle ChatGPT Projects.
- финальный review repo-first инструкции и внешних шагов обновления ChatGPT Project UI.

Рекомендуемый профиль:

- модель: `gpt-5.4`
- reasoning: `high`

---

## 2. Правила переключения

### Правило 1

Глобальный дефолт:

- `gpt-5.4`
- `medium`

### Правило 2

Не держать `high` как постоянный режим.

### Правило 3

После тяжелого анализа возвращаться на `default-dev`.

### Правило 4

На рутинные подзадачи переключаться на `fast-routine`.

### Правило 5

Release verify не выполнять на `mini`.

### Правило 6

`VERIFIED_SYNC.sh` запускать из `default-dev` или `fast-routine` только после зеленого verify.
Для low-risk post-verify follow-up diff допускается lightweight follow-up mode в `fast-routine`: достаточно минимального deterministic verify без полного повторного regression pass.

### Правило 7

`EXECUTE_RELEASE_DECISION.sh` запускать только в `release-verify`, когда есть явный `release-decision.yaml`.

---

## 3. Практический протокол внутри живой сессии

Перед началом каждого нового подэтапа Codex должен:

1. коротко классифицировать задачу;
2. выбрать профиль;
3. продолжить работу уже в соответствующем режиме.

Пример:

```text
Класс задачи: heavy-analysis.
Причина: есть расхождение между launcher, validators и scenario-pack.
Работаю в профиле heavy-analysis.
```

Если heavy-analysis уже закрыл обязательные gate'ы и задача стала достаточно определенной для handoff, следующий ответ должен содержать готовый inline handoff, а не еще один purely-analytic summary.

Если heavy-analysis показал, что remaining work остается внутренним release-followup внутри repo, следующий ответ не должен уходить в user-only closeout.

---

## 4. Что внедрять сразу

Сразу внедрить:

- `.codex/config.toml` с профилями;
- `AGENTS.md` с правилами классификации;
- правило: перед новым подэтапом фиксируй профиль.

Этого достаточно для быстрого старта именно на одном проекте `factory-template`.
