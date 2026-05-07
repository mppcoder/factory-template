# Пакеты ранбуков и чеклистов

Этот каталог — финальный слой пошаговых пакетов "с пустого ПК до Codex takeover и рабочего состояния".
Он не заменяет scenario-pack, presets или validators. Он связывает их в operator-facing маршрут и отделяет user-only setup от automation, которую после takeover выполняет Codex.

Полная карта жизненного цикла находится в `docs/template-architecture-and-event-workflows.md#41-полный-factory-to-battle-lifecycle`.
Она связывает эти пакеты с downstream upgrade policy, factory feedback loop, ChatGPT Project границей, Codex remote execution и production runtime/deploy zone.

## Пакеты

- `01-factory-template` — развитие самого repo `factory-template` как `greenfield-product` с дополнительным `factory-producer-owned` слоем.
- `02-greenfield-product` — чистый новый боевой проект, который сразу живет как `greenfield-product`.
- `03-brownfield-with-repo-to-greenfield` — существующий repo проходит audit/adoption/conversion и становится `greenfield-product`.
- `04-brownfield-without-repo-to-greenfield` — входящие материалы без repo проходят intake/reconstruction, затем with-repo adoption/conversion и становятся `greenfield-product`.

## Как использовать

1. Прочитайте `00-package-contract.md`.
2. Выберите один пакет по реальному входу.
3. Идите по файлам пакета по порядку:
   - `01-user-runbook.md`;
   - `02-codex-runbook.md`;
   - `03-checklist.md`;
   - `04-verify.md`;
   - `05-closeout.md`.
4. Для любой новой задачи сначала все равно открывайте `template-repo/scenario-pack/00-master-router.md`.

## Сквозной lifecycle для нового боевого проекта

| Этап | Пакет/source | Каноническая граница |
| --- | --- | --- |
| Установить фабрику на VPS | `01-factory-template` и `docs/operator/beginner-first-windows-to-first-project.md` | Пользователь делает external setup до `FT-170`; дальше remote Codex clone/setup/verify/sync. |
| Создать downstream/battle repo | `02-greenfield-product` | Пользователь стартует в factory ChatGPT Project командой `новый проект`; Codex после `GF-050` создает repo/root/scaffold. |
| Создать battle ChatGPT Project | `02-greenfield-product/02-codex-runbook.md` и `05-closeout.md` | Codex готовит repo-first instruction; пользователь создает Project в ChatGPT UI и вставляет текст. |
| Разрабатывать боевой проект | `template-repo/scenario-pack/15-handoff-to-codex.md` и repo-local `.chatgpt/task-launch.yaml` | Battle ChatGPT Project готовит один handoff; Codex исполняет в remote contour. |
| Deploy на VPS | downstream deploy docs/templates и `docs/downstream-upgrade-policy.md` | Reusable deploy templates/scripts template-owned; secrets/runtime/approvals project-owned. |
| Сопровождать | downstream verify/dashboard/support artifacts | Codex выполняет internal verify/sync; external actions только при реальном UI/secret/approval blocker. |
| Вернуть learning в фабрику | GitHub issue/PR, `reports/factory-feedback/`, feedback scripts | Reusable defect/learning получает evidence, validation и ingest/triage path. |
| Обновить downstream из upstream | `docs/downstream-upgrade-policy.md`, `factory-ops` workspace pack | Dry-run preview -> safe-generated/safe-clone apply -> upgrade report -> verify -> rollback option. |

## Граница для новичка

В каждом package есть два слоя:

- `USER-ONLY SETUP`: пользователь делает внешние действия: аккаунты, GitHub connector, VPS, SSH key, Remote SSH, Codex sign in, approvals и secrets.
- `CODEX-AUTOMATION`: после remote Codex takeover Codex сам ставит packages, clone-ит repo, запускает bootstrap/verify, обновляет dashboard и делает verified sync при доступности.

Intake/questionnaire в package layer должен быть recommendation-first:

- сначала выбирается `default_decision_mode`;
- safe defaults объясняются и могут быть заменены;
- accepted defaults и overrides фиксируются в handoff/intake state;
- risky, paid, destructive, security, privacy, legal и secret-related decisions требуют explicit user confirmation.

Основные Codex contours:

- `codex-app-remote-ssh`;
- `vscode-remote-ssh-codex-extension`.

User-runbook должен остановиться на takeover point: один большой handoff вставлен в remote Codex chat/thread. Дальше пользователь не выполняет internal repo commands вручную.

## Правило финального состояния

Боевой проект в финале может быть только `greenfield-product`.
Brownfield with repo и brownfield without repo — временные entry/adoption/reconstruction paths.
Brownfield считается done только после conversion в `greenfield-product` / `greenfield-converted` или explicit documented blocker.
