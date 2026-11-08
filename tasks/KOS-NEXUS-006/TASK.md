# KOS-NEXUS-006 Consolidate top-level system architecture

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | IN_REVIEW (started by Dinesh on 2026-11-07; submitted for owner review on 2026-11-08; proposed, not baselined; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | none (input: KOS-NEXUS-084) |
| Workstream | ARCH |
| Readiness | PLANNABLE |
| Proposal status | PROPOSED |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-010, AC-012. |
| Deliverables | `architecture/` index and system architecture document, with the Kritva document header. |
| Acceptance evidence | None yet. Merge commit SHA, pull request, review record. Evidence type: software. |

Objective: Write the top-level Nexus system architecture from the existing A0 integration draft, as an architecture document owned by this repository.

Scope: Application domain, AI and vision blocks, memory, multimedia and connectivity, the security domain, the always-on management domain, and clock, reset, interrupt and security interfaces at overview level. Each decision is labelled SELECTED, PROPOSED or OPEN.

Out of scope: Detailed interconnect, memory and address-map content (KOS-NEXUS-007 and 008); subsystem microarchitecture; RTL.

Inputs: The A0 integration draft ([architecture/A0_INTEGRATION_DRAFT.md](../../architecture/A0_INTEGRATION_DRAFT.md), a reconstruction of a working discussion, not an original document), the owner decisions in [decisions/](../../decisions/DECISIONS.md) and the requirements in [requirements/REQUIREMENTS.md](../../requirements/REQUIREMENTS.md) (KOS-NEXUS-084, accepted).

Verification method: Architecture review; the owner records any decision promoted to SELECTED.

Progress note: [architecture/SYSTEM_ARCHITECTURE.md](../../architecture/SYSTEM_ARCHITECTURE.md) (DRAFT, version 0.7.0, after an external review by ChatGPT that found no label stronger than the register supports) has the rules, system context, domain map, a section for every domain, RTL partitioning, simulator and prototype architecture, the interface register and the open-issues register, and [architecture/README.md](../../architecture/README.md) is the index. The task is IN_REVIEW; acceptance is the owner's decision. The NX-M1 architecture outcome is not complete: AC-013 to AC-016 still need their questions resolved or kept as owner-approved open dispositions.
