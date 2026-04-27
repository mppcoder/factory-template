# Глоссарий

Дайте расшифровку терминов, сокращений и внутренних обозначений.

## Термины feature planning

- `user-spec` — документ о том, что хочет пользователь и как он поймёт, что результат готов.
- `tech-spec` — документ о том, как агент реализует user-spec.
- `US-*` — короткая метка пользовательского намерения, например `US-001`.
- `User Intent Binding` — связь tech-spec или task с конкретными `US-*`.
- `User-Spec Deviations` — список мест, где агент не следует исходному user-spec, с причиной и проверкой.
- `decisions.md` — журнал важных решений, deviations и verification после выполнения задач.
- `project-knowledge-update-proposal.md` — closeout-артефакт, который явно говорит, нужно ли переносить устойчивые выводы в `project-knowledge/`.
- `downstream-impact.md` — closeout-артефакт о том, затрагивает ли feature downstream sync или project-owned knowledge review.
- `Verify-smoke` — проверка, которую агент может выполнить сам.
- `Verify-user` — проверка, которую нужно показать пользователю или подтвердить вручную.
