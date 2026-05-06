# Ранбук внешних действий для downstream/battle pilot

## Назначение

Этот ранбук описывает только внешнюю границу, без которой нельзя запустить
downstream/battle application proof и нельзя заявлять `proof_status: passed`.

Repo уже подготовил внутренний контур:

- supported topology: один большой VPS с разделением `/projects/<repo>` и `/srv/<project>-prod`;
- downstream proof report: `reports/release/downstream-application-proof-report.md`;
- validator: `template-repo/scripts/validate-downstream-application-proof.py`;
- roadmap: `docs/releases/single-vps-downstream-proof-roadmap.md`.

Пока внешние действия ниже не выполнены, допустимый статус proof остается
`blocked_external_inputs` или `ready_for_external_pilot`.

## Быстрый реестр

| Шаг | Кто делает | Что нужно дать | Куда не писать |
|---|---|---|---|
| 1. Выбрать downstream/battle repo | пользователь | repo path/URL и owner-approved scope | не в report как pass evidence |
| 2. Подтвердить real `APP_IMAGE` | пользователь или project owner | image reference или digest | не использовать placeholder image |
| 3. Подтвердить target VPS/staging | пользователь | SSH alias/host label и runtime target | не публиковать IP/secrets в transcript без нужды |
| 4. Внести secrets вне repo | пользователь | только факт, что secrets внесены | не вставлять secrets в chat/repo/report |
| 5. Дать approval на deploy/restore/rollback | пользователь | явное approval statement | не выполнять destructive/runtime mutation без approval |

## Окна выполнения

- Browser ChatGPT: принять решение, дать короткие approvals и без секретов описать выбранный контур.
- GitHub UI: выбрать repo, проверить owner/visibility/access, при необходимости дать Codex/GitHub connector доступ.
- Windows PowerShell или локальный terminal: только если нужно проверить SSH alias или показать sanitized error.
- VS Code Remote SSH: открыть downstream repo на VPS в `/projects/<repo>`.
- VPS terminal: выполнить runtime/deploy/restore/rollback команды после approval.
- Codex app / Codex extension: выполнять repo/VPS automation только в remote context, а не в локальной случайной папке.

## Шаг 1. Выбрать downstream/battle repo

Пользователь выбирает один реальный проект, на котором можно проверять не
placeholder runtime, а business workload.

Нужно подготовить:

- `downstream_repo_path`: например `/projects/my-product` на VPS;
- `github_repo`: например `mppcoder/my-product`, если есть GitHub remote;
- `project_slug`: короткое имя для `/srv/<project>-prod`, compose project, systemd unit, nginx site and backups;
- owner-approved scope: что именно можно деплоить и тестировать;
- protected paths: что нельзя менять без отдельного approval.

Минимальный ответ пользователя:

```text
Downstream pilot repo: /projects/<repo>
GitHub repo: <owner>/<repo> или none
Project slug: <project>
Scope: можно подготовить deploy proof на staging/prod target
Protected: не трогать <список>, если есть
```

Codex после этого должен проверить, что он находится в remote repo root:

```bash
pwd
git status --short --branch
git remote -v
test -f AGENTS.md && sed -n '1,160p' AGENTS.md
```

Pass criteria:

- repo существует и доступен на VPS;
- `AGENTS.md`/repo instructions не противоречат repo-first workflow;
- рабочая ветка понятна;
- dirty state зафиксирован и не будет случайно перетерт.

Stop criteria:

- repo не выбран;
- нет write access;
- repo содержит неизвестные production changes без owner decision;
- пользователь просит доказать pass без реального downstream repo.

## Шаг 2. Предоставить или подтвердить real `APP_IMAGE`

`APP_IMAGE` должен быть образом реального приложения, а не template placeholder.

Разрешено:

