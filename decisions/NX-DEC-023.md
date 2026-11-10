# NX-DEC-023: Approval of the RTL Design Standard KNX-RTL-STD-001

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's answers on the approval and its scope, stated in the project chat on 2026-11-10 and relayed to this repository; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-10 |
| Requirements | NX-REQ-082, NX-REQ-083, NX-REQ-084, NX-REQ-085, NX-REQ-086, NX-REQ-087, NX-REQ-088, NX-REQ-089 |
| Task | [KOS-NEXUS-020](../tasks/KOS-NEXUS-020/TASK.md) |
| Evidence | The standard at version 1.0.1 ([RTL_DESIGN_STANDARD.md](../standards/RTL_DESIGN_STANDARD.md)); its external review is recorded in [planning/CHANGELOG.md](../planning/CHANGELOG.md) |

Context: The imported draft of the RTL standard was corrected and reviewed externally (versions 1.0.0-draft and 1.0.1-draft). The owner was asked whether to record the approval as SELECTED or PROPOSED, and which scope to approve.

Decisions:

1. The RTL Design Standard KNX-RTL-STD-001 at version 1.0.1 is approved as the mandatory standard for Kritva Nexus design RTL, and its status becomes APPROVED. Owner: record as SELECTED on approval.
2. The scope is all rules of the standard. The section 19 compliance-check plan and the section 20 methodology defaults (STD-D-001 to STD-D-013) stay PROPOSED, and the clock-gating figures (99%, 80%, above 60%) stay provisional until section 20 selects them. Owner: all rules, with unresolved items provisional.

Alternatives considered: Approve only the rules that a first-phase check can decide (naming, file, header and coding rules) and leave the library, memory, CDC and clock-gating rules until their library and tool tasks exist; or keep the whole standard PROPOSED until a later change request. The owner chose neither.

Rationale: Owner answers as listed. No further rationale was recorded.

Consequences: Any design RTL added to the repository must conform to the standard or carry a waiver (standard section 18.3). No RTL exists yet, so nothing is non-conforming. No checker, workflow, library manifest or tool pin exists, so CI cannot enforce the rules yet and no compliance claim is made. The standard changes by change request, and a change to a SELECTED rule also needs a new decision record. This approval is a repository decision by an interim, non-independent owner; it is not a review by an independent reviewer and carries no kritva-program weight or credit. AC-033 is not marked passed by this record.

## History

| Date | Change |
|---|---|
| 2026-11-10 | Record created for KOS-NEXUS-020 with label SELECTED. |
