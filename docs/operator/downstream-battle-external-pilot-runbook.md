# Handoff-ранбук с пошаговым опросом для downstream/battle pilot

## Назначение

Этот ранбук нужен, чтобы запустить downstream/battle application proof как
управляемый handoff: пользователь вставляет один стартовый handoff в Codex, а
дальше Codex не просит большой блок данных. Он задает по одному вопросу,
объясняет зачем вопрос нужен, предлагает варианты ответа и после каждого ответа
решает: идти дальше, уточнить недостающее или оставить proof blocked.

Пока не выбран реальный downstream repo, real `APP_IMAGE`, target, secrets
boundary и approvals на deploy/restore/rollback, proof остается
`blocked_external_inputs` или `ready_for_external_pilot`. Заявлять
`proof_status: passed` запрещено.

## Стартовый handoff для Codex

Пользователь запускает диалог, вставляя в Codex один блок:

```text
launch_source: user-external-pilot-dialog
project: factory-template
handoff_shape: codex-task-handoff
goal: провести пошаговый опрос для downstream/battle application proof, не выполнять deploy/restore/rollback без отдельных approvals и не заявлять pass без real evidence

Прочитай:
- template-repo/scenario-pack/00-master-router.md
- docs/operator/downstream-battle-external-pilot-runbook.md
- docs/downstream-application-proof.md
- docs/releases/single-vps-downstream-proof-roadmap.md
- reports/release/downstream-application-proof-report.md

Правила:
- задавай пользователю только один вопрос за раз;
- каждый вопрос должен содержать короткое пояснение, почему он нужен;
- каждый вопрос должен дать варианты ответа;
- не проси secrets, tokens, passwords, private keys или raw env values;
- если пользователь выбирает not_ready/unknown/no, зафиксируй blocker and stop at the current gate;
- если пользователь отвечает свободным текстом, нормализуй его в выбранный вариант и коротко подтверди;
- после каждого принятого ответа задай следующий вопрос;
- runtime mutation разрешена только после отдельных deploy/restore/rollback approvals.

Начни с Вопроса 1.
```

## Правила опроса для Codex

- Codex задает ровно один вопрос за ход.
- Codex не просит пользователя заполнить большой общий блок.
- Codex принимает ответ в одном из предложенных вариантов или в свободной форме.
- Если ответ свободный, Codex переформулирует его в выбранный вариант и просит
  подтверждение только если смысл неочевиден.
- Если выбран `not_ready`, `unknown` или `no`, Codex не давит на пользователя,
  фиксирует текущий blocker and keeps proof status blocked.
- Если пользователь случайно вставил secret, Codex останавливает диалог,
  просит rotate leaked secret and sanitize transcript.
- После пяти вопросов Codex собирает итоговый evidence summary and asks for
  final confirmation before any deploy/restore/rollback work.

## Вопрос 1. Какой downstream/battle проект выбираем?

**Codex спрашивает:**

```text
Вопрос 1/5: какой downstream/battle проект берем в pilot?

Зачем спрашиваю:
выбирается не проект шаблона `factory-template`, а боевой/downstream проект,
чью реальную application workload нужно доказать. Без выбранного проекта я не
могу проверять APP_IMAGE, deploy path, backup, restore или rollback.

Repo-first остается целевым proof mode: для pass нужен git repo или Codex должен
сначала материализовать/подключить repo. Папка проекта без git repo или папка
в нестандартном месте VPS допустима только как legacy intake/preflight
candidate, но не как downstream proof pass.

Выбери вариант:
A. Боевой repo уже есть на VPS: /projects/<repo>
B. Боевой repo есть в GitHub, но еще не открыт/не клонирован на VPS: <owner>/<repo>
C. Есть папка проекта без git repo или вне стандарта: <absolute-path>
D. Проект еще не выбран
E. Другое: опиши коротко

Ответь одной строкой, без secrets.
```

**Примеры ответа пользователя:**

```text
A: /projects/my-product
```

```text
B: mppcoder/my-product
```

```text
C: /my-product-source
```

```text
C: /root/my-product-source
```

```text
D: проект еще не выбран
```

**Codex после ответа:**

- если `A`, проверяет remote context and repo root:

```bash
pwd
git status --short --branch
git remote -v
test -f AGENTS.md && sed -n '1,160p' AGENTS.md
```

- если `B`, выясняет, можно ли Codex clone/open repo через available GitHub/SSH
  path;
