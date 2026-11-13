# Kritva Nexus Address Maps

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-ARCH-004 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Architecture |
| Status | DRAFT (parts 2 and 3 of KOS-NEXUS-008: the application and secure address maps and the two domain crossings, approved by the owner in NX-DEC-030; the peripheral register windows and the crossing details are approved in NX-DEC-033; the secure width and attributes are approved in NX-DEC-034; the register layouts are PROPOSED; the document itself has no approval record) |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.9.0-draft |
| Last Updated | 2026-11-13 |
| Authority | DERIVED (the machine-readable files are the source; not AUTHORITATIVE) |
| Related Tasks / Milestones | KOS-NEXUS-008; NX-M1 |
| Related Documents | [Memory architecture](MEMORY_ARCHITECTURE.md); [application map source](maps/application_map.yaml); [secure map source](maps/secure_map.yaml); [peripheral windows source](maps/peripheral_windows.yaml); [system architecture](SYSTEM_ARCHITECTURE.md); [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md) |

## Purpose

This document shows the application address map and the secure address map for task KOS-NEXUS-008. The maps are held in two machine-readable files, one per address space: [maps/application_map.yaml](maps/application_map.yaml) and [maps/secure_map.yaml](maps/secure_map.yaml). A third file, [maps/peripheral_windows.yaml](maps/peripheral_windows.yaml), divides the peripheral register space of the application map into windows (section 2.1). The tables below are copied from those files and are not a second source. If a table and its file differ, the file is the source and the table is corrected.

## 1. Status and rules

1. Both maps are SELECTED by the owner's approval (NX-DEC-030, NX-REQ-053 and NX-REQ-054). The bases and apertures come from sections 9.6 and 7.4 of the [A0 integration draft](A0_INTEGRATION_DRAFT.md); the secure window sizes come from this part. A region label covers its base, size and attributes; a capacity keeps the label of its own requirement. AC-015 requires the application address width to be confirmed against the C910 and every application master before the application map is SELECTED. The owner approved the map first (NX-DEC-030) and then confirmed the 40-bit width for the C910 and every other application master (NX-DEC-031, NX-REQ-029), which meets AC-015; the confirmation is an owner statement and the RTL evidence is not recorded (NX-ARCH-OI-001), so a master that cannot generate 40-bit addresses leads to a new decision record.
2. The application address width is 40 bits, SELECTED (NX-DEC-026, NX-REQ-101); its confirmation for every application master is the owner's statement (NX-DEC-031, NX-REQ-029). The secure address width is 32 bits, SELECTED (NX-REQ-033, NX-DEC-034), and the secure access attributes are SELECTED (NX-REQ-119, NX-DEC-034).
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

## 2.1 Peripheral register windows (SELECTED)

Source: [maps/peripheral_windows.yaml](maps/peripheral_windows.yaml). The windows divide the application region Peripheral register space (0x00_4000_0000 to 0x00_4FFF_FFFF), which stays SELECTED with its base, size and attributes (NX-REQ-053, NX-REQ-102). The division is SELECTED (NX-REQ-112, NX-DEC-033; NX-ARCH-OI-036 is closed).

