# KOS-NEXUS-006 Consolidate top-level system architecture

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | NOT_STARTED (proposed; Nexus is outside the V2 plan and is not registered in kritva-program) |
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

Inputs: The A0 integration draft (an external working discussion, not yet in this repository), owner decisions, KOS-NEXUS-084 requirements.

Verification method: Architecture review; the owner records any decision promoted to SELECTED.
