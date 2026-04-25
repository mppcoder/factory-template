# Operator Next Step

Этот файл нужен, когда вы хотите быстро понять: что сейчас происходит и какую команду запускать следующей.

## 1) Открыть минимальную панель оператора

Рекомендуемый unified entrypoint:

```bash
python3 template-repo/scripts/factory-launcher.py --mode continue
```

Прямой fallback:

```bash
python3 template-repo/scripts/operator-dashboard.py
```

Панель показывает:
- готовность deploy baseline;
- выбранный `OPERATOR_PRESET`;
- env validation для starter/production presets;
- доступность Docker Compose;
- статус последнего dry-run;
- статус последнего deploy;
- короткий verify snapshot;
- одну рекомендуемую следующую команду.

## 2) Безопасная проверка перед deploy

```bash
bash template-repo/scripts/deploy-dry-run.sh
```

Для production presets:

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset app-db
bash template-repo/scripts/deploy-dry-run.sh --preset reverse-proxy
bash template-repo/scripts/deploy-dry-run.sh --preset production
```

Для отдельного env-файла:

```bash
bash template-repo/scripts/deploy-dry-run.sh --env-file /path/to/prod.env --preset production --strict-env
```

Что делает dry-run:
- проверяет `deploy/compose.yaml` и `deploy/compose.production.yaml`;
- подключает `deploy/presets/*.yaml` для выбранного preset;
- выбирает `deploy/.env` (или безопасный fallback `deploy/.env.example`);
- запускает `template-repo/scripts/validate-operator-env.py`;
- валидирует итоговый compose config без запуска контейнеров;
- сохраняет короткий отчёт в `.factory-runtime/reports/deploy-dry-run-latest.txt`.

## 3) Проверить readiness для remote VPS

Перед реальным удалённым VPS deploy:

- создайте `deploy/.env` из примера и замените все secrets/placeholders;
- для `production` задайте `APP_BIND_ADDRESS=127.0.0.1`, `DOMAIN`, `TLS_EMAIL`, `ACME_AGREE=true`;
- убедитесь, что DNS указывает на VPS, а порты `80/443` открыты;
- проверьте backup path и restore drill для `app-db`/`production`;
- выполните strict dry-run:

```bash
bash template-repo/scripts/deploy-dry-run.sh --preset production --strict-env
```

## 4) One-button-ish deploy на локальный VPS

```bash
bash template-repo/scripts/deploy-local-vps.sh --yes
```

Скрипт:
1. сначала автоматически запускает dry-run;
2. затем выполняет `docker compose pull` и `up -d`;
3. показывает `docker compose ps`;
4. сохраняет отчёт в `.factory-runtime/reports/deploy-last-run.txt`.

Для opt-in preset:

```bash
bash template-repo/scripts/deploy-local-vps.sh --yes --preset production
```

## 5) Backup hook

```bash
docker compose \
  -f deploy/compose.yaml \
  -f deploy/compose.production.yaml \
  -f deploy/presets/app-db.yaml \
  --env-file deploy/.env \
  run --rm db-backup
```

## 6) Короткая проверка после deploy

```bash
python3 template-repo/scripts/operator-dashboard.py --verify-summary
```

Если нужно обновить полный verify baseline:

```bash
bash template-repo/scripts/verify-all.sh quick
```
