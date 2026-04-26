# Boundary Actions For {{repo_name}}

## Инструкция пользователю

Используйте этот блок только для реальных внешних границ.
Internal repo follow-up, включая release-followup, source-pack refresh, export refresh, closeout-sync и release-facing consistency pass внутри repo, остается работой Codex и не должен вытесняться этим footer.

## Модель воздействия

- `impact.factory_sources` — {{impact_factory_sources}}
- `impact.downstream_template_sync` — {{impact_downstream_template_sync}}
- `impact.downstream_project_sources` — {{impact_downstream_project_sources}}
- `impact.manual_archive_required` — {{impact_manual_archive_required}}
- `impact.delete_before_replace` — {{impact_delete_before_replace}}

## Completion package для repo-first instruction changes

Этот раздел описывает обновление repo-first instruction changes.

Если completed change затрагивает downstream-consumed template content, финальный boundary output должен содержать:

1. Что изменено
2. Какие файлы обновлены в repo
3. Нужно ли обновлять repo-first инструкцию factory-template ChatGPT Project
4. Нужно ли обновлять downstream template in battle repos
5. Нужно ли обновлять repo-first инструкции battle ChatGPT Projects
6. Готовые артефакты для скачивания
7. Команды/скрипты для repo-level sync
8. Удалить перед заменой
9. Пошаговая инструкция по окнам
10. Что прислать обратно после внешнего шага

Отдельно обязателен подраздел `Рекомендация по внешним действиям`.
В нем для каждого внешнего contour нужно явно указать:
- `Рекомендация`: `требуется`, `рекомендуется`, `не требуется`, `опционально` или `только legacy/hybrid fallback`;
- `Причина`: почему именно такой статус;
- `Действие пользователя`: точная команда, UI-шаг или фраза `действие не требуется`.

Минимальный набор contour'ов:
- `factory-template ChatGPT Project instructions`;
- `downstream/battle repo sync`;
- `downstream/battle ChatGPT Project instructions`;
- `Sources fallback`.

Контуры, которые нужно различать явно:

- Обновление repo-first инструкции проекта шаблона в ChatGPT
- Обновление шаблона в боевых repo
- Обновление repo-first инструкции боевых ChatGPT Projects

Если contour не затронут, это нужно написать явно.

### Удалить перед заменой

Если replacement может создать конфликтующий старый текст, перечислите точные инструкции или файлы, которые нужно удалить перед заменой.

### Готовые артефакты для скачивания

- готовый текст repo-first инструкции для ChatGPT Project
- downstream patch bundle через `{{repo_patch_export_script}}`
- reference export dir: `{{sources_export_dir}}`
- canonical archive pack: `{{canonical_archive_pack}}`
- cold archive pack: `{{canonical_cold_archive_pack}}`
- direct profile: `{{canonical_direct_profile}}`
- direct profile dir: `{{direct_sources_dir}}`
- recommended pack: `{{recommended_sources_pack}}`

Важно:
- эти export/reference артефакты не означают обязательный шаг обновления `Sources`;
- по умолчанию ChatGPT Project должен работать напрямую с GitHub repo;
- используйте packs и direct profile только как optional compatibility fallback для legacy/hybrid Projects.

### Команды/скрипты для repo-level sync

- `{{repo_patch_export_script}}`
- `{{repo_patch_apply_script}}`

Для repo-first instruction layer downstream repo:
- source-of-truth: `template-repo/AGENTS.md`
- materialized clone: root `AGENTS.md` боевого repo
- после штатного sync/update flow Codex в battle repo должен читать именно root `AGENTS.md`

### Ограничение repo-first режима

- ChatGPT Project не должен хранить сценарии как source of truth
- сначала всегда читается GitHub repo, потом `00-master-router.md`
- старые инструкции про project artifacts и старый staging-workflow нужно удалять, если они конфликтуют с новым правилом
- не предлагайте refresh `Sources` как обязательный шаг после релиза, если project уже работает в repo-first режиме
- текущая phase recommendation: `{{current_phase}}`
- phase detection reason: `{{phase_detection_reason}}`
- phase recommendations:
{{phase_recommendations_bullets}}
- phase override packs:
{{phase_override_packs_bullets}}

### Пошаговая инструкция по окнам

- VS Code Explorer — открыть каталог с уже подготовленными export/patch артефактами
- VS Code Terminal — только если нужен внешний repo-level sync в downstream repo; внутренние prepare-команды Codex выполняет сам
- ChatGPT Project UI — заменить старую инструкцию на новую repo-first версию
- GitHub/repo window — выполнить review commit/push, если это действительно внешний шаг

### GitHub Repo

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

### Подключение Local Repo К GitHub

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

### ChatGPT Project

Цель: создать внешний ChatGPT Project для сценарной работы по `{{repo_name}}`.

Где делать:

- ChatGPT UI

Шаги:

1. Создайте Project с названием `{{project_name}}`.
2. Не храните сценарии внутри Project как основной источник правды.
3. Вставьте repo-first инструкцию из этого repo.

Что прислать обратно:

- подтверждение, что Project создан
- подтверждение, что repo-first инструкция вставлена

### Update Repo-First Instruction

Цель: обновить инструкцию в ChatGPT Project так, чтобы сценарии читались прямо из GitHub repo.

Где делать:

- ChatGPT Project UI

Шаги:

1. Откройте текущие инструкции проекта.
2. Удалите старый текст про project artifacts, upload packs и staging-workflow, если он конфликтует с новым правилом.
3. Вставьте новую repo-first инструкцию, подготовленную Codex.
4. Проверьте, что в инструкции явно указан repo `{{repo_name}}` и путь `template-repo/scenario-pack/00-master-router.md`.

Что прислать обратно:

- подтверждение, что старая инструкция удалена
- подтверждение, что новая repo-first инструкция сохранена

### Upload New Incoming Archive

Цель: положить новый внешний архив в project-local `_incoming` без смешивания с другими project roots.

Где делать:

- VS Code / SSH file upload или другой ручной канал загрузки

Шаги:

1. Загрузите архив в `{{uploads_dir}}`.
2. Не распаковывайте архив поверх `{{root_path}}` вручную.
3. После загрузки пришлите точное имя файла.
4. Не создавайте ради этого отдельную верхнеуровневую папку в `/projects`: в корне `/projects` должны оставаться только project roots.

Что прислать обратно:

- полный путь к архиву в `{{uploads_dir}}`
- кратко, что это за пакет
