# Entry Modes

## Canonical Entry Modes

Шаблон `factory-template` поддерживает 3 канонических режима запуска и сопровождения.

## Единый Sources Pack

Для generated projects используется один и тот же базовый Sources pack:

- общий `scenario-pack`, экспортируемый через `./scripts/export-sources-pack.sh .`

Различие между режимами задается не разными наборами загружаемых файлов, а через:

- `project preset`
- `change class`
- entry routing
- порядок прохождения сценариев
- обязательные стартовые артефакты

Это сделано специально, чтобы целевое состояние всех проектов на шаблоне сходилось к одному фабричному контуру и было проще обновлять шаблон в будущем.

## 1. Новый проект с нуля

- Тип контура: `greenfield`
- Типовой профиль: `product-dev`
- Когда использовать:
  когда нужно запустить новый продукт, сервис или внутренний проект с пустого старта
- Основной сценарный вход:
  после `00-master-router.md` переходите к `template-repo/scenario-pack/04-discovery-new-project.md`

## 2. Перевод на шаблон имеющегося проекта без репо

- Тип контура: `brownfield`
- Типовой профиль: `brownfield-dogfood-codex-assisted`
- Когда использовать:
  когда есть живая система, файлы, окружение или знания о продукте, но нет нормализованного рабочего repo
- Основной сценарный вход:
  после `00-master-router.md` переходите к `template-repo/scenario-pack/brownfield/00-brownfield-entry.md`
- Особенность:
  сначала идёт evidence-first и stabilization flow, а не притворство, что полноценный repo уже существует

## 3. Перевод на шаблон имеющегося проекта с репо

- Тип контура: `brownfield`
- Типовые профили:
  - `legacy-modernization`
  - `integration-project`
  - `audit-only`
- Когда использовать:
  когда уже есть существующий репозиторий, который нужно привести к фабричному процессу и артефактному слою
- Основной сценарный вход:
  после `00-master-router.md` переходите к `template-repo/scenario-pack/brownfield/01-system-inventory.md`

## Quick Mapping

- новый проект с нуля -> `greenfield` -> `product-dev`
- существующий проект без repo -> `brownfield` -> `brownfield-dogfood-codex-assisted`
- существующий проект с repo -> `brownfield` -> `legacy-modernization` / `integration-project` / `audit-only`
