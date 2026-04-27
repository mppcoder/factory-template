# Reference runtime app шаблона

## Назначение

`factory-template` должен уметь устанавливаться и восстанавливаться на VPS без внешнего боевого приложения. Для этого repo содержит template-owned reference runtime app.

Это не отдельный продуктовый сервис и не proof бизнес-логики. Это минимальный runtime artifact для:

- первичной установки шаблона на VPS;
- smoke-проверки production presets;
- восстановления после падения VPS, если боевого downstream app еще нет;
- демонстрации того, что reverse proxy, healthcheck, backup/restore и rollback path работают.

## Источник истины

Source живет прямо в repo:

- `deploy/static-placeholder/index.html`
- `deploy/static-placeholder/placeholder.svg`
- `template-repo/scripts/build-placeholder-app-image.py`
- `template-repo/scripts/install-static-placeholder.py`

Канонический локальный image tag:

```text
factory-template-placeholder-app:local
```

## Почему не npm install

Для текущего `factory-template` канонический install source - сам repo: clone/pull или release archive, затем repo scripts.

NPM package или published Docker registry image могут быть будущим packaging contour, но они не обязательны для template proof. Начальный пользовательский путь должен работать из repo без внешней публикации.

## Первичная установка на VPS

Минимальный путь:

```bash
cp deploy/.env.example deploy/.env
python3 template-repo/scripts/prepare-production-env-defaults.py
python3 template-repo/scripts/build-placeholder-app-image.py --install-volume
bash template-repo/scripts/deploy-dry-run.sh --preset production --strict-env
bash template-repo/scripts/deploy-local-vps.sh --yes --preset production
```

Секреты (`DB_PASSWORD`, `TLS_EMAIL`) вводятся в `deploy/.env` вне repo и не коммитятся.

## Восстановление после падения VPS

Если VPS восстановлен с repo, но боевого downstream app еще нет:

```bash
git pull --ff-only
python3 template-repo/scripts/prepare-production-env-defaults.py
python3 template-repo/scripts/build-placeholder-app-image.py --install-volume
bash template-repo/scripts/deploy-dry-run.sh --preset production --strict-env
bash template-repo/scripts/deploy-local-vps.sh --yes --preset production
```

Если сохранились DB backups, restore выполняется по production runbook. Reference app не заменяет application-specific restore logic для downstream/battle проекта.

## Downstream замена

Когда generated/battle project получает реальное приложение:

- `APP_IMAGE` меняется на image этого проекта;
- `APP_PULL_POLICY` возвращается к policy, подходящей для registry/deploy flow;
- healthcheck path, migrations, backup/restore и rollback proof становятся responsibility downstream app.

`factory-template-placeholder-app:local` остается fallback/reference artifact, а не runtime blocker.
