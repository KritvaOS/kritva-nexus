# KOS-NEXUS-008 Define memory and address-map architecture

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | IN_PROGRESS (started by the owner on 2026-11-12; proposed; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | KOS-NEXUS-006, KOS-NEXUS-007, KOS-NEXUS-084 |
| Workstream | ARCH |
| Readiness | PLANNABLE |
| Proposal status | PROPOSED |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-010, AC-013, AC-015. Open item NX-ARCH-GAP-002 and NX-ARCH-GAP-003 are resolved or explicitly left OPEN with an owner. |
| Deliverables | Memory architecture document and address-map documents, with the maps kept in one machine-readable source once the format is agreed. |
| Acceptance evidence | None yet. Merge commit SHA, pull request, review record. Evidence type: software. |

Objective: Define the external and on-chip memory architecture and the application and secure address maps.

Scope: DDR4, OSPI PSRAM, OSPI NOR and on-chip SRAM roles; cacheability, coherency, access-permission and unmapped-access policy; application and secure address spaces stated as separate spaces; peripheral register windows.

Out of scope: Memory controller RTL; SRAM macro selection.

Inputs: KOS-NEXUS-006, KOS-NEXUS-007, KOS-NEXUS-084, the configuration of the selected CPU.

Verification method: Architecture review; the address width is checked against the CPU configuration.

Progress note: part 1 is [architecture/MEMORY_ARCHITECTURE.md](../../architecture/MEMORY_ARCHITECTURE.md) with NX-DEC-026 (40-bit width SELECTED) and NX-REQ-101 to NX-REQ-104. Still to do: the application and secure address maps in one machine-readable source with the format agreed, the separation of the two address spaces (NX-ARCH-GAP-002), and the confirmation of the width against the C910 configuration and every application master (NX-ARCH-GAP-003, owner Dinesh). The task stays IN_PROGRESS.
