# NX-DEC-025: 32-channel general-purpose DMA controller

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's statement "32 channel DMA" with a feature list, and the owner's answers to three questions on the label, the placement and the feature wording, stated in the project chat on 2026-11-11 and relayed to this repository; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-11 |
| Requirements | NX-REQ-092 |
| Task | [KOS-NEXUS-007](../tasks/KOS-NEXUS-007/TASK.md) |
| Evidence | Requirements NX-REQ-093 to NX-REQ-100 in [REQUIREMENTS.md](../requirements/REQUIREMENTS.md); section 6 of [SYSTEM_ARCHITECTURE.md](../architecture/SYSTEM_ARCHITECTURE.md) |

Context: The register and the architecture named only per-peripheral DMA masters (camera, storage, peripheral and I2S, and the Ethernet MAC descriptor DMA) and no general-purpose DMA controller or channel count. The owner asked for a 32-channel DMA controller and supplied a feature list: CPU offloading, multiple independent channels, four transfer directions, burst, cycle-stealing and transparent modes, data widths of 8 to 128 bits with increment, decrement and fixed addressing, scatter-gather, priority arbitration, completion and error interrupts, and operation while the core sleeps. The owner was asked three questions and answered as recorded below.

Decisions:

1. The SoC includes a general-purpose DMA controller with 32 independent channels (NX-REQ-092). Owner: record as SELECTED on approval.
2. The features of the owner's list are written as PROPOSED requirements NX-REQ-093 to NX-REQ-100, adapted to AXI: bursts have a configurable length and a limit on consecutive bursts instead of holding the bus; cycle stealing becomes one beat per arbitration; transparent mode becomes background transfers at the lowest priority level, with no detection of CPU idle cycles; priority arbitration uses per-channel priority, round-robin among equal priorities and the QoS class of NX-REQ-078; the 128-bit data width is not carried because the chosen fabric is 64 bits wide; sleep-mode operation depends on the OPEN power-domain and always-on definitions (NX-REQ-060, NX-REQ-031). Owner: adapt to AXI as PROPOSED.
3. The DMA controller master is placed on AXI-3 as the peripheral and I2S DMA master of NX-REQ-051. The owner chose AXI-3 among AXI-3, AXI-0 and AXI-2. The placement is written as PROPOSED (NX-REQ-093) because the fabric partition it depends on is PROPOSED (NX-REQ-050, NX-REQ-051). Owner: AXI-3.

Alternatives considered: Record the controller and channel count as PROPOSED; place the master on AXI-0 (128-bit, next to the C910 and the memory path) or on AXI-2 (128-bit multimedia fabric); copy the feature list unchanged. The owner chose none of these.

Rationale: Owner answers as listed. No further rationale was recorded.

Consequences: The DMA controller is a new AXI-3 master and its register window is a new peripheral target; the address map is held by KOS-NEXUS-008. Memory-to-memory copies cross AXI-3 (64-bit) and the Memory Access Crossbar; their throughput is not quantified. The DDR4 bandwidth budget (NX-REQ-077) has no DMA line, so DMA traffic falls under the "NPU and other DMA" class (NX-REQ-078) and the unallocated headroom until a change request revises the budget. Peripheral request mapping, descriptor format, memory coherency, the DMA power domain and wake-up are tracked as NX-ARCH-OI-035. A change to the channel count needs a new decision record. The datasheet and its diagrams follow in a separate pull request. This is a repository decision by an interim, non-independent owner and carries no kritva-program weight or credit.

## History

| Date | Change |
|---|---|
| 2026-11-11 | Record created for KOS-NEXUS-007 with label SELECTED. |
