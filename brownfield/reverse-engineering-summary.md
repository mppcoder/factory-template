# Сводка reverse engineering: OpenClaw+

Дата: 2026-04-26

## Что подтверждено

- Профиль field test корректен: `brownfield-without-repo`.
- Входных корня два:
  - `/root/.openclaw`
  - `/root/openclaw-plus`
- Оба корня существуют.
- Оба корня не являются git repo.
- Live runtime фактически работает: gateway/retrieval/vectorizer/gpt2giga/postgresql/nginx active и enabled.
- Package validators проходят final acceptance, но один live warning указывает на duplicated content/context bloat.

## Как выглядит система

- `/root/.openclaw` — runtime/config/state/secrets-bearing root.
- `/root/openclaw-plus` — package/overlay/docs/validators/systemd/templates/scripts root.
- `/etc/openclaw-plus.env` — secret-bearing runtime env.

## Главные риски

- naive repo import невозможен без шума и secret leakage risk.
- `.venvs/` и wrapper dependency tree занимают большую часть package root.
- backup-файлы важны как evidence, но опасны как source-of-truth без triage.
- README не отражает реальную архитектуру; evidence нужно собирать из architecture/runbooks/known-bugs/validators/runtime.

## Выполненный follow-up

- `brownfield/source-candidate-map.md` создан.
- `brownfield/reconstruction-allowlist.md` создан.
- `brownfield/reconstruction-denylist.md` создан.
- `brownfield/change-map.md` создан.

## Следующий безопасный шаг

Создать reconstruction workspace внутри выделенного project root, например `/projects/openclaw-brownfield/reconstruction/`, и собрать redacted source pack по allowlist/denylist.

Remediation runtime пока не разрешена.
