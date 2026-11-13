# Kritva Nexus Memory Architecture

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-ARCH-003 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Architecture |
| Status | DRAFT (parts 1 and 3 of KOS-NEXUS-008: memory roles, address width, access policy and the domain boundary; the address maps are in ADDRESS_MAP.md; the owner approved the proposals in NX-DEC-030; the document itself has no approval record) |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.9.0-draft |
| Last Updated | 2026-11-13 |
| Authority | INPUT (not AUTHORITATIVE until the owner approves it) |
| Related Tasks / Milestones | KOS-NEXUS-008; NX-M1 |
| Related Documents | [System architecture](SYSTEM_ARCHITECTURE.md); [interconnect specification](INTERCONNECT_SPECIFICATION.md); [A0 integration draft](A0_INTEGRATION_DRAFT.md); [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md); [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) |

## Purpose

This document defines the memory architecture of the Nexus SoC for task KOS-NEXUS-008: which memory plays which role, how wide the application address is, and the access policy (cacheability, coherency, permissions and unmapped access) that the application address map will carry. It states every item with one label and names its requirement or decision record. It does not contain the address maps themselves.

## 1. Status of this part

This is the first part of KOS-NEXUS-008. It decides and proposes the following.

1. The application address width is 40 bits, SELECTED by the owner (NX-DEC-026, NX-REQ-101). The confirmation against the C910 configuration and against every application master is a procedure with an owner (section 4); it is not yet done.
2. The memory roles, the access attributes per memory class, the coherency position and the unmapped-access policy are SELECTED by the owner's approval (NX-DEC-030, NX-REQ-102 to NX-REQ-104). Changing them needs a new decision record.
3. The application address map and the secure address map are held in [maps/application_map.yaml](maps/application_map.yaml) and [maps/secure_map.yaml](maps/secure_map.yaml) and shown in [ADDRESS_MAP.md](ADDRESS_MAP.md) (part 2); both are SELECTED by the owner's approval (NX-DEC-030, NX-REQ-053, NX-REQ-054), with the width confirmation OPEN (NX-REQ-029). The separation of the two address spaces and the two controlled crossings between the security and application domains are section 5 (part 3; NX-DEC-027, NX-REQ-105 to NX-REQ-108).

No capacity, bandwidth, latency or timing value appears here that a requirement or the owner has not stated.

## 2. Rules for this document

1. Every statement carries one label: `SELECTED` (recorded owner decision, with a decision record), `PROPOSED` (a recommendation, including every one from an AI tool) or `OPEN` (needs engineering definition).
2. A SELECTED statement names its decision record (NX-DEC-NNN). A PROPOSED or OPEN statement names its requirement (NX-REQ-NNN), gap (NX-ARCH-GAP-NNN) or open issue (NX-ARCH-OI-NNN).
3. Where this document and the requirements register or a decision record differ, the register or record wins and this document is corrected.
4. A PROPOSED item is changed by a change request: a pull request that edits it with a changelog entry. A SELECTED item also needs a new decision record.

## 3. Memory inventory

