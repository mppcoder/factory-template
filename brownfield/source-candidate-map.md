# Карта source-candidate: OpenClaw+

Дата: 2026-04-26

## Цель

Определить, какие части `/root/.openclaw` и `/root/openclaw-plus` можно рассматривать как кандидаты для будущего reconstructed source repo, а какие являются runtime state, generated artifacts или secret-bearing data.

## Итоговая классификация

| Root | Роль | Source candidate | Комментарий |
| --- | --- | --- | --- |
| `/root/.openclaw` | live runtime | ограниченно | Большая часть root является runtime state и secrets. В source можно брать только redacted config/policy/prompt/routing candidates после review. |
| `/root/openclaw-plus` | package / overlay | да | Основной источник package source, docs, validators, templates, scripts и policy/model/routing layers. Generated dependency zones нужно исключить. |
| `/etc/openclaw-plus.env` | runtime env | нет | Только redacted key inventory, значения секретов не переносить. |

## Source candidates из `/root/openclaw-plus`

Primary candidates:
- `ARCHITECTURE.md`
- `KNOWN-BUGS.md`
- `RUNBOOK-FULL.md`
- `RUNBOOK-RETRIEVAL-BLOCK.md`
- `RUNBOOK-TOOLS-BLOCK.md`
- `MEMORY-TOKEN-CONTROL.md`
- `VERSIONS_SNAPSHOT.txt`
- `.env.example`
- `.env.example.patch`
- `accounts/*.yaml`
- `docs/**/*.md`
- `env/*.append`
- `facade/**/*.py`
- `facade/**/*.yaml`
- `hooks/**/*.py`
- `hooks/**/*.md`
- `infra/db/**/*.sql`
- `infra/**/*.sh`
- `infra/nginx/*.conf`
- `infra/python/*.txt`
- `infra/systemd/*.service`
- `memory/*.yaml`
- `models/*.yaml`
- `policies/*.yaml`
- `prompts/**/*.md`
- `requirements-*.txt`
- `retrieval/app/*.py`
- `routing/*.yaml`
- `scripts/*.py`
- `scripts/*.sh`
- `sidecars/gpt2giga/config.yaml`
- `sidecars/gpt2giga/healthcheck.sh`
- `sidecars/gpt2giga/run.sh`
- `sidecars/gpt2giga/security.md`
- `skills/**/*.md`
- `snippets/**/*`
- `telemetry/*.py`
- `templates/*`
- `tools/*.py`
- `tools/*.yaml`
- `validators/**/*.sh`
- `validators/**/*.md`
- `wrappers/delegate-specialist-plugin/index.js`
- `wrappers/delegate-specialist-plugin/openclaw.plugin.json`
- `wrappers/delegate-specialist-plugin/package.json`
- `wrappers/delegate-specialist-plugin/package-lock.json`
- `wrappers/docs/*`
- `wrappers/scripts/*.py`
- `wrappers/snippets/*`
- `wrappers/tools/*`
- `wrappers/validators/*.sh`

## Limited candidates из `/root/.openclaw`

Только после redaction/review:
- `openclaw.json`
- `policies/*.yaml`
- `prompts/**/*.md`
- `routing/*.yaml`
- `hooks/**/*.py`
- `canvas/index.html`
- `agents/*/agent/models.json`

Не переносить автоматически:
- session logs;
- sqlite DB;
- credentials;
- identity/device state;
- telegram offsets/hashes;
- media;
- runtime cache;
- delivery queue.

## Triage backup-файлов

Backup-файлы не являются source-of-truth по умолчанию. Они нужны как evidence для change history:
- `/root/.openclaw/openclaw.json.bak*`
- `/root/.openclaw/hooks/**/*.bak*`
- `/root/openclaw-plus/**/*.bak*`

Решение:
- в source pack не включать backup-файлы как active source;
- собрать отдельный evidence inventory;
- сравнивать backup с active file только при расследовании конкретного drift/bug.

## Secret-bearing зоны

Запрещены для source import:
- `/etc/openclaw-plus.env` values;
- `/root/.openclaw/credentials/`;
- `/root/.openclaw/identity/`;
- `/root/.openclaw/telegram/`;
- `/root/.openclaw/devices/`;
- `*.jsonl` session/log files;
- SQLite runtime DB files.

## Generated / dependency зоны

Исключить:
- `/root/openclaw-plus/.venvs/`
- `/root/openclaw-plus/wrappers/delegate-specialist-plugin/node_modules/`
- `__pycache__/`
- `*.pyc`
- `/root/openclaw-plus/var/`
- runtime logs under `sidecars/gpt2giga/logs/`
- `*.log`

## Следующий внутренний шаг

Создать reconstruction workspace внутри выделенного project root, например:
- `/projects/openclaw-brownfield/reconstruction/`

Не создавать repo внутри `/root/.openclaw`, `/root/openclaw-plus` или прямо как temporary sibling в `/projects`.
