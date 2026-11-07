# NX-DEC-019: Separate secure AXI interconnect

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | Dinesh, as relayed in the A0 discussion; confirmed by approval of the pull request that adds this record |
| Date | Not recorded (the decision predates this repository) |
| Requirements | NX-REQ-032 |
| Task | [KOS-NEXUS-084](../tasks/KOS-NEXUS-084/TASK.md) |
| Evidence | Owner wording as relayed; the A0 draft is imported at [A0_INTEGRATION_DRAFT.md](../architecture/A0_INTEGRATION_DRAFT.md) (a reconstruction, not an original document) |

Context: The security domain needs a bus path that the application fabrics cannot reach.

Alternatives considered: Sharing an application fabric with access filtering; no alternatives recorded.

Rationale: Owner requested a dedicated separate secure AXI interconnect. No further rationale recorded.

Consequences: Concept only. Port counts, widths, address map and the access boundary to the application domain are PROPOSED in NX-REQ-033 onward and need their own decisions.

Owner wording: "A dedicated separate secure AXI interconnect."

## History

| Date | Change |
|---|---|
| 2026-11-07 | Record created from the A0 discussion for KOS-NEXUS-084 with label SELECTED. |
