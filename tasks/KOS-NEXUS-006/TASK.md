# KOS-NEXUS-006 Consolidate top-level system architecture

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | ACCEPTED (started by Dinesh on 2026-11-07; submitted for owner review on 2026-11-08; accepted by Dinesh on 2026-11-09 as a repository task only, with no weight or credit; proposed, not baselined; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | none (input: KOS-NEXUS-084) |
| Workstream | ARCH |
| Readiness | PLANNABLE |
| Proposal status | PROPOSED |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-010, AC-012. |
| Deliverables | `architecture/` index and system architecture document, with the Kritva document header. |
| Acceptance evidence | Evidence type: software (architecture review; no tool run). Merge commits on `main`: `0d11805857a13c5cbb286677f48993bfefe973c2` task start (PR #9); `e9d13fb4142792db5789196893d25fda804196fd` part 1 (PR #10); `e9d669b4f354e699b8bd8c8542917e866fef4275` part 2 (PR #11); `a8db71a5dda292d344e765f619e42f702636936e` part 3 (PR #12); `b6faa49c8c886783a7e232cc1d77363dee744688` part 4 (PR #13); `7c5e4e3deecb37a58872263fe2e841ffb49976d5` part 5 (PR #14); `37e143136b6e0bd47b024476e1e7dd79921df910` part 6 (PR #15); `a4b51e8192cd1d54b941ae382eae5e5a6c7b695e` external-review corrections (PR #16); `ec7e02a548fd0d5babab6b26bdbd50edb8d3faf7` IN_REVIEW and index (PR #17), the commit that holds the reviewed document (system architecture version 0.7.0-draft). Review record: an external review by ChatGPT (no label found stronger than the register supports) and the owner's approval of the acceptance pull request. The owner and reviewer are the same person (interim, not independent). |

Objective: Write the top-level Nexus system architecture from the existing A0 integration draft, as an architecture document owned by this repository.

Scope: Application domain, AI and vision blocks, memory, multimedia and connectivity, the security domain, the always-on management domain, and clock, reset, interrupt and security interfaces at overview level. Each decision is labelled SELECTED, PROPOSED or OPEN.

Out of scope: Detailed interconnect, memory and address-map content (KOS-NEXUS-007 and 008); subsystem microarchitecture; RTL.

Inputs: The A0 integration draft ([architecture/A0_INTEGRATION_DRAFT.md](../../architecture/A0_INTEGRATION_DRAFT.md), a reconstruction of a working discussion, not an original document), the owner decisions in [decisions/](../../decisions/DECISIONS.md) and the requirements in [requirements/REQUIREMENTS.md](../../requirements/REQUIREMENTS.md) (KOS-NEXUS-084, accepted).

Verification method: Architecture review; the owner records any decision promoted to SELECTED.

Progress note: [architecture/SYSTEM_ARCHITECTURE.md](../../architecture/SYSTEM_ARCHITECTURE.md) (DRAFT, version 0.7.0, after an external review by ChatGPT that found no label stronger than the register supports) has the rules, system context, domain map, a section for every domain, RTL partitioning, simulator and prototype architecture, the interface register and the open-issues register, and [architecture/README.md](../../architecture/README.md) is the index. The task is ACCEPTED as a repository task. The NX-M1 architecture outcome is not complete: AC-013 to AC-016 still need their questions resolved or kept as owner-approved open dispositions.
