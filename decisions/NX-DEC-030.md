# NX-DEC-030: Approval of the memory architecture proposals of KOS-NEXUS-008

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's review answers of 2026-11-13, relayed to this repository: "Keep 40-bit width for C910", "You can split Peripheral register split" and "Other thing are approved", with the owner's choices "All PROPOSED architecture items", "C910 only; other masters still to confirm" and "Propose a split as PROPOSED, you review"; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-13 |
| Requirements | NX-REQ-028, NX-REQ-053, NX-REQ-054, NX-REQ-102, NX-REQ-103, NX-REQ-104, NX-REQ-106, NX-REQ-107, NX-REQ-108 |
| Task | [KOS-NEXUS-008](../tasks/KOS-NEXUS-008/TASK.md) |
| Evidence | The requirement rows in [REQUIREMENTS.md](../requirements/REQUIREMENTS.md); [MEMORY_ARCHITECTURE.md](../architecture/MEMORY_ARCHITECTURE.md); [ADDRESS_MAP.md](../architecture/ADDRESS_MAP.md) and the two map files |

Context: After NX-DEC-026, NX-DEC-027 and NX-DEC-029, the application address map, the secure address map, the memory-class access attributes, the coherency and IOMMU position, the unmapped-access policy, the boot window, the mailbox and the isolation rules were still PROPOSED. The owner reviewed the architecture and answered that the 40-bit width is kept for the C910, that the peripheral register space may be split by proposal, and that the other items are approved. The owner chose to select all the PROPOSED architecture items, to confirm the C910 only, and to review the peripheral register split as a proposal before selecting it.

Decisions:

1. NX-REQ-028, NX-REQ-053, NX-REQ-054, NX-REQ-102, NX-REQ-103, NX-REQ-104, NX-REQ-106, NX-REQ-107 and NX-REQ-108 are SELECTED. The application and secure address maps, with every region's base, size and access attributes as held in the two map files, are SELECTED. Owner: the other items are approved.
2. The 40-bit application address width of NX-DEC-026 is kept, and the owner confirms that the C910 is used at 40 bits. NX-REQ-029 and NX-ARCH-GAP-003 stay OPEN for every other application master, with the procedure and owner of section 4 of MEMORY_ARCHITECTURE. Owner: keep 40-bit width for C910.
3. AC-015 requires the width to be confirmed against the C910 and every application master before the application map is marked SELECTED. The owner approved the map before the confirmation for the other masters. This decision records that order as an owner decision and does not hide the open check. If any application master cannot generate 40-bit addresses, a new decision record supersedes this decision or NX-DEC-026.
4. The peripheral register space is split by a PROPOSED requirement and PROPOSED map records, which the owner reviews first (NX-ARCH-OI-036). The split is not part of this decision.
5. The following stay OPEN: the attachment of the two crossings, the mailbox register layout, message format, interrupt directions and validation rule (NX-ARCH-OI-037); the secure access attributes (NX-ARCH-OI-021); the secure address width (NX-REQ-033, PROPOSED); and the PSRAM, NOR and on-chip memory organisation (NX-ARCH-OI-006, NX-ARCH-OI-007). NX-ARCH-GAP-002 and NX-ARCH-OI-003 are CLOSED. The execute permission of the NOR window, which NX-DEC-029 left PROPOSED, is SELECTED with NX-REQ-102.

Alternatives considered: Select everything except the address map values (the access policy, boot window, mailbox and isolation rules only); select only items the owner lists. The owner chose to select all the PROPOSED architecture items.

Rationale: Owner answers as listed. No further rationale was recorded.

Consequences: The memory-architecture requirements are SELECTED, so a change to a base, an aperture, an attribute, a crossing or an isolation rule needs a new decision record, not a change request. The map checker (`scripts/check_address_maps.py`) stays structural and does not show that a value is right. The C910 confirmation is an owner statement; the RTL configuration source is not yet recorded (NX-ARCH-OI-001). The map is SELECTED while the width of the other masters is unconfirmed, which is the risk named in decision 3.

## History

| Date | Change |
|---|---|
| 2026-11-13 | Record created with label SELECTED. |
