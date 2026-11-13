# Kritva Nexus Address Maps

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-ARCH-004 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Architecture |
| Status | DRAFT (parts 2 and 3 of KOS-NEXUS-008: the application and secure address maps and the two domain crossings, approved by the owner in NX-DEC-030; the peripheral register windows are PROPOSED; the document itself has no approval record) |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.6.0-draft |
| Last Updated | 2026-11-13 |
| Authority | DERIVED (the machine-readable files are the source; not AUTHORITATIVE) |
| Related Tasks / Milestones | KOS-NEXUS-008; NX-M1 |
| Related Documents | [Memory architecture](MEMORY_ARCHITECTURE.md); [application map source](maps/application_map.yaml); [secure map source](maps/secure_map.yaml); [peripheral windows source](maps/peripheral_windows.yaml); [system architecture](SYSTEM_ARCHITECTURE.md); [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md) |

## Purpose

This document shows the application address map and the secure address map for task KOS-NEXUS-008. The maps are held in two machine-readable files, one per address space: [maps/application_map.yaml](maps/application_map.yaml) and [maps/secure_map.yaml](maps/secure_map.yaml). A third file, [maps/peripheral_windows.yaml](maps/peripheral_windows.yaml), divides the peripheral register space of the application map into windows (section 2.1). The tables below are copied from those files and are not a second source. If a table and its file differ, the file is the source and the table is corrected.

## 1. Status and rules

1. Both maps are SELECTED by the owner's approval (NX-DEC-030, NX-REQ-053 and NX-REQ-054). The bases and apertures come from sections 9.6 and 7.4 of the [A0 integration draft](A0_INTEGRATION_DRAFT.md); the secure window sizes come from this part. A region label covers its base, size and attributes; a capacity keeps the label of its own requirement. AC-015 requires the application address width to be confirmed against the C910 and every application master before the application map is SELECTED. The owner approved the map first (NX-DEC-030) and then confirmed the 40-bit width for the C910 and every other application master (NX-DEC-031, NX-REQ-029), which meets AC-015; the confirmation is an owner statement and the RTL evidence is not recorded (NX-ARCH-OI-001), so a master that cannot generate 40-bit addresses leads to a new decision record.
2. The application address width is 40 bits, SELECTED (NX-DEC-026, NX-REQ-101); its confirmation for every application master is the owner's statement (NX-DEC-031, NX-REQ-029). The secure address width is 32 bits, PROPOSED (NX-REQ-033), and the secure access attributes are OPEN (NX-ARCH-OI-021).
3. An aperture is a range of addresses, not a memory capacity. The selected capacities are those of the register: the 6 MiB camera frame pool and the 64 KiB security ROM and SRAM. The DDR4, PSRAM and NOR capacities are not selected.
4. Any address that no region lists is unmapped. An access to an unmapped or reserved address returns DECERR, and an access that a region forbids returns SLVERR (NX-REQ-079, NX-REQ-104).
5. A SELECTED region changes only by a new decision record. A region added later as PROPOSED changes by a change request: a pull request that edits the file with a changelog entry.
6. `scripts/check_address_maps.py` checks the two files and these tables (`make check-maps`, also run by `make check` and the address-map-check workflow): file structure and header keys, region keys and labels, unique names, 4 KiB alignment, address-width bounds, ascending order and no overlap inside each space, the boot-window alias against its application region, the mailbox region, the division of the peripheral register space into windows (inside the parent region and the named APB window, no overlap, DMA controller, NOR controller and mailbox windows present), the NX-REQ identifiers against the register, and every table row against its file. A PASS does not show that a base, size or attribute is right or that the width fits the C910 or any master.

## 2. Application address map (40-bit, SELECTED)

Source: [maps/application_map.yaml](maps/application_map.yaml). The attributes follow NX-REQ-102 (SELECTED). The System SRAM region is also the target of the boot window crossing (section 4).