| Memory | Where it sits | Role | Label | Records |
|---|---|---|---|---|
| DDR4 | External device behind the DDR4 controller and PHY; reached through the Memory Access Crossbar | Primary system memory for Linux and applications, NPU models and large activations, display framebuffers and DMA buffers | SELECTED role | NX-REQ-002, NX-DEC-001 |
| Octal SPI PSRAM | External device behind its own controller | Secondary memory | SELECTED role | NX-REQ-003, NX-DEC-002 |
| OSPI NOR | External device behind its own controller | Primary boot medium: boot firmware, bootloader and recovery, configuration and authenticated updates | SELECTED role | NX-REQ-004, NX-DEC-003 |
| System SRAM | On-chip, application address space | Early application memory; its capacity is the aperture of the map and is not selected | SELECTED aperture; capacity OPEN | NX-REQ-053, NX-DEC-030 |
| Camera frame pool | On-chip, AI and vision path | Frame buffers for the camera path; 6 MiB of usable capacity | SELECTED capacity | NX-REQ-005, NX-DEC-004 |
| ISP local SRAM | On-chip, AI and vision path | Local working memory of the ISP; the normal AI and vision path does not need DDR4 intermediate storage | PROPOSED | NX-REQ-047 |
| NPU local SRAM | On-chip, AI and vision path | Local working memory of the NPU; the normal AI and vision path does not need DDR4 intermediate storage | PROPOSED | NX-REQ-047 |
| Security ROM and SRAM | On-chip, secure address space only | 64 KiB ROM and 64 KiB SRAM of the security core; not reachable from the application fabrics | SELECTED capacity; PROPOSED isolation | NX-REQ-010, NX-REQ-011, NX-DEC-009, NX-DEC-010, NX-REQ-034 |
| C910 caches | Inside the C910 cluster | 64 KB L1 instruction and data per core and a shared 1 MB L2, as proposed for the cluster | PROPOSED | NX-REQ-055 |

The NOR and the PSRAM are separate devices with separate controllers. The DDR4 device capacity is chosen at board level; the DDR4 address window of 64 GiB is not a device size (NX-REQ-076, NX-ASM-003). The frame-pool address aperture is 16 MiB in the map and the usable capacity is the selected 6 MiB. The ISP SRAM and NPU SRAM windows are apertures, not capacities. Bank count, width, port organisation, ECC and macro selection of the on-chip memories are OPEN (NX-ARCH-OI-007); the PSRAM protocol, mode and capacity and the NOR device are OPEN (NX-ARCH-OI-006).

## 4. Application address width

### 4.1 The selected width

The application address width is 40 bits (NX-DEC-026, NX-REQ-101): SELECTED. It applies to the C910, to every master on the four application AXI fabrics and to the Memory Access Crossbar. The secure address space is separate and uses a 32-bit address (NX-REQ-033, PROPOSED).

The selection of NX-DEC-026 is of the width only. The owner then approved the application address map (NX-DEC-030, NX-REQ-053) before the width was confirmed against every master. AC-015 requires that confirmation before the map is SELECTED, so the approval is an owner decision made ahead of it: the owner confirmed the C910 at 40 bits (NX-DEC-030) and later every other application master (NX-DEC-031, section 4.2), which meets AC-015. If a master cannot generate 40-bit addresses, a new decision record supersedes NX-DEC-026, NX-DEC-030 or NX-DEC-031.

### 4.2 Confirmation procedure (closed by the owner's statement)

The confirmation is NX-REQ-029 and NX-ARCH-GAP-003. The owner confirmed the width for the C910 (NX-DEC-030) and for every other application master (NX-DEC-031), which closes both. The steps below remain the way to record the evidence source (NX-ARCH-OI-001); none is recorded yet. Steps:

1. Name the exact C910 RTL release and configuration in use (NX-ARCH-OI-001).
2. Read the physical address width that configuration generates on its AXI master interface and record the source (RTL parameter, configuration file or datasheet) and the value.
3. For every master in the table of section 4.3, record the address width of its AXI master interface from its own specification or RTL, with the source.
4. Check each recorded width against 40 bits. A master that generates fewer bits can reach only the lower part of the map; record which proposed regions it cannot reach and whether that is acceptable for its job (for example a DMA master that must reach DDR4 in the proposed window above 4 GiB).
5. Record the outcome in this document, with the evidence source, and in a review record. If every master presents 40 bits, NX-REQ-029 and NX-ARCH-GAP-003 are closed. If any master does not, a new decision record supersedes NX-DEC-026 or names the master change (decision 4 of NX-DEC-026).

The widths in the table below are the owner's statement, not values read from the RTL or a specification, and this document records no source.

### 4.3 Application masters (40 bits confirmed by the owner)