| Window | APB | First address | Last address | Size | Label | NX-REQ |
|---|---|---|---|---|---|---|
| APB-0 (bridge window) | - | 0x00_4000_0000 | 0x00_40FF_FFFF | 16 MiB | SELECTED | 016, 112 |
| APB-1 (bridge window) | - | 0x00_4100_0000 | 0x00_41FF_FFFF | 16 MiB | SELECTED | 016, 112 |
| PWM controller | APB-0 | 0x00_4000_0000 | 0x00_4000_FFFF | 64 KiB | SELECTED | 019, 112 |
| GPIO controller | APB-0 | 0x00_4001_0000 | 0x00_4001_FFFF | 64 KiB | SELECTED | 020, 112 |
| General-purpose timers | APB-0 | 0x00_4002_0000 | 0x00_4002_FFFF | 64 KiB | SELECTED | 021, 112 |
| UART0 | APB-0 | 0x00_4003_0000 | 0x00_4003_FFFF | 64 KiB | SELECTED | 022, 112 |
| UART1 | APB-0 | 0x00_4004_0000 | 0x00_4004_FFFF | 64 KiB | SELECTED | 022, 112 |
| UART2 | APB-0 | 0x00_4005_0000 | 0x00_4005_FFFF | 64 KiB | SELECTED | 022, 112 |
| UART3 | APB-0 | 0x00_4006_0000 | 0x00_4006_FFFF | 64 KiB | SELECTED | 022, 112 |
| I2C0 | APB-0 | 0x00_4007_0000 | 0x00_4007_FFFF | 64 KiB | SELECTED | 023, 112 |
| I2C1 | APB-0 | 0x00_4008_0000 | 0x00_4008_FFFF | 64 KiB | SELECTED | 023, 112 |
| I2C2 | APB-0 | 0x00_4009_0000 | 0x00_4009_FFFF | 64 KiB | SELECTED | 023, 112 |
| I2C3 | APB-0 | 0x00_400A_0000 | 0x00_400A_FFFF | 64 KiB | SELECTED | 023, 112 |
| SPI master | APB-0 | 0x00_400B_0000 | 0x00_400B_FFFF | 64 KiB | SELECTED | 024, 112 |
| SPI slave | APB-0 | 0x00_400C_0000 | 0x00_400C_FFFF | 64 KiB | SELECTED | 025, 112 |
| I2S0 | APB-0 | 0x00_400D_0000 | 0x00_400D_FFFF | 64 KiB | SELECTED | 026, 112 |
| I2S1 | APB-0 | 0x00_400E_0000 | 0x00_400E_FFFF | 64 KiB | SELECTED | 026, 112 |
| DMA controller | APB-1 | 0x00_4100_0000 | 0x00_4100_FFFF | 64 KiB | SELECTED | 092, 093, 112 |
| OSPI NOR controller | APB-1 | 0x00_4101_0000 | 0x00_4101_FFFF | 64 KiB | SELECTED | 004, 111, 112 |
| OSPI PSRAM controller | APB-1 | 0x00_4102_0000 | 0x00_4102_FFFF | 64 KiB | SELECTED | 003, 112 |
| DDR4 controller | APB-1 | 0x00_4103_0000 | 0x00_4103_FFFF | 64 KiB | SELECTED | 002, 112 |
| Clock, reset and power control | APB-1 | 0x00_4104_0000 | 0x00_4104_FFFF | 64 KiB | SELECTED | 058, 060, 061, 112 |
| Mailbox (application side) | APB-1 | 0x00_4105_0000 | 0x00_4105_FFFF | 64 KiB | SELECTED | 107, 110, 112 |
| ISP | APB-1 | 0x00_4106_0000 | 0x00_4106_FFFF | 64 KiB | SELECTED | 045, 112 |
| NPU | APB-1 | 0x00_4107_0000 | 0x00_4107_FFFF | 64 KiB | SELECTED | 046, 112 |
| Camera interface and DMA | APB-1 | 0x00_4108_0000 | 0x00_4108_FFFF | 64 KiB | SELECTED | 042, 112 |
| Display controller | APB-1 | 0x00_4109_0000 | 0x00_4109_FFFF | 64 KiB | SELECTED | 006, 112 |
| Ethernet MAC0 | APB-1 | 0x00_410A_0000 | 0x00_410A_FFFF | 64 KiB | SELECTED | 008, 112 |
| Ethernet MAC1 | APB-1 | 0x00_410B_0000 | 0x00_410B_FFFF | 64 KiB | SELECTED | 008, 112 |
| Storage DMA | APB-1 | 0x00_410C_0000 | 0x00_410C_FFFF | 64 KiB | SELECTED | 051, 112 |
| Application interrupt controller (PLIC) | APB-1 | 0x00_4140_0000 | 0x00_417F_FFFF | 4 MiB | SELECTED | 057, 112, 116 |
| Application timer and software interrupt (CLINT) | APB-1 | 0x00_4180_0000 | 0x00_4180_FFFF | 64 KiB | SELECTED | 057, 112, 116 |

Notes. APB-0 carries the peripherals whose counts are SELECTED (NX-REQ-019 to NX-REQ-026, NX-DEC-020) and APB-1 carries the control and block registers; the 16 MiB apertures of the two bridge windows and the 64 KiB size of each window are apertures, not register counts. Each instance has its own window, so a peripheral is never shared between instances in one window except the blocks that the requirements count as one block (PWM, GPIO and the general-purpose timers). The mailbox window (0x00_4105_0000 to 0x00_4105_FFFF) is the only security-related window on the C910-to-APB path (NX-REQ-110) and gives no route to the secure map. The DMA controller window is at 0x00_4100_0000 and the OSPI NOR controller window, the only way to program or erase the NOR device (NX-REQ-111), is at 0x00_4101_0000. The PLIC and CLINT windows follow the application interrupt controller baseline (NX-REQ-116, SELECTED); the register layout of every block is OPEN. An address of the region that no window lists is unmapped and returns DECERR (NX-REQ-104).

## 2.2 Register layouts (PROPOSED)

Source: [maps/register_layouts.yaml](maps/register_layouts.yaml). This section proposes the register conventions (NX-REQ-117) and the registers of each block class (NX-REQ-118). It does not define bit fields: those depend on IP selection and block specifications (NX-ARCH-OI-039, PROPOSED). The mailbox layouts follow MEMORY_ARCHITECTURE 5.5 and are SELECTED (NX-REQ-114).

Conventions (NX-REQ-117): every register is one 32-bit word at a 4-byte aligned offset inside the 64 KiB window of its block (the PLIC window is 4 MiB); a 64-bit or 40-bit value is two registers, low word at the lower offset; reserved bits read as zero and ignore writes; access types are RO, RW, WO, W1C (write 1 to clear) and W1S (write 1 to set); an offset that the layout does not list returns SLVERR; offsets 0x000 to 0x0FF hold the common header and block registers start at 0x100, except for the mailbox, the PLIC and the CLINT, which keep their own layouts. Per-channel and per-instance arrays are listed by their first entry with the stride in the note.