- immutable digest: `registry.example.com/app@sha256:<digest>`;
- versioned tag: `registry.example.com/app:2026-05-06-1`;
- private registry image, если credentials внесены вне repo;
- локально собранный image только если это реально downstream app image и есть build evidence.

Запрещено для pass claim:

- `factory-template-placeholder-app:local`;
- `nginx:...` как demo workload;
- `latest` без accepted reason;
- image без healthcheck/migration policy;
- image, для которого нет права deploy.

Минимальный ответ пользователя:

```text
APP_IMAGE: <registry>/<app>:<tag> или <registry>/<app>@sha256:<digest>
Это real downstream app image: да
Registry access будет настроен вне repo: да/не требуется
Можно использовать этот image для pilot deploy: да
```

Если image еще нужно собрать, пользователь выбирает boundary:

```text
Codex может собрать image из downstream repo: да
Push target registry: <registry>/<app>
Registry credentials внесу вне repo: да
```

Codex после этого должен:

- проверить, что image не placeholder;
- зафиксировать image reference in report без secrets;
- определить healthcheck endpoint;
- определить migrations policy.

Evidence examples без секретов:

```text
app_image: registry.example.com/my-product:2026-05-06-1
app_image_evidence: owner confirmed image is real downstream app image; digest captured by docker inspect after pull
```

## Шаг 3. Подтвердить target VPS/staging

Target должен быть явно approved. Для первого real pilot предпочтителен staging или disposable target; production допустим только с отдельным явным approval.

Нужно подготовить:

- SSH alias или host label;
- target type: `staging`, `disposable_restore`, `production`;
- runtime root: `/srv/<project>-prod` или `/srv/<project>-staging`;
- public domain, если нужен HTTPS/nginx proof;
- expected exposed ports: обычно только `80/443`, app bind на `127.0.0.1`;
- backup path: `/var/backups/projects/<project>`;
- rollback target: previous image/tag/version.

Минимальный ответ пользователя:

```text
Target: <ssh-alias-or-host-label>
Target type: staging/production/disposable_restore
Runtime root: /srv/<project>-prod
Domain: <domain> или none
Approval: можно готовить runtime files и выполнить deploy после отдельного финального confirmation
```

Codex перед runtime mutation должен показать sanitized preflight:

```bash
whoami
pwd
hostname
uname -a
docker --version
docker compose version
nginx -v
systemctl --version
```

Pass criteria:

- remote context marker captured;
- `/projects/<repo>` and `/srv/<project>-prod` не смешаны;
- target owner approved;
- app ports/domains/systemd unit names не конфликтуют;
- old runtime не удаляется до backup/restore/rollback proof.

Stop criteria:

- непонятно, production это или staging;
- нет SSH/runtime access;
- domain/DNS/TLS нужны, но не готовы;
- target содержит existing production без backup/rollback plan.

## Шаг 4. Внести secrets вне repo

Secrets вводит только пользователь или authorized operator. Codex не должен просить вставить secrets в chat, markdown, report, git tracked files or transcript.

Разрешенные места:

- `/etc/<project>.env` on VPS with restricted permissions;
- secret manager;
- CI/CD secrets UI;
- private registry credential store;
- Docker login on target host.

Запрещенные места:

- `deploy/.env` в repo;
- `reports/**`;
- ChatGPT/Codex chat;
- screenshots/transcripts with raw tokens/passwords/private keys;
- shell history snippets containing secret values.

Минимальный ответ пользователя после ввода:

```text
Secrets внесены вне repo: да
Location type: /etc/<project>.env / secret manager / CI secrets / docker credential store
Secrets не вставлялись в chat/repo/report: да
Codex может проверять только наличие/permissions, не значения: да
```

Codex может проверять только безопасные факты:

```bash
test -f /etc/<project>.env
stat -c '%a %U:%G %n' /etc/<project>.env
grep -E '^[A-Z0-9_]+=' /etc/<project>.env | sed 's/=.*/=<redacted>/'
```

Правильное evidence:

