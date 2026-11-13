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

Progress note: part 1 is [architecture/MEMORY_ARCHITECTURE.md](../../architecture/MEMORY_ARCHITECTURE.md) with NX-DEC-026 (40-bit width SELECTED) and NX-REQ-101 to NX-REQ-104. Part 2 is [architecture/ADDRESS_MAP.md](../../architecture/ADDRESS_MAP.md) with the proposed maps in [application_map.yaml](../../architecture/maps/application_map.yaml) and [secure_map.yaml](../../architecture/maps/secure_map.yaml). Part 3 is NX-DEC-027 (two controlled crossings between the security and application domains, SELECTED) with NX-REQ-105 to NX-REQ-108 and section 5 of the memory architecture; NX-ARCH-GAP-002 is PROPOSED. Still to do: the division of the peripheral register space (NX-ARCH-OI-036), the crossing attachment and mailbox details (NX-ARCH-OI-037), a checker for the map files under an owner-only path, the confirmation of the width against the C910 configuration and every application master (NX-ARCH-GAP-003, owner Dinesh), and the review and acceptance of the task. ChatGPT review 4 found the address arithmetic and the label discipline sound and two defects: the mailbox window against the APB security rule (fixed) and the missing map checker. The checker is now `scripts/check_address_maps.py` with tests in `tests/address_map_check/`, run by `make check`, `make check-maps` and the address-map-check workflow; it is structural only. Still open: the division of the peripheral register space (NX-ARCH-OI-036), the crossing attachment and mailbox details (NX-ARCH-OI-037), the confirmation of the width against the C910 configuration and every application master (NX-ARCH-GAP-003, owner Dinesh), the owner review of the map values, and adding address-map-check to the required checks of the branch protection if the owner wants it required. After the owner review of the memory architecture, NX-DEC-029 records three SELECTED points (NX-REQ-109 boot window System SRAM only, NX-REQ-110 mailbox keeps NX-REQ-072, NX-REQ-111 NOR window cacheable and read-only with program and erase only through the controller registers). The owner chose to keep reviewing the architecture before the task goes to IN_REVIEW. NX-DEC-030 then records the owner's approval of the remaining PROPOSED architecture items; the owner confirmed the C910 at 40 bits, and the check for every other application master (NX-ARCH-GAP-003, owner Dinesh) stays open. The peripheral register split is NX-REQ-112 (PROPOSED), held in architecture/maps/peripheral_windows.yaml and shown in ADDRESS_MAP section 2.1, for the owner's review (NX-ARCH-OI-036). Still open: the owner's review and selection of the windows, the crossing attachment and mailbox layout (NX-ARCH-OI-037), and the interrupt controller window (NX-REQ-057). NX-DEC-031 records the owner's confirmation of the 40-bit width for every application master, which closes NX-ARCH-GAP-003, and NX-DEC-032 makes address-map-check a required check. NX-REQ-113 to NX-REQ-116 (PROPOSED) then propose the crossing details and the application interrupt controller baseline for the owner's review (NX-ARCH-OI-037, NX-ARCH-OI-032). NX-DEC-033 then records the owner's approval of NX-REQ-112 to NX-REQ-116. What remains open: the register layout of each block, the mailbox allow-list and the boot-window reset domain (NX-ARCH-OI-038, NX-ARCH-OI-025), the security and always-on interrupt controllers and the routing (NX-REQ-057, NX-ARCH-OI-032), and the owner's review of the task for IN_REVIEW. NX-REQ-117 to NX-REQ-119 (PROPOSED) then propose the register conventions, the block register layouts and the secure address-space attributes, with the secure width NX-REQ-033 shown to cover the secure map. The task stays IN_PROGRESS.