| Master | Fabric | Address width generated | Source | Reaches DDR4 window | Label |
|---|---|---|---|---|---|
| C910 cluster | AXI-0 | 40 bits, owner confirmation (NX-DEC-030) | Owner statement of 2026-11-13; the RTL configuration source is not yet recorded (NX-ARCH-OI-001) | Not yet recorded | SELECTED |
| ISP | AXI-1 | 40 bits, owner confirmation (NX-DEC-031) | Owner statement of 2026-11-13; no source recorded | Not yet recorded | SELECTED |
| NPU | AXI-1 | 40 bits, owner confirmation (NX-DEC-031) | Owner statement of 2026-11-13; no source recorded | Not yet recorded | SELECTED |
| Camera DMA | AXI-1 | 40 bits, owner confirmation (NX-DEC-031) | Owner statement of 2026-11-13; no source recorded | Not yet recorded | SELECTED |
| Display controller | AXI-2 | 40 bits, owner confirmation (NX-DEC-031) | Owner statement of 2026-11-13; no source recorded | Not yet recorded | SELECTED |
| Ethernet MACs (2) | AXI-2 | 40 bits, owner confirmation (NX-DEC-031) | Owner statement of 2026-11-13; no source recorded | Not yet recorded | SELECTED |
| Storage DMA | AXI-2 | 40 bits, owner confirmation (NX-DEC-031) | Owner statement of 2026-11-13; no source recorded | Not yet recorded | SELECTED |
| DMA controller (peripheral and I2S DMA) | AXI-3 | 40 bits, owner confirmation (NX-DEC-031) | Owner statement of 2026-11-13; no source recorded | Not yet recorded | SELECTED |

The master placement is PROPOSED (NX-REQ-051). The DMA controller is NX-REQ-092 (SELECTED) with placement PROPOSED (NX-REQ-093).

## 5. Address spaces and domain crossings

The application address space and the secure address space are two separate address spaces on two separate interconnects (NX-REQ-028, NX-REQ-033, NX-REQ-034). The numerical ranges of the two maps overlap in places, and an overlap is not a conflict because an address is interpreted in the space of the interconnect it arrives on (NX-REQ-108). The two maps are in [maps/application_map.yaml](maps/application_map.yaml) and [maps/secure_map.yaml](maps/secure_map.yaml).

The boundary between the security domain and the application domain has exactly two controlled crossings (NX-DEC-027, NX-REQ-105): SELECTED. Everything else in the security domain stays unreachable from the application domain (NX-REQ-034, PROPOSED). Three further points were confirmed by the owner in review and are SELECTED (NX-DEC-029): the boot window reaches System SRAM only and never DDR4 (NX-REQ-109), the mailbox window keeps NX-REQ-072 intact (NX-REQ-110), and the NOR window access of section 6 (NX-REQ-111). The remaining statements of this section were approved by the owner and are SELECTED (NX-DEC-030, NX-REQ-106 to NX-REQ-108), except the details marked OPEN.

### 5.1 Boot window: security core to application (NX-INT-024)

The security core reaches the application domain through a secure-to-application bridge (NX-REQ-106). The only reachable application region is System SRAM, so the security core can verify or place the boot image there (NX-REQ-036); the bridge and this scope are SELECTED (NX-REQ-109, NX-DEC-029). In the secure map it appears as the Application boot window, a 1 MiB alias at 0x3000_0000, the size of the System SRAM aperture. DDR4 and every other application region are unreachable from the security core (SELECTED, NX-REQ-109), because DDR4 may not be initialised when the security core runs first. How the bridge attaches to an application fabric is defined in section 5.4 (NX-REQ-113, SELECTED); whatever the attachment, the window must be usable after the security core starts and before C910 reset release, so that the boot image can be verified and placed before the application subsystems are initialised.

### 5.2 Mailbox: application to security (NX-INT-025)

