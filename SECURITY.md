# Security policy / политика безопасности

## Поддерживаемые версии

| Version line | Status |
| --- | --- |
| 2.5.x | Supported |
| 2.4.x | Security fixes only |
| < 2.4 | Not supported |

## Как сообщить об уязвимости

1. Используйте GitHub Private Vulnerability Reporting для этого repository.
2. Укажите воспроизводимые steps, affected paths и impact.
3. Не публикуйте exploit details в public issues до triage.

Если private reporting недоступен, откройте минимальный public issue без sensitive details и попросите secure follow-up channel.

Public security issue autofix refused: public issues may only trigger safe refusal and private-channel guidance. Any security fix automation requires a private report channel, explicit `security-fix` approval, sanitized handoff, no public logs and human review.

## Целевые сроки ответа

- Initial triage: в течение 3 business days.
- Status update после triage: в течение 7 business days.
- Critical/high severity fixes: приоритет для ближайшего patch window.

## Baseline обработки секретов

- Никогда не коммитьте real credentials, tokens, keys или session artifacts.
- Держите local secrets в non-committed `.env` files; используйте `.env.example` как единственный committed template.
- Никогда не вставляйте secrets в `.chatgpt/*`, bug reports, release notes или handoff artifacts.
- Для CI храните secrets только в GitHub Actions Secrets и не печатайте их в logs.
- Немедленно rotate credentials, если есть подозрение на accidental exposure.

## Coordinated disclosure / согласованное раскрытие

Security fixes должны включать:

- clear impact statement,
- verification evidence,
- release notes entry, когда применимо,
- follow-up hardening tasks для reusable defects.
