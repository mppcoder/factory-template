# Матрица gates full autonomous mode

Дата: 2026-05-05

| Action | Default | Required approval | Required validators | Allowed environment | Audit required | Rollback required | Human review required | Auto allowed? | Current status |
|---|---|---|---|---|---|---|---|---|---|
| live label mutation | disabled | matching issue-fix or rollback scope | permission model, human review policy | approved workflow only | yes | yes | yes | no | future gated |
| issue comments | dry-run/gated | issue-fix for trusted actor | permission model | approved workflow only | yes | no destructive rollback | conditional | limited | future gated |
| branch push | disabled in verify | issue-fix or high-risk | permission model, bounded runner | automation branch only | yes | yes | conditional | limited | gated substrate |
| PR creation | disabled in verify | issue-fix or high-risk | permission model, bounded runner | automation branch only | yes | yes | yes before merge | limited | gated substrate |
| auto-merge | disabled | `auto-merge` | auto-merge gate, permission model, approval | protected PR after green checks | yes | yes | yes | no by default | gate implemented dry-run |
| production deploy | disabled | `production-deploy` | production deploy gate, permission model, approval | explicit target/environment | yes | yes | yes | no | gate implemented dry-run |
| security fix | public issue path refused | `security-fix` | security issue gate, permission model, approval | private channel only | sanitized | yes | yes | no | refusal/private placeholder |
| public external submit | disabled | `public-submit` | public submit gate, redaction/consent checks | explicit target repo | yes | yes | yes | no | gate implemented dry-run |
| parallel runner | max `1` | `parallel-runner` for >1 | worktree manager, bounded runner, ledger, rollback, approval | temp/dry-run or approved isolated worktrees | yes | yes | yes for >1 | no by default | dry-run proof complete |

Dangerous actions remain disabled/default and require explicit unlock conditions.
