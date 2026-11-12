# NX-DEC-026: 40-bit application address width

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's answer "Select 40-bit by owner decision" to the question on how the 40-bit application address width (NX-ARCH-GAP-003) is to be handled, stated in the project chat on 2026-11-12 and relayed to this repository; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-12 |
| Requirements | NX-REQ-101 |
| Task | [KOS-NEXUS-008](../tasks/KOS-NEXUS-008/TASK.md) |
| Evidence | NX-REQ-101 and NX-REQ-029 in [REQUIREMENTS.md](../requirements/REQUIREMENTS.md); section 4 of [MEMORY_ARCHITECTURE.md](../architecture/MEMORY_ARCHITECTURE.md) |

Context: The proposed application address map of the A0 draft (section 9.6) assumes a 40-bit address. The width was never confirmed against the exact C910 RTL configuration (NX-ARCH-GAP-003, NX-REQ-029), and the C910 configuration cannot be checked from the planning environment. AC-015 requires the width to be confirmed against the configured CPU and all DMA masters before the address map is marked SELECTED. The owner was offered two ways to proceed: keep 40 bits PROPOSED with a verification procedure, or select 40 bits now.

Decisions:

1. The application address width is 40 bits (NX-REQ-101). Owner: SELECTED.
2. The decision selects the width only. It does not select the application address map: the region bases and apertures stay PROPOSED (NX-REQ-053), and AC-015 still applies before the map is marked SELECTED.
3. NX-REQ-029 (confirm the width against the selected C910 configuration and document the resulting constraints) stays OPEN. The confirmation is now a verification of a selected width, with the procedure and owner in section 4 of [MEMORY_ARCHITECTURE.md](../architecture/MEMORY_ARCHITECTURE.md).
4. If the confirmation shows that the C910 configuration or any application master cannot generate 40-bit addresses, this decision is not silently changed: a new decision record supersedes it.

Alternatives considered: Keep the width PROPOSED with a deciding procedure (the recommended option). The owner chose to select it now.

Rationale: Owner answer as listed. No further rationale was recorded.

Consequences: Every application-domain address in the architecture is 40 bits wide. The DDR4 window of the proposed map (0x10_0000_0000 to 0x1F_FFFF_FFFF) fits in 40 bits, and the C910 and every application-fabric master, including the DMA controller of NX-DEC-025, must present 40-bit addresses. The secure address space is separate and keeps its own 32-bit width (NX-REQ-033). NX-ASM-001 is rewritten to refer to this decision; NX-ARCH-GAP-003 stays OPEN until the confirmation is recorded.

## History

| Date | Change |
|---|---|
| 2026-11-12 | Record created for KOS-NEXUS-008 with label SELECTED. |
