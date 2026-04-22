# Codex context

## Change focus
- Canonical VPS layout for repo folders.
- `/projects` must contain only project roots.
- Project-local incoming path: `/projects/<project-root>/_incoming/`.
- Brownfield temporary, intermediate and reconstructed repos must never be top-level siblings in `/projects`.

## Main affected layers
- `template-repo/scenario-pack/`
- `factory_template_only_pack/`
- `workspace-packs/`
- `template-repo/template/docs/`
- root/operator docs and current `.chatgpt` closeout artifacts

## Consistency target
- advisory layer and executable layer must not conflict;
- tree examples must show only project roots in `/projects`;
- brownfield without repo must explicitly forbid flat temp repo placement.
