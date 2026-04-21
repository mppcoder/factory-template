# Инструкция для ChatGPT Project шаблона фабрики — repo-first режим

## Принцип

Для `factory-template` ChatGPT Project больше не хранит сценарии как основной источник правды.

Источник правды теперь один:

- GitHub repo `mppcoder/factory-template`

## 1. Что держать в ChatGPT Project

В ChatGPT Project нужно держать только короткую инструкцию:

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

## 2. Где лежат сценарии

Сценарии и связанные правила должны читаться прямо из repo:

- `template-repo/scenario-pack/`
- `factory_template_only_pack/`
- `AGENTS` / runbook / policy files
- другие канонические repo-артефакты

## 3. Что запрещено

- хранить сценарии только внутри ChatGPT Project;
- считать внешний staging-контур каноническим источником сценариев;
- отвечать по памяти без чтения repo;
- заменять `00-master-router.md` собственным workflow.

## 4. Вспомогательные export-артефакты

Repo по-прежнему может собирать export/reference packs для внутренней автоматизации, проверок и архивов.
Но ежедневная работа ChatGPT Project должна опираться на GitHub repo, а не на обязательную ручную загрузку `Sources` или внешний staging-sync.