| Region | First address | Last address | Size | C910 cacheable | Permissions | Label | NX-REQ |
|---|---|---|---|---|---|---|---|
| System SRAM | 0x00_0000_0000 | 0x00_000F_FFFF | 1 MiB | No | rwx | SELECTED | 053, 102, 109 |
| Camera frame pool | 0x00_1000_0000 | 0x00_10FF_FFFF | 16 MiB | No | rw- | SELECTED | 005, 047, 053, 102 |
| ISP SRAM | 0x00_1100_0000 | 0x00_11FF_FFFF | 16 MiB | No | rw- | SELECTED | 047, 053, 102 |
| NPU SRAM | 0x00_1200_0000 | 0x00_13FF_FFFF | 32 MiB | No | rw- | SELECTED | 047, 053, 102 |
| Reserved | 0x00_1400_0000 | 0x00_1FFF_FFFF | 192 MiB | No | --- | SELECTED | 053, 104 |
| Peripheral register space | 0x00_4000_0000 | 0x00_4FFF_FFFF | 256 MiB | No | rw- | SELECTED | 053, 072, 102, 110 |
| OSPI NOR window | 0x00_6000_0000 | 0x00_6FFF_FFFF | 256 MiB | Yes | r-x | SELECTED | 004, 053, 102, 111 |
| OSPI PSRAM | 0x00_7000_0000 | 0x00_7FFF_FFFF | 256 MiB | Yes | rwx | SELECTED | 003, 053, 102 |
| DDR4 | 0x10_0000_0000 | 0x1F_FFFF_FFFF | 64 GiB | Yes | rwx | SELECTED | 002, 053, 076, 102 |

Notes. The OSPI NOR window is cacheable and read-only, and program and erase go only through the NOR controller registers (SELECTED, NX-REQ-111, NX-DEC-029). The DDR4 window starts at 0x10_0000_0000 and needs a master that generates 40-bit addresses; the width check of section 4 of the memory architecture covers it. The frame-pool aperture is 16 MiB and its usable capacity is the SELECTED 6 MiB. The ISP SRAM and NPU SRAM windows are apertures. The peripheral register space is one range; how it is divided among the peripheral instances, including the register window of the DMA controller (NX-REQ-092, NX-REQ-093), is proposed in section 2.1 (NX-REQ-112, PROPOSED). The memory-class attributes are explained in section 6 of the memory architecture.

## 2.1 Peripheral register windows (PROPOSED)

Source: [maps/peripheral_windows.yaml](maps/peripheral_windows.yaml). The windows divide the application region Peripheral register space (0x00_4000_0000 to 0x00_4FFF_FFFF), which stays SELECTED with its base, size and attributes (NX-REQ-053, NX-REQ-102). The division is PROPOSED (NX-REQ-112, NX-ARCH-OI-036); the owner reviews it before it is selected.

