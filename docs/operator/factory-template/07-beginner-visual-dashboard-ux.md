# Визуальная панель для новичка

## Назначение

Beginner visual dashboard UX — это короткий понятный слой поверх repo-native `project-lifecycle-dashboard`.

Он не добавляет web app, daemon, SQLite, Telegram notifications, websocket/live-refresh или background worker. Default остается легким:

- ChatGPT Project показывает mini status card;
- Codex App / VS Code Codex extension показывает execution progress card;
- repo хранит полный Markdown dashboard в `reports/project-lifecycle-dashboard.md`.

Все три поверхности читаются из одного source-of-truth: `.chatgpt/project-lifecycle-dashboard.yaml` в generated project или `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` в `factory-template`.

## Что видно в ChatGPT Project

ChatGPT Project — это пульт управления. Его карточка короткая и без технического шума:

```text
📍 Проект: <name>
🧭 Фаза: <phase> → <next>
🧩 Активная задача: <change title>
🟡 Статус: <status>
✅ Готово: <completed>/<total>
⛔ Блокеры: <none/list>
👤 От пользователя требуется: <action/ничего>
➡️ Следующий шаг: <next safe action>
```

Эта карточка отвечает на пять вопросов:

- где мы сейчас;
- что делается;
- что уже готово;
- что требуется от пользователя;
- какой следующий безопасный шаг.

Если есть запись в `external_actions_ledger`, карточка не имеет права писать “ничего не требуется”. Она должна назвать действие пользователя, runtime action, downstream action, model mapping blocker или secret boundary blocker.

## Что видно в Codex App / VS Code

Codex — это пульт исполнения. В начале большой задачи он показывает route receipt:

```text
route receipt:
- task_class: <task_class>
- selected_profile: <selected_profile>
- selected_model: <selected_model>
- selected_reasoning_effort: <selected_reasoning_effort>
- scenario: <scenario>

progress:
✅ completed steps: <completed>
🟡 active step / wave: <active>
⬜ remaining steps: <remaining>

blockers:
- <none/list>

next:
- <next internal action>

external:
- <user action required / not required>
```

Во время длинной задачи Codex обновляет progress card по wave/task/checkpoint. В closeout он должен назвать verify/sync status: какие validators прошли, выполнен ли quick verify, есть ли commit/push или явный blocker.

Финальный ответ Codex по repo change обязан включать раздел `Карточка проекта` со свежим `chatgpt-card` readout из renderer. Минимальная карточка содержит project name, lifecycle chain, `Модули:` и `В работе:`. Раздел `В работе:` в compact card показывает текущую задачу и незакрытые задачи, а не всю историю закрытых handoff. Если карточка не может быть сгенерирована, Codex должен назвать blocker, а не закрывать задачу как fully done.

Если Codex пишет `executed`, `completed`, `passed`, `done` или другой зеленый статус, рядом должна быть evidence или accepted reason. Без evidence статус остается `pending` или `in_progress`.

## Что видно в Markdown dashboard

Markdown dashboard — это единая доска состояния. Полный отчет лежит в:

```text
reports/project-lifecycle-dashboard.md
```

Его можно открыть в VS Code Markdown Preview или GitHub preview. Там видны project identity, lifecycle phase, active change, stage gates, execution waves, handoff/orchestration, release readiness, deploy/runtime state, standards navigator, software update governance, external actions ledger, recommended next step и fallback.

Mini cards не заменяют dashboard. Они являются коротким readout из того же dashboard YAML.

## Как читать статусы

Канонические beginner statuses:

- `pending` — еще не начато или ожидает входных данных;
- `in_progress` — Codex или repo work сейчас выполняет шаг;
- `blocked` — есть blocker, указанный с owner boundary;
- `passed` — проверка прошла и есть evidence;
- `failed` — проверка или gate упали;
- `completed` — работа завершена и есть evidence;
- `not_applicable` — не применимо, но нужен accepted reason.

Repo-compatible aliases вроде `done`, `ready` или `archived` допустимы в dashboard internals, но для новичка лучше показывать один из beginner statuses выше.

## Что значит действие пользователя

Owner boundary говорит, кто должен действовать:

- `internal-repo-follow-up` — это работа Codex внутри repo, пользователь ничего не делает;
- `external-user-action` — пользователю нужно выполнить ручной шаг;
- `runtime-action` — нужен внешний runtime/deploy шаг или approval;
- `downstream-battle-action` — действие относится к боевому downstream project;
- `model-mapping-blocker` — route/model mapping требует нового launch или ручного выбора;
- `secret-boundary-blocker` — нужен секрет или приватный ввод вне repo.

Если карточка пишет “от пользователя требуется: ничего”, `external_actions_ledger` должен быть пуст.

## Как понять, что Codex работает, а не завис

Смотрите на Codex execution card:

- `request` показывает текущий `FT-CX` / `FT-CH` номер;
- `route receipt` появился в начале задачи;
- `active step / wave` меняется после checkpoint;
- completed steps растут только с evidence;
- blockers либо пустые, либо имеют owner boundary;
- next internal action назван конкретно;
- closeout содержит verify/sync status.

Если долго нет нового вывода, но active step понятен и external action не требуется, это обычно внутренняя repo work. Если появился `blocked`, карточка должна назвать, кто владелец блокера и что делать дальше.

## Где смотреть полный отчет

Короткий путь:

```bash
python3 template-repo/scripts/render-project-lifecycle-dashboard.py \
  --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml \
  --format markdown-full \
  --output reports/project-lifecycle-dashboard.md
```

Карточки:

```bash
python3 template-repo/scripts/render-project-lifecycle-dashboard.py \
  --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml \
  --format chatgpt-card \
  --stdout

python3 template-repo/scripts/render-project-lifecycle-dashboard.py \
  --input template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml \
  --format codex-card \
  --stdout
```

В обычном one-paste flow эти команды выполняет Codex. Пользователь открывает готовый `reports/project-lifecycle-dashboard.md` или читает короткие карточки в ChatGPT/Codex.
