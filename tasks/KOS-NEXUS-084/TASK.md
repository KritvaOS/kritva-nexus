# KOS-NEXUS-084 Establish requirements register and architecture decision records

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | IN_PROGRESS (started by Dinesh on 2026-11-06; proposed, not baselined; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | KOS-NEXUS-006 (input) |
| Workstream | ARCH |
| Readiness | PLANNABLE |
| Proposal status | PROPOSED (new; pending re-alignment) |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-010, AC-011. |
| Deliverables | `requirements/` register and `decisions/` records. |
| Acceptance evidence | None yet. Merge commit SHA, pull request, review record. Evidence type: software. |

Objective: Create the requirements register and decision records that the architecture documents trace to.

Scope: Stable requirement IDs, a link from each requirement to an architecture element and a verification method, and decision records with alternatives and rationale for each owner decision.

Out of scope: Numeric performance targets that the architecture has not yet defined; the verification plans themselves.

Inputs: Owner decisions, the A0 draft, KOS-NEXUS-006.

Verification method: Review of traceability.

Note: This ID is new: the earlier proposed catalogue had no task that produced the requirements register. It is proposed here and needs owner and cross-reviewer agreement.

Progress note: the second batch brings [requirements/REQUIREMENTS.md](../../requirements/REQUIREMENTS.md) to 66 requirements (26 SELECTED, 34 PROPOSED, 6 OPEN) and [decisions/DECISIONS.md](../../decisions/DECISIONS.md) to 20 records. The A0 draft is imported in [architecture/A0_INTEGRATION_DRAFT.md](../../architecture/A0_INTEGRATION_DRAFT.md). The status stays IN_PROGRESS: the frame-pool bank and ECC organisation, key provisioning, anti-rollback, debug lifecycle, peripheral feature details and the six OPEN requirements are not yet resolved.