Each block of section 2.1 and each security peripheral of section 3 uses one layout.

| Block | Space | Layout | Label | NX-REQ |
|---|---|---|---|---|
| PWM controller | application | pwm | PROPOSED | 118 |
| GPIO controller | application | gpio | PROPOSED | 118 |
| General-purpose timers | application | timer | PROPOSED | 118 |
| UART0 | application | uart | PROPOSED | 118 |
| UART1 | application | uart | PROPOSED | 118 |
| UART2 | application | uart | PROPOSED | 118 |
| UART3 | application | uart | PROPOSED | 118 |
| I2C0 | application | i2c | PROPOSED | 118 |
| I2C1 | application | i2c | PROPOSED | 118 |
| I2C2 | application | i2c | PROPOSED | 118 |
| I2C3 | application | i2c | PROPOSED | 118 |
| SPI master | application | spi | PROPOSED | 118 |
| SPI slave | application | spi | PROPOSED | 118 |
| I2S0 | application | i2s | PROPOSED | 118 |
| I2S1 | application | i2s | PROPOSED | 118 |
| DMA controller | application | dma | PROPOSED | 118 |
| OSPI NOR controller | application | nor_ctrl | PROPOSED | 118 |
| OSPI PSRAM controller | application | psram_ctrl | PROPOSED | 118 |
| DDR4 controller | application | ddr_ctrl | PROPOSED | 118 |
| Clock, reset and power control | application | sysctl | PROPOSED | 118 |
| Mailbox (application side) | application | mailbox_app | SELECTED | 114 |
| ISP | application | media_ctrl | PROPOSED | 118 |
| NPU | application | ai_ctrl | PROPOSED | 118 |
| Camera interface and DMA | application | media_ctrl | PROPOSED | 118 |
| Display controller | application | media_ctrl | PROPOSED | 118 |
| Ethernet MAC0 | application | eth_ctrl | PROPOSED | 118 |
| Ethernet MAC1 | application | eth_ctrl | PROPOSED | 118 |
| Storage DMA | application | media_ctrl | PROPOSED | 118 |
| Application interrupt controller (PLIC) | application | plic | PROPOSED | 116 |
| Application timer and software interrupt (CLINT) | application | clint | PROPOSED | 116 |
| AES | secure | aes | PROPOSED | 118 |
| SHA | secure | sha | PROPOSED | 118 |
| Asymmetric cryptography | secure | pka | PROPOSED | 118 |
| eFuse | secure | efuse | PROPOSED | 118 |
| Key management | secure | keymgmt | PROPOSED | 118 |
| Security control | secure | secctrl | PROPOSED | 118 |
| Security interrupt controller | secure | none | OPEN | 057 |
| Security timer and watchdog | secure | sectimer | PROPOSED | 118 |
| OSPI registers | secure | nor_ctrl | PROPOSED | 118 |
| Mailbox (secure side) | secure | mailbox_sec | SELECTED | 114 |

### Layout common header (PROPOSED, NX-REQ-117)

Offsets 0x000 to 0x0FF of every block that has a header.

| Register | Offset | Access | Note |
|---|---|---|---|
| ID | 0x0000 | RO | Block identifier |
| VERSION | 0x0004 | RO | Block version |
| CONTROL | 0x0008 | RW | Bit 0 enable, bit 1 soft reset (self-clearing); other bits are block specific |
| STATUS | 0x000C | RO | Bit 0 busy, bit 1 error; other bits are block specific |
| INT_ENABLE | 0x0010 | RW | One enable bit per interrupt cause of the block |
| INT_STATUS | 0x0014 | W1C | One status bit per interrupt cause of the block; write 1 to clear |

### Layout pwm (PROPOSED)

Pulse-width modulation; the channel count is not defined.

| Register | Offset | Access | Note |
|---|---|---|---|
| CH_ENABLE | 0x0100 | RW | One enable bit per channel |
| CH0_PERIOD | 0x0120 | RW | Channel n at an offset of 0x10 times n |
| CH0_DUTY | 0x0124 | RW | Duty compare value |
| CH0_CTRL | 0x0128 | RW | Polarity and mode |

### Layout gpio (PROPOSED)

General-purpose input and output; the pin count is not defined.

| Register | Offset | Access | Note |
|---|---|---|---|
| DATA_IN | 0x0100 | RO | Sampled pin values |
| DATA_OUT | 0x0104 | RW | Output values |
| DIRECTION | 0x0108 | RW | 1 for output |
| INT_TYPE | 0x010C | RW | Edge or level per pin |
| INT_POLARITY | 0x0110 | RW | High or low, rising or falling per pin |

### Layout timer (PROPOSED)

General-purpose timers; the timer count is not defined.

