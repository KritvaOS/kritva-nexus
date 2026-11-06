# KOS-NEXUS-018 Establish external and internal IP inventory

| Property | Value |
|---|---|
| Milestone | NX-M2 |
| Status | NOT_STARTED (proposed; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | KOS-NEXUS-006 |
| Workstream | IP |
| Readiness | PLANNABLE |
| Proposal status | PROPOSED |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-020. |
| Deliverables | IP register. |
| Acceptance evidence | None yet. Merge commit SHA, pull request, review record. Evidence type: software. |

Objective: List every IP block the SoC needs and classify each one.

Scope: Application CPU cluster, DDR4 controller and PHY, NPU, ISP, security processor and crypto blocks, Ethernet, display, storage and peripheral blocks, clocking and memory macros. Each is classified as developed here, integrated from outside, or placeholder only.

Out of scope: Licence negotiation; integration work; RTL.

Inputs: KOS-NEXUS-006.

Verification method: Review of the register.
