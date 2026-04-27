# Deploy на VPS

## Цель

Дать безопасный single-VPS маршрут без тяжёлого orchestration-слоя:
- сначала dry-run;
- потом один deploy-скрипт;
- затем читаемый статус.

По умолчанию используется минимальный `starter` profile. Production-функции подключаются только через opt-in presets, чтобы первый deploy не превращался в тяжёлый production checklist.

## Быстрый старт

1. Проверьте операторский статус:

```bash
python3 template-repo/scripts/operator-dashboard.py
```

2. При необходимости создайте env из примера:

```bash
cp deploy/.env.example deploy/.env
```

3. Выполните безопасный dry-run:

```bash
bash template-repo/scripts/deploy-dry-run.sh
```

4. Выполните deploy только после явного решения оператора:

```bash
bash template-repo/scripts/deploy-local-vps.sh
```

5. Проверьте короткий verify summary:

```bash
python3 template-repo/scripts/operator-dashboard.py --verify-summary
```

## Операторские presets

Preset выбирается через `OPERATOR_PRESET` в `deploy/.env` или через флаг `--preset`.
Можно указать один preset или список через запятую: `app-db,backup`, `reverse-proxy-tls,healthcheck`.

- `starter`: один app-контейнер, порт `APP_PORT`, без обязательных DB/TLS секретов.
- `app-db`: добавляет Postgres, health check и `DATABASE_URL`.
- `reverse-proxy-tls`: добавляет Caddy reverse proxy с HTTP/HTTPS портами.
- `backup`: добавляет одноразовый `db-backup` hook; требует `app-db`.
- `healthcheck`: явно включает настраиваемый healthcheck endpoint.
- `production`: короткий alias для `app-db,reverse-proxy-tls,backup,healthcheck`.

Старый alias `reverse-proxy` сохранён для совместимости и раскрывается как `reverse-proxy-tls`.

Примеры:

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset app-db
bash template-repo/scripts/deploy-dry-run.sh --preset app-db,backup
bash template-repo/scripts/deploy-dry-run.sh --preset reverse-proxy-tls
bash template-repo/scripts/deploy-dry-run.sh --preset production
```

Для проверки отдельного env-файла без изменения `deploy/.env`:

```bash
bash template-repo/scripts/deploy-dry-run.sh --env-file /path/to/prod.env --preset production --strict-env
```

Для production field pilot evidence без deploy:

```bash
bash template-repo/scripts/deploy-dry-run.sh \
  --env-file /path/to/prod.env \
  --preset production \
  --strict-env \
  --field-pilot-report /path/to/production-vps-field-pilot-latest.md