| Register | Offset | Access | Note |
|---|---|---|---|
| COUNT_LO | 0x0100 | RO | Free-running count, low word |
| COUNT_HI | 0x0104 | RO | Free-running count, high word |
| COMPARE0_LO | 0x0120 | RW | Timer n at an offset of 0x10 times n |
| COMPARE0_HI | 0x0124 | RW | Compare value, high word |
| TIMER0_CTRL | 0x0128 | RW | One-shot or periodic mode |

### Layout uart (PROPOSED)

Serial port; the FIFO depth and the flow-control signals are not defined.

| Register | Offset | Access | Note |
|---|---|---|---|
| TX_DATA | 0x0100 | WO | Transmit FIFO write |
| RX_DATA | 0x0104 | RO | Receive FIFO read |
| BAUD_DIV | 0x0108 | RW | Baud-rate divisor |
| LINE_CTRL | 0x010C | RW | Data bits, parity and stop bits |
| FIFO_CTRL | 0x0110 | RW | FIFO enable, clear and trigger levels |
| FIFO_STATUS | 0x0114 | RO | FIFO fill levels and flags |
| FLOW_CTRL | 0x0118 | RW | Hardware flow control, if present |

### Layout i2c (PROPOSED)

Two-wire bus controller; the roles supported are not defined.

| Register | Offset | Access | Note |
|---|---|---|---|
| PRESCALE | 0x0100 | RW | Clock prescaler |
| SLAVE_ADDR | 0x0104 | RW | Own address when addressed as a target |
| TX_DATA | 0x0108 | WO | Transmit data |
| RX_DATA | 0x010C | RO | Received data |
| COMMAND | 0x0110 | WO | Start, stop, read, write and acknowledge commands |
| BUS_STATUS | 0x0114 | RO | Bus busy, arbitration lost and acknowledge flags |

### Layout spi (PROPOSED)

Serial peripheral interface; master and slave use this layout.

| Register | Offset | Access | Note |
|---|---|---|---|
| CLK_DIV | 0x0100 | RW | Serial clock divisor |
| FRAME_FORMAT | 0x0104 | RW | Clock mode, word size and bit order |
| TX_DATA | 0x0108 | WO | Transmit FIFO write |
| RX_DATA | 0x010C | RO | Receive FIFO read |
| FIFO_STATUS | 0x0110 | RO | FIFO fill levels and flags |
| CS_CTRL | 0x0114 | RW | Chip-select control |

### Layout i2s (PROPOSED)

Audio serial interface.

| Register | Offset | Access | Note |
|---|---|---|---|
| CLK_CONFIG | 0x0100 | RW | Bit clock and word clock configuration |
| FORMAT | 0x0104 | RW | Word length and frame format |
| TX_DATA | 0x0108 | WO | Transmit FIFO write |
| RX_DATA | 0x010C | RO | Receive FIFO read |
| FIFO_STATUS | 0x0110 | RO | FIFO fill levels and flags |
| DMA_CTRL | 0x0114 | RW | DMA request enables |

### Layout dma (PROPOSED)

General-purpose DMA controller with 32 channels (NX-REQ-092); addresses are 40 bits, as two words.

| Register | Offset | Access | Note |
|---|---|---|---|
| CHANNEL_ENABLE | 0x0100 | RW | One bit per channel |
| CHANNEL_BUSY | 0x0104 | RO | One bit per channel |
| ERROR_STATUS | 0x0108 | W1C | One bit per channel |
| CH0_SRC_LO | 0x0200 | RW | Channel n at an offset of 0x40 times n |
| CH0_SRC_HI | 0x0204 | RW | Source address bits 39 to 32 |
| CH0_DST_LO | 0x0208 | RW | Destination address, low word |
| CH0_DST_HI | 0x020C | RW | Destination address bits 39 to 32 |
| CH0_LENGTH | 0x0210 | RW | Transfer length in bytes |
| CH0_CTRL | 0x0214 | RW | Direction, width, burst and request selection |
| CH0_STATUS | 0x0218 | RO | Remaining length and state |

### Layout nor_ctrl (PROPOSED)

OSPI NOR controller; program and erase go only through these registers (NX-REQ-111).

| Register | Offset | Access | Note |
|---|---|---|---|
| COMMAND | 0x0100 | WO | Read, program, erase and status commands |
| ADDRESS | 0x0104 | RW | Flash address for a command |
| DATA | 0x0108 | RW | Data for a command |
| XIP_CTRL | 0x010C | RW | Enable the read-only memory window |
| TIMING | 0x0110 | RW | Clock divisor and dummy cycles |
| FLASH_STATUS | 0x0114 | RO | Busy and write-enable flags |

### Layout psram_ctrl (PROPOSED)

OSPI PSRAM controller.

| Register | Offset | Access | Note |
|---|---|---|---|
| TIMING | 0x0100 | RW | Clock divisor and read and write latency |
| MODE | 0x0104 | RW | Device mode registers access |
| CAL_CTRL | 0x0108 | RW | Calibration control |
| CAL_STATUS | 0x010C | RO | Calibration result |

### Layout ddr_ctrl (PROPOSED)

DDR4 controller; the register set of the controller IP is not selected.

