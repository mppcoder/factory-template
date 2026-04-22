# Codex task pack

## Remediation checklist
- [x] Найти conflicting references to flat `/projects` layout.
- [x] Ввести единое canonical rule для `/projects/<project-root>/...`.
- [x] Отдельно зафиксировать brownfield without repo rule.
- [x] Синхронизировать runbooks, scenario-pack, workspace/bootstrap examples и boundary templates.
- [x] Проверить, что launcher/scaffold logic не создаёт top-level temp repos.
- [x] Подготовить completion package для factory sources и downstream контуров.

## Canonical rule
- `/projects` contains only project roots.
- `_incoming` is optional and lives only inside a project root.
- Brownfield temporary/intermediate/reconstructed repos live only inside their project root.
