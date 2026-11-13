# Claude Sessions

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-SESSIONS-001 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Log |
| Status | DRAFT |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.1.0-draft |
| Last Updated | 2026-11-12 |
| Authority | REFERENCE (not evidence) |
| Related Tasks / Milestones | None (repository working rule); NX-M1 |
| Related Documents | [NX-DEC-028](../decisions/NX-DEC-028.md); [NX-DEC-024](../decisions/NX-DEC-024.md); [AGENTS.md](../AGENTS.md); [CONTRIBUTING.md](../CONTRIBUTING.md) |

## Purpose

This is the one file that lists the Claude sessions that helped write commits in this repository. The session identifier is plain text in the table below and nowhere else: not a commit trailer, not a link and not in a pull request description (NX-DEC-024, NX-DEC-028).

## Rules

1. Every commit that Claude helped write also updates this file in the same commit. If the table has no row for that session and that date, the commit adds one; if it has, the commit extends the Work cell of that row. A row of an earlier date is never edited.
2. A row has the date, the session identifier exactly as Claude reports it, and a short statement of the work (tasks, documents, decision records).
3. A session identifier is a reference. It is not evidence, does not count toward acceptance, carries no kritva-program weight or credit, and is not proof that anyone can open the session. Who can open a session depends on the claude.ai sharing settings, which this repository cannot verify (NX-DEC-024).
4. When two pull requests add rows at the same time, resolve the merge by keeping both rows.
5. No check enforces rule 1. A check would belong under the owner-only script path and is not planned here.

## Sessions

| Date | Session identifier | Work |
|---|---|---|
| 2026-11-11 | session_01KqgaDkHBpV3gbQLqZQqZgm | KOS-NEXUS-085 datasheet revision 0.2.0-draft and NX-DEC-024 (copied unchanged from the session table of NX-DEC-024) |
| 2026-11-12 | session_01KqgaDkHBpV3gbQLqZQqZgm | Same session. Work of 2026-11-11 not listed above: datasheet revision 0.2.1-draft and NX-DEC-025 (32-channel DMA controller, NX-REQ-092 to NX-REQ-100). Work of 2026-11-12: datasheet revisions 0.3.0-draft to 0.3.4-draft; KOS-NEXUS-008 memory architecture, address maps and domain crossings (NX-DEC-026, NX-DEC-027); NX-DEC-028 and this file; the mailbox clarification after review 4 (NX-REQ-106 to NX-REQ-108); the address-map checker (scripts/check_address_maps.py) |
| 2026-11-13 | session_01KqgaDkHBpV3gbQLqZQqZgm | Same session. Work of 2026-11-13: KOS-NEXUS-008 owner review answers recorded as NX-DEC-029 (NX-REQ-109 to NX-REQ-111), memory architecture 0.4.0-draft, datasheet revision 0.3.5-draft; test fix for the System SRAM record list; NX-DEC-030 (approval of the PROPOSED architecture items), memory architecture 0.5.0-draft, datasheet revision 0.3.6-draft; NX-REQ-112 (peripheral register windows, PROPOSED), map checker extension, datasheet revision 0.3.7-draft; NX-DEC-031 (40-bit width for every application master) and NX-DEC-032 (address-map-check required), datasheet revision 0.3.8-draft |

## History

| Version | Date | Change |
|---|---|---|
| 0.1.0-draft | 2026-11-12 | File created by NX-DEC-028; the session table of NX-DEC-024 is copied as the first row |
| 0.1.1-draft | 2026-11-13 | Row for 2026-11-13 added |
| 0.1.2-draft | 2026-11-13 | Row for 2026-11-13 extended |
| 0.1.3-draft | 2026-11-13 | Row for 2026-11-13 extended again |
| 0.1.4-draft | 2026-11-13 | Row for 2026-11-13 extended again |