| Register | Offset | Access | Note |
|---|---|---|---|
| INIT_CTRL | 0x0100 | RW | Start initialisation |
| INIT_STATUS | 0x0104 | RO | Initialisation done and error flags |
| TIMING0 | 0x0108 | RW | Device timing parameters |
| REFRESH | 0x010C | RW | Refresh interval |
| TRAIN_CTRL | 0x0110 | RW | Start training |
| TRAIN_STATUS | 0x0114 | RO | Training result |

### Layout sysctl (PROPOSED)

Clock, reset and power control, including the DVFS of the C910 and the NPU (NX-REQ-017, NX-REQ-018).

| Register | Offset | Access | Note |
|---|---|---|---|
| CLOCK_ENABLE | 0x0100 | RW | One bit per clock gate |
| CLOCK_DIV | 0x0104 | RW | Divider selection |
| PLL_CTRL | 0x0108 | RW | PLL enable and settings |
| PLL_STATUS | 0x010C | RO | PLL lock flags |
| RESET_CTRL | 0x0110 | RW | One bit per reset domain |
| RESET_STATUS | 0x0114 | RO | Reset state per domain |
| POWER_CTRL | 0x0118 | RW | Power domain requests |
| POWER_STATUS | 0x011C | RO | Power domain state |
| DVFS_CTRL | 0x0120 | RW | Operating point request |
| DVFS_STATUS | 0x0124 | RO | Operating point state |

### Layout media_ctrl (PROPOSED)

Buffer-based stream block (ISP, camera, display, storage DMA); the frame format list is not defined.

| Register | Offset | Access | Note |
|---|---|---|---|
| BUFFER_BASE_LO | 0x0100 | RW | Buffer address, low word |
| BUFFER_BASE_HI | 0x0104 | RW | Buffer address bits 39 to 32 |
| STRIDE | 0x0108 | RW | Line stride in bytes |
| FRAME_SIZE | 0x010C | RW | Width and height |
| FORMAT | 0x0110 | RW | Pixel or data format |
| FRAME_CTRL | 0x0114 | RW | Start, stop and continuous mode |
| FRAME_STATUS | 0x0118 | RO | Frame counter and error flags |

### Layout ai_ctrl (PROPOSED)

NPU control; the command format is not defined.

| Register | Offset | Access | Note |
|---|---|---|---|
| CMD_BASE_LO | 0x0100 | RW | Command buffer address, low word |
| CMD_BASE_HI | 0x0104 | RW | Command buffer address bits 39 to 32 |
| CMD_LENGTH | 0x0108 | RW | Command buffer length in bytes |
| KICK | 0x010C | WO | Start the command buffer |
| NPU_STATUS | 0x0110 | RO | Busy and error flags |
| PERF_COUNT | 0x0114 | RO | Active cycle count |
| DVFS_REQ | 0x0118 | RW | Operating point request |

### Layout eth_ctrl (PROPOSED)

Ethernet MAC; the PHY interface and the descriptor format are not defined.

| Register | Offset | Access | Note |
|---|---|---|---|
| MAC_ADDR_LO | 0x0100 | RW | Station address, low word |
| MAC_ADDR_HI | 0x0104 | RW | Station address, high half |
| MAC_CONFIG | 0x0108 | RW | Speed, duplex and filtering |
| TX_RING_LO | 0x010C | RW | Transmit ring address, low word |
| TX_RING_HI | 0x0110 | RW | Transmit ring address bits 39 to 32 |
| RX_RING_LO | 0x0114 | RW | Receive ring address, low word |
| RX_RING_HI | 0x0118 | RW | Receive ring address bits 39 to 32 |
| TX_TAIL | 0x011C | RW | Transmit ring tail pointer |
| RX_TAIL | 0x0120 | RW | Receive ring tail pointer |
| MDIO_CTRL | 0x0124 | RW | Management bus command |
| MDIO_DATA | 0x0128 | RW | Management bus data |

### Layout plic (PROPOSED)

Standard RISC-V PLIC layout with 128 sources; whether the C910 PLIC matches it is not confirmed (NX-ARCH-OI-001).

| Register | Offset | Access | Note |
|---|---|---|---|
| SOURCE_PRIORITY | 0x0000 | RW | Source n at an offset of 4 times n |
| PENDING | 0x1000 | RO | One bit per source, 4 words |
| ENABLE_CTX0 | 0x2000 | RW | Context n at an offset of 0x80 times n |
| THRESHOLD_CTX0 | 0x200000 | RW | Context n at an offset of 0x1000 times n |
| CLAIM_COMPLETE_CTX0 | 0x200004 | RW | Read to claim, write to complete |

### Layout clint (PROPOSED)

Standard RISC-V CLINT layout; whether the C910 CLINT matches it is not confirmed (NX-ARCH-OI-001).

| Register | Offset | Access | Note |
|---|---|---|---|
| MSIP0 | 0x0000 | RW | Hart n at an offset of 4 times n |
| MTIMECMP0_LO | 0x4000 | RW | Hart n at an offset of 8 times n |
| MTIMECMP0_HI | 0x4004 | RW | Compare value, high word |
| MTIME_LO | 0xBFF8 | RW | Shared timebase, low word |
| MTIME_HI | 0xBFFC | RW | Shared timebase, high word |