The mailbox is one block of the security domain with two register windows: one in the secure map and one in the application peripheral register space, reached through the AXI-to-APB interconnects (NX-REQ-107). It carries an interrupt in each direction, with routing as in NX-REQ-057 (OPEN). The security domain validates every request. The application domain reaches the mailbox window and no other security resource. The application-side window is an application-domain peripheral window of the application map, reached by the C910 on the C910-to-APB path like any other allowed window (NX-REQ-072, NX-DEC-022); it is not a security-domain resource, so the rule that secure resources are unreachable on that path is unchanged, and the window gives no route to the secure map or to any other security peripheral. It is the only security-related window on that path. This rule is SELECTED (NX-REQ-110, NX-DEC-029), and so is the rest of the mailbox (NX-REQ-107, NX-DEC-030), except the details marked OPEN. The register layout, the message format, the validation rule and the interrupts are defined in section 5.5 (NX-REQ-114, NX-REQ-115, SELECTED); the application side window is at 0x00_4105_0000 in the peripheral register windows (NX-REQ-112, SELECTED). No security claim is made from this architecture.

### 5.3 Isolation rules

1. Both crossings are default-deny, and no path other than the two crossings exists between the domains (NX-REQ-108).
2. An address is interpreted in the address space of the interconnect it arrives on; a crossing translates the address explicitly, and no master reaches both spaces through one decode.
3. An unmapped or forbidden access at a crossing returns DECERR or SLVERR as in section 6.3 (NX-REQ-104, NX-REQ-108).
4. C910 reset release stays hardware-controlled by the security domain and is not one of the crossings (NX-REQ-037, NX-INT-014).
5. Changing either crossing, or adding a third, needs a new decision record (NX-DEC-027).

### 5.4 Bridge attachment (SELECTED, NX-REQ-113, NX-DEC-033)

The secure-to-application bridge is one AXI master port of the security domain. It attaches to the application AXI-3 fabric, which is the control fabric of the C910-to-APB path (NX-INT-002) and the fabric of the peripheral and DMA masters. The bridge forwards only transactions that fall in the Application boot window of the secure map, translates them to the System SRAM aperture (0x00_0000_0000 to 0x00_000F_FFFF) and issues them on AXI-3. Every other address is answered inside the bridge with DECERR or SLVERR and is never issued on AXI-3, so the security core cannot reach the APB peripherals, the NOR window or DDR4 through the AXI-3 decode. The bridge is a master only: no application transaction enters the secure side through it.

The boot image has to be placed and verified before the C910 runs (NX-REQ-036, NX-REQ-037), so the bridge, the AXI-3 path to System SRAM and System SRAM itself must be clocked and out of reset while the C910 reset is still held. The reset domain of AXI-3 and of System SRAM is not defined (NX-ARCH-OI-025, OPEN), and that definition is a dependency of this decision (NX-ARCH-OI-038). The System SRAM attachment point on the application fabrics, and the width and clock conversion between the secure AXI and AXI-3, are OPEN.

### 5.5 Mailbox layout, messages, validation and interrupts (SELECTED, NX-REQ-114, NX-REQ-115, NX-DEC-033)

The mailbox is one register block. The secure map shows it as a 64 KiB window at 0x2009_0000 and the application peripheral windows show it as a 64 KiB window at 0x00_4105_0000 (ADDRESS_MAP.md section 2.1); both are views of the same block at the same offsets. The sizes are apertures chosen in the proposal that the owner approved (NX-DEC-033).

| Offset | Register | Application access | Security access |
|---|---|---|---|
| 0x000 | ID and version | Read | Read |
| 0x004 | Status: request pending, response ready, busy, error | Read | Read |
| 0x008 | Request doorbell | Write 1 to set; ignored while a request is pending | Read |
| 0x00C | Response doorbell | None | Write 1 to set |
| 0x010 | Application interrupt status | Read, write 1 to clear | Read |
| 0x014 | Application interrupt enable | Read and write | None |
| 0x018 | Security interrupt status | Read | Read, write 1 to clear |
| 0x01C | Security interrupt enable | None | Read and write |
| 0x020 | Error code | Read | Read and write |
| 0x100 to 0x1FF | Request buffer, 256 bytes | Write while no request is pending; read | Read |
| 0x200 to 0x2FF | Response buffer, 256 bytes | Read | Write |

