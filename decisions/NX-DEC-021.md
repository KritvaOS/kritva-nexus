# NX-DEC-021: C910 access to APB peripherals through AXI-0 and AXI-3

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's choice of Option A for NX-ARCH-GAP-001, stated in the project chat on 2026-11-09 and relayed to this repository; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-09 |
| Requirements | NX-REQ-067; narrows NX-REQ-027 |
| Task | [KOS-NEXUS-007](../tasks/KOS-NEXUS-007/TASK.md) |
| Evidence | Options and recommendation in [INTERCONNECT_SPECIFICATION.md](../architecture/INTERCONNECT_SPECIFICATION.md) section 3 |

Context: NX-ARCH-GAP-001 left the C910 access path to the APB peripherals undefined. The interconnect specification set out three options: A, the C910 reaches the APB bridges through AXI-0, an AXI fabric bridge from AXI-0 to AXI-3, AXI-3 decode and the AXI-to-APB interconnects; B, the APB bridges as direct slaves of AXI-0; C, a separate C910 peripheral port (unverified).

Alternatives considered: Option B and Option C, as described in the interconnect specification section 3.2.

Rationale: Owner stated: "GAP-001 - Option -A". No further rationale was recorded; the specification gives the advantages and drawbacks of each option.

Consequences: The route is selected. The following are not decided by this record and stay PROPOSED or OPEN: the error-response mapping, timeout policy, ordering, burst handling, outstanding-transaction limits, the trusted address-window access control, reset behaviour, whether width conversion and the clock crossing are one bridge, the protocol version of AXI-3 and the APB bridges, and whether any master other than the C910 needs the path. The choice stays subject to the C910 configuration check (NX-ARCH-OI-001). NX-ARCH-GAP-001 is therefore narrowed, not closed, until those items are decided.

## History

| Date | Change |
|---|---|
| 2026-11-09 | Record created for KOS-NEXUS-007 with label SELECTED. |