### Layout mailbox_app (SELECTED)

Application-side view of the mailbox, as in MEMORY_ARCHITECTURE 5.5; registers the application may not access are not listed and return SLVERR.

| Register | Offset | Access | Note |
|---|---|---|---|
| ID_VERSION | 0x0000 | RO | ID and version |
| STATUS | 0x0004 | RO | Request pending, response ready, busy, error |
| REQUEST_DOORBELL | 0x0008 | W1S | Ignored while a request is pending |
| APP_INT_STATUS | 0x0010 | W1C | Application interrupt status |
| APP_INT_ENABLE | 0x0014 | RW | Application interrupt enable |
| SEC_INT_STATUS | 0x0018 | RO | Security interrupt status |
| ERROR_CODE | 0x0020 | RO | Error code |
| REQUEST_BUFFER | 0x0100 | RW | 256 bytes to 0x1FF; write only while no request is pending |
| RESPONSE_BUFFER | 0x0200 | RO | 256 bytes to 0x2FF |

### Layout mailbox_sec (SELECTED)

Security-side view of the mailbox, as in MEMORY_ARCHITECTURE 5.5; registers the security domain may not access are not listed and return SLVERR.

| Register | Offset | Access | Note |
|---|---|---|---|
| ID_VERSION | 0x0000 | RO | ID and version |
| STATUS | 0x0004 | RO | Request pending, response ready, busy, error |
| REQUEST_DOORBELL | 0x0008 | RO | Request doorbell state |
| RESPONSE_DOORBELL | 0x000C | W1S | Sets the response doorbell |
| APP_INT_STATUS | 0x0010 | RO | Application interrupt status |
| SEC_INT_STATUS | 0x0018 | W1C | Security interrupt status |
| SEC_INT_ENABLE | 0x001C | RW | Security interrupt enable |
| ERROR_CODE | 0x0020 | RW | Error code |
| REQUEST_BUFFER | 0x0100 | RO | 256 bytes to 0x1FF |
| RESPONSE_BUFFER | 0x0200 | WO | 256 bytes to 0x2FF |

### Layout aes (PROPOSED)

AES block; the modes and key sizes are not defined. Keys are never readable.

| Register | Offset | Access | Note |
|---|---|---|---|
| MODE | 0x0100 | RW | Algorithm mode and direction |
| KEY_SELECT | 0x0104 | RW | Key slot index |
| IV0 | 0x0108 | WO | Initial value word 0 (words 1 to 3 follow) |
| DATA_IN0 | 0x0120 | WO | Input block word 0 (words 1 to 3 follow) |
| DATA_OUT0 | 0x0140 | RO | Output block word 0 (words 1 to 3 follow) |
| START | 0x0160 | WO | Start one block operation |

### Layout sha (PROPOSED)

SHA-256 block.

| Register | Offset | Access | Note |
|---|---|---|---|
| MODE | 0x0100 | RW | Initialise or continue |
| DATA_IN | 0x0104 | WO | Message word |
| MSG_LENGTH | 0x0108 | RW | Message length in bytes |
| START | 0x010C | WO | Process the buffered block |
| DIGEST0 | 0x0120 | RO | Digest word 0 (words 1 to 7 follow) |

### Layout pka (PROPOSED)

Asymmetric accelerator; the algorithms are not defined (NX-REQ-035), so only the frame is proposed.

| Register | Offset | Access | Note |
|---|---|---|---|
| COMMAND | 0x0100 | WO | Operation command |
| OPERAND_A | 0x0200 | RW | Operand area, 256 bytes |
| RESULT | 0x0300 | RO | Result area, 256 bytes |

### Layout efuse (PROPOSED)

eFuse macro access; the provisioning scheme is not defined.

| Register | Offset | Access | Note |
|---|---|---|---|
| READ_ADDR | 0x0100 | RW | Fuse word to read |
| READ_DATA | 0x0104 | RO | Fuse word value |
| PROG_ADDR | 0x0108 | RW | Fuse word to program |
| PROG_DATA | 0x010C | WO | Value to program |
| PROG_CTRL | 0x0110 | WO | Start a program cycle |
| LOCK_STATUS | 0x0114 | RO | Programmed and locked flags |

### Layout keymgmt (PROPOSED)

Key management; the key hierarchy is not defined.

| Register | Offset | Access | Note |
|---|---|---|---|
| SLOT_SELECT | 0x0100 | RW | Key slot index |
| KEY_CTRL | 0x0104 | WO | Load, derive and clear commands |
| SLOT_STATUS | 0x0108 | RO | Slot valid and usage flags |
| SLOT_LOCK | 0x010C | W1S | Lock a slot until reset |

### Layout secctrl (PROPOSED)

Security control; the debug lifecycle is not defined (NX-ARCH-OI-020).

