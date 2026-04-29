# Навигатор стандартов жизненного цикла

`standards navigator` — обязательный repo-native навигатор и контролер жизненного цикла проекта. Он отвечает на вопрос:

> что должно быть проверено на этой фазе проекта, какая evidence нужна, и можно ли безопасно двигаться дальше.

Это не сертификационный слой. Он не выдает ISO, NIST, OWASP, WCAG, DORA или OpenAI certification/compliance. Он связывает существующие repo-механизмы с практичными evidence gates.

## Как устроено

- `template-repo/standards/lifecycle-standards-registry.yaml` — machine-readable registry стандартов, профилей и source status.
- `template-repo/standards/lifecycle-stage-map.yaml` — карта фаз от idea/intake до operate, maintenance, incident response и retirement.
- `template-repo/template/.chatgpt/standards-gates.yaml` — generated-project template для evidence gates.
- `template-repo/template/.chatgpt/project-lifecycle-dashboard.yaml` — dashboard показывает standards profile, gate summary, missing evidence, monitoring status и `allowed_to_advance_phase`.
- `template-repo/scripts/validate-standards-gates.py` — блокирует false green и false compliance.
- `template-repo/scripts/check-standards-watchlist.py` — offline-first freshness/proposal check без network requirement.

## Профили

`solo_lightweight` — default для одного разработчика или маленькой команды. Требует минимум evidence: intent, requirements, quality/security/accessibility decisions, verification notes и honest accepted reasons.

`commercial_production` — включается, когда проект становится коммерческим, production-critical, публичным с uptime/user-data expectations или high-impact. Требует дополнительные gates: security review, ASVS-relevant web security, WCAG evidence, operations/DORA baseline, incident response and false compliance check.

`custom` — только через явное решение: какие standards включены/исключены, почему, кто владелец и какие gates заменяют default.

## Стек стандартов

- Lifecycle backbone: `ISO/IEC/IEEE 12207:2017`; ISO source currently marks it published/current but revision-pending, so version changes require proposal.
- Execution rhythm: `Scrum Guide 2020` plus Kanban-lite, without enterprise Scrum ceremony.
- Product quality: `ISO/IEC 25010:2023`.
- Secure SDLC: `NIST SP 800-218 SSDF v1.1`.
- Web security: `OWASP ASVS 5.0.0`.
- Accessibility/UI: `WCAG 2.2`.
- Delivery/operations: current DORA metrics, with legacy four-key terminology as compatibility fallback.
- AI overlay when applicable: OpenAI safety guidance, prompt injection checks, moderation where applicable, HITL for high-impact outputs and secrets/key safety.

## Как читать beginner status

Пример compact line:

```text
Стандарты: solo_lightweight, gates 5/8 passed; не хватает security_minimum_checked
```

Если `allowed_to_advance_phase: false`, это не значит, что работа остановлена полностью. Это значит, что следующая lifecycle phase не должна считаться пройденной, пока missing evidence не заполнена или не записан accepted reason.

## Политика drift

Любое изменение версии стандарта проходит только так:

```text
standards-update-proposal -> impact classification -> user approval -> template update
```

Quick verify не ходит в сеть и не меняет registry. Он проверяет, что watchlist свежий или честно сообщает `proposal-needed`.
