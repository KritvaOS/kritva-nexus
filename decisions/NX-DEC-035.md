# NX-DEC-035: DDR4 ingress and fabric behaviour approved as proposed

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's answer "Approve all as proposed" of 2026-11-14 to the question on the PROPOSED DDR4 ingress and fabric behaviour items of KOS-NEXUS-007, relayed to this repository; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-14 |
| Requirements | NX-REQ-030, NX-REQ-076, NX-REQ-077, NX-REQ-078, NX-REQ-079, NX-REQ-080, NX-REQ-081 |
| Task | [KOS-NEXUS-007](../tasks/KOS-NEXUS-007/TASK.md) |
| Evidence | NX-REQ-030 and NX-REQ-076 to NX-REQ-081 in [REQUIREMENTS.md](../requirements/REQUIREMENTS.md); sections 4 and 6 of [INTERCONNECT_SPECIFICATION.md](../architecture/INTERCONNECT_SPECIFICATION.md) |

Context: The DDR4 controller ingress (NX-ARCH-GAP-004) and the fabric behaviour and bridge details (NX-ARCH-OI-004, NX-ARCH-OI-033, NX-ARCH-OI-034) were PROPOSED by this repository for the owner's review.

Decisions:

1. NX-REQ-030, NX-REQ-076, NX-REQ-077 and NX-REQ-078 are SELECTED as in section 4 of the interconnect specification: one 256-bit AXI4 ingress port at 500 MHz from the Memory Access Crossbar to the DDR4 controller, derived for one x32 DDR4-3200 channel with a 70% sustained fraction and the bandwidth budgets of section 4.4, and four QoS classes in priority order (display, Ethernet DMA, C910, NPU and other DMA) with starvation prevention for the lowest class.
2. NX-REQ-079, NX-REQ-080 and NX-REQ-081 are SELECTED as in section 6: AXI4 on the fabrics with decode by the application address map and DECERR for an unmapped address, a C910-to-APB timeout of 1024 bridge-clock cycles with SLVERR, one outstanding access per APB target with backpressure and the AXI ID returned, and APB4 on APB-0 and APB-1.
3. NX-ARCH-GAP-004, NX-ARCH-OI-004, NX-ARCH-OI-005, NX-ARCH-OI-033 and NX-ARCH-OI-034 are CLOSED.
4. NX-REQ-049 (the Memory Access Crossbar), NX-REQ-064 (the DDR4-3200 target), NX-REQ-050 to NX-REQ-052 (fabric roles, master placement, APB bridge parameters) and NX-REQ-093 (DMA placement) are not part of this decision and stay PROPOSED; the ingress of decision 1 assumes the crossbar.
5. The decision makes no performance claim: the figures are sizing arithmetic and no bandwidth, latency or timing result exists.

Alternatives considered: Approve the DDR4 ingress only; change values before approving (both offered; not chosen).

Rationale: Owner answer as listed. No further rationale was recorded.

Consequences: A change to a selected figure or behaviour needs a new decision record. If the owner later changes the crossbar (NX-REQ-049) or the DDR4 target (NX-REQ-064), the ingress sizing is repeated.

## History

| Date | Change |
|---|---|
| 2026-11-14 | Record created with label SELECTED. |
