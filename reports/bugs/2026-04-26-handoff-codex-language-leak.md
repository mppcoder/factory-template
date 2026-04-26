# Handoff and Codex replies leak English human-readable text

## Статус

зафиксировано, remediation в текущем change

## Дата

2026-04-26

## Сигнал

Пользователь сообщил: ChatGPT снова готовит handoff на английском, а ответы Codex тоже уходят на английский.

## Ожидаемое поведение

- Человекочитаемые пояснения handoff пишутся на русском.
- Handoff явно требует от Codex отвечать пользователю на русском языке.
- Английский допускается только как technical literal: команды, пути, YAML/JSON keys, model IDs, route fields и literal values.
- Если upstream input содержит английские разделы вроде `Goal`, `Hard constraints`, `Required implementation`, это считается language-contract defect и нормализуется до русского handoff.

## Фактическое поведение

- Generated `.chatgpt/handoff-response.md` использует англоязычные labels внутри copy-paste блока: `Repo`, `Entry point`, `Scope`.
- Handoff не содержит явного обязательного правила: "Codex отвечает пользователю на русском".
- `validate-handoff-response-format.py` проверяет single-block/file-based формат, но не требует русского языка ответа Codex.
- `validate-handoff-language.py` ловит часть англоязычных headings/phrases, но не проверяет обязательное наличие language contract в handoff.

## Граница ответственности

Reusable factory-template language layer: handoff generator, validators and source docs.

## Remediation

- Add mandatory Codex response language rule into generated handoff.
- Replace English human-readable labels in copy-paste handoff block with Russian labels.
- Strengthen handoff validators so the language rule is machine-checkable.
- Update language policy/docs and verification evidence.
