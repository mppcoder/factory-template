# Политика человекочитаемого языка

Для `factory-template` основной человекочитаемый слой ведется на русском языке.

## Активный source-facing слой

К активному source-facing слою относятся:

- `README.md`, `CURRENT_FUNCTIONAL_STATE.md`, `AGENTS.md`;
- `docs/`, `template-repo/README.md`, `template-repo/AGENTS.md`;
- `template-repo/scenario-pack/`, `template-repo/template/docs/`;
- reusable skills в `template-repo/skills/`;
- `.chatgpt` handoff/closeout artifacts, если они обновляются текущей задачей;
- release-facing checklist/report files, которые используются как актуальные operator docs.

Правило: заголовки и инструкции пишутся по-русски. Английский допустим как technical literal: команды, пути, YAML/JSON keys, model IDs, product names, established repo terms (`repo-first`, `handoff`, `routing`, `validator`, `release`, `apply`, `preview`) и цитаты внешних интерфейсов.

## Archival exceptions / архивные исключения

Исторические reports, старые `work/completed`, legacy packs и fixture evidence не переводятся массово задним числом. Они являются evidence records, поэтому сохраняют исходный текст, но должны быть перечислены в `template-repo/language-archive-exceptions.yaml`.

Если архивный файл снова становится активным source-of-truth, его нужно вывести из exception list и нормализовать.

## Validator / проверка

Проверка выполняется командой:

```bash
python3 template-repo/scripts/validate-human-language-layer.py .
```

Validator fails для английских человекочитаемых headings в active source-facing слое и отдельно сообщает количество совпадений внутри documented archival exceptions.
