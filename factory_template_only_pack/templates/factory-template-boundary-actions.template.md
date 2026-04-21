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

## Completion package для source-update changes

Если completed change затрагивает downstream-consumed template content, финальный boundary output должен содержать:

1. Что изменено
2. Какие файлы обновлены в repo
3. Нужно ли обновлять Sources factory-template ChatGPT Project
4. Нужно ли обновлять downstream template in battle repos
5. Нужно ли обновлять Sources battle ChatGPT Projects
6. Готовые артефакты для скачивания
7. Команды/скрипты для repo-level sync
8. Удалить перед заменой
9. Пошаговая инструкция по окнам
10. Что прислать обратно после внешнего шага

Контуры, которые нужно различать явно:

- Обновление Sources проекта шаблона в ChatGPT
- Обновление шаблона в боевых repo
- Обновление Sources боевых ChatGPT Projects

Если contour не затронут, это нужно написать явно.

### Удалить перед заменой

Если replacement может создать stale duplicates, перечислите точные файлы и архивы, которые нужно удалить из Sources до загрузки новых.

### Готовые артефакты для скачивания

- generated каталоги и архивы из `{{sources_export_dir}}`
- direct hot-set `{{canonical_direct_profile}}` в одной flat-папке без подпапок
- cold archive `{{canonical_cold_archive_pack}}`
- canonical archive `{{canonical_archive_pack}}`
- downstream patch bundle через `{{repo_patch_export_script}}`

### Команды/скрипты для repo-level sync

- `bash EXPORT_FACTORY_TEMPLATE_SOURCES.sh` — выполняет Codex внутри repo до выдачи финального completion package
- `{{repo_patch_export_script}}`
- `{{repo_patch_apply_script}}`

### Пошаговая инструкция по окнам

- VS Code Explorer — открыть каталог с уже подготовленными export/patch артефактами
- VS Code Terminal — только если нужен внешний repo-level sync в downstream repo; внутренние prepare-команды Codex выполняет сам
- ChatGPT Project → Sources — удалить старые Sources и загрузить новые
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
2. Не загружайте произвольные файлы вручную.
3. Используйте curated Sources pack из этого repo.

Что прислать обратно:

- подтверждение, что Project создан
- сколько Sources-слотов доступно сейчас

### Upload Curated Sources

Цель: использовать штатную hybrid-схему `direct hot-set + cold archive remainder + canonical archive` без ручной догадки по составу.

Где делать:

- VS Code Explorer: `{{sources_export_dir}}`
- затем ChatGPT Project UI

Шаги:

1. Откройте каталог `{{sources_export_dir}}` с уже подготовленными артефактами.
3. Для ежедневной постоянной работы используйте direct profile `{{canonical_direct_profile}}`.
4. Загрузите в ChatGPT Project напрямую файлы из flat-папки `{{direct_sources_dir}}`; подпапок внутри hot-set быть не должно.
5. Загрузите `{{canonical_cold_archive_pack}}` как cold/reference archive remainder без дублей hot-set.
6. Canonical archive pack `{{canonical_archive_pack}}` держите как полный steady-work snapshot и резервный reference bundle.
7. Для автоматически определенной фазы `{{current_phase}}` используйте phase-aware archive recommendation ниже, если нужен operator override.
   Причина: `{{phase_detection_reason}}`
{{phase_recommendations_bullets}}
8. Phase-specific archive override выбирайте только при отдельной фазовой причине:
{{phase_override_packs_bullets}}
9. По умолчанию archive override не нужен: для steady-state работы достаточно `{{canonical_direct_profile}}` + `{{canonical_cold_archive_pack}}`, а canonical archive остаётся reference snapshot. Если всё же нужен один archive pack по умолчанию, используйте `{{recommended_sources_pack}}`.
10. Если Sources уже заняты, держите один постоянный direct hot-set и один cold/reference remainder archive, а phase-specific archive pack не смешивайте с ними как второй постоянный набор.

Что прислать обратно:

- что загружено как постоянный direct hot-set
- нужен ли phase-specific archive override

### Upload New Incoming Archive

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
