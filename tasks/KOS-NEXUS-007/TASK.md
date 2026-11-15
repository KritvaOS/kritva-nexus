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

Progress note: NX-ARCH-GAP-001 is closed by owner decisions (NX-DEC-021, NX-DEC-022); NX-ARCH-GAP-004 and the interconnect open issues are closed by NX-DEC-035 (NX-REQ-030, NX-REQ-076 to NX-REQ-081 SELECTED); the Memory Access Crossbar, the fabric roles and placement, the APB bridge parameters, the DDR4-3200 target, the DMA placement and the connectivity matrix (architecture/maps/connectivity.yaml, interconnect specification section 7) are SELECTED by NX-DEC-036 (NX-REQ-049 to NX-REQ-052, 064, 093, 120, 121), with System SRAM on AXI-0, the OSPI controllers on AXI-3 and an AXI-0 to AXI-1 bridge for the C910. Still open: the AXI-3 to AXI-0 bridge for System SRAM access (NX-REQ-122, PROPOSED) and the behaviour of memory accesses through the fabric bridges (NX-ARCH-OI-041, OPEN). The task stays IN_PROGRESS. See [architecture/INTERCONNECT_SPECIFICATION.md](../../architecture/INTERCONNECT_SPECIFICATION.md).