| Register | Offset | Access | Note |
|---|---|---|---|
| LIFECYCLE_STATE | 0x0100 | RO | Lifecycle state |
| BOOT_CTRL | 0x0104 | RW | Boot source and boot-image controls |
| APP_RESET_CTRL | 0x0108 | RW | Hold or release the C910 reset |
| FAULT_STATUS | 0x010C | W1C | Fault flags |
| DEBUG_CTRL | 0x0110 | RW | Debug enable requests |

### Layout sectimer (PROPOSED)

Security timer and watchdog.

| Register | Offset | Access | Note |
|---|---|---|---|
| COUNT | 0x0100 | RO | Timer count |
| COMPARE | 0x0104 | RW | Timer compare value |
| WDOG_TIMEOUT | 0x0108 | RW | Watchdog timeout |
| WDOG_KICK | 0x010C | WO | Restart the watchdog |
| WDOG_STATUS | 0x0110 | RO | Watchdog state |

## 3. Secure address map (32-bit width, attributes and map SELECTED)

Source: [maps/secure_map.yaml](maps/secure_map.yaml). The cacheability and permission columns are SELECTED (NX-REQ-119, NX-DEC-034, section 3.1), as are the base, size and label of a region (NX-REQ-054).

| Region | First address | Last address | Size | Cacheable | Permissions | Label | NX-REQ |
|---|---|---|---|---|---|---|---|
| Security ROM | 0x0000_0000 | 0x0000_FFFF | 64 KiB | No | r-x | SELECTED | 010, 054 |
| Security SRAM | 0x0001_0000 | 0x0001_FFFF | 64 KiB | No | rw- | SELECTED | 011, 054 |
| OSPI NOR secure aperture | 0x1000_0000 | 0x1FFF_FFFF | 256 MiB | No | r-x | SELECTED | 038, 054 |
| AES | 0x2000_0000 | 0x2000_FFFF | 64 KiB | No | rw- | SELECTED | 013, 054 |
| SHA | 0x2001_0000 | 0x2001_FFFF | 64 KiB | No | rw- | SELECTED | 014, 054 |
| Asymmetric cryptography | 0x2002_0000 | 0x2002_FFFF | 64 KiB | No | rw- | SELECTED | 035, 054 |
| eFuse | 0x2003_0000 | 0x2003_FFFF | 64 KiB | No | rw- | SELECTED | 012, 054 |
| Key management | 0x2004_0000 | 0x2004_FFFF | 64 KiB | No | rw- | SELECTED | 054 |
| Security control | 0x2005_0000 | 0x2005_FFFF | 64 KiB | No | rw- | SELECTED | 054 |
| Security interrupt controller | 0x2006_0000 | 0x2006_FFFF | 64 KiB | No | rw- | SELECTED | 054, 057 |
| Security timer and watchdog | 0x2007_0000 | 0x2007_FFFF | 64 KiB | No | rw- | SELECTED | 054 |
| OSPI registers | 0x2008_0000 | 0x2008_FFFF | 64 KiB | No | rw- | SELECTED | 054 |
| Mailbox (secure side) | 0x2009_0000 | 0x2009_FFFF | 64 KiB | No | rw- | SELECTED | 105, 107, 110, 054 |
| Application boot window | 0x3000_0000 | 0x300F_FFFF | 1 MiB | No | rw- | SELECTED | 105, 106, 109, 054 |

Notes. The security ROM and SRAM capacities of 64 KiB are SELECTED; their bases are proposed. The secure NOR aperture is a range for the security core path and does not select a NOR capacity. The interrupt architecture of the security interrupt controller is OPEN (NX-REQ-057). The mailbox window and the application boot window are the two controlled crossings of NX-DEC-027 (section 4); the boot window is an alias of the 1 MiB application System SRAM aperture and is not a memory of the security domain.

### 3.1 Secure width and attributes (SELECTED, NX-DEC-034)

Width (NX-REQ-033, SELECTED). The secure interconnect has a 32-bit address, a 32-bit data width and 2 outstanding reads and 2 outstanding writes. The security core is a 32-bit RISC-V core, and the highest secure address is 0x300F_FFFF, so every region of the secure map fits in 32 bits; the address-map-check workflow verifies that each region ends inside the declared width. The boot window alias reaches the application System SRAM at 0x00_0000_0000, so the bridge supplies bits 39 to 32 as zero; the width and clock conversion between the secure AXI and AXI-3 stays OPEN (NX-ARCH-OI-038). The data width and the outstanding counts come from the A0 draft and the owner accepted them as written (NX-DEC-034); no RTL evidence is recorded for them.

