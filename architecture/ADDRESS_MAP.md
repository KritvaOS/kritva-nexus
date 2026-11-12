# Kritva Nexus Address Maps

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-ARCH-004 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Architecture |
| Status | DRAFT (parts 2 and 3 of KOS-NEXUS-008: the proposed application and secure address maps and the two domain crossings; not reviewed or approved) |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.2.1-draft |
| Last Updated | 2026-11-12 |
| Authority | DERIVED (the machine-readable files are the source; not AUTHORITATIVE) |
| Related Tasks / Milestones | KOS-NEXUS-008; NX-M1 |
| Related Documents | [Memory architecture](MEMORY_ARCHITECTURE.md); [application map source](maps/application_map.yaml); [secure map source](maps/secure_map.yaml); [system architecture](SYSTEM_ARCHITECTURE.md); [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md) |

## Purpose

This document shows the application address map and the secure address map for task KOS-NEXUS-008. The maps are held in two machine-readable files, one per address space: [maps/application_map.yaml](maps/application_map.yaml) and [maps/secure_map.yaml](maps/secure_map.yaml). The tables below are copied from those files and are not a second source. If a table and its file differ, the file is the source and the table is corrected.

## 1. Status and rules

1. Both maps are PROPOSED (NX-REQ-053 and NX-REQ-054). The bases and apertures come from sections 9.6 and 7.4 of the [A0 integration draft](A0_INTEGRATION_DRAFT.md); the secure window sizes are proposals of this part. No map is SELECTED, and AC-015 still requires the application address width to be confirmed against the C910 and every application master before the application map is marked SELECTED.
2. The application address width is 40 bits, SELECTED (NX-DEC-026, NX-REQ-101); its confirmation is OPEN (NX-REQ-029, NX-ARCH-GAP-003). The secure address width is 32 bits, PROPOSED (NX-REQ-033).
3. An aperture is a range of addresses, not a memory capacity. The selected capacities are those of the register: the 6 MiB camera frame pool and the 64 KiB security ROM and SRAM. The DDR4, PSRAM and NOR capacities are not selected.
4. Any address that no region lists is unmapped. An access to an unmapped or reserved address returns DECERR, and an access that a region forbids returns SLVERR (NX-REQ-079, NX-REQ-104, PROPOSED).
5. A PROPOSED region changes by a change request: a pull request that edits the file with a changelog entry. Moving to SELECTED needs a decision record.
6. `scripts/check_address_maps.py` checks the two files and these tables (`make check-maps`, also run by `make check` and the address-map-check workflow): file structure and header keys, region keys and labels, unique names, 4 KiB alignment, address-width bounds, ascending order and no overlap inside each space, the boot-window alias against its application region, the mailbox region, the NX-REQ identifiers against the register, and every table row against its file. A PASS does not show that a base, size or attribute is right or that the width fits the C910 or any master.

## 2. Application address map (40-bit, PROPOSED)

Source: [maps/application_map.yaml](maps/application_map.yaml). The attributes follow NX-REQ-102. The System SRAM region is also the target of the boot window crossing (section 4).

| Region | First address | Last address | Size | C910 cacheable | Permissions | Label | NX-REQ |
|---|---|---|---|---|---|---|---|
| System SRAM | 0x00_0000_0000 | 0x00_000F_FFFF | 1 MiB | No | rwx | PROPOSED | 053, 102 |
| Camera frame pool | 0x00_1000_0000 | 0x00_10FF_FFFF | 16 MiB | No | rw- | PROPOSED | 005, 047, 053, 102 |
| ISP SRAM | 0x00_1100_0000 | 0x00_11FF_FFFF | 16 MiB | No | rw- | PROPOSED | 047, 053, 102 |
| NPU SRAM | 0x00_1200_0000 | 0x00_13FF_FFFF | 32 MiB | No | rw- | PROPOSED | 047, 053, 102 |
| Reserved | 0x00_1400_0000 | 0x00_1FFF_FFFF | 192 MiB | No | --- | PROPOSED | 053, 104 |
| Peripheral register space | 0x00_4000_0000 | 0x00_4FFF_FFFF | 256 MiB | No | rw- | PROPOSED | 053, 072, 102 |
| OSPI NOR window | 0x00_6000_0000 | 0x00_6FFF_FFFF | 256 MiB | Yes | r-x | PROPOSED | 004, 053, 102 |
| OSPI PSRAM | 0x00_7000_0000 | 0x00_7FFF_FFFF | 256 MiB | Yes | rwx | PROPOSED | 003, 053, 102 |
| DDR4 | 0x10_0000_0000 | 0x1F_FFFF_FFFF | 64 GiB | Yes | rwx | PROPOSED | 002, 053, 076, 102 |

Notes. The DDR4 window starts at 0x10_0000_0000 and needs a master that generates 40-bit addresses; the width check of section 4 of the memory architecture covers it. The frame-pool aperture is 16 MiB and its usable capacity is the SELECTED 6 MiB. The ISP SRAM and NPU SRAM windows are apertures. The peripheral register space is one range; how it is divided among the peripheral instances, including the register window of the DMA controller (NX-REQ-092, NX-REQ-093), is OPEN (NX-ARCH-OI-036). The memory-class attributes are explained in section 6 of the memory architecture.

## 3. Secure address map (32-bit, PROPOSED)

Source: [maps/secure_map.yaml](maps/secure_map.yaml). The access attributes of the secure space are not defined (NX-ARCH-OI-021, OPEN), so the table has no attribute column.

