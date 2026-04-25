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
- доступность Docker Compose;
- статус последнего dry-run;
- статус последнего deploy;
- короткий verify snapshot;
- одну рекомендуемую следующую команду.

## 2) Безопасная проверка перед deploy

```bash
bash template-repo/scripts/deploy-dry-run.sh
```

Что делает dry-run:
- проверяет `deploy/compose.yaml` и `deploy/compose.production.yaml`;
- выбирает `deploy/.env` (или безопасный fallback `deploy/.env.example`);
- валидирует итоговый compose config без запуска контейнеров;
- сохраняет короткий отчёт в `.factory-runtime/reports/deploy-dry-run-latest.txt`.

## 3) One-button-ish deploy на локальный VPS

```bash
bash template-repo/scripts/deploy-local-vps.sh --yes
```

Скрипт:
1. сначала автоматически запускает dry-run;
2. затем выполняет `docker compose pull` и `up -d`;
3. показывает `docker compose ps`;
4. сохраняет отчёт в `.factory-runtime/reports/deploy-last-run.txt`.

## 4) Короткая проверка после deploy

```bash
python3 template-repo/scripts/operator-dashboard.py --verify-summary
```

Если нужно обновить полный verify baseline:

```bash
bash template-repo/scripts/verify-all.sh quick
```