```

Для реального deploy с production presets используйте `deploy/.env`, а не только `.env.example`:

```bash
cp deploy/.env.example deploy/.env
$EDITOR deploy/.env
python3 template-repo/scripts/validate-operator-env.py --preset production
bash template-repo/scripts/deploy-local-vps.sh --yes --preset production
```

Чтобы Codex/operator не перекладывал на пользователя non-secret настройки, сначала можно подготовить defaults:

```bash
python3 template-repo/scripts/prepare-production-env-defaults.py
```

Скрипт выставит production preset, DB name/user, backup path, `sslip.io` domain для публичного IPv4, `ACME_AGREE=true` и оставит оператору только реальные secrets/manual values: `DB_PASSWORD`, `TLS_EMAIL` и при необходимости настоящий `APP_IMAGE`.

Если реального app image еще нет, используйте generated placeholder вместо ручного поиска картинки:

```bash
python3 template-repo/scripts/install-static-placeholder.py
```

По умолчанию он установит `deploy/static-placeholder/index.html` и `placeholder.svg` в app volume. Для своей картинки можно передать URL:

```bash
python3 template-repo/scripts/install-static-placeholder.py --image-url "https://example.com/placeholder.png"
```

## Что настраивается через env

Файл: `deploy/.env`

- `OPERATOR_PRESET` — `starter`, `app-db`, `reverse-proxy-tls`, `backup`, `healthcheck`, `production` или список через запятую.
- `APP_IMAGE` — Docker image приложения.
- `APP_PULL_POLICY` — policy для получения image при deploy. По умолчанию `always`; для rollback drill с локальным candidate tag можно временно поставить `never`.
- `APP_PLACEHOLDER_MODE` — `static`, если production smoke использует generated placeholder вместо реального приложения.
- `APP_PLACEHOLDER_IMAGE_URL` — URL картинки для placeholder page. По умолчанию локальный `/placeholder.svg`.
- `APP_CONTAINER_NAME` — имя контейнера.
- `APP_BIND_ADDRESS` — bind address для app-порта. Для reverse proxy обычно `127.0.0.1`.
- `APP_PORT` — внешний порт на VPS.
- `APP_DATA_VOLUME` — имя Docker volume для app data.
- `APP_HEALTHCHECK_ENDPOINT` — HTTP path для базового app health check.

Для `app-db`, `backup` и `production`:

- `DB_IMAGE`, `DB_CONTAINER_NAME`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
- `DB_PORT`, `DB_DATA_VOLUME`.

Для `backup` и `production`:

- `BACKUP_ENABLED=true`, `BACKUP_PATH`, `BACKUP_RETENTION_DAYS`.

Для `reverse-proxy-tls` / `production`:

- `REVERSE_PROXY_IMAGE`, `REVERSE_PROXY_CONTAINER_NAME`.
- `DOMAIN` — реальный публичный hostname.
- `TLS_EMAIL` — email для ACME/TLS уведомлений.
- `ACME_AGREE=true` — подтверждение принятия условий CA.
- `HTTP_PORT`, `HTTPS_PORT`, `CADDY_DATA_VOLUME`, `CADDY_CONFIG_VOLUME`.

Для `healthcheck` / `production`:

- `HEALTHCHECK_ENDPOINT` — HTTP path внутри app-контейнера, например `/health`.
- `APP_HEALTHCHECK_INTERVAL`, `APP_HEALTHCHECK_TIMEOUT`, `APP_HEALTHCHECK_RETRIES`, `APP_HEALTHCHECK_START_PERIOD`.

По умолчанию используется демонстрационный безопасный baseline:
- image: `nginx:1.27-alpine`
- порт: `8080`

## Что делает каждый compose-файл

- `deploy/compose.yaml`: базовый single-service контур (app, network, volume).
- `deploy/compose.production.yaml`: production override (pull_policy, лог-ротация, security flags).
- `deploy/presets/starter.yaml`: no-op overlay для явного starter artifact.
- `deploy/presets/app-db.yaml`: optional Postgres.
- `deploy/presets/reverse-proxy-tls.yaml`: optional Caddy reverse proxy / TLS.
- `deploy/presets/backup.yaml`: optional database backup hook.
- `deploy/presets/healthcheck.yaml`: optional explicit healthcheck overlay.
- `deploy/presets/reverse-proxy.yaml`: compatibility alias content для старого имени.

Скрипты сами добавляют нужные preset overlays в зависимости от `OPERATOR_PRESET` или `--preset`.

## Checklist готовности remote VPS

Перед production deploy на удалённый VPS проверьте:

- DNS `A/AAAA` для `DOMAIN` указывает на VPS.
- Порты `80` и `443` открыты на firewall/security group.
- `docker compose version` проходит под операторским пользователем.
- `deploy/.env` существует, права ограничены, секреты не коммитятся.
- `APP_IMAGE` указывает на настоящий production image/tag.
- Для `reverse-proxy-tls`/`production`: `APP_BIND_ADDRESS=127.0.0.1`, `DOMAIN` не `example.com`, `TLS_EMAIL` реальный, `ACME_AGREE=true`.
- Для `app-db`/`production`: `DB_PASSWORD` длинный и случайный, `DB_DATA_VOLUME` задан осознанно.
- Для `backup`/`production`: `BACKUP_ENABLED=true`, `BACKUP_PATH` существует или будет создан, известен restore path.
- Для `healthcheck`/`production`: `HEALTHCHECK_ENDPOINT` отвечает внутри app container.
- Dry-run прошёл на том же VPS и с тем же preset:

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset production --strict-env
```

Расширенный field pilot runbook: `docs/production-vps-field-pilot.md`.

## Backups / резервные копии

`backup` preset добавляет одноразовый backup hook `db-backup`. Он требует `app-db` и не запускается как daemon при обычном `up -d`; его нужно вызывать явно или из cron/systemd timer:

```bash
docker compose \
  -f deploy/compose.yaml \
  -f deploy/compose.production.yaml \
  -f deploy/presets/app-db.yaml \
  -f deploy/presets/backup.yaml \
  --env-file deploy/.env \
  run --rm db-backup
```

