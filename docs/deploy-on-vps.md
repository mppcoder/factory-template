# Deploy на VPS

## Цель

Дать безопасный single-VPS маршрут без тяжёлого orchestration-слоя:
- сначала dry-run;
- потом один deploy-скрипт;
- затем читаемый статус.

По умолчанию используется минимальный `starter` profile. Production-функции подключаются только через opt-in presets.

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

4. Выполните deploy:

```bash
bash template-repo/scripts/deploy-local-vps.sh --yes
```

5. Проверьте короткий verify summary:

```bash
python3 template-repo/scripts/operator-dashboard.py --verify-summary
```

## Операторские presets

Preset выбирается через `OPERATOR_PRESET` в `deploy/.env` или через флаг `--preset`.

- `starter`: один app-контейнер, порт `APP_PORT`, без обязательных DB/TLS секретов.
- `app-db`: добавляет Postgres, health check, `DATABASE_URL` и backup hook.
- `reverse-proxy`: добавляет Caddy reverse proxy с HTTP/HTTPS портами.
- `production`: включает `app-db` и `reverse-proxy` вместе.

Примеры:

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset app-db
bash template-repo/scripts/deploy-dry-run.sh --preset reverse-proxy
bash template-repo/scripts/deploy-dry-run.sh --preset production
```

Для проверки отдельного env-файла без изменения `deploy/.env`:

```bash
bash template-repo/scripts/deploy-dry-run.sh --env-file /path/to/prod.env --preset production --strict-env
```

Для реального deploy с production presets используйте `deploy/.env`, а не только `.env.example`:

```bash
cp deploy/.env.example deploy/.env
$EDITOR deploy/.env
python3 template-repo/scripts/validate-operator-env.py --preset production
bash template-repo/scripts/deploy-local-vps.sh --yes --preset production
```

## Что настраивается через env

Файл: `deploy/.env`

- `OPERATOR_PRESET` — `starter`, `app-db`, `reverse-proxy` или `production`.
- `APP_IMAGE` — Docker image приложения.
- `APP_CONTAINER_NAME` — имя контейнера.
- `APP_BIND_ADDRESS` — bind address для app-порта. Для reverse proxy обычно `127.0.0.1`.
- `APP_PORT` — внешний порт на VPS.
- `APP_HEALTHCHECK_PATH` — HTTP path для app health check.

Для `app-db` / `production`:

- `DB_IMAGE`, `DB_CONTAINER_NAME`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
- `BACKUP_ENABLED`, `BACKUP_PATH`, `BACKUP_RETENTION_DAYS`.

Для `reverse-proxy` / `production`:

- `REVERSE_PROXY_IMAGE`, `REVERSE_PROXY_CONTAINER_NAME`.
- `DOMAIN` — реальный публичный hostname.
- `TLS_EMAIL` — email для ACME/TLS уведомлений.
- `ACME_AGREE=true` — подтверждение принятия условий CA.

По умолчанию используется демонстрационный безопасный baseline:
- image: `nginx:1.27-alpine`
- порт: `8080`

## Что делает каждый compose-файл

- `deploy/compose.yaml`: базовый single-service контур (app, network, volume).
- `deploy/compose.production.yaml`: production override (pull_policy, лог-ротация, security flags).
- `deploy/presets/app-db.yaml`: optional Postgres + backup hook.
- `deploy/presets/reverse-proxy.yaml`: optional Caddy reverse proxy / TLS.

Скрипты сами добавляют нужные preset overlays в зависимости от `OPERATOR_PRESET` или `--preset`.

## Checklist готовности remote VPS

Перед production deploy на удалённый VPS проверьте:

- DNS `A/AAAA` для `DOMAIN` указывает на VPS.
- Порты `80` и `443` открыты на firewall/security group.
- `docker compose version` проходит под операторским пользователем.
- `deploy/.env` существует, права ограничены, секреты не коммитятся.
- `APP_IMAGE` указывает на настоящий production image/tag.
- Для `reverse-proxy`/`production`: `APP_BIND_ADDRESS=127.0.0.1`, `DOMAIN` не `example.com`, `TLS_EMAIL` реальный, `ACME_AGREE=true`.
- Для `app-db`/`production`: `DB_PASSWORD` длинный и случайный, `BACKUP_PATH` существует или будет создан, известен restore path.
- Dry-run прошёл на том же VPS и с тем же preset:

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset production --strict-env
```

## Backups / резервные копии

`app-db` preset добавляет одноразовый backup hook `db-backup`. Он не запускается как daemon при обычном `up -d`; его нужно вызывать явно или из cron/systemd timer:

```bash
docker compose \
  -f deploy/compose.yaml \
  -f deploy/compose.production.yaml \
  -f deploy/presets/app-db.yaml \
  --env-file deploy/.env \
  run --rm db-backup
```

Минимальная restore-проверка перед cutover: убедитесь, что свежий `.sql` файл создан в `BACKUP_PATH` и может быть прочитан оператором.

## Health checks / проверки здоровья

- `app` проверяет `http://127.0.0.1${APP_HEALTHCHECK_PATH}` внутри контейнера.
- `db` в `app-db` preset проверяет `pg_isready`.
- `reverse-proxy` проверяет доступность Caddy binary и зависит от healthy `app`.

Проверка после deploy:

```bash
docker compose \
  -f deploy/compose.yaml \
  -f deploy/compose.production.yaml \
  -f deploy/presets/app-db.yaml \
  -f deploy/presets/reverse-proxy.yaml \
  --env-file deploy/.env \
  ps
python3 template-repo/scripts/operator-dashboard.py --verify-summary
```

## Человекочитаемые отчёты

Скрипты пишут короткие отчёты:
- `.factory-runtime/reports/deploy-dry-run-latest.txt`
- `.factory-runtime/reports/deploy-last-run.txt`

Панель оператора читает эти файлы и выдаёт рекомендацию "что дальше".

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

## Зафиксированные риски и ограничения

- `R-DEPLOY-01`: baseline рассчитан на single-VPS контур и не заменяет multi-node orchestration.
- `R-DEPLOY-02`: скрипты зависят от `docker compose` (или legacy `docker-compose`) в окружении VPS.
- `R-DEPLOY-03`: TLS/домен/реверс-прокси доступны как opt-in preset, но DNS/firewall/секреты остаются ответственностью оператора.
- `R-DEPLOY-04`: дефолтный image (`nginx`) демонстрационный; для реального сервиса нужен явный production image в `APP_IMAGE`.
