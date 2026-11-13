# NX-DEC-029: Boot window scope, mailbox rule and NOR window access

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's review answers of 2026-11-13, relayed to this repository: the boot window has System SRAM access only and no DDR4 access for the security core; the mailbox keeps NX-REQ-072 intact; the NOR window is cacheable and read-only, with program and erase only through the controller registers; and the owner's answer "New decision NX-DEC-029, split out SELECTED requirements" on how to record them; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-13 |
| Requirements | NX-REQ-109, NX-REQ-110, NX-REQ-111 |
| Task | [KOS-NEXUS-008](../tasks/KOS-NEXUS-008/TASK.md) |
| Evidence | NX-REQ-109 to NX-REQ-111 in [REQUIREMENTS.md](../requirements/REQUIREMENTS.md); sections 5 and 6 of [MEMORY_ARCHITECTURE.md](../architecture/MEMORY_ARCHITECTURE.md) |

Context: During the owner review of the memory architecture the owner answered three questions about proposals made in NX-REQ-102, NX-REQ-106, NX-REQ-107 and NX-REQ-108 (themselves PROPOSED): whether the security core may reach DDR4 through the boot window, whether the mailbox window keeps the access rule of NX-REQ-072, and whether the NOR window is cacheable and read-only with program and erase only through the controller registers. The owner confirmed all three and asked for them to be recorded as a decision with separate SELECTED requirements.

Decisions:

1. The security core reaches the application domain only through the System SRAM region of the application map; it has no access to DDR4 or to any other application region (NX-REQ-109). Owner: boot window has System SRAM access only, no DDR4 for the security core.
2. The application-side mailbox window keeps NX-REQ-072 intact: secure resources stay unreachable on the C910-to-APB path, the mailbox window is the only security-related window on that path, and it gives no route to the secure map or to any other security peripheral (NX-REQ-110). Owner: keep the mailbox rule NX-REQ-072.
3. The NOR window of the application map is cacheable for the C910 and read-only for the application domain, and program and erase of the NOR device go only through the NOR controller registers on the peripheral register path, under the window policy of NX-REQ-072 (NX-REQ-111). Owner: the NOR window is right as cacheable and read-only, with program and erase only through the controller registers.
4. Everything else in NX-REQ-102, NX-REQ-106, NX-REQ-107 and NX-REQ-108 stays PROPOSED: the other memory-class attributes, the alias in the secure map, the bridge attachment, the use before C910 reset release, the mailbox registers and interrupts, and the isolation rules. The map bases and apertures stay PROPOSED (NX-REQ-053, NX-REQ-054).

Alternatives considered: Keep the three points PROPOSED with a note of owner confirmation; record them only in the review note. The owner chose a decision record.

Rationale: Owner answers as listed. No further rationale was recorded.

Consequences: Three requirements move from PROPOSED text to SELECTED requirements. Reaching DDR4 from the security core later, a second application window for the security core, a writable or executable-from-window change to the NOR window, or program and erase through the window needs a new decision record. The SELECTED statements say nothing about how the bridge attaches or how the controller registers are laid out; those stay with NX-ARCH-OI-037 and NX-ARCH-OI-036.

## History

| Date | Change |
|---|---|
| 2026-11-13 | Record created with label SELECTED. |