Минимальная restore-проверка перед cutover: убедитесь, что свежий `.sql` файл создан в `BACKUP_PATH` и может быть прочитан оператором.

## Health checks / проверки здоровья

- `app` проверяет `http://127.0.0.1${APP_HEALTHCHECK_ENDPOINT}` внутри контейнера.
- `db` в `app-db` preset проверяет `pg_isready`.
- `reverse-proxy-tls` проверяет доступность Caddy binary и зависит от healthy `app`.
- `healthcheck` preset позволяет явно переопределить endpoint через `HEALTHCHECK_ENDPOINT`.

Проверка после deploy:

```bash
docker compose \
  -f deploy/compose.yaml \
  -f deploy/compose.production.yaml \
  -f deploy/presets/app-db.yaml \
  -f deploy/presets/reverse-proxy-tls.yaml \
  -f deploy/presets/backup.yaml \
  -f deploy/presets/healthcheck.yaml \
  --env-file deploy/.env \
  ps
python3 template-repo/scripts/operator-dashboard.py --verify-summary
```

## Человекочитаемые отчёты

Скрипты пишут короткие отчёты:
- `.factory-runtime/reports/deploy-dry-run-latest.txt`
- `.factory-runtime/reports/deploy-last-run.txt`
- `.factory-runtime/reports/production-vps-field-pilot-latest.md` при `--field-pilot-report`
- `.factory-runtime/reports/operator-env-field-pilot-latest.md` при `validate-operator-env.py --field-pilot-report`

Панель оператора читает эти файлы и выдаёт рекомендацию "что дальше".

Важно: field pilot report фиксирует evidence boundary. Если был только dry-run, отчет должен оставаться в статусе pending real VPS/user approval и не считается production proof.

## QA до и после deploy

Pre-deploy QA перед real production run:

- env validation и dry-run проходят на том же VPS, тем же preset и тем же `deploy/.env`;
- DNS/firewall/TLS/backup/healthcheck inputs проверены;
- secrets остаются только в `deploy/.env` или внешнем secret manager, не в repo notes;
- backup restore target и rollback drill plan утверждены до cutover.

Post-deploy QA после approved run:

- healthcheck проходит через final public route;
- backup создан и restore test выполнен на disposable/staging target либо явно отмечен pending;
- rollback drill выполнен либо явно отмечен pending;
- sanitized runtime transcript записывает команды, timestamps, image tags и pass/fail results без secrets.

Dry-run/report-ready не является production proof. Production proof можно заявлять только после approved runtime run и sanitized transcript с deploy, healthcheck, backup restore и rollback evidence.

## Rollback (минимальный)

Откат к предыдущему image/tag:
1. поменяйте `APP_IMAGE` в `deploy/.env`;
2. выполните dry-run с тем же preset;
3. запустите deploy:

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset production --strict-env
bash template-repo/scripts/deploy-local-vps.sh --yes
```

Если откатываете DB schema, сначала сохраните fresh backup через `db-backup`, затем применяйте проверенный restore/migration rollback из приложения.

## Когда добавлять production presets

Начинайте с `starter`, если нужно проверить VPS, Docker Compose, image pull и базовый HTTP endpoint.

Добавляйте `app-db`, когда приложению нужен stateful database на том же VPS и вы готовы управлять `DB_PASSWORD`, volume и migration/restore процедурой.

Добавляйте `reverse-proxy-tls`, когда есть публичный домен, DNS уже указывает на VPS, а порты `80/443` открыты. После этого держите `APP_BIND_ADDRESS=127.0.0.1`, чтобы приложение не торчало наружу мимо TLS proxy.

Добавляйте `backup` после `app-db`, когда есть понятный host path, retention policy и хотя бы одна restore-проверка.

Добавляйте `healthcheck`, когда приложение имеет отдельный endpoint вроде `/health` и оператор хочет сделать его частью deploy gate.

## Зафиксированные риски и ограничения

- `R-DEPLOY-01`: baseline рассчитан на single-VPS контур и не заменяет multi-node orchestration.
- `R-DEPLOY-02`: скрипты зависят от `docker compose` (или legacy `docker-compose`) в окружении VPS.
- `R-DEPLOY-03`: TLS/домен/реверс-прокси доступны как opt-in preset, но DNS/firewall/секреты остаются ответственностью оператора.
- `R-DEPLOY-04`: дефолтный image (`nginx`) демонстрационный; для реального сервиса нужен явный production image в `APP_IMAGE`.
