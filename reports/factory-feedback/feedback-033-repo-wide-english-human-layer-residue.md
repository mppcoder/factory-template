# Factory feedback

## Источник
bug-033-repo-wide-english-human-layer-residue

## Краткое описание
После исправления handoff/closeout validators в repo все еще остается английский человекочитаемый слой в широком наборе docs и исторических artifacts. Нужен явный policy split: актуальный source-facing слой исправлять сразу, historical artifacts либо нормализовать отдельной задачей, либо пометить archival exception.

## Reusable issue
Да.

## Предлагаемое правило
- Добавить отдельный language audit validator с allowlist для technical literals и archival paths.
- В quick verify проверять актуальный source-facing слой.
- Для historical artifacts завести отдельный cleanup task или documented exception.

## Проверка
- Repo-wide `rg` по английским headings/prose.
- Focused validation для current `.chatgpt`, scenario-pack, template docs, generated guidance.
