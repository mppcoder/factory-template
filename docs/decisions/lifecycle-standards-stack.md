# ADR: облегченный стек стандартов жизненного цикла

Status: accepted for template implementation.
Date: `2026-04-29`.
Parent task: `p9-lifecycle-standards-navigator`.

## Контекст

`factory-template` is both a generated-project template and a product in its own right. It already has repo-native control surfaces for task state, feature execution, parent orchestration, lifecycle dashboard, runtime/deploy readouts and software update governance.

The missing layer is a mandatory lifecycle navigator/controller that says what should be checked from idea to production use, maintenance, growth and retirement. The layer must be useful for a solo/small-company product without becoming enterprise process theatre.

## Решение

Adopt a lightweight standards stack:

- Lifecycle backbone: `ISO/IEC/IEEE 12207:2017`, selected as current baseline with `verify-current` monitoring because ISO marks it as published/current but to be revised.
- Execution rhythm: `Scrum Guide 2020` plus Kanban-lite conventions; no heavy enterprise Scrum requirement.
- Product quality: `ISO/IEC 25010:2023`.
- Secure SDLC: `NIST SP 800-218 SSDF v1.1`.
- Web security verification: `OWASP ASVS 5.0.0`.
- Accessibility/UI baseline: `WCAG 2.2`.
- Delivery/operations health: current DORA software delivery performance metrics, with legacy four-key terminology retained as fallback compatibility because DORA has evolved to a five-metric model.
- AI-specific overlay when applicable: OpenAI safety/model-spec-inspired app guardrails, prompt injection/adversarial checks, moderation where applicable, HITL for high-impact outputs, secrets/key safety.

## Почему облегченный профиль

The default profile is `solo_lightweight`: enough evidence to avoid false green and unsafe production claims, but not enough ceremony to block a single developer from moving. `commercial_production` adds stricter quality/security/accessibility/operations evidence when a project is commercial, production-critical or user-impacting. `custom` is available for regulated or unusual domains and must document deviations.

## Границы

- This is not formal certification or conformance attestation.
- Repo artifacts may say "aligned with", "mapped to" or "uses as guidance"; they must not claim ISO certification, OWASP certification, WCAG certification, NIST certification or DORA certification.
- Version changes require proposal, impact classification, user approval and template update.
- Network/live standards research is not part of quick verify. Quick verify validates freshness metadata and gates offline.
- Advisory routing text does not switch Codex model/profile/reasoning inside an already-open live session.

## Последствия

- Generated projects receive `.chatgpt/standards-gates.yaml`.
- The template receives `template-repo/standards/lifecycle-standards-registry.yaml` and `template-repo/standards/lifecycle-stage-map.yaml`.
- Lifecycle dashboard shows standards profile, required current phase standards, missing evidence, monitoring status and whether phase advancement is allowed.
- Validators block false green, false certification/compliance claims, stale current-version overclaim, production/commercial claim without production gates and AI readiness without AI safety gate.

## Карта источников

- ISO 12207: https://www.iso.org/standard/63712.html
- ISO 25010: https://www.iso.org/standard/78176.html
- Scrum Guide 2020: https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf
- NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
- OWASP ASVS releases: https://github.com/OWASP/ASVS/releases
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- DORA metrics: https://dora.dev/guides/dora-metrics/
- OpenAI agent safety: https://developers.openai.com/api/docs/guides/agent-builder-safety
- OpenAI prompt injection overview: https://openai.com/index/prompt-injections/