| Window | APB | First address | Last address | Size | Label | NX-REQ |
|---|---|---|---|---|---|---|
| APB-0 (bridge window) | - | 0x00_4000_0000 | 0x00_40FF_FFFF | 16 MiB | PROPOSED | 016, 112 |
| APB-1 (bridge window) | - | 0x00_4100_0000 | 0x00_41FF_FFFF | 16 MiB | PROPOSED | 016, 112 |
| PWM controller | APB-0 | 0x00_4000_0000 | 0x00_4000_FFFF | 64 KiB | PROPOSED | 019, 112 |
| GPIO controller | APB-0 | 0x00_4001_0000 | 0x00_4001_FFFF | 64 KiB | PROPOSED | 020, 112 |
| General-purpose timers | APB-0 | 0x00_4002_0000 | 0x00_4002_FFFF | 64 KiB | PROPOSED | 021, 112 |
| UART0 | APB-0 | 0x00_4003_0000 | 0x00_4003_FFFF | 64 KiB | PROPOSED | 022, 112 |
| UART1 | APB-0 | 0x00_4004_0000 | 0x00_4004_FFFF | 64 KiB | PROPOSED | 022, 112 |
| UART2 | APB-0 | 0x00_4005_0000 | 0x00_4005_FFFF | 64 KiB | PROPOSED | 022, 112 |
| UART3 | APB-0 | 0x00_4006_0000 | 0x00_4006_FFFF | 64 KiB | PROPOSED | 022, 112 |
| I2C0 | APB-0 | 0x00_4007_0000 | 0x00_4007_FFFF | 64 KiB | PROPOSED | 023, 112 |
| I2C1 | APB-0 | 0x00_4008_0000 | 0x00_4008_FFFF | 64 KiB | PROPOSED | 023, 112 |
| I2C2 | APB-0 | 0x00_4009_0000 | 0x00_4009_FFFF | 64 KiB | PROPOSED | 023, 112 |
| I2C3 | APB-0 | 0x00_400A_0000 | 0x00_400A_FFFF | 64 KiB | PROPOSED | 023, 112 |
| SPI master | APB-0 | 0x00_400B_0000 | 0x00_400B_FFFF | 64 KiB | PROPOSED | 024, 112 |
| SPI slave | APB-0 | 0x00_400C_0000 | 0x00_400C_FFFF | 64 KiB | PROPOSED | 025, 112 |
| I2S0 | APB-0 | 0x00_400D_0000 | 0x00_400D_FFFF | 64 KiB | PROPOSED | 026, 112 |
| I2S1 | APB-0 | 0x00_400E_0000 | 0x00_400E_FFFF | 64 KiB | PROPOSED | 026, 112 |
| DMA controller | APB-1 | 0x00_4100_0000 | 0x00_4100_FFFF | 64 KiB | PROPOSED | 092, 093, 112 |
| OSPI NOR controller | APB-1 | 0x00_4101_0000 | 0x00_4101_FFFF | 64 KiB | PROPOSED | 004, 111, 112 |
| OSPI PSRAM controller | APB-1 | 0x00_4102_0000 | 0x00_4102_FFFF | 64 KiB | PROPOSED | 003, 112 |
| DDR4 controller | APB-1 | 0x00_4103_0000 | 0x00_4103_FFFF | 64 KiB | PROPOSED | 002, 112 |
| Clock, reset and power control | APB-1 | 0x00_4104_0000 | 0x00_4104_FFFF | 64 KiB | PROPOSED | 058, 060, 061, 112 |
| Mailbox (application side) | APB-1 | 0x00_4105_0000 | 0x00_4105_FFFF | 64 KiB | PROPOSED | 107, 110, 112 |
| ISP | APB-1 | 0x00_4106_0000 | 0x00_4106_FFFF | 64 KiB | PROPOSED | 045, 112 |
| NPU | APB-1 | 0x00_4107_0000 | 0x00_4107_FFFF | 64 KiB | PROPOSED | 046, 112 |
| Camera interface and DMA | APB-1 | 0x00_4108_0000 | 0x00_4108_FFFF | 64 KiB | PROPOSED | 042, 112 |
| Display controller | APB-1 | 0x00_4109_0000 | 0x00_4109_FFFF | 64 KiB | PROPOSED | 006, 112 |
| Ethernet MAC0 | APB-1 | 0x00_410A_0000 | 0x00_410A_FFFF | 64 KiB | PROPOSED | 008, 112 |
| Ethernet MAC1 | APB-1 | 0x00_410B_0000 | 0x00_410B_FFFF | 64 KiB | PROPOSED | 008, 112 |
| Storage DMA | APB-1 | 0x00_410C_0000 | 0x00_410C_FFFF | 64 KiB | PROPOSED | 051, 112 |
| Application interrupt controller (PLIC) | APB-1 | 0x00_4140_0000 | 0x00_417F_FFFF | 4 MiB | PROPOSED | 057, 112, 116 |
| Application timer and software interrupt (CLINT) | APB-1 | 0x00_4180_0000 | 0x00_4180_FFFF | 64 KiB | PROPOSED | 057, 112, 116 |

