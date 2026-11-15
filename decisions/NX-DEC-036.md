# NX-DEC-036: Fabric structure, master placement and connectivity matrix approved

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's answers of 2026-11-15 to the questions on the PROPOSED fabric items and the connectivity matrix of KOS-NEXUS-007 ("Approve all as proposed, with the C910 path added"; the C910 path to the AXI-1 local memories "AXI-0 to AXI-1 bridge, rw to all three"; System SRAM on AXI-0 and the OSPI controllers on AXI-3), relayed to this repository; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-15 |
| Requirements | NX-REQ-049, NX-REQ-050, NX-REQ-051, NX-REQ-052, NX-REQ-064, NX-REQ-093, NX-REQ-120, NX-REQ-121 |
| Task | [KOS-NEXUS-007](../tasks/KOS-NEXUS-007/TASK.md) |
| Evidence | The rows of these requirements in [REQUIREMENTS.md](../requirements/REQUIREMENTS.md); [connectivity.yaml](../architecture/maps/connectivity.yaml); section 7 of [INTERCONNECT_SPECIFICATION.md](../architecture/INTERCONNECT_SPECIFICATION.md) |

Context: After NX-DEC-035 the Memory Access Crossbar, the fabric roles and widths, the master placement, the APB bridge parameters, the DDR4-3200 target, the DMA controller placement and the connectivity matrix of KOS-NEXUS-007 were PROPOSED, with the attachment of System SRAM and the OSPI controllers and the C910 path to the AXI-1 local memories OPEN (NX-ARCH-OI-040).

Decisions:

1. NX-REQ-049 (Memory Access Crossbar), NX-REQ-050 (fabric roles and widths, 400 to 600 MHz), NX-REQ-051 (master placement), NX-REQ-052 (APB bridge parameters), NX-REQ-064 (DDR4-3200 target) and NX-REQ-093 (DMA controller placement on AXI-3) are SELECTED as written.
2. NX-REQ-120 is SELECTED: the master-to-memory connectivity of `architecture/maps/connectivity.yaml` (22 links before this decision, 25 after it), with default deny and the rules of the requirement.
3. The C910 has read and write access to the camera frame pool, the ISP SRAM and the NPU SRAM through an AXI fabric bridge from AXI-0 to AXI-1 (NX-REQ-121, new, SELECTED). No other master reaches them across a fabric bridge.
4. System SRAM is attached to AXI-0, and the OSPI NOR window and the OSPI PSRAM controllers are attached to AXI-3, so the C910 reaches the NOR and the PSRAM through the AXI-0 to AXI-3 bridge of NX-REQ-067. NX-ARCH-OI-040 is CLOSED.
5. The matrix needs a path from AXI-3 to System SRAM on AXI-0 for the DMA controller and the boot window bridge (NX-REQ-113). That bridge, NX-REQ-122, is PROPOSED here for the owner's review; it is not decided. Until it is, the links of the DMA controller and of the boot window bridge to System SRAM have no listed bridge behind them.
6. The behaviour of memory accesses through the fabric bridges (bursts, ordering, width conversion, protection, timeout, reset) is not decided. NX-REQ-072 to NX-REQ-075 are decided for the C910 APB register accesses and are not extended. NX-ARCH-OI-041 (OPEN) tracks it.
7. The decision makes no performance, security or timing claim. The link records name the requirement that gives each link its need; requirements named there keep their own labels.

Alternatives considered: Approve the matrix and fabric items except the DDR4-3200 target; record only the C910 path and leave approval for later; read-only access to the frame pool; System SRAM and the OSPI controllers all on AXI-3; a different C910 route to the AXI-1 memories (all offered; not chosen).

Rationale: Owner answers as listed. No further rationale was recorded.

Consequences: A change to a selected item needs a new decision record. The AXI-3 to AXI-0 bridge and the bridge behaviour for memory accesses are the remaining open points of KOS-NEXUS-007.

## History

| Date | Change |
|---|---|
| 2026-11-15 | Record created with label SELECTED. |
