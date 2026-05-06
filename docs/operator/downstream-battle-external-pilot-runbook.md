# Диалоговый ранбук внешних действий для downstream/battle pilot

## Назначение

Этот ранбук задает форму разговора: Codex задает один вопрос, пользователь
отвечает одним готовым блоком. После каждого ответа Codex проверяет только
безопасные факты и не двигается к runtime mutation, если ответ неполный.

Цель не в том, чтобы пользователь сам собрал чеклист. Цель в том, чтобы Codex
провел пользователя через внешнюю границу:

1. выбрать downstream/battle repo;
2. подтвердить real `APP_IMAGE`;
3. подтвердить target VPS/staging;
4. внести secrets вне repo;
5. дать отдельные approvals на deploy, restore и rollback.

Пока эти ответы не получены, downstream/battle application proof остается в
статусе `blocked_external_inputs` или `ready_for_external_pilot`. Заявлять
`proof_status: passed` запрещено.

## Как Codex ведет интервью

Codex задает вопросы строго по порядку. Нельзя перескакивать к deploy approval,
если еще не выбран repo или не подтвержден real `APP_IMAGE`.

Правила для Codex:

- задавать один вопрос за раз;
- давать пользователю готовый шаблон ответа;
- просить только решения, approvals и безопасные identifiers;
- не просить secrets, tokens, passwords, private keys or raw `.env` values;
- после каждого ответа фиксировать, что принято, что осталось неполным и какой
  следующий вопрос;
- если пользователь отвечает не полностью, повторить только недостающие поля;
- если пользователь дает secret в чат, остановиться, попросить rotate secret and
  sanitize transcript;
- если approval отсутствует, держать proof blocked и не выполнять runtime
  mutation.

## Окна выполнения

Codex называет окно в каждом вопросе:

- Browser ChatGPT: пользователь отвечает на вопросы и дает approvals.
- GitHub UI: пользователь выбирает repo или подтверждает доступ.
- VS Code Remote SSH: Codex/оператор открывает downstream repo на VPS.
- VPS terminal: Codex выполняет preflight/deploy/restore/rollback только после
  approval.
- Codex app / Codex extension: работает в remote context, не в локальной
  случайной папке.

## Вопрос 1. Какой downstream/battle repo берем в pilot?

**Codex спрашивает:**

```text
Вопрос 1/5. Выбери один реальный downstream/battle repo для application proof.

Ответь одним блоком. Не вставляй secrets.

Downstream pilot repo: /projects/<repo>
GitHub repo: <owner>/<repo> или none
Project slug: <project>
Owner-approved scope: что можно готовить, деплоить и проверять
Protected paths/data: что нельзя менять без отдельного approval
Рабочее окно: Browser ChatGPT / GitHub UI
```

**Пользователь отвечает:**

```text
Downstream pilot repo: /projects/<repo>
GitHub repo: <owner>/<repo> или none
Project slug: <project>
Owner-approved scope: можно подготовить deploy proof на staging/prod target
Protected paths/data: не трогать <список> без отдельного approval
Рабочее окно: Browser ChatGPT / GitHub UI
```

**Codex проверяет после ответа:**

```bash
pwd
git status --short --branch
git remote -v
test -f AGENTS.md && sed -n '1,160p' AGENTS.md
```

**Codex принимает ответ, если:**

- repo path указан;
- project slug можно использовать для `/srv/<project>-prod`, systemd, nginx,
  compose project and backup path;
- scope явно разрешает подготовку proof;
- protected paths/data названы или явно указано `none`;
- repo доступен и dirty state не будет случайно перетерт.

**Codex останавливается, если:**

- repo не выбран;
- нет write/read access;
- пользователь просит pass без реального downstream repo;
- repo содержит неизвестные production changes без owner decision.

## Вопрос 2. Какой real `APP_IMAGE` используем?

**Codex спрашивает:**