An access that the table does not permit, to a reserved offset, or to the request buffer while a request is pending, returns SLVERR (NX-REQ-104), and there is no write path from the application to the response buffer or to any security register. Only one request is outstanding at a time; a second request doorbell while one is pending is ignored and sets the error bit.

A message is a 16-byte header followed by a payload of at most 240 bytes: a 32-bit message identifier, a 16-bit command, a 16-bit payload length, a 16-bit flags field, a 16-bit status (response only) and a reserved word. A message carries no address. Data larger than 240 bytes is placed in System SRAM and named by an offset and a length inside the boot window; the security core reaches it only through the boot window of section 5.1.

The security domain checks every request in this order: the command is in an allow-list held in security software, the payload length is at most 240 bytes, any offset and length lie inside the boot window, and the identifier is the one expected for the request. It then writes the response header with a status of OK, DENIED, INVALID or BUSY and sets the response doorbell. The allow-list contents, the authentication of the requester, replay and flood protection and the response to repeated invalid requests are OPEN, and no security claim is made from this decision.

The request doorbell raises a level-sensitive request interrupt to one source of the security interrupt controller (32 sources, NX-REQ-057), and the response doorbell raises a level-sensitive response interrupt to one source of the application interrupt controller (128 sources). Each is masked by the enable register of the receiving side, cleared by a write to the status register of the receiving side, and carries no data. The application reaches the security interrupt controller only through the request path (NX-REQ-115). The source numbers depend on the interrupt architecture and are OPEN (NX-REQ-057).

## 6. Access policy of the application address map (SELECTED)

The access attributes below are the ones the application address map carries. The owner approved them for the whole map (NX-DEC-030, NX-REQ-102), and they answer NX-ARCH-OI-003, which is CLOSED.

| Memory class | C910 cacheability | Application permissions | Notes |
|---|---|---|---|
| DDR4, PSRAM | Cacheable, normal memory | Read, write and execute | DDR4 holds Linux and application code and data |
| OSPI NOR window | Cacheable, read-only | Read and execute; no write | SELECTED (NX-REQ-111, NX-DEC-029): program and erase are not done through the window; they use the NOR controller registers on the peripheral path under NX-REQ-072. The execute permission is SELECTED with the other attributes (NX-REQ-102, NX-DEC-030) |
| System SRAM | Non-cacheable by default | Read, write and execute | Shared with other masters |
| Camera frame pool, ISP SRAM, NPU SRAM | Non-cacheable | Read and write; no execute | Shared with the camera, ISP and NPU masters; the CPU does not keep a cached copy |
| Peripheral registers | Non-cacheable, device memory, no speculative access | Read and write; no execute | Window policy as in NX-REQ-072 for the C910-to-APB path |
| Reserved and unmapped | Not applicable | None | Section 6.3 |

Permissions are checked per window with the read, write and execute bits and the AxPROT attributes (NX-REQ-072 for the peripheral path, NX-REQ-102 for the others). The windows are those of the application address map; this part does not set their bases or sizes.

### 6.1 Coherency (SELECTED)

The masters on AXI-1, AXI-2 and AXI-3 are treated as non-coherent with the C910 caches (NX-REQ-103). Software cleans or invalidates the cache lines of a shared buffer around a transfer. Hardware coherency, if wanted, needs a cluster and interconnect configuration that is not selected (NX-ARCH-OI-001), and would need a new decision record. The DMA controller is covered: its buffers in DDR4 are non-coherent and its descriptors are written and read with the same maintenance rules (NX-REQ-097, NX-ARCH-OI-035).

### 6.2 IOMMU (SELECTED)

No requirement asks for an IOMMU, so this baseline has none (NX-REQ-103). A master can then reach every window its fabric decodes, within the permissions of section 6. If isolation between masters is needed, it needs a new decision record.

### 6.3 Unmapped, reserved and denied access (SELECTED)

