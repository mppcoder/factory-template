# Deploy On VPS (минимальный операторский маршрут)

## Цель

Дать безопасный и короткий путь deploy без тяжёлого orchestration-слоя:
- сначала dry-run;
- потом один deploy-скрипт;
- затем читаемый статус.

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

## Что настраивается через env

Файл: `deploy/.env`

- `APP_IMAGE` — Docker image приложения.
- `APP_CONTAINER_NAME` — имя контейнера.
- `APP_PORT` — внешний порт на VPS.

По умолчанию используется демонстрационный безопасный baseline:
- image: `nginx:1.27-alpine`
- порт: `8080`

## Что делает каждый compose-файл

- `deploy/compose.yaml`: базовый single-service контур (app, network, volume).
- `deploy/compose.production.yaml`: production override (pull_policy, лог-ротация, security flags).

## Human-readable отчёты

Скрипты пишут короткие отчёты:
- `.factory-runtime/reports/deploy-dry-run-latest.txt`
- `.factory-runtime/reports/deploy-last-run.txt`

Панель оператора читает эти файлы и выдаёт рекомендацию "что дальше".

## Rollback (минимальный)

Откат к предыдущему image/tag:
1. поменяйте `APP_IMAGE` в `deploy/.env`;
2. запустите:

```bash
bash template-repo/scripts/deploy-local-vps.sh --yes
```

## Зафиксированные риски и ограничения

- `R-DEPLOY-01`: baseline рассчитан на single-VPS контур и не заменяет multi-node orchestration.
- `R-DEPLOY-02`: скрипты зависят от `docker compose` (или legacy `docker-compose`) в окружении VPS.
- `R-DEPLOY-03`: TLS/домен/реверс-прокси не настраиваются автоматически в этом минимальном профиле.
- `R-DEPLOY-04`: дефолтный image (`nginx`) демонстрационный; для реального сервиса нужен явный production image в `APP_IMAGE`.