Attributes (NX-REQ-119, SELECTED). The secure space has no cache: every region is non-cacheable. The security ROM and the OSPI NOR secure aperture are read and execute with no write (program and erase of the NOR go only through its controller registers, as in NX-REQ-111). The security SRAM is read and write with no execute, because security software runs from the ROM (the owner's answer, NX-DEC-034); what runs from the NOR aperture is not defined. The security peripheral windows are device memory, read and write, no execute. The application boot window is read and write with no execute, because the security core places the boot image and never runs it. An unmapped or reserved secure address returns DECERR and an access that a region forbids returns SLVERR, as in NX-REQ-104 for the application space. Privilege levels, lock states and per-register policy of the secure space, and the security interrupt and fault-response details, stay OPEN (NX-ARCH-OI-021).

## 4. Two separate address spaces and two controlled crossings

The application and secure address spaces are separate spaces on separate interconnects (NX-REQ-028, NX-REQ-033, NX-REQ-034). Several numerical ranges of the two maps coincide, for example the secure NOR aperture at 0x1000_0000 and the application camera frame pool at 0x00_1000_0000. That is not a conflict: an address is interpreted in the address space of the interconnect it arrives on (NX-REQ-108), no master reaches both spaces through one decode, and the two files are checked separately.

The boundary has exactly two controlled crossings (NX-DEC-027, NX-REQ-105, SELECTED), and both are default-deny (NX-REQ-108, SELECTED).

| Crossing | Direction | Secure map | Application map | Label | Records |
|---|---|---|---|---|---|
| Boot window | Security core to application | Application boot window, 0x3000_0000 to 0x300F_FFFF (1 MiB alias) | System SRAM, 0x00_0000_0000 to 0x00_000F_FFFF; no other application region and no DDR4 | SELECTED | NX-REQ-105, NX-REQ-106, NX-REQ-109, NX-REQ-113 |
| Mailbox | Application to security | Mailbox (secure side), 0x2009_0000 to 0x2009_FFFF | Mailbox (application side), 0x00_4105_0000 to 0x00_4105_FFFF (SELECTED, NX-REQ-112) | SELECTED | NX-REQ-105, NX-REQ-107, NX-REQ-110, NX-REQ-114, NX-REQ-115 |

The bridge attachment, the mailbox register layout and message format, the interrupt directions and the secure-side validation rule are SELECTED (NX-REQ-113 to NX-REQ-115, NX-DEC-033); the allow-list, requester authentication and the boot-window reset domain stay OPEN (NX-ARCH-OI-038). The security core does not reach DDR4 in this decision. All other secure regions stay unreachable from the application space (NX-REQ-034).

## 5. Open items

| Item | Label | Records | Owner |
|---|---|---|---|
| Mailbox allow-list, requester authentication, replay and flood protection; AXI-3 and System SRAM reset domain; System SRAM attachment point | OPEN | NX-ARCH-OI-038, NX-ARCH-OI-025 | Dinesh |
| Register layout of every block: conventions and registers of each block class | PROPOSED | NX-REQ-117, NX-REQ-118, NX-ARCH-OI-039 | Dinesh |
| Bit fields of every register, and the security and always-on interrupt controllers | OPEN | NX-ARCH-OI-039, NX-REQ-057, NX-ARCH-OI-032 | Dinesh |
| Privilege levels, lock states, per-register policy, security interrupt and fault response of the secure space | OPEN | NX-ARCH-OI-021 | Dinesh |
| PSRAM, NOR and on-chip memory capacities and organisation | OPEN | NX-ARCH-OI-006, NX-ARCH-OI-007 | Dinesh |

## History

| Version | Date | Change |
|---|---|---|
| 0.1.0-draft | 2026-11-12 | First part 2 draft for KOS-NEXUS-008: the two map files and their tables |
| 0.2.0-draft | 2026-11-12 | Part 3: the two controlled crossings (NX-DEC-027) added to the secure map and the separation section |
| 0.2.1-draft | 2026-11-12 | The map checker exists (scripts/check_address_maps.py); rule 6 and the open items updated |
| 0.2.2-draft | 2026-11-13 | Records of NX-DEC-029 added to the System SRAM, peripheral space and NOR regions and to the two crossing regions |
| 0.3.0-draft | 2026-11-13 | NX-DEC-030: both maps and every region are SELECTED; the width confirmation is OPEN for every master except the C910 |
| 0.4.0-draft | 2026-11-13 | Section 2.1: the peripheral register space is divided into APB-0 and APB-1 windows and per-instance windows (SELECTED, NX-REQ-112) |
| 0.5.0-draft | 2026-11-13 | NX-DEC-031: the width confirmation is closed by the owner's statement for every application master |
| 0.6.0-draft | 2026-11-13 | PLIC and CLINT windows added to section 2.1 (NX-REQ-116); the crossing details are proposed (NX-REQ-113 to NX-REQ-115) |
| 0.7.0-draft | 2026-11-13 | NX-DEC-033: the peripheral register windows, the crossing details and the interrupt controller baseline are SELECTED |
| 0.8.0-draft | 2026-11-13 | Section 2.2 register layouts (NX-REQ-117, NX-REQ-118, PROPOSED), section 3.1 and attribute columns of the secure map (NX-REQ-033, NX-REQ-119, PROPOSED) |
| 0.9.0-draft | 2026-11-13 | NX-DEC-034: the secure width and parameters (NX-REQ-033) and the secure attributes (NX-REQ-119) are SELECTED |
