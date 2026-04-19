# Boundary Actions For {{repo_name}}

## GitHub Repo

Цель: создать внешний GitHub-репозиторий для текущего состояния `{{repo_name}}`.

Где делать:

- GitHub UI

Шаги:

1. Создайте пустой репозиторий `{{repo_name}}`.
2. Не включайте auto-generated `README`, `.gitignore` и license, если хотите чистое подключение существующего локального дерева.
3. Скопируйте URL репозитория (`SSH` или `HTTPS`).

Что прислать обратно:

- URL созданного GitHub repo
- какой transport выбран: `ssh` или `https`

## Подключение Local Repo К GitHub

Цель: подключить локальный `{{root_path}}` к уже созданному GitHub repo.

Где делать:

- терминал в `{{root_path}}`

Шаги:

1. Убедитесь, что внутренний verify уже завершён.
2. Инициализируйте git только после отдельного решения о фиксации состояния.
3. Добавьте `origin` на присланный URL.
4. Выполните первый push только после review summary и вашего подтверждения.

Что прислать обратно:

- URL `origin`
- имя основной ветки, которую хотите использовать

## ChatGPT Project

Цель: создать внешний ChatGPT Project для сценарной работы по `{{repo_name}}`.

Где делать:

- ChatGPT UI

Шаги:

1. Создайте Project с названием `{{project_name}}`.
2. Не загружайте произвольные файлы вручную.
3. Используйте curated Sources pack из этого repo.

Что прислать обратно:

- подтверждение, что Project создан
- сколько Sources-слотов доступно сейчас

## Upload Curated Sources

Цель: загрузить curated Sources pack без ручного выбора файлов.

Где делать:

- терминал: `{{root_path}}`
- затем ChatGPT Project UI

Шаги:

1. В терминале запустите `bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh`.
2. Откройте каталог `{{sources_export_dir}}`.
3. Выберите один из архивов:
{{available_sources_packs_bullets}}
4. По умолчанию используйте `{{recommended_sources_pack}}`, если нет отдельной phase-specific причины взять другой pack.
5. Загрузите содержимое выбранного pack в Project Sources.
6. Если Sources уже заняты, заменяйте только целевой набор, а не смешивайте phase-specific packs.

Что прислать обратно:

- какой pack загружен
- какие файлы были заменены в Project Sources

## Upload New Incoming Archive

Цель: положить новый внешний архив в `_incoming` без смешивания с repo.

Где делать:

- VS Code / SSH file upload или другой ручной канал загрузки

Шаги:

1. Загрузите архив в `{{uploads_dir}}`.
2. Не распаковывайте архив поверх `{{root_path}}` вручную.
3. После загрузки пришлите точное имя файла.

Что прислать обратно:

- полный путь к архиву в `{{uploads_dir}}`
- кратко, что это за пакет
