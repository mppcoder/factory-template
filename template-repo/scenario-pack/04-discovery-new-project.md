# Исследование нового проекта (discovery)

Цель: понять, что создается, для кого, с какими ограничениями и каким будет первый полезный результат.

## Слой решений по умолчанию

Перед основным опросом выбери режим:

```text
Использовать рекомендуемые решения по умолчанию на основе лучших доступных практик, концепции и масштаба проекта?

- Да, используй рекомендуемые решения по умолчанию; спрашивай меня только там, где реально нужен мой выбор.
- Нет, подтверждай каждое рекомендуемое решение отдельно.
- Я хочу задавать свои решения вручную.
```

Если выбран `global-defaults`, принимай safe defaults и спрашивай только decisions_requiring_user_confirmation. Если выбран `confirm-each-default`, используй per-question-default mode. Если выбран `manual`, всё равно показывай safe recommendation как подсказку, но не записывай ее в accepted defaults без ответа пользователя.

## Формат вопросов

Каждый вопрос, где safe default существует, задавай recommendation-first:

```text
Вопрос: Где создать репозиторий?
Рекомендация по умолчанию: GitHub repo в аккаунте пользователя, slug из названия проекта.
Почему: это соответствует repo-first flow фабрики и позволяет Codex создать repo/origin/first push.
Ответ:
- Enter / "по умолчанию" — принять рекомендацию;
- или напишите свой вариант.
```

Blank expert-only questions are forbidden if safe defaults exist. Default must be explainable and overrideable.

## Что собрать
- цель проекта;
- целевую аудиторию;
- ограничения;
- первый релиз или первую поставку.

## Рекомендации greenfield

- название проекта: пользовательское, без default кроме подсказки;
- slug/repo name: recommended default из названия проекта по naming rules;
- GitHub repo visibility: recommended default `private`, если пользователь не просит public/open-source;
- VPS root path: recommended default `/projects/<slug>`;
- starter preset: recommended default `starter` / minimal production-ready baseline;
- Codex contour: recommended default `vscode-remote-ssh-codex-extension`, fallback `codex-app-remote-ssh`;
- verification mode: recommended default `quick`, `full` только для release/deploy/matrix contour;
- ChatGPT Project instruction: Codex готовит default text после automation.

## Состояние intake

Сохраняй в generated intake/session artifacts и handoff:

- `default_decision_mode`;
- `accepted_defaults`;
- `overridden_defaults`;
- `default_source_basis`;
- `uncertainty_notes`;
- `decisions_requiring_user_confirmation`.

Risky, paid, destructive, security, privacy, legal и secret-related decisions требуют explicit user confirmation и не silently default.
