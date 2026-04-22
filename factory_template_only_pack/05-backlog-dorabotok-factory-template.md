# Backlog доработок — только для factory-template

## Цель

Ниже — список улучшений именно для самого шаблона фабрики, без боевых контуров.

---

## 1. Стабилизировать export/reference packs

Нужно сделать штатные curated exports:

- `sources-pack-core-20/`
- `sources-pack-release-20/`
- `sources-pack-bugfix-20/`

Чтобы пользователь не собирал reference/export набор вручную.

Статус:

- базовые curated packs для самого `factory-template` уже автоматизированы через `EXPORT_FACTORY_TEMPLATE_SOURCES.sh`
- состав pack'ов вынесен в декларативный `factory-template-ops-policy.yaml`
- добавлен validator не только на pack composition, но и на semantic profile `core / release / bugfix`
- `sources-pack-release-20` теперь несет release-facing docs вместо временных audit/backlog файлов
- `sources-pack-bugfix-20` теперь включает handoff/feedback validators
- добавлена phase-aware recommendation matrix для `controlled-fixes / release / bugfix-drift`
- добавлен automatic state detection по changed paths вместо ручного `current_phase`
- для `release` добавлены document intent signals через `RELEASE_CHECKLIST.md`, чтобы не ловить ложные release-switch
- для `bugfix-drift` добавлены document intent signals через `reports/bugs/*.md`
- добавлен synthetic self-test `PHASE_DETECTION_TEST.sh` для automatic phase detection
- дальше можно расширять фазовые policy manifests и делать более глубокий intent detection поверх git/release state

---

## 2. Усилить codex task pack

Нужно добавить более явные артефакты:

- `codex-context.md`
- `codex-input.md`
- `codex-task-pack.md`
- `boundary-actions.md`

Цель: сделать handoff в Codex всегда одинаковым и воспроизводимым.

Статус:

- `create-codex-task-pack.py` уже собирает `codex-context.md`, `codex-task-pack.md`, `done-checklist.md`
- добавлена автоматическая генерация `.chatgpt/boundary-actions.md`
- добавлен validator `template-repo/scripts/validate-codex-task-pack.py` для semantic-проверки handoff contents
- исправлена синхронизация route line с `active-scenarios.yaml`
- дальше можно усиливать качество самого `classification.md` / `codex-input.md`, а не только generated pack

---

## 3. Добавить boundary-action generator

Фабрика должна уметь генерировать инструкции пользователю на внешние действия:

- создать GitHub repo;
- подключить репозиторий;
- создать ChatGPT Project;
- обновить repo-first инструкцию в ChatGPT Project;
- загрузить новый архив в `_incoming`.

Статус:

- базовый generator уже автоматизирован через `GENERATE_BOUNDARY_ACTIONS.sh`
- текст generator вынесен в шаблон `factory_template_only_pack/templates/factory-template-boundary-actions.template.md`
- дальше можно сделать phase-aware инструкции и привязку к конкретному release/pack

---

## 4. Выравнять docs ↔ scripts ↔ validators

Нужен регулярный контроль на рассогласования между:

- runbook;
- launcher;
- scripts;
- validators;
- examples;
- `.chatgpt/`.

---

## 5. Выделить release layer

Нужно явнее оформить release-контур шаблона:

- release checklist;
- release verify pack;
- release note template;
- bundle manifest.

Статус:

- добавлены operator-facing `RELEASE_CHECKLIST.md` и `VERIFY_SUMMARY.md`
- добавлен базовый `RELEASE_NOTE_TEMPLATE.md`
- дальше можно собрать phase-specific release verify pack

---

## 6. Встроить routing rules для профилей Codex

Минимум:

- `default-dev`
- `fast-routine`
- `heavy-analysis`
- `release-verify`

Пока достаточно как правил в `AGENTS.md` + примера `.codex/config.toml`.

---

## 7. Отдельный feedback ingestion layer

Нужно стандартизовать, как feedback из dogfood/боевых проектов возвращается обратно в шаблон:

- bug report into template;
- feature extraction into template;
- scenario correction into template;
- validator correction into template.

Статус:

- добавлен базовый ingestion script `INGEST_FACTORY_FEEDBACK.sh`
- feedback из working project можно перенести в `meta-template-project/incoming-learnings/`
- добавлен dry-run triage script `TRIAGE_INCOMING_LEARNINGS.sh`
- добавлен validator `VALIDATE_FACTORY_FEEDBACK.sh` для качества `meta-feedback`
- дальше можно усиливать semantic validation и автоматическую запись в backlog / accepted / rejected
