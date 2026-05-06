# Полевая проверка production VPS

Этот runbook проверяет single-VPS production path без разрушительных действий по умолчанию. Реальный deploy, DNS/firewall changes, backup restore и rollback drill выполняются только после явного approval оператора.

Если цель - перенос нескольких боевых проектов или выбор между `single-host` и `split-host`, сначала примените `docs/architecture/vps-project-hosting-topologies.md` и `docs/runbooks/migrate-projects-vps-topologies.md`. Этот field pilot остается доказательством single-service production preset contour, а не полной миграцией нескольких runtime.

## Область проверки

- starter остаётся beginner default.
- production presets остаются opt-in: `app-db`, `reverse-proxy-tls`, `backup`, `healthcheck` или alias `production`.
- Dry-run/report evidence не считается real production proof.
- Field deploy status до реального VPS запуска: `pending-real-vps-approval`.
- P3-S5 готовит runtime QA boundary: pre-deploy QA, post-deploy QA, backup restore test, rollback drill и sanitized runtime transcript requirements.
- Этот runbook не просит хранить секреты в repo и не превращает report-ready состояние в passed production gate.

## Предусловия

- VPS с SSH-доступом оператора.
- Docker Compose доступен: `docker compose version` или `docker-compose --version`.
- Repo или generated project уже находится на VPS.
- `deploy/.env` создан из `deploy/.env.example` и не содержит example secrets.
- Production image/tag задан в `APP_IMAGE`; если реального приложения ещё нет, используется локально сгенерированный placeholder application image, а не внешняя обязанность пользователя найти образ.
- Для TLS: DNS `A/AAAA` для `DOMAIN` указывает на VPS, ports `80/443` открыты, `TLS_EMAIL` реальный, `ACME_AGREE=true`.
- Для DB/backup: задан `DB_PASSWORD`, `DB_DATA_VOLUME`, `BACKUP_ENABLED=true`, `BACKUP_PATH`, retention policy и restore procedure.

## Этап 0: безопасный отчет

```bash
python3 template-repo/scripts/validate-operator-env.py \
  --preset production \
  --field-pilot-report .factory-runtime/reports/operator-env-field-pilot-latest.md

bash template-repo/scripts/deploy-dry-run.sh \
  --preset production \
  --strict-env \
  --field-pilot-report .factory-runtime/reports/production-vps-field-pilot-latest.md
```

Expected output:

- `Проверка operator env` has no `FAIL`.
- `Dry-run ПРОЙДЕН: compose config валиден.`
- Report file exists and says dry-run/report evidence is not real VPS proof.

Failure handling:

- Env validation failure: fix `deploy/.env`; do not deploy.
- Compose config failure: inspect selected preset overlay; do not deploy.
- Missing Docker Compose: install Compose or use a VPS image that includes it.

## Предварительная QA перед deploy

Machine-readable label: `Pre-deploy QA gate`.

Перед approved production deploy оператор фиксирует:

- `validate-operator-env.py --preset production --field-pilot-report` без `FAIL`.
- `deploy-dry-run.sh --preset production --strict-env --field-pilot-report` проходит на том же VPS и с тем же env.
- DNS, firewall, Docker Compose, production image/tag, DB volume, backup path и healthcheck endpoint проверены.
- `deploy/.env` заполнен вне repo; секреты не копируются в task notes, commit, screenshots или runtime transcript.
- Backup restore procedure известна до cutover; если restore target не approved, production proof остается pending.

Pre-deploy QA может дать статус `ready-for-approved-runtime-run`, но не `production-proof-passed`.

Codex/operator helper:

```bash
python3 template-repo/scripts/prepare-production-env-defaults.py
```

Он заполняет non-secret defaults и оставляет оператору только секреты/manual values. Не просите пользователя вручную заполнять значения, которые Codex может безопасно вывести на VPS.

Если реального `APP_IMAGE` еще нет, сгенерируйте локальный placeholder application image:

```bash
python3 template-repo/scripts/build-placeholder-app-image.py --install-volume
```

Для внешней картинки-заглушки:

```bash
python3 template-repo/scripts/build-placeholder-app-image.py --install-volume --image-url "https://example.com/placeholder.png"
```

Это снимает с пользователя лишнюю обязанность искать Docker image или вручную собирать страницу-заглушку. Boundary остается явной: placeholder proof не является proof бизнес-приложения.

## Этап 1: starter smoke

Use this before production presets when validating a new VPS.

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset starter --strict-env
bash template-repo/scripts/deploy-local-vps.sh --preset starter
python3 template-repo/scripts/operator-dashboard.py --preset starter --verify-summary
```

Expected output:

- `starter` activates only the app container.
- No DB/TLS/backup secrets are required.
- The app endpoint responds on `APP_PORT`.

Rollback:

```bash
docker compose --env-file deploy/.env -f deploy/compose.yaml -f deploy/compose.production.yaml -f deploy/presets/starter.yaml down
```

## Этап 2: app-db

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset app-db --strict-env
bash template-repo/scripts/deploy-local-vps.sh --preset app-db
docker compose --env-file deploy/.env -f deploy/compose.yaml -f deploy/compose.production.yaml -f deploy/presets/app-db.yaml ps
```

