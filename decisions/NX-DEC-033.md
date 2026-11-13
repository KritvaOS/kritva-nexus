# NX-DEC-033: Approval of the peripheral register windows, the crossing details and the interrupt controller baseline

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's answer "Approved both" on 2026-11-13, relayed to this repository, approving the two sets of PROPOSED items offered for review: the peripheral register windows (NX-REQ-112) and the crossing details with the application interrupt controller baseline (NX-REQ-113 to NX-REQ-116); confirmed by approval of the pull request that adds this record |
| Date | 2026-11-13 |
| Requirements | NX-REQ-112, NX-REQ-113, NX-REQ-114, NX-REQ-115, NX-REQ-116 |
| Task | [KOS-NEXUS-008](../tasks/KOS-NEXUS-008/TASK.md) |
| Evidence | NX-REQ-112 to NX-REQ-116 in [REQUIREMENTS.md](../requirements/REQUIREMENTS.md); section 2.1 of [ADDRESS_MAP.md](../architecture/ADDRESS_MAP.md) and [peripheral_windows.yaml](../architecture/maps/peripheral_windows.yaml); sections 5.4 and 5.5 of [MEMORY_ARCHITECTURE.md](../architecture/MEMORY_ARCHITECTURE.md) |

Context: After NX-DEC-030 to NX-DEC-032, the division of the peripheral register space (NX-REQ-112), the secure-to-application bridge attachment (NX-REQ-113), the mailbox layout, messages and validation rule (NX-REQ-114), the mailbox interrupts (NX-REQ-115) and the application interrupt controller baseline (NX-REQ-116) were PROPOSED by this repository for the owner's review. The owner approved both sets without changes.

Decisions:

1. NX-REQ-112 to NX-REQ-116 are SELECTED. The values are those of the files and sections named in the evidence row: the APB-0 and APB-1 windows and the 30 windows of peripheral_windows.yaml, the bridge as one AXI master port on AXI-3 that forwards only the boot-window alias, the mailbox register block with 256-byte request and response buffers, the 16-byte message header and the security-side check, one level-sensitive interrupt in each direction, and the PLIC with 128 sources and the CLINT in APB-1 windows. Owner: approved both.
2. NX-ARCH-OI-036 and NX-ARCH-OI-037 are CLOSED. The register layout of each block, the mailbox allow-list contents, requester authentication, replay and flood protection, the AXI-3 and System SRAM reset domain, the System SRAM attachment point on the fabrics, and the width and clock conversion between the secure AXI and AXI-3 remain OPEN and are tracked by the new NX-ARCH-OI-038 and by NX-ARCH-OI-025.
3. NX-REQ-057 and NX-ARCH-OI-032 stay OPEN for the security and always-on interrupt controllers and for the routing among the three. The AIA is not used in this baseline; changing to the AIA needs a new decision record.
4. The decision makes no security claim. The mailbox validation is a structural rule, and the interrupt claim latency of the PLIC over the APB path is not measured or required here.

Alternatives considered: Change windows or sizes before selecting (offered; not chosen); select the windows only and keep the crossing and interrupt details PROPOSED. The owner approved both sets as proposed.

Rationale: Owner answer as listed. No further rationale was recorded.

Consequences: A change to a window, a size, a register offset, the message format, the buffer sizes, the bridge attachment or the interrupt controller baseline needs a new decision record, not a change request. If the C910 configuration (NX-ARCH-OI-001) does not match a PLIC and a CLINT, a new decision record supersedes this decision. The map checker (`scripts/check_address_maps.py`) stays structural and does not show that a value is right.

## History

| Date | Change |
|---|---|
| 2026-11-13 | Record created with label SELECTED. |
