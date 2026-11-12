# NX-DEC-024: Claude co-author line and session reference for Nexus commits

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's statements on commit attribution and session references, made in the project chat on 2026-11-11 and relayed to this repository; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-11 |
| Requirements | None (repository working rule; no NX-REQ) |
| Task | None (repository process decision; implements no task) |
| Evidence | [AGENTS.md](../AGENTS.md) section 3; the commit checks `scripts/security/check_commit_format.py` and `scripts/security/check_commit_messages.py`, which are unchanged by this record |

Context: Work on this repository is done with Claude. The owner asked that commits carry a Claude co-author line and that the Claude session details be shared, on the assumption that the session discussion is open only to the Kritva team. The repository forbids a session trailer and a session link in a commit or pull request description (AGENTS.md section 3), enforced by `commit-message-check`. That control comes from kritva-program decision D-032. The commit-format check allows a co-author line.

Decisions:

1. Commits for this repository that Claude helped write end with the line `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`, placed after the single `Task:` footer. The model name is the one in use when the commit is written. Owner: add the co-author line for kritva-nexus.
2. The session identifier is recorded as plain text in the session table of this record, one dated row per session, and nowhere else. It is not a commit trailer, not a link and not in a pull request description, so the commit checks keep passing unchanged. Owner: share the session details in a decision record.
3. The owner's assumption that the session discussion is visible only to the Kritva team is recorded as an assumption. This repository cannot verify it: who can open a session depends on the claude.ai sharing settings, not on anything here.

Alternatives considered: A `Claude-Session:` trailer or a session link in each commit, which the commit checks reject and which would need the owner to change the protected scripts and the program-level control D-032; or no session reference at all. The owner chose the decision record.

Rationale: Owner statements as listed. No further rationale was recorded.

Consequences: The `Claude-Session:` trailer and the session link stay forbidden in commits and pull request descriptions; the checks and AGENTS.md are unchanged. CONTRIBUTING.md says not to commit generated session metadata; this record is the owner-approved exception, limited to the plain-text session identifiers in the table below, and CONTRIBUTING.md is not changed here. A session identifier is a reference, not evidence: it does not count toward acceptance, carries no kritva-program weight or credit, and it is not proof that anyone can open the session. Earlier sessions are not recorded. A new session is added as a dated row in the History table; existing rows are not rewritten.

## Sessions

| Date | Session identifier | Work |
|---|---|---|
| 2026-11-11 | session_01KqgaDkHBpV3gbQLqZQqZgm | KOS-NEXUS-085 datasheet revision 0.2.0-draft and this record |

## History

| Date | Change |
|---|---|
| 2026-11-11 | Record created with label SELECTED. |
| 2026-11-12 | Decision 2 replaced by NX-DEC-028: new session rows go in planning/CLAUDE_SESSIONS.md, and every Claude-assisted commit updates that file. The table above is kept as history and is not edited; its row is copied into that file. |
