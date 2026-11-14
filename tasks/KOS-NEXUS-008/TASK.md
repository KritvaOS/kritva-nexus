# KOS-NEXUS-008 Define memory and address-map architecture

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | ACCEPTED (started by the owner on 2026-11-12; submitted for owner review on 2026-11-13; accepted by Dinesh on 2026-11-13 as a repository task only, with no weight or credit; proposed; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | KOS-NEXUS-006, KOS-NEXUS-007, KOS-NEXUS-084 |
| Workstream | ARCH |
| Readiness | PLANNABLE |
| Proposal status | PROPOSED |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-010, AC-013, AC-015. Open item NX-ARCH-GAP-002 and NX-ARCH-GAP-003 are resolved or explicitly left OPEN with an owner. |
| Deliverables | Memory architecture document and address-map documents, with the maps kept in one machine-readable source once the format is agreed. |
| Acceptance evidence | Evidence type: software (architecture review; the address-map checker and its tests ran in CI on the later pull requests). Merge commits on `main`: `9f2bed969a0cea0c1b0efa16221e4a2d1506bd00` memory architecture (PR #39); `58145ff46e215ba68b63ee956d00e9d77ecebb17` address maps (PR #40); `2c3ea3e43e2346f62f698bf8bd3e256eaaf5a67a` address-map checker (PR #44); `7a0bb46b0a81f6effbb9602aeb2ae20b3c8e53b8` NX-DEC-029 (PR #45); `0c10d49f2ef918897c821b1606a8f0f6ca57e94d` NX-DEC-030 (PR #46); `4fda01a47b53059a9cfab837f60f8a31a83c8784` peripheral register windows (PR #47); `700496b16a89413cc8638ab37080ed6b42169a96` NX-DEC-031 and NX-DEC-032 (PR #48); `a2c86b2d7fe00a5d888681ca488f75f2e9cf4eb5` crossing details and interrupt baseline (PR #49); `87b86a7a0b8123f667183ea39787808ff51c4bc7` NX-DEC-033 (PR #50); `d41bb71a72dcc0ddbbf89281fe160710c46e3381` removal of a stray swap file added by PR #50 (PR #51); `439d19c6c72f9aa4241c4d4e7a36a7869a2ebf86` register layouts and secure attributes (PR #52); `3834aeba8f0f0e06de378e6ce742f905f88c186f` NX-DEC-034 (PR #53); `2dca1a49e437adbe5e22441776ec0a3bf0c38048` IN_REVIEW, the commit that holds the reviewed documents (PR #54). Review record: an external review by ChatGPT of the early parts (address arithmetic and label discipline found sound; two defects fixed), the owner's decisions NX-DEC-026 to NX-DEC-034, the owner's statement "Accepted" of 2026-11-13 and the owner's approval of the acceptance pull request. PR #50 merged with a commit that carries a session trailer and a stray swap file, and PR #51 removed the file. The owner and reviewer are the same person (interim, not independent). |

Objective: Define the external and on-chip memory architecture and the application and secure address maps.

Scope: DDR4, OSPI PSRAM, OSPI NOR and on-chip SRAM roles; cacheability, coherency, access-permission and unmapped-access policy; application and secure address spaces stated as separate spaces; peripheral register windows.

Out of scope: Memory controller RTL; SRAM macro selection.

Inputs: KOS-NEXUS-006, KOS-NEXUS-007, KOS-NEXUS-084, the configuration of the selected CPU.

Verification method: Architecture review; the address width is checked against the CPU configuration.

Progress note: the task was submitted for owner review on 2026-11-13 and accepted by the owner the same day as a repository task. The deliverables are [architecture/MEMORY_ARCHITECTURE.md](../../architecture/MEMORY_ARCHITECTURE.md) (memory roles, the 40-bit application width, the two domain crossings and the access policy), [architecture/ADDRESS_MAP.md](../../architecture/ADDRESS_MAP.md) with the machine-readable sources [application_map.yaml](../../architecture/maps/application_map.yaml), [secure_map.yaml](../../architecture/maps/secure_map.yaml), [peripheral_windows.yaml](../../architecture/maps/peripheral_windows.yaml) and [register_layouts.yaml](../../architecture/maps/register_layouts.yaml), the structural checker `scripts/check_address_maps.py` with tests in `tests/address_map_check/` (a required check, NX-DEC-032), requirements NX-REQ-101 to NX-REQ-119 and decision records NX-DEC-026 to NX-DEC-034.

What the owner decided (SELECTED): the 40-bit application width, confirmed for the C910 and every application master (NX-DEC-026, NX-DEC-030, NX-DEC-031); the application and secure maps (NX-DEC-030); the two controlled crossings and their details (NX-DEC-027, NX-DEC-029, NX-DEC-033); the peripheral register windows and the PLIC and CLINT baseline (NX-DEC-033); and the secure interconnect parameters and secure address-space attributes (NX-DEC-034). NX-ARCH-GAP-002 and NX-ARCH-GAP-003 are CLOSED. The acceptance criteria AC-010, AC-013 and AC-015 are for the owner to judge in this review; this record does not mark them met; the owner accepted the task as a repository task only.

Still PROPOSED: the register conventions and block register layouts (NX-REQ-117, NX-REQ-118, NX-ARCH-OI-039, owner Dinesh).

Still OPEN, each with owner Dinesh: bit fields of every register (NX-ARCH-OI-039); privilege levels, lock states, per-register policy, security interrupt and fault response of the secure space (NX-ARCH-OI-021); the mailbox allow-list, requester authentication, replay and flood protection, the boot-window reset domain of AXI-3 and System SRAM, the System SRAM attachment point and the secure-to-AXI-3 width and clock conversion (NX-ARCH-OI-038, NX-ARCH-OI-025); the security and always-on interrupt controllers and the routing (NX-REQ-057, NX-ARCH-OI-032); the RTL evidence for the 40-bit width (NX-ARCH-OI-001); and the PSRAM, NOR and on-chip memory capacities (NX-ARCH-OI-006, NX-ARCH-OI-007).

Limits: the checker is structural and does not show that a base, size or attribute is right; no security claim is made; the architecture documents have no approval record of their own. The acceptance is a repository status only and the open items above stay open.
