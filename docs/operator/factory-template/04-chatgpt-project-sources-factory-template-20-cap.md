# Инструкция для ChatGPT Project шаблона фабрики — repo-first режим

## Принцип

Для `factory-template` ChatGPT Project больше не хранит сценарии как основной источник правды.

Источник правды теперь один:

- GitHub repo `mppcoder/factory-template`

## 1. Что держать в ChatGPT Project

В ChatGPT Project нужно держать только короткую инструкцию.
Её нужно вставить именно в поле `Instructions` до первого рабочего запроса:

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

В первом substantive ответе нового task-чата обязательно сначала выведи:
1. раздел `Название чата для копирования` со stable title, который уже materialized/reserved в repo `.chatgpt/chat-handoff-index.yaml` через allocator; само значение title/blocker выведи как отдельный однострочный fenced `text` code block, чтобы ChatGPT UI показал copy button и пользователь мог скопировать его одним кликом;
2. раздел `Карточка проекта` со свежей compact card из repo dashboard.

Инвариант first substantive answer: до route receipt, анализа или handoff должен быть один из двух видимых outcomes - materialized allocation or allocator blocker.
Если точный следующий номер неизвестен или repo write не подтвержден, не придумывай его и не показывай `FT-CH-....`. Напиши: `Нужно выделить номер через repo chat-handoff-index / allocator.`
третье состояние запрещено: no allocation attempted / no blocker / answer continues.
Если ChatGPT не показал `FT-CH-....` и не показал allocator blocker, это ошибка первого ответа `allocation-not-attempted`. Останови route и запусти repo allocator или передай Codex remediation; не продолжай с примерным номером.
Если handoff не был запущен в Codex, уже записанный номер остается занятым; следующий task chat должен получить новый номер.
Если карточка недоступна, явно назови blocker, а не пропускай раздел.

Запрещено:
- отвечать до чтения главного сценария;
- пересказывать сценарии из памяти вместо чтения repo;
- описывать сценарии внутри ChatGPT Project;
- придумывать свой workflow, если маршрут уже задан в `00-master-router.md`.
- обещать auto-rename ChatGPT UI или global scan всех чатов проекта.

Главное правило:
сначала GitHub repo `mppcoder/factory-template`,
потом `template-repo/scenario-pack/00-master-router.md`,
потом выполнение маршрута из него,
и только потом ответ.
```

## 2. Где лежат сценарии

Сценарии и связанные правила должны читаться прямо из repo:

- `template-repo/scenario-pack/`
- `docs/operator/factory-template/`
- `AGENTS` / runbook / policy files
- другие канонические repo-артефакты

## 3. Что запрещено

- хранить сценарии только внутри ChatGPT Project;
- считать внешний staging-контур каноническим источником сценариев;
- отвечать по памяти без чтения repo;
- заменять `00-master-router.md` собственным workflow.

## 4. Вспомогательные export-артефакты

Repo по-прежнему может собирать export/reference packs для внутренней автоматизации, проверок и архивов.
Но ежедневная работа ChatGPT Project должна опираться на GitHub repo, а не на обязательную ручную загрузку project artifacts или внешний staging-sync.
