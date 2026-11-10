# KOS-NEXUS-007 Define application AXI and memory access architecture

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | IN_PROGRESS (started by Dinesh on 2026-11-09; proposed, not baselined; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | KOS-NEXUS-006, KOS-NEXUS-084 |
| Workstream | ARCH |
| Readiness | PLANNABLE |
| Proposal status | PROPOSED |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-012, AC-014, AC-016. Open items NX-ARCH-GAP-001 and NX-ARCH-GAP-004 are resolved or explicitly left OPEN with an owner. |
| Deliverables | Interconnect specification and connectivity matrix. |
| Acceptance evidence | None yet. Merge commit SHA, pull request, review record. Evidence type: software. |

Objective: Define the four application AXI fabrics, the secure fabric, the APB bridges and the memory-access aggregation layer, including the open items found in A0.

Scope: Master and slave connectivity, widths and clock assumptions, the path from the application CPU to APB-0 and APB-1, QoS and protection at the memory-access layer, and derivation of memory-access port count from bandwidth.

Out of scope: Interconnect RTL; DDR4 controller IP selection (IP workstream).

Inputs: the accepted system architecture ([architecture/SYSTEM_ARCHITECTURE.md](../../architecture/SYSTEM_ARCHITECTURE.md), KOS-NEXUS-006), the accepted requirements and decisions (KOS-NEXUS-084), the open items NX-ARCH-GAP-001 and NX-ARCH-GAP-004, bandwidth and DMA requirements.

Verification method: Architecture review; bandwidth analysis recorded in the document.

Progress note: NX-ARCH-GAP-001 is closed by owner decisions (NX-DEC-021, NX-DEC-022); NX-ARCH-GAP-004 and the interconnect open issues are resolved by PROPOSED requirements (NX-REQ-030, NX-REQ-076 to NX-REQ-081), changed only by change request. See [architecture/INTERCONNECT_SPECIFICATION.md](../../architecture/INTERCONNECT_SPECIFICATION.md).