```text
Вопрос 2/5. Подтверди real APP_IMAGE для выбранного downstream проекта.

Это должен быть образ реального приложения, не placeholder.
Не вставляй registry passwords или tokens.

APP_IMAGE: <registry>/<app>:<tag> или <registry>/<app>@sha256:<digest>
Это real downstream app image: да/нет
Можно использовать image для pilot deploy: да/нет
Registry access будет настроен вне repo: да/не требуется
Если image нужно собрать, можно ли Codex собрать его из downstream repo: да/нет
Push target registry, если нужен build/push: <registry>/<app> или none
Рабочее окно: Browser ChatGPT / GitHub UI / VS Code Remote SSH
```

**Пользователь отвечает:**

```text
APP_IMAGE: <registry>/<app>:<tag>
Это real downstream app image: да
Можно использовать image для pilot deploy: да
Registry access будет настроен вне repo: да/не требуется
Если image нужно собрать, можно ли Codex собрать его из downstream repo: да/нет
Push target registry, если нужен build/push: <registry>/<app> или none
Рабочее окно: Browser ChatGPT / GitHub UI / VS Code Remote SSH
```

**Codex принимает ответ, если:**

- `APP_IMAGE` не равен `factory-template-placeholder-app:local`;
- image не является demo `nginx`;
- tag/version/digest достаточно конкретный;
- есть право использовать image для pilot deploy;
- registry credentials остаются вне repo and chat;
- healthcheck and migrations policy можно определить на следующем repo/runtime
  этапе.

**Codex останавливается, если:**

- image отсутствует;
- image является placeholder/demo workload;
- пользователь предлагает `latest` без accepted reason;
- registry credentials вставлены в чат;
- нет approval использовать image для pilot.

**Безопасное evidence после проверки:**

```text
app_image: <registry>/<app>:<tag>
app_image_evidence: owner confirmed image is real downstream app image; credentials were not captured
```

## Вопрос 3. Какой target VPS/staging approved?

**Codex спрашивает:**

```text
Вопрос 3/5. Подтверди runtime target для pilot.

Для первого proof лучше staging или disposable target. Production можно только
с явным approval. Не вставляй passwords, private keys или raw IP, если это не
нужно для работы.

Target label or SSH alias: <target>
Target type: staging/production/disposable_restore
Runtime root: /srv/<project>-prod или /srv/<project>-staging
Domain: <domain> или none
Expected public ports: 80/443 или none
Backup path: /var/backups/projects/<project>
Previous image/version for rollback, если уже известен: <value> или unknown
Approval сейчас: можно делать только preflight / можно готовить runtime files / можно deploy после отдельного confirmation
Рабочее окно: Browser ChatGPT / VS Code Remote SSH / VPS terminal
```

**Пользователь отвечает:**

```text
Target label or SSH alias: <target>
Target type: staging
Runtime root: /srv/<project>-staging
Domain: <domain> или none
Expected public ports: 80/443 или none
Backup path: /var/backups/projects/<project>
Previous image/version for rollback, если уже известен: <value> или unknown
Approval сейчас: можно делать preflight и готовить runtime files; deploy только после отдельного confirmation
Рабочее окно: Browser ChatGPT / VS Code Remote SSH / VPS terminal
```

**Codex проверяет preflight без destructive action:**

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

**Codex принимает ответ, если:**

- target type понятен;
- runtime root не смешан с `/projects/<repo>`;
- backup path per-project;
- public ports/domains не конфликтуют;
- production target имеет явное production approval или ограничен preflight-only;
- old runtime не удаляется до backup/restore/rollback proof.

**Codex останавливается, если:**

- непонятно, staging это или production;
- нет SSH/runtime access;
- domain/TLS нужен, но target не готов;
- target содержит existing production без backup/rollback plan.

## Вопрос 4. Secrets внесены вне repo?

**Codex спрашивает:**

```text
Вопрос 4/5. Внеси secrets вне repo и подтверди только факт ввода.

Не вставляй значения secrets в ответ. Не вставляй .env, tokens, passwords,
private keys or registry credentials.

Secrets внесены вне repo: да/нет
Location type: /etc/<project>.env / secret manager / CI secrets / docker credential store / не требуется
Secrets не вставлялись в chat/repo/report: да/нет
Codex может проверять только наличие/permissions, не значения: да/нет
Рабочее окно: VPS terminal / GitHub UI / Browser ChatGPT
```

**Пользователь отвечает:**