```text
secrets_boundary: confirmed
secrets_boundary_evidence: /etc/<project>.env exists on target with restricted permissions; values not captured
```

Неправильное evidence:

```text
DB_PASSWORD=<real password>
TOKEN=<real token>
```

## Шаг 5. Дать approval на deploy/restore/rollback

Это три разных approval, потому что каждое действие меняет runtime или данные.

### 5.1 Deploy approval

Минимальная фраза:

```text
Approval deploy: да, можно выполнить deploy для <project> на <target> с APP_IMAGE=<image>. Backup/preflight обязателен до deploy.
```

Codex после approval должен:

- сохранить old image/version if present;
- выполнить preflight;
- подготовить runtime files under `/srv/<project>-prod`;
- выполнить deploy;
- проверить docker/systemd/nginx/HTTPS healthcheck;
- записать sanitized transcript.

### 5.2 Restore approval

Минимальная фраза:

```text
Approval restore drill: да, можно выполнить restore test на disposable/staging target <target>. Production data не перезаписывать.
```

Codex после approval должен:

- создать или выбрать backup artifact;
- restore выполнять только на disposable/staging target, если нет отдельного production recovery approval;
- проверить readable/restored state;
- удалить disposable probe только если это безопасно и approved;
- записать sanitized transcript.

### 5.3 Rollback approval

Минимальная фраза:

```text
Approval rollback drill: да, можно выполнить rollback drill для <project> на <target> к previous image/version <value> и проверить healthcheck.
```

Codex после approval должен:

- знать previous image/version;
- переключить runtime на candidate and back, либо выполнить documented rollback path;
- проверить healthcheck после rollback;
- не удалять backup/old runtime до owner approval;
- записать sanitized transcript.

## Санитизированный transcript

Transcript нужен для proof, но он должен быть очищен.

Можно оставлять:

- commands without secrets;
- redacted env key names;
- status lines;
- image names/digests;
- healthcheck status and HTTP code;
- backup filenames without secret-bearing paths;
- timestamps;
- selected target labels.

Нужно удалять или заменять:

- passwords, tokens, private keys, cookies;
- raw `.env` values;
- registry credentials;
- full private URLs with embedded credentials;
- personal data unrelated to proof.

Redaction format:

```text
DB_PASSWORD=<redacted>
Authorization: Bearer <redacted>
```

## Когда можно передать работу Codex

После пяти внешних действий пользователь может дать один цельный handoff:

```text
Downstream pilot inputs ready.
Repo: /projects/<repo>
Project slug: <project>
APP_IMAGE: <real image>
Target: <target label>
Target type: staging/production/disposable_restore
Runtime root: /srv/<project>-prod
Domain: <domain or none>
Secrets: внесены вне repo; значения не раскрывать
Deploy approval: yes/no
Restore drill approval: yes/no
Rollback drill approval: yes/no
Transcript policy: sanitize secrets and private values
Goal: run downstream application proof without false pass and fill reports/release/downstream-application-proof-report.md
```

Если `Deploy approval`, `Restore drill approval` или `Rollback drill approval` равны `no`, Codex должен остановиться на соответствующем gate and keep proof status blocked.

## Критерии готовности

Downstream/battle proof может стать `passed` только если есть:

- selected real downstream repo;
- real `APP_IMAGE`;
- approved target;
- secrets outside repo;
- app-specific healthcheck;
- migrations policy or accepted not-applicable reason;
- deploy evidence;
- backup evidence;
- restore evidence on disposable/staging target or approved recovery target;
- rollback evidence;
- sanitized transcript;
- valid `reports/release/downstream-application-proof-report.md`;
- green validator run:

```bash
python3 template-repo/scripts/validate-downstream-application-proof.py reports/release/downstream-application-proof-report.md
```

Если любой пункт отсутствует, correct status is `blocked_external_inputs`, `not_run` or `ready_for_external_pilot`, not `passed`.