- если `C`, проверяет папку только как legacy/non-standard project-root
  candidate, затем предлагает standardization path: move/copy to
  `/projects/<repo>`, `git init`, connect GitHub remote, or choose existing repo.
  Пока repo не материализован and layout не нормализован, proof остается blocked;
- если `D`, фиксирует `blocked_external_inputs: downstream project not selected`;
- если `E`, нормализует ответ в `A`, `B`, `C` или `D`, либо задает уточнение.

**Gate pass для вопроса 1:**

- выбран боевой/downstream проект, не `factory-template`;
- repo path/GitHub repo указан, либо дана absolute project-root папка для intake;
- repo доступен или есть понятный путь материализовать repo and normalize layout;
- protected paths/data еще не трогаются;
- пользователь не просит pass без real repo. Project-root без git repo или
  нестандартный VPS path остается `blocked_external_inputs` до repo
  materialization and `/projects/<repo>` standardization.

## Вопрос 2. Это real `APP_IMAGE` или его нужно собрать?

**Codex спрашивает:**

```text
Вопрос 2/5: какой real APP_IMAGE используем?

Зачем спрашиваю:
placeholder image доказывает только template/runtime path. Downstream proof pass
можно заявлять только с образом реального приложения.

Выбери вариант:
A. Real image уже есть: <registry>/<app>:<tag> или <registry>/<app>@sha256:<digest>
B. Image нужно собрать из выбранного downstream repo
C. Image еще не готов
D. Не знаю

Не вставляй registry passwords или tokens.
```

**Примеры ответа пользователя:**

```text
A: registry.example.com/my-product:2026-05-06-1
```

```text
B: нужно собрать из repo и запушить в registry.example.com/my-product
```

```text
C: image еще не готов
```

**Codex после ответа:**

- если `A`, проверяет, что image не `factory-template-placeholder-app:local`, не
  demo `nginx`, не unsafe `latest` without accepted reason;
- если `B`, спрашивает отдельное follow-up только про build/push boundary and
  registry target, без credentials;
- если `C` или `D`, фиксирует blocker and stops before deploy planning.

**Gate pass для вопроса 2:**

- image является real downstream app image; либо
- есть approved path собрать real image из downstream repo; и
- registry credentials остаются вне repo/chat.

## Вопрос 3. Где разрешен runtime target?

**Codex спрашивает:**

```text
Вопрос 3/5: какой VPS/staging target можно использовать?

Зачем спрашиваю:
deploy, restore и rollback меняют runtime. Я должен знать target type and runtime
root, чтобы не смешать /projects dev workspace и /srv runtime.

Выбери вариант:
A. Staging/disposable target: <ssh-alias-or-label>, runtime root /srv/<project>-staging
B. Production target: <ssh-alias-or-label>, runtime root /srv/<project>-prod
C. Только preflight, runtime mutation пока нельзя
D. Target еще не выбран

Не вставляй passwords, private keys или raw secrets.
```

**Примеры ответа пользователя:**

```text
A: vps-main, /srv/my-product-staging, domain staging.example.com
```

```text
B: vps-main, /srv/my-product-prod, domain example.com, production approval будет отдельно
```

```text
C: можно только preflight
```

**Codex после ответа:**

- если `A` или `B`, делает только безопасный preflight until explicit deploy
  approval:

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

- если `C`, ограничивается inventory/preflight and keeps deploy blocked;
- если `D`, фиксирует `blocked_external_inputs: target not selected`.

**Gate pass для вопроса 3:**

- target type понятен;
- runtime root в `/srv`, не в `/projects`;
- production не получает runtime mutation без отдельного approval;
- backup path and rollback boundary can be determined before deploy.

## Вопрос 4. Secrets уже внесены вне repo?

**Codex спрашивает:**

```text
Вопрос 4/5: secrets внесены вне repo?

Зачем спрашиваю:
proof transcript и repo не должны содержать passwords, tokens, private keys,
raw .env values or registry credentials. Мне нужен только факт и безопасная
проверка границы.

Выбери вариант:
A. Да, secrets внесены в /etc/<project>.env на target
B. Да, secrets внесены в secret manager / CI secrets / docker credential store
C. Secrets для этого pilot не требуются
D. Еще нет

Не вставляй сами значения secrets.
```

**Примеры ответа пользователя:**

```text
A: /etc/my-product.env, значения не раскрывать, можно проверить только permissions
```

