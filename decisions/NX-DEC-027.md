# NX-DEC-027: Two controlled crossings between the security and application domains

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's answers "Yes, one controlled window" and "Yes, one mailbox interface" to two questions on the access paths between the security domain and the application domain (NX-ARCH-GAP-002), stated in the project chat on 2026-11-12 and relayed to this repository; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-12 |
| Requirements | NX-REQ-105 |
| Task | [KOS-NEXUS-008](../tasks/KOS-NEXUS-008/TASK.md) |
| Evidence | NX-REQ-105 to NX-REQ-108 in [REQUIREMENTS.md](../requirements/REQUIREMENTS.md); section 5 of [MEMORY_ARCHITECTURE.md](../architecture/MEMORY_ARCHITECTURE.md); section 4 of [ADDRESS_MAP.md](../architecture/ADDRESS_MAP.md) |

Context: The secure and application address spaces are separate spaces on separate interconnects (NX-REQ-032, NX-REQ-034), and the isolation boundary and the permitted access paths were not defined (NX-ARCH-GAP-002, NX-REQ-028). The owner was asked two questions. May the security core reach anything in the application address space? May the application domain reach any secure service? The recommended answer to both was no path, and the owner chose to allow one path in each direction.

Decisions:

1. The boundary between the security domain and the application domain has exactly two controlled crossings (NX-REQ-105). Owner: SELECTED.
2. The first crossing is an access path from the security core into one defined application window, for example to verify or place the boot image. The window is proposed as the System SRAM region of the application map, reached through a secure-to-application bridge (NX-REQ-106, PROPOSED). The owner did not name the window, so its choice, the alias in the secure map and the bridge attachment are PROPOSED.
3. The second crossing is one mailbox interface through which the application domain sends requests to the security domain (NX-REQ-107, PROPOSED). The owner did not define the interface, so its registers, direction of interrupts and validation rule are PROPOSED or OPEN.
4. All other security resources stay unreachable from the application domain, both crossings are default-deny, and an address is interpreted in the space of the interconnect it arrives on (NX-REQ-108, PROPOSED; NX-REQ-034 is unchanged).
5. NX-REQ-028, NX-ARCH-GAP-002 and NX-INT-012 move from OPEN to PROPOSED, because the boundary is now defined by the decision and the proposals. Changing a SELECTED crossing, or adding a third one, needs a new decision record.

Alternatives considered: No crossing in either direction (the recommended option); one crossing in only one direction; deferring the boundary as OPEN. The owner chose one crossing in each direction.

Rationale: Owner answers as listed. No further rationale was recorded.

Consequences: The security core is able to reach one application window, so the isolation argument rests on that window and its bridge being default-deny and on the application domain reaching only the mailbox. Two interfaces are added to the interface register (NX-INT-024 and NX-INT-025). The application side attachment of the bridge and of the mailbox register window is OPEN (NX-ARCH-OI-037, NX-ARCH-OI-036). A secure-side validation rule for mailbox requests is proposed, and no cryptographic or security claim is made from it. The security core could in principle reach DDR4 later; that is not proposed here because DDR4 may not be initialised when the security core runs first (NX-REQ-036), and it needs a change request.

## History

| Date | Change |
|---|---|
| 2026-11-12 | Record created for KOS-NEXUS-008 with label SELECTED. |