Expected output:

- Services include `app` and `db`.
- `db` healthcheck is healthy before app cutover.

Failure handling:

- DB password/volume failures block deploy.
- Migration failures belong to the application runbook and require application-specific rollback.

## Этап 3: reverse-proxy-tls

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset app-db,reverse-proxy-tls --strict-env
bash template-repo/scripts/deploy-local-vps.sh --preset app-db,reverse-proxy-tls
curl -fsS "https://${DOMAIN}${HEALTHCHECK_ENDPOINT:-/}"
```

Expected output:

- Services include `app`, `db`, `reverse-proxy`.
- Caddy obtains/uses TLS for `DOMAIN`.
- App binds to `127.0.0.1` when exposed through proxy.

Failure handling:

- DNS failure: wait for propagation or correct the `A/AAAA` record.
- Firewall failure: open ports `80` and `443`.
- ACME failure: verify `TLS_EMAIL`, `ACME_AGREE=true`, rate limits and hostname.

## Этап 4: backup

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset app-db,backup --strict-env
docker compose \
  -f deploy/compose.yaml \
  -f deploy/compose.production.yaml \
  -f deploy/presets/app-db.yaml \
  -f deploy/presets/backup.yaml \
  --env-file deploy/.env \
  run --rm db-backup
ls -lh "$BACKUP_PATH"
```

Expected output:

- A readable `*.sql` dump exists in `BACKUP_PATH`.
- Retention command does not delete the fresh backup.

Restore test:

- Copy the latest dump to a safe test target.
- Restore into a disposable database or staging VPS.
- Record command, timestamp, dump filename and result in the field pilot report.

## Этап 5: healthcheck

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset production --strict-env --field-pilot-report
bash template-repo/scripts/deploy-local-vps.sh --preset production --field-pilot-report
python3 template-repo/scripts/operator-dashboard.py --preset production --field-pilot-report --verify-summary
```

Expected output:

- Services include `app`, `db`, `reverse-proxy`, `db-backup`.
- `HEALTHCHECK_ENDPOINT` returns success through the final public route.
- `.factory-runtime/reports/production-vps-field-pilot-latest.md` records deploy evidence.

## Последующая QA после deploy

Machine-readable label: `Post-deploy QA gate`.

После approved deploy оператор фиксирует sanitized runtime transcript:

- deploy command, preset, image tag and timestamp;
- `docker compose ps` summary without secrets;
- public healthcheck result;
- backup command result and backup filename/path with sensitive host/user values redacted if needed;
- restore test result or explicit `restore_test_status: pending`;
- rollback drill result or explicit `rollback_drill_status: pending`;
- final status: `passed` only when deploy, healthcheck, backup restore and rollback drill evidence are all present.

Transcript redaction rules:

- Replace secrets, tokens, private keys, passwords, full `.env` contents and private connection strings with `[REDACTED]`.
- Keep commands, timestamps, image tags, service names and pass/fail status.
- Do not commit raw `.factory-runtime/` reports from a real VPS if they include sensitive values; commit only sanitized release evidence.

## Тренировка отката

Minimum image rollback:

1. Record current `APP_IMAGE` and current healthy status.
2. Set a candidate `APP_IMAGE`.
3. Run `deploy-dry-run.sh --preset production --strict-env`.
4. Deploy only after approval.
5. Revert `APP_IMAGE` to the previous tag.
6. Run dry-run again.
7. Run `deploy-local-vps.sh --preset production --field-pilot-report`.
8. Verify healthcheck and record result.

DB rollback boundary:

- Before migration, run `db-backup` and verify the dump exists.
- Restore/migration rollback is application-specific and must be tested before production cutover.
- If restore is not tested, production field pilot status remains `pending-backup-restore-proof`.

## Цикл Project Knowledge Done

For this field pilot, record:

- Decisions: selected preset sequence, why starter stayed default, why production presets stayed opt-in.
- Backup выводы: backup path, dump result, restore test status.
- Rollback выводы: previous/current image tags, rollback command, healthcheck after rollback.
- Downstream impact: whether downstream repos need template sync.
- Done evidence: env report, dry-run report, deploy transcript if approved, rollback/restore result.
- Sanitized transcript: required for any claim beyond dry-run/report-ready.

## Текущие repo-доказательства

As of 2026-04-27, this repo has dry-run/report automation and P3-S5 runtime QA boundary docs only. No real VPS deploy, backup restore test or rollback drill was executed in this remediation because destructive runtime work requires explicit user approval and runtime VPS access.