```text
Secrets внесены вне repo: да
Location type: /etc/<project>.env
Secrets не вставлялись в chat/repo/report: да
Codex может проверять только наличие/permissions, не значения: да
Рабочее окно: VPS terminal / Browser ChatGPT
```

**Codex может проверять только безопасные факты:**

```bash
test -f /etc/<project>.env
stat -c '%a %U:%G %n' /etc/<project>.env
grep -E '^[A-Z0-9_]+=' /etc/<project>.env | sed 's/=.*/=<redacted>/'
```

**Codex принимает ответ, если:**

- secrets находятся вне repo;
- пользователь подтвердил, что значения не попали в chat/repo/report;
- Codex ограничен проверкой наличия, permissions and redacted key names;
- transcript можно sanitize.

**Codex останавливается, если:**

- secrets не внесены;
- пользователь вставил secret value в чат;
- env лежит в tracked repo path;
- пользователь просит Codex прочитать или сохранить raw secret values.

**Правильное evidence:**

```text
secrets_boundary: confirmed
secrets_boundary_evidence: /etc/<project>.env exists on target with restricted permissions; values not captured
```

## Вопрос 5. Какие approvals даны сейчас?

**Codex спрашивает:**

```text
Вопрос 5/5. Дай отдельные approvals. Можно ответить yes/no по каждому.

Deploy, restore и rollback - разные runtime actions. Если где-то no, Codex
остановится на этом gate and proof останется blocked.

Deploy approval: yes/no
Deploy scope: target, APP_IMAGE, обязательный backup/preflight before deploy
Restore drill approval: yes/no
Restore scope: disposable/staging target; production data не перезаписывать
Rollback drill approval: yes/no
Rollback scope: previous image/version and healthcheck after rollback
Можно сохранять sanitized transcript без secrets: yes/no
Рабочее окно: Browser ChatGPT
```

**Пользователь отвечает:**

```text
Deploy approval: yes
Deploy scope: можно выполнить deploy для <project> на <target> с APP_IMAGE=<image>; backup/preflight обязателен до deploy
Restore drill approval: yes
Restore scope: можно выполнить restore test на disposable/staging target <target>; production data не перезаписывать
Rollback drill approval: yes
Rollback scope: можно выполнить rollback drill к previous image/version <value> и проверить healthcheck
Можно сохранять sanitized transcript без secrets: yes
Рабочее окно: Browser ChatGPT
```

**Codex принимает ответ, если:**

- approvals даны отдельно;
- deploy scope содержит target and image;
- restore scope не перезаписывает production data без отдельного production
  recovery approval;
- rollback scope содержит previous image/version или explicit plan выяснить его
  перед deploy;
- transcript разрешен and sanitized.

**Codex останавливается, если:**

- любой approval равен `no` для соответствующего gate;
- approval общий и не различает deploy/restore/rollback;
- пользователь просит выполнить destructive action без backup/preflight;
- transcript нельзя сохранить, но proof claim уже ожидается.

## Итоговый ответ пользователя для запуска pilot

Когда все пять вопросов закрыты, пользователь может дать один цельный блок:

```text
Downstream pilot inputs ready.
Repo: /projects/<repo>
GitHub repo: <owner>/<repo> или none
Project slug: <project>
Protected paths/data: <список> или none
APP_IMAGE: <real image>
Target: <target label>
Target type: staging/production/disposable_restore
Runtime root: /srv/<project>-prod
Domain: <domain or none>
Backup path: /var/backups/projects/<project>
Previous image/version for rollback: <value> или unknown-before-preflight
Secrets: внесены вне repo; значения не раскрывать
Deploy approval: yes/no
Restore drill approval: yes/no
Rollback drill approval: yes/no
Transcript policy: sanitize secrets and private values
Goal: run downstream application proof without false pass and fill reports/release/downstream-application-proof-report.md
```

Codex после такого ответа выполняет repo/VPS work сам, если доступ и approvals
достаточны. Если любой gate закрыт неполно, Codex обновляет proof report как
`blocked_external_inputs`, а не заявляет pass.

## Санитизированный transcript

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

Если любой пункт отсутствует, correct status is `blocked_external_inputs`,
`not_run` or `ready_for_external_pilot`, not `passed`.