The application fabrics and the Memory Access Crossbar deny by default (NX-REQ-104). An access to an unmapped or reserved address returns DECERR (NX-REQ-079). An access that a window forbids returns SLVERR, as on the C910-to-APB path (NX-REQ-068). A reserved region of the map is treated as unmapped. Reads of an unmapped address return no valid data and writes have no effect. The error response reaches the master as a bus error; a DMA channel stops on it (NX-REQ-099).

## 7. Open items and owners

| Item | Label | Records | Owner |
|---|---|---|---|
| Confirmation of the 40-bit width against the C910 configuration and every application master (owner statement; RTL evidence source not recorded, NX-ARCH-OI-001) | SELECTED | NX-REQ-029, NX-DEC-031 | Dinesh |
| Attachment of the two crossings, mailbox layout, message format, validation rule and interrupts (sections 5.4 and 5.5); the allow-list and the AXI-3 reset domain stay OPEN as NX-ARCH-OI-038 and NX-ARCH-OI-025 | SELECTED | NX-REQ-113, NX-REQ-114, NX-REQ-115, NX-DEC-033 | Dinesh |
| Application interrupt controller baseline (PLIC and CLINT; the security and always-on controllers and the routing stay OPEN) | SELECTED | NX-REQ-116, NX-DEC-033 | Dinesh |
| Division of the peripheral register space into windows (ADDRESS_MAP.md section 2.1 and peripheral_windows.yaml) | SELECTED | NX-REQ-112, NX-DEC-033 | Dinesh |
| Application and secure address maps (in ADDRESS_MAP.md and the two map files), approved by the owner | SELECTED | NX-REQ-053, NX-REQ-054, NX-DEC-030 | Dinesh |
| PSRAM, NOR and on-chip memory organisation details | OPEN | NX-ARCH-OI-006, NX-ARCH-OI-007 | Dinesh |
| DMA request mapping, descriptor format, coherency and power domain | OPEN | NX-ARCH-OI-035 | Dinesh |

## History

| Version | Date | Change |
|---|---|---|
| 0.1.0-draft | 2026-11-12 | First part for KOS-NEXUS-008: memory inventory, the selected 40-bit address width with its confirmation procedure, address-space statement and the proposed access policy |
| 0.2.0-draft | 2026-11-12 | The address maps moved to ADDRESS_MAP.md and the two map files (part 2) |
| 0.3.0-draft | 2026-11-12 | Part 3: section 5 defines the two controlled crossings of NX-DEC-027 and the isolation rules |
| 0.3.1-draft | 2026-11-12 | After review 4: the mailbox application-side window is stated as an application-domain window under NX-REQ-072 and the boot window must be usable before C910 reset release |
| 0.4.0-draft | 2026-11-13 | Three owner-confirmed points are SELECTED by NX-DEC-029: boot window scope, mailbox rule and NOR window access |
| 0.5.0-draft | 2026-11-13 | NX-DEC-030: the owner approved the proposed maps, access policy, boot window, mailbox and isolation rules; the C910 is confirmed at 40 bits and the other masters stay OPEN |
| 0.6.0-draft | 2026-11-13 | The peripheral register space is divided into windows by a PROPOSED requirement (NX-REQ-112); the mailbox window base is proposed |
| 0.7.0-draft | 2026-11-13 | NX-DEC-031: the owner confirmed the 40-bit width for every application master; section 4.3 records the statement and NX-REQ-029 and NX-ARCH-GAP-003 are closed |
| 0.8.0-draft | 2026-11-13 | Sections 5.4 and 5.5: the bridge attachment, the mailbox register layout, message format, validation rule and interrupts are proposed (NX-REQ-113 to NX-REQ-115); the application interrupt controller baseline is proposed (NX-REQ-116) |
| 0.9.0-draft | 2026-11-13 | NX-DEC-033: the bridge attachment, the mailbox layout, messages, validation rule and interrupts, the peripheral register windows and the application interrupt controller baseline are SELECTED |
