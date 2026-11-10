# KOS-NEXUS-020 Define RTL coding and module conventions

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | IN_PROGRESS (started by Dinesh on 2026-11-09; proposed, not baselined; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | KOS-NEXUS-006, KOS-NEXUS-084 |
| Workstream | RTL |
| Readiness | PLANNABLE |
| Proposal status | PROPOSED |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-033 (module-size guidelines and RTL coding guidelines written and applied). The checks named in AC-030 to AC-032 are implemented by later tasks (for example KOS-NEXUS-081) and are not part of this task. |
| Deliverables | `standards/RTL_DESIGN_STANDARD.md` (KNX-RTL-STD-001; written in the next pull request) with stable rule identifiers, an enforcement level per rule, a proposed compliance-check plan, a waiver format and a manifest schema. |
| Acceptance evidence | None yet. Merge commit SHA, pull request, review record. Evidence type: software. |

Objective: Define the RTL coding, naming, file, reset, clock, library, memory and latch conventions for Kritva Nexus, and say which rules a CI check can decide.

Scope: the standard document; stable rule identifiers; proposed defaults for the open methodology decisions (STD-D-001 to STD-D-013); the planned automated compliance checks (port naming, clock and reset naming, maximum file length, latch inference, common-library dependency, memory-wrapper usage, source header, waiver validity) with phases and result states.

Out of scope: the checker script, the CI workflow (a protected `.github/workflows/` path, added by the owner in its own pull request), the toolchain and its pinned versions (KOS-NEXUS-002, KOS-NEXUS-003), the common library and memory wrappers (KOS-NEXUS-021, KOS-NEXUS-073 to KOS-NEXUS-078), the approved-module manifest content, any RTL, and any weight or credit model.

Inputs: [architecture/SYSTEM_ARCHITECTURE.md](../../architecture/SYSTEM_ARCHITECTURE.md) section 12, the A0 draft guidance on RTL partitioning, the imported draft of KNX-RTL-STD-001, the repository LICENSE (Apache-2.0), the owner's copyright holder (Kritva Robotics) and the external ChatGPT review of the corrections and the CI plan.

Verification method: Review of the standard against AC-033; each A-rule is checked later by the check that implements it, with positive and negative fixtures.

Progress note: the standard is DRAFT and every rule is PROPOSED. The standard becomes mandatory only when the owner approves it by a decision record and the matching requirement rows; until then the checks in the standard are a plan and no compliance claim is made.
