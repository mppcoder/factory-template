# Guided launcher / управляемый launcher

Единый beginner-first вход:

```bash
python3 template-repo/scripts/factory-launcher.py --guided
```

`--guided` ведет по полному пути первого проекта:

1. выбрать режим;
2. запустить preflight: короткую проверку окружения перед созданием проекта;
3. создать проект;
4. проверить `project-knowledge` - папку для устойчивых знаний о проекте;
5. создать workspace первой задачи;
6. показать следующий шаг оператора;
7. по желанию запустить безопасный deploy dry-run.

Без параметров launcher задает простые вопросы и ведет по одному из трех маршрутов:

1. `greenfield` - новый проект с нуля.
2. `brownfield` - существующий проект или система.
3. `continue` - уже созданный flow, workspace задачи или следующий шаг оператора.

## Быстрый greenfield start

```bash
python3 template-repo/scripts/factory-launcher.py \
  --mode greenfield \
  --project-name "My First Service" \
  --project-slug my-first-service \
  --guided
```

Что происходит:
- launcher выбирает `greenfield-product`;
- показывает рекомендацию следующего шага;
- вызывает существующий `first-project-wizard.py`;
- wizard запускает `preflight-vps-check.py`;
- проект создается через прежний `template-repo/launcher.sh`.
- launcher создает workspace первой задачи и показывает следующий шаг оператора.

Чтобы только посмотреть маршрут без создания проекта:

```bash
python3 template-repo/scripts/factory-launcher.py --mode greenfield --project-name "My First Service" --project-slug my-first-service --route-only
```

## Brownfield start / старт brownfield

```bash
python3 template-repo/scripts/factory-launcher.py \
  --mode brownfield \
  --brownfield-kind modernize \
  --project-name "Legacy Service" \
  --project-slug legacy-service \
  --guided
```

Доступные `--brownfield-kind`:
- `modernize` -> `brownfield-with-repo-modernization`;
- `integrate` -> `brownfield-with-repo-integration`;
- `audit` -> `brownfield-with-repo-audit`;
- `no-repo` -> `brownfield-without-repo`.

## Продолжить существующий flow

Показать рекомендацию оператора:

```bash
python3 template-repo/scripts/factory-launcher.py --continue
```

Создать workspace следующей задачи и затем показать статус оператора:

```bash
python3 template-repo/scripts/factory-launcher.py --continue --feature-id feat-first-payment
```

Показать только статус и следующий шаг:

```bash
python3 template-repo/scripts/factory-launcher.py --status
```

Запустить безопасный deploy dry-run из continue-flow:

```bash
python3 template-repo/scripts/factory-launcher.py --continue --run-dry-run
```

Только посмотреть маршрут:

```bash
python3 template-repo/scripts/factory-launcher.py --mode continue --route-only
```

## Fallback commands / fallback-команды

Launcher не заменяет старые scripts. Эти команды остаются прямыми fallback-путями:

```bash
python3 template-repo/scripts/first-project-wizard.py
python3 template-repo/scripts/preflight-vps-check.py --project-slug my-first-service
bash template-repo/scripts/init-feature-workspace.sh --feature-id first-feature
python3 template-repo/scripts/operator-dashboard.py
```