| Region | First address | Last address | Size | Label | NX-REQ |
|---|---|---|---|---|---|
| Security ROM | 0x0000_0000 | 0x0000_FFFF | 64 KiB | PROPOSED | 010, 054 |
| Security SRAM | 0x0001_0000 | 0x0001_FFFF | 64 KiB | PROPOSED | 011, 054 |
| OSPI NOR secure aperture | 0x1000_0000 | 0x1FFF_FFFF | 256 MiB | PROPOSED | 038, 054 |
| AES | 0x2000_0000 | 0x2000_FFFF | 64 KiB | PROPOSED | 013, 054 |
| SHA | 0x2001_0000 | 0x2001_FFFF | 64 KiB | PROPOSED | 014, 054 |
| Asymmetric cryptography | 0x2002_0000 | 0x2002_FFFF | 64 KiB | PROPOSED | 035, 054 |
| eFuse | 0x2003_0000 | 0x2003_FFFF | 64 KiB | PROPOSED | 012, 054 |
| Key management | 0x2004_0000 | 0x2004_FFFF | 64 KiB | PROPOSED | 054 |
| Security control | 0x2005_0000 | 0x2005_FFFF | 64 KiB | PROPOSED | 054 |
| Security interrupt controller | 0x2006_0000 | 0x2006_FFFF | 64 KiB | PROPOSED | 054, 057 |
| Security timer and watchdog | 0x2007_0000 | 0x2007_FFFF | 64 KiB | PROPOSED | 054 |
| OSPI registers | 0x2008_0000 | 0x2008_FFFF | 64 KiB | PROPOSED | 054 |
| Mailbox (secure side) | 0x2009_0000 | 0x2009_FFFF | 64 KiB | PROPOSED | 105, 107, 054 |
| Application boot window | 0x3000_0000 | 0x300F_FFFF | 1 MiB | PROPOSED | 105, 106, 054 |

Notes. The security ROM and SRAM capacities of 64 KiB are SELECTED; their bases are proposed. The secure NOR aperture is a range for the security core path and does not select a NOR capacity. The interrupt architecture of the security interrupt controller is OPEN (NX-REQ-057). The mailbox window and the application boot window are the two controlled crossings of NX-DEC-027 (section 4); the boot window is an alias of the 1 MiB application System SRAM aperture and is not a memory of the security domain.

## 4. Two separate address spaces and two controlled crossings

The application and secure address spaces are separate spaces on separate interconnects (NX-REQ-028, NX-REQ-033, NX-REQ-034). Several numerical ranges of the two maps coincide, for example the secure NOR aperture at 0x1000_0000 and the application camera frame pool at 0x00_1000_0000. That is not a conflict: an address is interpreted in the address space of the interconnect it arrives on (NX-REQ-108), no master reaches both spaces through one decode, and the two files are checked separately.

The boundary has exactly two controlled crossings (NX-DEC-027, NX-REQ-105, SELECTED), and both are default-deny (NX-REQ-108, PROPOSED).

| Crossing | Direction | Secure map | Application map | Label | Records |
|---|---|---|---|---|---|
| Boot window | Security core to application | Application boot window, 0x3000_0000 to 0x300F_FFFF (1 MiB alias) | System SRAM, 0x00_0000_0000 to 0x00_000F_FFFF; no other application region | SELECTED crossing; PROPOSED window | NX-REQ-105, NX-REQ-106 |
| Mailbox | Application to security | Mailbox (secure side), 0x2009_0000 to 0x2009_FFFF | Mailbox window in the peripheral register space, base OPEN (NX-ARCH-OI-036) | SELECTED crossing; PROPOSED mailbox | NX-REQ-105, NX-REQ-107 |

The application side attachment of the bridge to an application fabric, the mailbox register layout and message format, the interrupt directions and the secure-side validation rule are OPEN (NX-ARCH-OI-037). The security core does not reach DDR4 in this proposal. All other secure regions stay unreachable from the application space (NX-REQ-034).

## 5. Open items

| Item | Label | Records | Owner |
|---|---|---|---|
| Confirmation of the 40-bit width against the C910 and every application master | OPEN | NX-REQ-029, NX-ARCH-GAP-003 | Dinesh |
| Attachment of the two crossings, mailbox layout and validation rule | OPEN | NX-ARCH-OI-037 | Dinesh |
| Division of the peripheral register space among instances, including the DMA controller registers | OPEN | NX-ARCH-OI-036 | Dinesh |
| Access attributes and finalisation of the secure map | OPEN | NX-ARCH-OI-021 | Dinesh |
| PSRAM, NOR and on-chip memory capacities and organisation | OPEN | NX-ARCH-OI-006, NX-ARCH-OI-007 | Dinesh |
| Review of the map values and attributes by the owner (the checker is structural only) | OPEN | NX-REQ-053, NX-REQ-054, NX-REQ-102 | Dinesh |

## History

| Version | Date | Change |
|---|---|---|
| 0.1.0-draft | 2026-11-12 | First part 2 draft for KOS-NEXUS-008: the two map files and their tables |
| 0.2.0-draft | 2026-11-12 | Part 3: the two controlled crossings (NX-DEC-027) added to the secure map and the separation section |
| 0.2.1-draft | 2026-11-12 | The map checker exists (scripts/check_address_maps.py); rule 6 and the open items updated |