```text
B: GitHub Actions secrets и docker credential store, значения не раскрывать
```

```text
D: secrets еще не внесены
```

**Codex после ответа:**

- если `A`, может проверить только existence/permissions/redacted key names:

```bash
test -f /etc/<project>.env
stat -c '%a %U:%G %n' /etc/<project>.env
grep -E '^[A-Z0-9_]+=' /etc/<project>.env | sed 's/=.*/=<redacted>/'
```

- если `B`, фиксирует location type without values;
- если `C`, требует accepted reason why not applicable;
- если `D`, keeps proof blocked before deploy.

**Gate pass для вопроса 4:**

- secret values не попали в chat/repo/report/transcript;
- Codex проверяет only safe facts;
- if not applicable, reason is explicit.

## Вопрос 5. Какие approvals можно дать сейчас?

**Codex спрашивает:**

```text
Вопрос 5/5: какие runtime approvals можно дать сейчас?

Зачем спрашиваю:
deploy, restore and rollback are separate runtime actions. Я не могу выполнить
их по общему "можно" без отдельного approval на каждый контур.

Выбери вариант:
A. Только preflight и подготовка runtime files, без deploy
B. Deploy approval: yes; restore/rollback пока no
C. Deploy + restore drill approval: yes; rollback пока no
D. Deploy + restore drill + rollback drill approval: yes
E. Никаких runtime actions сейчас

Если выбираешь B/C/D, уточни target and APP_IMAGE. Не вставляй secrets.
```

**Примеры ответа пользователя:**

```text
A: можно preflight и подготовить runtime files, deploy пока нельзя
```

```text
B: deploy yes для my-product на vps-main с APP_IMAGE=registry.example.com/my-product:2026-05-06-1; restore/rollback no
```

```text
D: deploy yes, restore drill yes на staging, rollback drill yes к previous image; transcript sanitize
```

**Codex после ответа:**

- если `A`, готовит only non-mutating plan/files and keeps deploy blocked;
- если `B`, requires backup/preflight before deploy and does not claim pass
  because restore/rollback missing;
- если `C`, still does not claim pass because rollback missing;
- если `D`, may proceed to runtime proof only after confirming all previous gates;
- если `E`, stops with proof blocked.

**Gate pass для вопроса 5:**

- approvals are specific to deploy, restore and rollback;
- restore does not overwrite production data unless separately approved;
- rollback target/version is known or must be captured before deploy;
- sanitized transcript is allowed.

## После опроса

Codex собирает краткое резюме:

```text
Downstream pilot survey summary:
- repo: <accepted/blocked>
- APP_IMAGE: <accepted/blocked>
- target: <accepted/blocked>
- secrets boundary: <confirmed/not_applicable/blocked>
- approvals: <preflight/deploy/restore/rollback>
- next gate: <what happens next>
- proof status: blocked_external_inputs / ready_for_external_pilot / can_run_runtime_proof
```

Если все gates готовы, Codex выполняет repo/VPS work сам в approved boundary.
Если любой gate неполный, Codex обновляет proof report as blocked and does not
claim pass.

## Развилка закрытия proof

После deploy, healthcheck, backup, restore и rollback Codex обязан отдельно
зафиксировать, какой proof закрывается:

```text
Вопрос закрытия: какой scope закрываем сейчас?

Зачем спрашиваю:
local runtime proof и public HTTPS/nginx proof имеют разные риски. Нельзя
заявлять public endpoint proof, если мы проверили только localhost/systemd/docker
runtime.

Выбери вариант:
A. Закрыть как local prod runtime proof, public HTTPS/nginx не заявлять
B. Продолжить отдельный public HTTPS/reverse-proxy proof
C. Остановиться и оставить proof blocked
```

Если пользователь выбирает `A`, Codex может зафиксировать
`local_prod_runtime_proof_passed` при наличии real repo, real `APP_IMAGE`,
approved target, secrets outside repo, deploy, healthcheck, backup, restore,
rollback и sanitized transcript. При этом `public_https` должен остаться
`not_claimed`.

Если пользователь выбирает `B`, Codex переходит к отдельному approval boundary
для domain, TLS, nginx/reverse-proxy, exposed ports and public healthcheck.

Если пользователь выбирает `C`, Codex фиксирует blocker and does not claim pass.

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
- secrets outside repo or accepted not-applicable reason;
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
