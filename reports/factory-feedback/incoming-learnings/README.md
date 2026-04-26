# Как использовать incoming-learnings

1. Зафиксируйте проблему или улучшение фабрики через шаблон:
   - `work-templates/factory-feedback/factory-bug-report.md`
   - `work-templates/factory-feedback/factory-task.md`

2. Сохраните оформленный документ в `reports/factory-feedback/incoming-learnings/`.

Или используйте автоматический ingest из working project:

```bash
cd /projects/factory-template
bash VALIDATE_FACTORY_FEEDBACK.sh /abs/path/to/working-project
bash INGEST_FACTORY_FEEDBACK.sh /abs/path/to/working-project --dry-run
bash INGEST_FACTORY_FEEDBACK.sh /abs/path/to/working-project
```

По умолчанию ingest остановится, если `factory-task.md` или `factory-bug-report.md` выглядят слишком пустыми.
Для осознанного ingest сырого feedback можно использовать:

```bash
bash INGEST_FACTORY_FEEDBACK.sh /abs/path/to/working-project --allow-incomplete
```

3. После первичной оценки перенесите результат:
   - в `project-knowledge/factory/template-evolution/FACTORY_BACKLOG.md`,
   - в `project-knowledge/factory/template-evolution/accepted-patterns/`,
   - или в `project-knowledge/factory/template-evolution/rejected-patterns/`.

Для первичной рекомендации по маршрутизации можно использовать:

```bash
cd /projects/factory-template
bash TRIAGE_INCOMING_LEARNINGS.sh --dry-run
```

Если рекомендация выглядит корректной, примените triage:

```bash
cd /projects/factory-template
bash TRIAGE_INCOMING_LEARNINGS.sh --apply
```

При `--apply`:

- backlog-сигналы дописываются в `FACTORY_BACKLOG.md`
- template-gap сигналы дописываются в `TEMPLATE_GAPS.md`
- processed backlog/gap файлы архивируются в `incoming-learnings/processed/`
- accepted/rejected сигналы переносятся в соответствующие каталоги

4. После принятия решения обновите `RELEASE_NOTES.md`.
