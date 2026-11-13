# KOS-NEXUS-008 Define memory and address-map architecture

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | IN_REVIEW (started by the owner on 2026-11-12; submitted for owner review on 2026-11-13; proposed; Nexus is outside the V2 plan and is not registered in kritva-program) |
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

Progress note: the task is submitted for owner review on 2026-11-13. The deliverables are [architecture/MEMORY_ARCHITECTURE.md](../../architecture/MEMORY_ARCHITECTURE.md) (memory roles, the 40-bit application width, the two domain crossings and the access policy), [architecture/ADDRESS_MAP.md](../../architecture/ADDRESS_MAP.md) with the machine-readable sources [application_map.yaml](../../architecture/maps/application_map.yaml), [secure_map.yaml](../../architecture/maps/secure_map.yaml), [peripheral_windows.yaml](../../architecture/maps/peripheral_windows.yaml) and [register_layouts.yaml](../../architecture/maps/register_layouts.yaml), the structural checker `scripts/check_address_maps.py` with tests in `tests/address_map_check/` (a required check, NX-DEC-032), requirements NX-REQ-101 to NX-REQ-119 and decision records NX-DEC-026 to NX-DEC-034.

What the owner decided (SELECTED): the 40-bit application width, confirmed for the C910 and every application master (NX-DEC-026, NX-DEC-030, NX-DEC-031); the application and secure maps (NX-DEC-030); the two controlled crossings and their details (NX-DEC-027, NX-DEC-029, NX-DEC-033); the peripheral register windows and the PLIC and CLINT baseline (NX-DEC-033); and the secure interconnect parameters and secure address-space attributes (NX-DEC-034). NX-ARCH-GAP-002 and NX-ARCH-GAP-003 are CLOSED. The acceptance criteria AC-010, AC-013 and AC-015 are for the owner to judge in this review; this record does not mark them met.

Still PROPOSED: the register conventions and block register layouts (NX-REQ-117, NX-REQ-118, NX-ARCH-OI-039, owner Dinesh).

Still OPEN, each with owner Dinesh: bit fields of every register (NX-ARCH-OI-039); privilege levels, lock states, per-register policy, security interrupt and fault response of the secure space (NX-ARCH-OI-021); the mailbox allow-list, requester authentication, replay and flood protection, the boot-window reset domain of AXI-3 and System SRAM, the System SRAM attachment point and the secure-to-AXI-3 width and clock conversion (NX-ARCH-OI-038, NX-ARCH-OI-025); the security and always-on interrupt controllers and the routing (NX-REQ-057, NX-ARCH-OI-032); the RTL evidence for the 40-bit width (NX-ARCH-OI-001); and the PSRAM, NOR and on-chip memory capacities (NX-ARCH-OI-006, NX-ARCH-OI-007).

Limits: the checker is structural and does not show that a base, size or attribute is right; no security claim is made; the architecture documents have no approval record of their own. The task is not ACCEPTED and no evidence record exists.
