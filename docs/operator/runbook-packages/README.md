# Пакеты ранбуков и чеклистов

Этот каталог — финальный слой пошаговых пакетов "с нуля до рабочего состояния".
Он не заменяет scenario-pack, presets или validators. Он связывает их в operator-facing маршрут.

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

## Правило финального состояния

Боевой проект в финале может быть только `greenfield-product`.
Brownfield with repo и brownfield without repo — временные entry/adoption/reconstruction paths.
Brownfield считается done только после conversion в `greenfield-product` / `greenfield-converted` или explicit documented blocker.