Notes. APB-0 carries the peripherals whose counts are SELECTED (NX-REQ-019 to NX-REQ-026, NX-DEC-020) and APB-1 carries the control and block registers; the 16 MiB apertures of the two bridge windows and the 64 KiB size of each window are proposals, not register counts. Each instance has its own window, so a peripheral is never shared between instances in one window except the blocks that the requirements count as one block (PWM, GPIO and the general-purpose timers). The mailbox window (0x00_4105_0000 to 0x00_4105_FFFF) is the only security-related window on the C910-to-APB path (NX-REQ-110) and gives no route to the secure map. The DMA controller window is at 0x00_4100_0000 and the OSPI NOR controller window, the only way to program or erase the NOR device (NX-REQ-111), is at 0x00_4101_0000. The PLIC and CLINT windows follow the proposed application interrupt controller baseline (NX-REQ-116); the register layout of every block is OPEN. An address of the region that no window lists is unmapped and returns DECERR (NX-REQ-104).

## 3. Secure address map (32-bit width PROPOSED, map SELECTED)

Source: [maps/secure_map.yaml](maps/secure_map.yaml). The access attributes of the secure space are not defined (NX-ARCH-OI-021, OPEN), so the table has no attribute column.

| Region | First address | Last address | Size | Label | NX-REQ |
|---|---|---|---|---|---|
| Security ROM | 0x0000_0000 | 0x0000_FFFF | 64 KiB | SELECTED | 010, 054 |
| Security SRAM | 0x0001_0000 | 0x0001_FFFF | 64 KiB | SELECTED | 011, 054 |
| OSPI NOR secure aperture | 0x1000_0000 | 0x1FFF_FFFF | 256 MiB | SELECTED | 038, 054 |
| AES | 0x2000_0000 | 0x2000_FFFF | 64 KiB | SELECTED | 013, 054 |
| SHA | 0x2001_0000 | 0x2001_FFFF | 64 KiB | SELECTED | 014, 054 |
| Asymmetric cryptography | 0x2002_0000 | 0x2002_FFFF | 64 KiB | SELECTED | 035, 054 |
| eFuse | 0x2003_0000 | 0x2003_FFFF | 64 KiB | SELECTED | 012, 054 |
| Key management | 0x2004_0000 | 0x2004_FFFF | 64 KiB | SELECTED | 054 |
| Security control | 0x2005_0000 | 0x2005_FFFF | 64 KiB | SELECTED | 054 |
| Security interrupt controller | 0x2006_0000 | 0x2006_FFFF | 64 KiB | SELECTED | 054, 057 |
| Security timer and watchdog | 0x2007_0000 | 0x2007_FFFF | 64 KiB | SELECTED | 054 |
| OSPI registers | 0x2008_0000 | 0x2008_FFFF | 64 KiB | SELECTED | 054 |
| Mailbox (secure side) | 0x2009_0000 | 0x2009_FFFF | 64 KiB | SELECTED | 105, 107, 110, 054 |
| Application boot window | 0x3000_0000 | 0x300F_FFFF | 1 MiB | SELECTED | 105, 106, 109, 054 |

Notes. The security ROM and SRAM capacities of 64 KiB are SELECTED; their bases are proposed. The secure NOR aperture is a range for the security core path and does not select a NOR capacity. The interrupt architecture of the security interrupt controller is OPEN (NX-REQ-057). The mailbox window and the application boot window are the two controlled crossings of NX-DEC-027 (section 4); the boot window is an alias of the 1 MiB application System SRAM aperture and is not a memory of the security domain.

## 4. Two separate address spaces and two controlled crossings

The application and secure address spaces are separate spaces on separate interconnects (NX-REQ-028, NX-REQ-033, NX-REQ-034). Several numerical ranges of the two maps coincide, for example the secure NOR aperture at 0x1000_0000 and the application camera frame pool at 0x00_1000_0000. That is not a conflict: an address is interpreted in the address space of the interconnect it arrives on (NX-REQ-108), no master reaches both spaces through one decode, and the two files are checked separately.

