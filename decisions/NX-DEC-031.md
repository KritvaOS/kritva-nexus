# NX-DEC-031: 40-bit width confirmed for every application master

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's answer "Keep all other application master support 40-bit width", stated in the project chat on 2026-11-13 and relayed to this repository, which follows the owner's earlier answer "Keep 40-bit width for C910" (NX-DEC-030); confirmed by approval of the pull request that adds this record |
| Date | 2026-11-13 |
| Requirements | NX-REQ-029, NX-REQ-101 |
| Task | [KOS-NEXUS-008](../tasks/KOS-NEXUS-008/TASK.md) |
| Evidence | Section 4 of [MEMORY_ARCHITECTURE.md](../architecture/MEMORY_ARCHITECTURE.md); NX-REQ-029 and NX-REQ-101 in [REQUIREMENTS.md](../requirements/REQUIREMENTS.md) |

Context: NX-DEC-026 selected the 40-bit application address width and NX-DEC-030 recorded that the owner confirmed the C910 at 40 bits, while the check for every other application master stayed OPEN (NX-REQ-029, NX-ARCH-GAP-003). AC-015 requires the width to be confirmed against the configured CPU and all DMA masters. The owner then stated that all the other application masters support a 40-bit width.

Decisions:

1. Every application master supports a 40-bit address: the C910, the ISP, the NPU, the camera DMA, the display controller, the two Ethernet MACs, the storage DMA and the DMA controller (the masters of section 4.3 of MEMORY_ARCHITECTURE). Owner: all other application masters support the 40-bit width.
2. NX-REQ-029 is SELECTED and NX-ARCH-GAP-003 is CLOSED. The confirmation is an owner statement. The address width of each master's AXI interface, with its source, is not recorded in the repository (NX-ARCH-OI-001), and the repository does not check it.
3. The order of the two steps in AC-015 is met: the map was approved by NX-DEC-030 and the width is now confirmed for every master by this record.
4. If a master is found that cannot generate 40-bit addresses, this decision is not silently changed: a new decision record supersedes it, NX-DEC-026 or NX-DEC-030, or names the master change.

Alternatives considered: Keep the confirmation OPEN until each master's RTL or specification is read (the recommended procedure of section 4.2 of MEMORY_ARCHITECTURE). The owner chose to confirm now.

Rationale: Owner answer as listed. No further rationale was recorded.

Consequences: The map is no longer approved ahead of an open width check. A later contradiction by RTL evidence needs a new decision record. The 128-bit C910 AXI interface (NX-REQ-056) and the other interface parameters stay PROPOSED, and the DDR4 window above 4 GiB relies on every master presenting the high address bits.

## History

| Date | Change |
|---|---|
| 2026-11-13 | Record created with label SELECTED. |
