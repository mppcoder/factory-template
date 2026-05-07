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
  --project-name "Мой первый проект!!!" \
  --guided
```

Что происходит:
- launcher выбирает `greenfield-product`;
- генерирует `project_slug` `moy-pervyy-proekt` из human-readable `project_name`;
- выделяет один `PROJECT_CODE` для проекта и записывает его в repo-local identity;
- показывает рекомендацию следующего шага;
- вызывает существующий `first-project-wizard.py`;
- wizard запускает `preflight-vps-check.py`;
- проект создается через прежний `template-repo/launcher.sh`.
- launcher создает workspace первой задачи и показывает следующий шаг оператора.

Чтобы только посмотреть маршрут без создания проекта:

```bash
python3 template-repo/scripts/factory-launcher.py --mode greenfield --project-name "AI Factory" --route-only
```

Naming examples:

- `Краб — CRM для ремонта` -> `krab-crm-remonta`;
- `AI Factory` -> `ai-factory`;
- `Мой первый проект!!!` -> `moy-pervyy-proekt`.

`project_name` остается свободным human-readable названием. `project_slug` используется для local repo path, GitHub repo name, registry и `project-origin`. Empty slug и reserved/generic slugs блокируются без явного override.

`PROJECT_CODE` выбирается один раз при создании проекта. По умолчанию launcher генерирует uppercase code из `project_slug`, например `moy-pervyy-proekt` -> `MPP`; его можно явно передать через `--project-code`. Этот code становится префиксом repo-local пространств:
- ChatGPT handoff ids: `<PROJECT_CODE>-CH-<NNNN>`;
- Codex work ids: `<PROJECT_CODE>-CX-<NNNN>`;
- universal task ids: `<PROJECT_CODE>-TASK-<NNNN>`.

При создании проекта `.chatgpt/chat-handoff-index.yaml` и `.chatgpt/codex-work-index.yaml` генерируются локально: `project_code` заменяется на выбранный `PROJECT_CODE`, counters CH и CX независимо сбрасываются на `1`, `items: []` остается пустым. Factory-template `FT`-нумерация не переносится в downstream-проекты.

Проверка identity:

```bash
python3 scripts/validate-project-index-identity.py .
```

## Brownfield start / старт brownfield

```bash
python3 template-repo/scripts/factory-launcher.py \
  --mode brownfield \
  --brownfield-kind modernize \
  --project-name "Legacy Service" \
  --guided
```

Brownfield final repo naming follows the target product slug. Launcher не добавляет `-brownfield` или `-greenfield` автоматически; temporary/reconstructed/helper repos должны находиться внутри `/projects/<project_slug>/...`, а не sibling roots под `/projects`.

## Создание GitHub repo

Local repo basename и GitHub repo name должны совпадать с `project_slug` exactly.

```bash
python3 template-repo/scripts/factory-launcher.py \
  --mode greenfield \
  --project-name "AI Factory" \
  --create-github-repo \
  --github-owner mppcoder \
  --guided
```

GitHub repo создается как `<github_owner>/<project_slug>` с default visibility `private`. Если `--github-owner` не задан, launcher может использовать authenticated `gh` user только когда owner однозначен. Existing repo можно использовать только после явного подтверждения через `--reuse-existing-github-repo` или interactive confirmation. Launcher не добавляет suffixes вроде `-2`, `-copy`, date или random string.

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
