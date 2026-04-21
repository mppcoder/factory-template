# Repo-First Strategy For ChatGPT Projects

## Canonical Rule

Для `factory-template` ChatGPT Project больше не должен хранить сценарии как основной источник правды.

Канонический workflow теперь такой:

1. ChatGPT Project содержит только короткую repo-first инструкцию.
2. На каждый запрос сначала открывается GitHub repo проекта.
3. Первое обязательное действие: открыть `template-repo/scenario-pack/00-master-router.md`.
4. Прочитать `00-master-router.md` и действовать строго по нему.
5. Если router направляет в другие сценарии, читать уже их.
6. Только после этого формировать ответ.

## Canonical Instruction Text

```text
Работаем по проекту factory-template.

В этом ChatGPT Project сценарии не хранятся.
На каждый запрос сначала иди в GitHub repo `mppcoder/factory-template`.

Первое обязательное действие на каждый запрос:
1. открыть главный сценарий `template-repo/scenario-pack/00-master-router.md`;
2. прочитать его;
3. действовать строго по нему;
4. если главный сценарий направляет в другие сценарии, читать и исполнять уже их;
5. только после этого формировать ответ.

Запрещено:
- отвечать до чтения главного сценария;
- пересказывать сценарии из памяти вместо чтения repo;
- описывать сценарии внутри ChatGPT Project;
- придумывать свой workflow, если маршрут уже задан в `00-master-router.md`.

Главное правило:
сначала GitHub repo `mppcoder/factory-template`,
потом `template-repo/scenario-pack/00-master-router.md`,
потом выполнение маршрута из него,
и только потом ответ.
```

## What Stays In Repo

Source of truth остаётся в GitHub repo:

- `template-repo/scenario-pack/`
- `factory_template_only_pack/`
- `AGENTS` / runbook / policy files
- остальные канонические repo-артефакты

Export packs можно оставлять как вспомогательный reference/export слой, но не как обязательный ежедневный источник сценариев для ChatGPT Project.
