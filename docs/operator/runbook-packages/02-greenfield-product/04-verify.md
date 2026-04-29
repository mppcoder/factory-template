# Проверка: greenfield-product

Package layer должен содержать `USER-ONLY SETUP`, `CODEX-AUTOMATION`, takeover point и beginner step cards.

## Проверка ChatGPT intake

- старт был в ChatGPT Project шаблона фабрики `factory-template`;
- пользователь открыл новый чат внутри этого Project;
- пользователь ввел команду:

```text
новый проект
```

- ChatGPT Project сначала прочитал `template-repo/scenario-pack/00-master-router.md`;
- handoff создан после опроса, а не из raw Codex prompt;
- default decision mode selected до основного опроса: `global-defaults`, `confirm-each-default` или `manual`;
- опрос recommendation-first: safe defaults explainable and overrideable, без blank expert-only questions там, где default должен существовать;
- опрос собрал:
  - project name;
  - slug proposal или правило slug generation;
  - краткую идею;
  - тип проекта;
  - readiness state;
  - выбранный Codex contour;
  - blockers.
- handoff содержит:
  - `default_decision_mode`;
  - accepted defaults;
  - overrides;
  - unresolved decisions/blockers;
  - no hidden forced defaults for risky actions.
- handoff содержит boundary: GitHub repo/root/verify/sync делает Codex;
- пользовательские external actions ограничены factory ChatGPT intake, вставкой handoff в Codex, созданием battle ChatGPT Project, открытием Project settings/instructions, вставкой готовой instruction и сохранением настроек.

## Проверка Codex automation после handoff

- Codex получил ChatGPT-generated handoff и вывел handoff receipt;
- Codex не проводил заново весь пользовательский опрос, если handoff уже содержит ответы;
- Codex нормализовал project slug/repo name;
- Codex создал GitHub repo или documented blocker;
- Codex создал/подготовил `/projects/<project-slug>`;
- Codex запустил wizard/launcher;
- repo-first core materialized;
- `.chatgpt`, `AGENTS`, scenario-pack, dashboard, project-knowledge созданы/обновлены;
- bootstrap/verify выполнены;
- initial commit/push/verified sync выполнены или blocker documented;
- Codex подготовил готовый текст repo-first instruction для battle ChatGPT Project;
- Codex подготовил пошаговую инструкцию пользователю, куда вставить этот текст в ChatGPT UI;
- Codex не создавал ChatGPT Project, не вставлял instruction и не сохранял настройки через browser/desktop UI automation.

## Проверка battle ChatGPT Project

- пользователь создал ChatGPT Project боевого проекта;
- пользователь открыл Project settings/instructions;
- пользователь вставил готовую repo-first instruction;
- пользователь сохранил настройки;
- проверочная формулировка соблюдена: Codex готовит repo-first instruction для боевого ChatGPT Project. Пользователь создает ChatGPT Project в UI и вставляет готовый текст.
- дальнейшие задачи идут через боевой Project, а не через factory-template Project.

## Проверка package layer из factory-template root

```bash
python3 template-repo/scripts/validate-runbook-packages.py .
```

## Проверка generated project root после materialization

```bash
python3 scripts/validate-project-preset.py .
python3 scripts/validate-greenfield-conversion.py .
python3 scripts/validate-codex-routing.py .
python3 scripts/validate-project-lifecycle-dashboard.py .chatgpt/project-lifecycle-dashboard.yaml
bash scripts/verify-all.sh quick
```
