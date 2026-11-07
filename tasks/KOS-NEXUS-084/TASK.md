# KOS-NEXUS-084 Establish requirements register and architecture decision records

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | ACCEPTED (started by Dinesh on 2026-11-06; submitted for owner review on 2026-11-07; accepted by Dinesh on 2026-11-07 as a repository task only, with no weight or credit; proposed, not baselined; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | KOS-NEXUS-006 (input) |
| Workstream | ARCH |
| Readiness | PLANNABLE |
| Proposal status | PROPOSED (new; pending re-alignment) |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-010, AC-011. |
| Deliverables | `requirements/` register and `decisions/` records. |
| Acceptance evidence | Evidence type: software (review of traceability; no tool run). Merge commits on `main`: `7fea521ecd308a120bcb779fc4aec2f874befb3d` is the task start (PR #3); `f460fa73b76281448304402242b5a9c927e8c3ba` first batch (PR #4); `0084bd1caa52a83b03fa1008b08a858d39f133cd` A0 draft import (PR #5); `0a532b5a1186a534fa4e37f7fe121c8ae27a11e6` second batch (PR #6); `711267d3be00888afdf27efe8495851d7647e7fd` IN_REVIEW (PR #7), the commit that holds the reviewed register and records. Review record: the owner's approval of the acceptance pull request. The owner and reviewer are the same person (interim, not independent). |

Objective: Create the requirements register and decision records that the architecture documents trace to.

Scope: Stable requirement IDs, a link from each requirement to an architecture element and a verification method, and decision records with alternatives and rationale for each owner decision.

Out of scope: Numeric performance targets that the architecture has not yet defined; the verification plans themselves.

Inputs: Owner decisions, the A0 draft, KOS-NEXUS-006.

Verification method: Review of traceability.

Note: This ID is new: the earlier proposed catalogue had no task that produced the requirements register. It is proposed here and needs owner and cross-reviewer agreement.

Progress note: the second batch brings [requirements/REQUIREMENTS.md](../../requirements/REQUIREMENTS.md) to 66 requirements (26 SELECTED, 34 PROPOSED, 6 OPEN) and [decisions/DECISIONS.md](../../decisions/DECISIONS.md) to 20 records. The A0 draft is imported in [architecture/A0_INTEGRATION_DRAFT.md](../../architecture/A0_INTEGRATION_DRAFT.md). The task is ACCEPTED as a repository task. Not covered and left for later tasks or batches: the frame-pool bank and ECC organisation, key provisioning, anti-rollback, debug lifecycle, peripheral feature details and the six OPEN requirements are not yet resolved.
