# План reverse engineering: OpenClaw+

Дата: 2026-04-26

## Цель

Построить безопасную реконструкцию brownfield-системы без repo из двух корней:
- `/root/.openclaw`
- `/root/openclaw-plus`

До remediation фиксируются только факты, boundaries, gaps и source candidates.

## Фаза 1: intake / evidence freeze

Статус: started

Действия:
- подтвердить существование корней;
- подтвердить отсутствие git repo;
- снять top-level tree, sizes, file counts;
- зафиксировать активные services;
- проверить package validators без изменения runtime;
- зафиксировать secret-bearing зоны без раскрытия секретов.

Артефакты:
- `brownfield/system-inventory.md`
- `brownfield/repo-audit.md`
- `brownfield/as-is-architecture.md`
- `brownfield/gap-register.md`
- `.chatgpt/evidence-register.md`
- `.chatgpt/reality-check.md`

## Фаза 2: source candidate map

Статус: completed

Действия:
- разделить files на source / docs / config / templates / generated / runtime-state / secret-bearing;
- отдельно классифицировать backup-файлы;
- определить allowlist для reconstruction source pack;
- определить denylist для `.venvs/`, `node_modules/`, caches, pyc, sqlite runtime DB, credentials, identity, telegram state.

Ожидаемый артефакт:
- `brownfield/source-candidate-map.md`
- `brownfield/reconstruction-allowlist.md`
- `brownfield/reconstruction-denylist.md`
- `brownfield/change-map.md`

## Фаза 3: reconstruction workspace

Статус: pending

Действия:
- создать dedicated project root внутри `/projects`, не рядом с другими temporary repo;
- собрать redacted source pack;
- создать initial git repo только внутри reconstruction workspace;
- сохранить runtime evidence отдельно от source tree.

Важно:
- не создавать temporary/intermediate repo прямо в `/projects`;
- не создавать git repo в `/root/.openclaw` или `/root/openclaw-plus` на этом этапе.

## Фаза 4: traceability / risk review

Статус: pending

Действия:
- связать source candidates с docs/runbooks/validators;
- сопоставить `KNOWN-BUGS.md` с текущими backup-файлами и validators;
- оформить unresolved gaps как structured defects;
- определить, какие изменения являются package fixes, а какие runtime migration.

## Фаза 5: remediation planning

Статус: blocked until phases 1-4 complete

Правило:
- remediation запрещена до фиксации gap/defect reports и source reconstruction boundary.
