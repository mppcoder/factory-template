# Factory feedback

## Источник
bug-033-repo-wide-english-human-layer-residue

## Краткое описание
После исправления handoff/closeout validators в repo все еще остается английский человекочитаемый слой в широком наборе docs и исторических artifacts. Нужен явный policy split: актуальный source-facing слой исправлять сразу, historical artifacts либо нормализовать отдельной задачей, либо пометить archival exception.

## Reusable issue
Да.

## Предлагаемое правило
- Добавлен отдельный language audit validator с allowlist для technical literals и archival paths.
- В quick verify проверяется актуальный source-facing слой.
- Historical artifacts переведены в documented archival exception, если они являются evidence/legacy records, а не active source-of-truth.

## Проверка
- Repo-wide `rg` по английским headings/prose.
- Focused validation для current `.chatgpt`, scenario-pack, template docs, generated guidance.
- `python3 template-repo/scripts/validate-human-language-layer.py .` должен давать `active findings: 0`.
