# NX-DEC-034: Secure interconnect parameters and secure address-space attributes

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's answers of 2026-11-13, relayed to this repository: "security software runs from the ROM" (the security SRAM has no execute permission) and acceptance of the secure interconnect as written in NX-REQ-033 (32-bit address, 32-bit data, 2 outstanding reads and 2 outstanding writes); confirmed by approval of the pull request that adds this record |
| Date | 2026-11-13 |
| Requirements | NX-REQ-033, NX-REQ-119 |
| Task | [KOS-NEXUS-008](../tasks/KOS-NEXUS-008/TASK.md) |
| Evidence | NX-REQ-033 and NX-REQ-119 in [REQUIREMENTS.md](../requirements/REQUIREMENTS.md); sections 3 and 3.1 of [ADDRESS_MAP.md](../architecture/ADDRESS_MAP.md) and [secure_map.yaml](../architecture/maps/secure_map.yaml); section 6.4 of [MEMORY_ARCHITECTURE.md](../architecture/MEMORY_ARCHITECTURE.md) |

Context: The secure interconnect parameters of NX-REQ-033 came from the A0 draft and were not owner-selected, and the access attributes of the secure address space were open (NX-ARCH-OI-021). The repository proposed attributes in NX-REQ-119 and showed that the whole secure map fits in 32 bits, and asked the owner about the execute permission of the security SRAM and about the parameters of NX-REQ-033.

Decisions:

1. NX-REQ-033 is SELECTED as written: the secure AXI interconnect uses a 32-bit address width, a 32-bit data width and 2 outstanding reads and 2 outstanding writes. Owner: accepted as written.
2. NX-REQ-119 is SELECTED as held in secure_map.yaml: no secure region is cacheable; the security ROM and the OSPI NOR secure aperture are read and execute with no write; the security SRAM is read and write with no execute because security software runs from the ROM; the security peripheral windows are read and write device memory; the application boot window is read and write with no execute; an unmapped or reserved secure address returns DECERR and a forbidden access returns SLVERR. Owner: security software runs from the ROM.
3. NX-REQ-117 and NX-REQ-118 (register conventions and block register layouts) are not part of this decision and stay PROPOSED, with NX-ARCH-OI-039.
4. NX-ARCH-OI-021 stays OPEN for the privilege levels, lock states and per-register policy of the secure space, and for the security interrupt and fault-response details. The width and clock conversion between the secure AXI and AXI-3 stays OPEN (NX-ARCH-OI-038).
5. The decision makes no security claim: the attributes are properties of the address map, and a permission check in RTL is not shown by this record.

Alternatives considered: Execute permission on the security SRAM (offered; not chosen); changing the parameters of NX-REQ-033 (offered; not chosen).

Rationale: Owner answers as listed. No further rationale was recorded.

Consequences: A change to the secure width, the data width, the outstanding counts, a secure region permission or cacheability needs a new decision record. The NOR aperture keeps its read and execute permission; what runs from it is not defined by this record. The map checker (`scripts/check_address_maps.py`) stays structural and does not show that an attribute is right.

## History

| Date | Change |
|---|---|
| 2026-11-13 | Record created with label SELECTED. |
