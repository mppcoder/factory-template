# Guided launcher

Единый beginner-first вход:

```bash
python3 template-repo/scripts/factory-launcher.py
```

Launcher задает conversational-вопросы и ведет по одному из трех маршрутов:

1. `greenfield` - новый проект с нуля.
2. `brownfield` - существующий проект или система.
3. `continue` - уже созданный flow, planning workspace или operator next step.

## Быстрый greenfield start

```bash
python3 template-repo/scripts/factory-launcher.py \
  --mode greenfield \
  --project-name "My First Service" \
  --project-slug my-first-service
```

Что происходит:
- launcher выбирает `greenfield-product`;
- показывает next-step recommendation;
- вызывает существующий `first-project-wizard.py`;
- wizard запускает `preflight-vps-check.py`;
- проект создается через прежний `template-repo/launcher.sh`.

Для dry route без создания проекта:

```bash
python3 template-repo/scripts/factory-launcher.py --mode greenfield --project-name "My First Service" --project-slug my-first-service --route-only
```

## Brownfield start

```bash
python3 template-repo/scripts/factory-launcher.py \
  --mode brownfield \
  --brownfield-kind modernize \
  --project-name "Legacy Service" \
  --project-slug legacy-service
```

Доступные `--brownfield-kind`:
- `modernize` -> `brownfield-with-repo-modernization`;
- `integrate` -> `brownfield-with-repo-integration`;
- `audit` -> `brownfield-with-repo-audit`;
- `no-repo` -> `brownfield-without-repo`.

## Продолжить существующий flow

Показать operator recommendation:

```bash
python3 template-repo/scripts/factory-launcher.py --mode continue
```

Создать planning workspace для следующей feature и затем показать operator status:

```bash
python3 template-repo/scripts/factory-launcher.py --mode continue --feature-id feat-first-payment
```

Только посмотреть маршрут:

```bash
python3 template-repo/scripts/factory-launcher.py --mode continue --route-only
```

## Fallback commands

Launcher не заменяет старые scripts. Эти команды остаются прямыми fallback-путями:

```bash
python3 template-repo/scripts/first-project-wizard.py
python3 template-repo/scripts/preflight-vps-check.py --project-slug my-first-service
bash template-repo/scripts/init-feature-workspace.sh --feature-id first-feature
python3 template-repo/scripts/operator-dashboard.py
```
