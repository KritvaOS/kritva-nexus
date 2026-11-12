# NX-DEC-028: One file for the Claude session identifiers, updated by every commit

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's statement, in the project chat on 2026-11-12 and relayed to this repository, that the file name of the session record is not easy to remember and should be generic, that the Claude session identifiers are to be consolidated in that one file, and that the documents are to say every commit updates it; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-12 |
| Requirements | None (repository working rule) |
| Task | None (repository working rule) |
| Evidence | [planning/CLAUDE_SESSIONS.md](../planning/CLAUDE_SESSIONS.md); section 3 of [AGENTS.md](../AGENTS.md); [CONTRIBUTING.md](../CONTRIBUTING.md) |

Context: NX-DEC-024 records the session identifier as plain text in the session table of its own decision record. That file name is hard to remember, and the table was already out of date after one day of work. The owner asked for a generic file name, one consolidated file, and a rule in the documents that each commit updates it.

Decisions:

1. The Claude session identifiers are consolidated in `planning/CLAUDE_SESSIONS.md`, a generic file name in the planning folder, next to the changelog and the other work records. Owner: use a generic file name and one consolidated file.
2. Every commit that Claude helped write also updates `CLAUDE_SESSIONS.md` in the same commit, as the rules of that file describe: a new row for a new session and date, otherwise the Work cell of the existing row is extended. AGENTS.md section 3 and CONTRIBUTING.md state the rule.
3. This record replaces decision 2 of NX-DEC-024 (where the identifier is recorded). Decisions 1 and 3 of NX-DEC-024, the co-author line and the unverified visibility assumption, are unchanged. The session table of NX-DEC-024 is kept as history and is not edited; its row is copied into the new file.
4. The session identifier stays plain text in that file only. It is not a commit trailer, not a link and not in a pull request description, so `commit-message-check` is unchanged.

Alternatives considered: Keep the table in NX-DEC-024 and add rows there (the earlier decision); a session trailer in each commit, which the checks reject. The owner chose one generic file.

Rationale: Owner statement as listed. No further rationale was recorded.

Consequences: Every Claude-assisted commit touches one more file, and two open pull requests that both add a row will conflict (resolved by keeping both rows). No check enforces the rule, because a check would need the owner-only script path; a missing row is found in review. CONTRIBUTING.md still says not to commit generated session metadata; the exception is now the plain-text identifiers in `CLAUDE_SESSIONS.md`, stated in CONTRIBUTING.md by this change. A session identifier remains a reference, not evidence, and carries no weight or credit.

## History

| Date | Change |
|---|---|
| 2026-11-12 | Record created with label SELECTED. |
