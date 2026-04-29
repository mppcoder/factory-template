# Пакеты ранбуков и чеклистов

Этот каталог — финальный слой пошаговых пакетов "с пустого ПК до Codex takeover и рабочего состояния".
Он не заменяет scenario-pack, presets или validators. Он связывает их в operator-facing маршрут и отделяет user-only setup от automation, которую после takeover выполняет Codex.

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
