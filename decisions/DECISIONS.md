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