The boundary has exactly two controlled crossings (NX-DEC-027, NX-REQ-105, SELECTED), and both are default-deny (NX-REQ-108, SELECTED).

| Crossing | Direction | Secure map | Application map | Label | Records |
|---|---|---|---|---|---|
| Boot window | Security core to application | Application boot window, 0x3000_0000 to 0x300F_FFFF (1 MiB alias) | System SRAM, 0x00_0000_0000 to 0x00_000F_FFFF; no other application region and no DDR4 | SELECTED; PROPOSED attachment (NX-REQ-113) | NX-REQ-105, NX-REQ-106, NX-REQ-109, NX-REQ-113 |
| Mailbox | Application to security | Mailbox (secure side), 0x2009_0000 to 0x2009_FFFF | Mailbox (application side), 0x00_4105_0000 to 0x00_4105_FFFF (PROPOSED, NX-REQ-112) | SELECTED; PROPOSED layout and interrupts (NX-REQ-114, NX-REQ-115) | NX-REQ-105, NX-REQ-107, NX-REQ-110, NX-REQ-114, NX-REQ-115 |

The application side attachment of the bridge to an application fabric, the mailbox register layout and message format, the interrupt directions and the secure-side validation rule are OPEN (NX-ARCH-OI-037). The security core does not reach DDR4 in this proposal. All other secure regions stay unreachable from the application space (NX-REQ-034).

## 5. Open items

| Item | Label | Records | Owner |
|---|---|---|---|
| Attachment of the two crossings, mailbox layout, messages, validation rule and interrupts (MEMORY_ARCHITECTURE 5.4 and 5.5) | PROPOSED | NX-REQ-113, NX-REQ-114, NX-REQ-115, NX-ARCH-OI-037 | Dinesh |
| Owner review and selection of the peripheral register windows (section 2.1) | PROPOSED | NX-REQ-112, NX-ARCH-OI-036 | Dinesh |
| Application interrupt controller baseline (PLIC and CLINT windows) | PROPOSED | NX-REQ-116, NX-ARCH-OI-032 | Dinesh |
| Register layout of every block, and the security and always-on interrupt controllers | OPEN | NX-REQ-057, NX-ARCH-OI-032 | Dinesh |
| Access attributes and finalisation of the secure map | OPEN | NX-ARCH-OI-021 | Dinesh |
| PSRAM, NOR and on-chip memory capacities and organisation | OPEN | NX-ARCH-OI-006, NX-ARCH-OI-007 | Dinesh |

## History

| Version | Date | Change |
|---|---|---|
| 0.1.0-draft | 2026-11-12 | First part 2 draft for KOS-NEXUS-008: the two map files and their tables |
| 0.2.0-draft | 2026-11-12 | Part 3: the two controlled crossings (NX-DEC-027) added to the secure map and the separation section |
| 0.2.1-draft | 2026-11-12 | The map checker exists (scripts/check_address_maps.py); rule 6 and the open items updated |
| 0.2.2-draft | 2026-11-13 | Records of NX-DEC-029 added to the System SRAM, peripheral space and NOR regions and to the two crossing regions |
| 0.3.0-draft | 2026-11-13 | NX-DEC-030: both maps and every region are SELECTED; the width confirmation is OPEN for every master except the C910 |
| 0.4.0-draft | 2026-11-13 | Section 2.1: the peripheral register space is divided into APB-0 and APB-1 windows and per-instance windows (PROPOSED, NX-REQ-112) |
| 0.5.0-draft | 2026-11-13 | NX-DEC-031: the width confirmation is closed by the owner's statement for every application master |
| 0.6.0-draft | 2026-11-13 | PLIC and CLINT windows added to section 2.1 (NX-REQ-116); the crossing details are proposed (NX-REQ-113 to NX-REQ-115) |
