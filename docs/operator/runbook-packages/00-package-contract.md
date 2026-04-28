# Контракт слоя пакетов ранбуков

## Источники истины

Executable routing остается в:

- `template-repo/codex-routing.yaml`;
- `.codex/config.toml`;
- `template-repo/scripts/resolve-codex-task-route.py`;
- `template-repo/scripts/launch-codex-task.sh`;
- `template-repo/scripts/orchestrate-codex-handoff.py`.

Advisory/policy layer остается в:

- `AGENTS.md`;
- `template-repo/scenario-pack/`;
- `docs/operator/`;
- `.chatgpt/*`;
- release-facing docs.

Runbook packages не переключают модель, профиль или reasoning внутри уже открытой сессии. Надежная routing boundary — новый task launch; user-facing default для VS Code Codex extension — новый чат/окно, ручной picker, затем один handoff block.
Brownfield здесь всегда означает временный adoption/reconstruction path, а не финальный класс проекта.

## Окна и границы

Каждый пакет обязан явно разделять:

- Browser ChatGPT Project;
- VS Code Remote SSH на VPS;
- Codex extension / Codex chat;
- Terminal only fallback;
- GitHub UI / external UI;
- secrets и external approvals.

## Финальные состояния

- `factory-template`: `greenfield-product` + `factory-producer-owned` layer.
- `greenfield-product`: active project root, lifecycle `greenfield-active` или после adoption `greenfield-converted`.
- `brownfield with repo`: transitional state до conversion или documented blocker.
- `brownfield without repo`: intake/reconstruction path; temporary/reconstructed/intermediate repos живут только внутри target project root, не siblings в `/projects`.

## Обязательные гейты

- master router прочитан из repo;
- выбран entry package;
- handoff содержит `Язык ответа Codex: русский`;
- one-paste handoff не заменяется ссылкой на файл;
- commands из verify layer существуют;
- brownfield done требует conversion или explicit blocker;
- transitional materials после conversion архивированы, переименованы или перенесены так, чтобы не путаться с active greenfield root;
- dashboard показывает phase, gates, blockers и next action.
