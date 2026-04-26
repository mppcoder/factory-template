# Инвентаризация brownfield-системы: OpenClaw+

Дата: 2026-04-26

## Контекст

Полевой тест шаблона фабрики проектов на сценарии `brownfield without repo`.

Входные корни:
- `/root/.openclaw` — live runtime / настроенный дистрибутив.
- `/root/openclaw-plus` — package / overlay / тонкий слой кастомных доработок.

## Проверка наличия корней

| Root | Статус | Тип | Размер | Git repo |
| --- | --- | --- | --- | --- |
| `/root/.openclaw` | существует | directory, `drwx------`, `root:root` | `16M` | нет |
| `/root/openclaw-plus` | существует | directory, `drwxr-xr-x`, `root:root` | `7.3G` | нет |

Факт: `git -C <root> rev-parse --show-toplevel` для обоих корней возвращает `fatal: not a git repository`.

## Runtime-корень: `/root/.openclaw`

Ключевые каталоги верхнего уровня:
- `agents/`
- `cache/`
- `canvas/`
- `credentials/`
- `delivery-queue/`
- `devices/`
- `flows/`
- `hooks/`
- `identity/`
- `logs/`
- `media/`
- `memory/`
- `policies/`
- `prompts/`
- `qqbot/`
- `routing/`
- `subagents/`
- `tasks/`
- `telegram/`

Ключевые файлы:
- `openclaw.json`
- `openclaw.json.bak*`
- `exec-approvals.json`
- `update-check.json`
- `flows/registry.sqlite`
- `memory/makar.sqlite`
- `tasks/runs.sqlite`

Счетчики:
- directories: `49`
- files: `346`
- symlinks: `0`

Размеры заметных runtime-зон:
- `agents/`: `5.4M`
- `tasks/`: `4.7M`
- `flows/`: `4.1M`
- `media/`: `564K`
- `cache/`: `80K`
- `memory/`: `76K`

`openclaw.json` top-level keys:
- `agents`
- `channels`
- `gateway`
- `hooks`
- `meta`
- `models`
- `plugins`

## Package / overlay корень: `/root/openclaw-plus`

Ключевые каталоги верхнего уровня:
- `.venvs/`
- `accounts/`
- `certs/`
- `docs/`
- `env/`
- `facade/`
- `hooks/`
- `infra/`
- `knowledge/`
- `memory/`
- `models/`
- `policies/`
- `prompts/`
- `retrieval/`
- `routing/`
- `scripts/`
- `sidecars/`
- `skills/`
- `snippets/`
- `telemetry/`
- `templates/`
- `tools/`
- `validators/`
- `var/`
- `wrappers/`

Ключевые файлы:
- `ARCHITECTURE.md`
- `KNOWN-BUGS.md`
- `README.md`
- `RUNBOOK-FULL.md`
- `RUNBOOK-RETRIEVAL-BLOCK.md`
- `RUNBOOK-TOOLS-BLOCK.md`
- `MEMORY-TOKEN-CONTROL.md`
- `VERSIONS_SNAPSHOT.txt`
- `.env.example`
- `requirements-retrieval-r3.1.txt`

Счетчики:
- directories: `19306`
- files: `188604`
- symlinks: `105`

Размеры заметных package-зон:
- `.venvs/`: `5.1G`
- `wrappers/`: `2.2G`
- `sidecars/`: `108M`
- `validators/`: `196K`
- `scripts/`: `184K`
- `docs/`: `140K`
- `var/`: `140K`

## Сервисы

Проверены статусы systemd:
- `openclaw-gateway`: active, enabled
- `openclaw-retrieval`: active, enabled
- `openclaw-vectorizer`: active, enabled
- `gpt2giga`: active, enabled
- `postgresql`: active, enabled
- `nginx`: active, enabled

Package содержит unit-файлы:
- `/root/openclaw-plus/infra/systemd/openclaw-gateway.service`
- `/root/openclaw-plus/infra/systemd/openclaw-retrieval.service`
- `/root/openclaw-plus/infra/systemd/openclaw-vectorizer.service`
- `/root/openclaw-plus/infra/systemd/gpt2giga.service`

## Env / секреты

`/etc/openclaw-plus.env` существует:
- mode: `-rw-------`
- owner: `root:root`
- size: `4631`

Ключи env зафиксированы без значений. Категории:
- gateway/runtime
- Telegram
- OpenRouter
- YandexGPT
- GPT2GIGA/GigaChat
- O365
- Google/GOG
- Yandex accounts
- PostgreSQL/retrieval
- telemetry/cost/balance
- visible reply settings

Правило evidence: значения секретов не переносились в repo-артефакты.

## Live-валидация

Из `/root/openclaw-plus` запущено:

```bash
bash validators/run-final-acceptance.sh
```

Результат:
- retrieval API health: OK
- response length: OK
- duplicated content/context bloat: WARN
- makar delegation pattern: OK
- retrieval API reachable: OK
- no signs of history replay: OK
- tool output size: OK
- local-first policy layer present: OK
- acceptance checks passed: OK
