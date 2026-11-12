# Contributing to kritva-nexus

1. Work from a task in [planning/TASKS.md](planning/TASKS.md). If there is none, propose one first.
2. Branch from `main` and open a pull request; do not push to `main`.
3. Commit format: `type(scope): summary` plus one `Task:` or `Tasks:` footer (`Tasks: None (reason)` on a docs or chore commit that implements no task). PRs use `.github/PULL_REQUEST_TEMPLATE.md`; the merge method is a merge commit. See [AGENTS.md](AGENTS.md).
4. Run `make check` and the gates that apply; an unimplemented gate exits 3 and is never reported as a pass. Report results in the PR.
5. Add or update the changelog ([planning/CHANGELOG.md](planning/CHANGELOG.md)) and, for a closing milestone, a `COMPLETION_RECORD.md`.
6. Required checks: secret-scan, commit-message-check and pr-acceptance-gate. Review by the Code Owner (see `.github/CODEOWNERS`): Dinesh, interim and not independent.

A commit that Claude helped write also updates [CLAUDE_SESSIONS.md](planning/CLAUDE_SESSIONS.md) in the same commit and carries the co-author line of [AGENTS.md](AGENTS.md) (NX-DEC-024, NX-DEC-028). That file is the only exception to the next rule.

Do not commit secrets, generated session metadata (except the plain-text identifiers in `CLAUDE_SESSIONS.md`), third-party IP or PDK files whose terms forbid it, or empty placeholder folders.
