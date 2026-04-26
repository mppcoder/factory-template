# FEEDBACK-036: Brownfield no-repo pass criteria должны требовать repo creation или явный blocker

Дата: 2026-04-26

## Наблюдение

`brownfield-without-repo` может пройти audit и evidence capture, но не должен считаться field-passed, если нет одного из двух результатов:

- создан project repo;
- зафиксирован явный blocker, почему repo пока создать нельзя.

## Почему это важно

Для brownfield без repo ключевой transition result — появление безопасной repo boundary. Иначе сценарий завершает только диагностику и оставляет основную migration работу оператору.

## Рекомендуемое правило для шаблона

FP-02 / brownfield no-repo closeout должен проверять:

- repo path создан вне runtime roots;
- source layer перенесен по allowlist;
- denylist применен;
- secrets/runtime state не перенесены;
- commit hash или explicit blocker зафиксирован в evidence.

## Current remediation

В текущем field run создан локальный repo:

```text
/projects/openclaw-brownfield
```

Первый commit:

```text
4a58c8d Initial sanitized OpenClaw brownfield repo
```

## Status

Captured; remediation выполнена в текущем field run.

