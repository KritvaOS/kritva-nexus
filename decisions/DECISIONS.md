# Decisions: kritva-nexus

Index of the Nexus architecture decision records for task KOS-NEXUS-084 (AC-010 and AC-011). Owner and reviewer: Dinesh (interim, not independent). Each record is `NX-DEC-NNN.md` in this folder.

Rules:

- IDs are stable and never reused. A record is append-only: the status, consequences and evidence may be updated as dated addenda in its History table; the original context, alternatives and rationale are never rewritten. A replaced decision becomes SUPERSEDED and names its replacement.
- Label: `SELECTED` only with a recorded owner decision; `PROPOSED` is a recommendation; `OPEN` needs engineering definition.
- Where an owner's alternatives or rationale were not recorded, the record says so. It does not invent them.
- These records are repository decisions of Nexus. They are not kritva-program decision records (D-NNN or PD-NNN) and carry no central approval.

| Decision | Title | Label | Requirements |
|---|---|---|---|
| [NX-DEC-001](NX-DEC-001.md) | DDR4 primary system memory | SELECTED | NX-REQ-002 |
| [NX-DEC-002](NX-DEC-002.md) | Octal SPI PSRAM secondary memory | SELECTED | NX-REQ-003 |
| [NX-DEC-003](NX-DEC-003.md) | OSPI NOR primary boot medium | SELECTED | NX-REQ-004 |
| [NX-DEC-004](NX-DEC-004.md) | 6 MiB usable camera frame pool | SELECTED | NX-REQ-005 |
| [NX-DEC-005](NX-DEC-005.md) | 720p60 parallel DPI display mode | SELECTED | NX-REQ-006 |
| [NX-DEC-006](NX-DEC-006.md) | Three display composition layers | SELECTED | NX-REQ-007 |
| [NX-DEC-007](NX-DEC-007.md) | Two independent Ethernet MACs | SELECTED | NX-REQ-008 |
| [NX-DEC-008](NX-DEC-008.md) | Isolated 32-bit RISC-V security core | SELECTED | NX-REQ-009 |
| [NX-DEC-009](NX-DEC-009.md) | Dedicated 64 KiB security ROM | SELECTED | NX-REQ-010 |
| [NX-DEC-010](NX-DEC-010.md) | Dedicated 64 KiB security SRAM | SELECTED | NX-REQ-011 |
| [NX-DEC-011](NX-DEC-011.md) | Dedicated security eFuse | SELECTED | NX-REQ-012 |
| [NX-DEC-012](NX-DEC-012.md) | AES-128 and AES-256 support | SELECTED | NX-REQ-013 |
| [NX-DEC-013](NX-DEC-013.md) | Mandatory SHA-256 support | SELECTED | NX-REQ-014 |
| [NX-DEC-014](NX-DEC-014.md) | Four application AXI fabrics | SELECTED | NX-REQ-015 |
| [NX-DEC-015](NX-DEC-015.md) | Two AXI-to-APB interconnects | SELECTED | NX-REQ-016 |
| [NX-DEC-016](NX-DEC-016.md) | C910 DVFS support | SELECTED | NX-REQ-017 |
| [NX-DEC-017](NX-DEC-017.md) | NPU DVFS support | SELECTED | NX-REQ-018 |
| [NX-DEC-018](NX-DEC-018.md) | Xuantie C910 application CPU direction | PROPOSED | NX-REQ-001, NX-REQ-029 |
| [NX-DEC-019](NX-DEC-019.md) | Separate secure AXI interconnect | SELECTED | NX-REQ-032 |
| [NX-DEC-020](NX-DEC-020.md) | Peripheral instance counts | SELECTED | NX-REQ-019 to NX-REQ-026 |
| [NX-DEC-021](NX-DEC-021.md) | C910 access to APB peripherals through AXI-0 and AXI-3 | SELECTED | NX-REQ-067, NX-REQ-027 |
| [NX-DEC-022](NX-DEC-022.md) | Behaviour of the C910-to-APB path | SELECTED | NX-REQ-068 to NX-REQ-075 |
| [NX-DEC-023](NX-DEC-023.md) | Approval of the RTL Design Standard KNX-RTL-STD-001 | SELECTED | NX-REQ-082 to NX-REQ-089 |
| [NX-DEC-024](NX-DEC-024.md) | Claude co-author line and session reference for Nexus commits | SELECTED | None (repository working rule) |
| [NX-DEC-025](NX-DEC-025.md) | 32-channel general-purpose DMA controller | SELECTED | NX-REQ-092 |
| [NX-DEC-026](NX-DEC-026.md) | 40-bit application address width | SELECTED | NX-REQ-101 |
| [NX-DEC-027](NX-DEC-027.md) | Two controlled crossings between the security and application domains | SELECTED | NX-REQ-105 |
| [NX-DEC-028](NX-DEC-028.md) | One file for the Claude session identifiers, updated by every commit | SELECTED | None (repository working rule) |
| [NX-DEC-029](NX-DEC-029.md) | Boot window scope, mailbox rule and NOR window access | SELECTED | NX-REQ-109, NX-REQ-110, NX-REQ-111 |
| [NX-DEC-030](NX-DEC-030.md) | Approval of the memory architecture proposals of KOS-NEXUS-008 | SELECTED | NX-REQ-028, NX-REQ-053, NX-REQ-054, NX-REQ-102 to NX-REQ-104, NX-REQ-106 to NX-REQ-108 |
| [NX-DEC-031](NX-DEC-031.md) | 40-bit width confirmed for every application master | SELECTED | NX-REQ-029, NX-REQ-101 |
| [NX-DEC-032](NX-DEC-032.md) | address-map-check is a required check | SELECTED | None (repository working rule) |
