# Режимы входа

## Канонические режимы входа

Шаблон `factory-template` поддерживает 3 канонических режима запуска и сопровождения.

Для одной визуальной схемы шаблона и подробных workflows по событиям запуска/развертывания/доработки смотрите:

- `docs/template-architecture-and-event-workflows.md`

## Единый Repo-First Contour

Для generated projects используется один и тот же базовый repo-first контур:

- общий `scenario-pack` в repo, который читается напрямую из GitHub

Различие между режимами задается не разными наборами загружаемых файлов, а через:

- `project preset`
- `change class`
- entry routing
- порядок прохождения сценариев
- обязательные стартовые артефакты

Это сделано специально, чтобы целевое состояние всех проектов на шаблоне сходилось к одному фабричному контуру и было проще обновлять шаблон в будущем.

## Каноническая VPS layout

- `/projects` содержит только project roots;
- у каждого проекта свой корень: `/projects/<project-root>/`;
- `_incoming` допускается только как подпапка проекта;
- brownfield temporary/intermediate/reconstructed/helper repos должны жить только внутри repo целевого `greenfield-product`, например `/projects/<target-greenfield-project>/...`, а не соседями в `/projects`.

## 1. Новый проект с нуля

- Тип контура: `greenfield`
- Типовой профиль: `greenfield-product`
- Когда использовать:
  когда нужно запустить новый продукт, сервис или внутренний проект с пустого старта
- Основной сценарный вход:
  после `00-master-router.md` переходите к `template-repo/scenario-pack/04-discovery-new-project.md`

## 2. Перевод на шаблон имеющегося проекта без репо

- Тип контура: `brownfield`
- Типовой профиль: `brownfield-without-repo`
- Когда использовать:
  когда есть живая система, файлы, окружение или знания о продукте, но нет нормализованного рабочего repo
- Основной сценарный вход:
  после `00-master-router.md` переходите к `template-repo/scenario-pack/brownfield/00-brownfield-entry.md`
- Особенность:
  сначала идёт evidence-first и stabilization flow, а не притворство, что полноценный repo уже существует

## 3. Перевод на шаблон имеющегося проекта с репо

- Тип контура: `brownfield`
- Типовые профили:
  - `brownfield-with-repo-modernization`
  - `brownfield-with-repo-integration`
  - `brownfield-with-repo-audit`
- Когда использовать:
  когда уже есть существующий репозиторий, который нужно привести к фабричному процессу и артефактному слою
- Основной сценарный вход:
  после `00-master-router.md` сначала переходите к `template-repo/scenario-pack/brownfield/00-brownfield-entry.md`, затем к `template-repo/scenario-pack/brownfield/01-system-inventory.md`
- Зачем нужен `brownfield/00-brownfield-entry.md`:
  это короткий brownfield gate, который фиксирует правило evidence-first даже если репозиторий уже существует

## Быстрая mapping

- новый проект с нуля -> `greenfield` -> `greenfield-product`
- существующий проект без repo -> `brownfield` -> `brownfield-without-repo`
- существующий проект с repo -> `brownfield` -> `brownfield-with-repo-modernization` / `brownfield-with-repo-integration` / `brownfield-with-repo-audit`

## Compatibility aliases / слой совместимости

Старые preset names не являются beginner UX и не перечисляются как нормальные варианты выбора.
Они принимаются только как compatibility input для существующих запусков через:

- `template-repo/compatibility-aliases.yaml`

Новые инструкции, handoff и onboarding должны использовать только canonical modes и presets из разделов выше.
