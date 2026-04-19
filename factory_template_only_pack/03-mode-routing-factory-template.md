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
- mechanical cleanup;
- простых validator runs.

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

Рекомендуемый профиль:

- модель: `gpt-5.4`
- reasoning: `high`

### release-verify

Использовать для финального контрольного прохода.

Подходит для:

- final audit;
- diff review;
- release bundle review;
- complete self-test pass review.

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

---

## 4. Что внедрять сразу

Сразу внедрить:

- `.codex/config.toml` с профилями;
- `AGENTS.md` с правилами классификации;
- правило: перед новым подэтапом фиксируй профиль.

Этого достаточно для быстрого старта именно на одном проекте `factory-template`.
