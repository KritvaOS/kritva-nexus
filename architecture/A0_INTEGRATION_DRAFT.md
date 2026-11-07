# Kritva Nexus SoC - A0 Integration Draft

Working draft imported from a discussion. Status: PROPOSED. Not approved.
Owner: Dinesh. Kritva Nexus is outside the Kritva V2 plan and is planned
for V3. It is not registered in Kritva Program V2. This document does not
create a V2 programme mapping or a V2 status.json.

Provenance: this file is a reconstruction of the latest A0 architecture
discussion, produced by ChatGPT and imported by Claude for the owner on
2026-11-06. It is not a verbatim recovery of an original A0 document, and
no original A0 file was available as a source. It has not been reviewed
against any other source. Where it disagrees with the owner's own
statements, the owner's statements win and this file is corrected by a
dated addendum, not silently.

This document records the A0 architecture direction and integration
discussion available at the time of import. It is not a frozen architecture
baseline. Values and implementation details are labelled SELECTED,
PROPOSED, OPEN or UNVERIFIED to distinguish owner decisions from
engineering proposals and unresolved questions. The SELECTED items are
recorded in [../decisions/DECISIONS.md](../decisions/DECISIONS.md) and
[../requirements/REQUIREMENTS.md](../requirements/REQUIREMENTS.md).

## 1. Architecture overview

Kritva Nexus is the application-processing and AI SoC for the Kritva
robotics platform. It interfaces with Kritva Edge over EtherCAT.

The architecture includes:

- An application CPU cluster.
- Application AXI fabrics and AXI-to-APB peripheral interconnects.
- DDR4 primary system memory, Octal SPI PSRAM secondary memory and
  OSPI NOR primary boot storage.
- Camera capture, frame storage, ISP and NPU processing.
- Display and multimedia functions.
- Ethernet MACs supporting standard Ethernet and EtherCAT MainDevice use.
- A separate security management subsystem.
- Always-on, clock, reset, power and interrupt control.
- Peripheral interfaces for board-level and subsystem integration.

The architecture is at A0 discussion-draft level. Detailed subsystem
specifications, address allocation, clocking, reset sequencing, CDC/RDC,
verification and physical implementation remain to be completed.

## 2. Application CPU cluster

### 2.1 CPU IP and cluster

**CPU IP: Xuantie C910**

Label: PROPOSED

The application CPU direction is Xuantie C910, using the RV64 ISA.

The discussed cluster configuration is:

| Parameter | Direction |
|---|---|
| CPU IP | Xuantie C910 |
| ISA | RV64 |
| Cores | 4 |
| Cluster | Single cluster with shared L2 |
| Frequency | 1.0-1.2 GHz target |
| DVFS | Agreed for C910 |
| L1 instruction cache | 64 KB per core |
| L1 data cache | 64 KB per core |
| Shared L2 cache | 1 MB |

The C910 direction is not treated as a formally selected CPU IP decision
in this draft. The exact RTL release and configuration must be confirmed.

The 1.0-1.2 GHz frequency is a target, not a timing-closure result.

### 2.2 CPU AXI interface

Label: PROPOSED / OPEN

The discussed CPU interface direction is:

| Parameter | Direction |
|---|---|
| Protocol | AXI4 |
| Data width | 128-bit |
| Address width | 40-bit, subject to confirmation |
| Outstanding reads | 8 AR |
| Outstanding writes | 8 AW |

The 40-bit application address width has not been confirmed against the
exact C910 RTL configuration.

The C910-to-peripheral access path through AXI-0 and the AXI-to-APB
interconnects remains unresolved.

### 2.3 Interrupts, timers and debug

Label: PROPOSED

The discussed CPU-side interrupt and timer direction is:

- 128 external interrupt sources.
- 16 inter-processor interrupts (IPI).
- A shared 64-bit timebase.
- A 32.768 kHz RTC.
- Per-hart timer compare support.
- TAP-based debug.

The exact C910 interrupt-controller integration must be confirmed.
The choice between PLIC/CLINT-style integration and RISC-V AIA remains
open pending confirmation of the selected C910 configuration.

### 2.4 CPU power management and implementation support

Label: PROPOSED, except DVFS support which is SELECTED

The CPU subsystem is expected to support:

- Clock gating.
- Power gating.
- DVFS.
- Hardware performance counters.
- Scan test.
- MBIST support for applicable memories.

The detailed clock, reset, power-control and DFT implementation is not
frozen.

## 3. Camera, frame storage, ISP and NPU

### 3.1 Camera inputs

Label: PROPOSED

The initial camera architecture discussion assumes:

- Four simultaneous cameras.
- Maximum initial resolution of 640x640 per camera.
- 10 FPS per camera.
- Bayer RAW10 and RAW12 input formats.

These are architecture targets and require interface and workload
verification.

### 3.2 Camera frame pool

Label: SELECTED for usable capacity; PROPOSED for organization

The owner-selected usable frame-pool capacity is 6 MiB.

The discussed organization is:

- Eight logical frame slots.
- Two logical slots per camera.
- A shared physical frame pool with per-camera allocation.
- Packed Bayer RAW storage.
- NPU-pull operation using frame descriptors and tile requests.

The logical frame-slot organization and physical memory implementation
are not frozen.

The capacity calculations discussed are:

| Format | Approximate frame size | Eight-frame storage |
|---|---:|---:|
| RAW10 | 500 KiB | 3.906 MiB |
| RAW12 | 600 KiB | 4.6875 MiB |

For the RAW12 calculation, the discussed remaining capacity within the
6 MiB usable pool is 1.312 MiB.

The 6 MiB figure is usable frame-pool capacity. ECC storage overhead is
not included in that figure.

### 3.3 Frame ownership and release

Label: PROPOSED

The discussed frame lifecycle is:

1. Camera capture writes a complete frame into an allocated frame slot.
2. The frame is made available to the consumer through a frame descriptor.
3. The NPU requests frame tiles.
4. The source frame is released after source consumption.
5. Inference completion is a separate event from source-frame release.

If no frame buffer is available, the proposed behavior is to drop the
complete frame. A partially captured frame must not be exposed as valid.

Controlled buffer borrowing was discussed as an optional policy.

The maximum source-consumption and release latency has not been selected.
A 100 ms value was discussed as a proposal only.

### 3.4 ISP

Label: PROPOSED

The ISP processing stages discussed include:

- Unpacking.
- Black-level correction.
- Defect-pixel correction.
- Lens-shading correction.
- Demosaic.
- White balance.
- Color correction.
- Gamma correction.

The exact ISP pipeline stages and their ordering remain to be specified.

RGB is the default ISP output direction for first silicon.

RGB888 channel ordering was discussed as a proposal and is not frozen.

Candidate ISP tile sizes are 64x64 and 128x128. Neither is selected.
Bayer halo requirements remain open.

A proposed ISP throughput target is 24.576 Mpixel/s.

### 3.5 ISP-to-NPU interface

Label: PROPOSED

The discussed interface direction is:

- 128-bit data path.
- VALID/READY handshake.
- Byte-valid indication.
- Row-major tile output.
- One active tile per camera.

The interface details and throughput requirements remain to be verified.

### 3.6 NPU

Label: PROPOSED, except DVFS support which is SELECTED

The discussed NPU direction is:

- Four homogeneous clusters.
- 8 TOPS INT8 peak target.
- INT8 inputs and weights.
- INT32 accumulators.
- DVFS support.

A 32x32 array at 1 GHz was discussed as a possible implementation,
not a selected architecture requirement.

INT16, FP16 and BF16 support are excluded from the discussed first-silicon
direction.

The exact NPU architecture, cluster interconnect, local SRAM organization,
model-loading mechanism and performance are not frozen.

### 3.7 AI and vision memory organization

Label: PROPOSED

Three logically distinct local memory resources are discussed:

1. Camera frame pool.
2. ISP local SRAM.
3. NPU local SRAM for activations and weights.

The normal camera-to-frame-pool-to-ISP-to-NPU path is not intended to
require DDR intermediate storage.

DDR may be used for large intermediates, recording, debug, large models,
activations or datasets.

The frame-pool bank count, width, port organization and ECC implementation
remain open.

Eight banks with 64-bit width and 1R1W access were discussed as a
recommendation only, not as an owner-selected configuration.

MBIST is required for applicable on-chip memories. ECC requirements
and implementation remain to be evaluated.

### 3.8 Camera and vision workload calculations

Label: PROPOSED workload assumptions

The discussion used the following aggregate workload:

| Parameter | Value |
|---|---:|
| Aggregate pixel rate | 16.384 Mpixel/s |
| Aggregate frame rate | 40 FPS |
| RAW10 input traffic | 20.48 MB/s |
| RAW12 input traffic | 24.576 MB/s |
| RGB888 output traffic | 49.152 MB/s |

These are workload calculations based on the discussed camera assumptions,
not measured silicon performance.

### 3.9 SoC power target

Label: PROPOSED

A total SoC power target of 10-20 W was discussed.

This is a target range, not a measured or verified power estimate.
The power budget by subsystem, operating mode and workload remains open.

## 4. External memory architecture

### 4.1 Memory roles

The owner-selected memory roles are:

| Memory | Role | Label |
|---|---|---|
| DDR4 | Primary system memory | SELECTED |
| Octal SPI PSRAM | Secondary memory | SELECTED |
| OSPI NOR | Primary boot medium | SELECTED |

The NOR and PSRAM are separate devices with separate controllers.

### 4.2 DDR4

Label: SELECTED for primary-memory role; PROPOSED for operating target

The discussed DDR4 operating target is DDR4-3200.

DDR4-3200 means 3200 MT/s per pin, with a CK frequency of 1600 MHz.

The DDR4 data width and capacity have not been selected.

The DDR4 subsystem is expected to serve:

- Linux and application memory.
- NPU models and large activations.
- Display framebuffers.
- Ethernet and DMA buffers.
- Other large system-memory allocations.

The DDR4 controller ingress topology and number of upstream ports remain
open.

### 4.3 Octal SPI PSRAM

Label: SELECTED for secondary-memory role; PROPOSED for controller target

The discussed PSRAM controller frequency target is 200-400 MHz.

The exact PSRAM protocol, operating mode, capacity and bandwidth remain
open.

### 4.4 OSPI NOR

Label: SELECTED for primary boot-medium role; PROPOSED for interface details

The discussed interface example is OSPI DDR x8 at 200 MHz, with a
theoretical bandwidth example of 400 MB/s.

This is an example calculation, not a confirmed device or controller
performance requirement.

The NOR is intended to hold boot firmware, bootloader and recovery
content, configuration and authenticated updates.

The secure boot path must be able to access NOR before the application
fabrics and C910 are active.

## 5. Display and multimedia

### 5.1 Display mode and interface

Label: SELECTED

The owner-selected display direction is:

- 720p60.
- Resolution 1280x720.
- Refresh rate 60 Hz.
- Parallel DPI interface.
- Three composition layers.

The display interface's exact electrical configuration and pin assignment
remain to be specified.

### 5.2 Display timing

Label: PROPOSED

The discussed reference timing is:

| Parameter | Value |
|---|---:|
| Pixel clock | 74.25 MHz |
| Horizontal active | 1280 |
| Horizontal total | 1650 |
| Vertical active | 720 |
| Vertical total | 750 |

The timing values are a proposed implementation reference and are not
separately recorded as owner-selected decisions.

### 5.3 Display compositor and formats

Label: PROPOSED

The discussed compositor direction includes:

- Three independent framebuffers.
- Alpha composition.
- Z-order control.
- Double buffering.
- Atomic update at Vsync.
- Programmable display timing.
- Underflow detection.
- Independent pixel clock.

The discussed pixel formats are:

- RGB565.
- RGB888.
- XRGB8888.
- ARGB8888.

The proposed memory interface uses AXI4 DMA and AXI4-Lite control.

Linux DRM/KMS support is required by the proposed software architecture.

Framebuffers are expected to reside in DDR4, with local line/output FIFO
storage in the display subsystem.

### 5.4 Display bandwidth calculations

Label: PROPOSED workload calculations

For 720p60, the discussed active-pixel rate is 55.296 Mpixel/s.

The discussed full-screen layer read traffic is:

| Pixel format | One layer |
|---|---:|
| RGB565 | 110.592 MB/s |
| RGB888 | 165.888 MB/s |
| XRGB8888 | 221.184 MB/s |

For three full-screen layers, the discussed nominal active read traffic is:

| Pixel format | Three layers |
|---|---:|
| RGB565 | 331.776 MB/s |
| RGB888 | 497.664 MB/s |
| XRGB8888 / ARGB8888 | 663.552 MB/s |

These are active-pixel traffic calculations. They do not include additional
burst, arbitration, refresh or implementation overhead.

## 6. Ethernet and EtherCAT

### 6.1 Ethernet MAC architecture

Label: SELECTED for MAC count and independence; PROPOSED for detailed
implementation

The owner selected two independent Ethernet MACs.

The discussed interface direction for both MACs is:

- 10/100/1000 Mbps.
- RGMII.
- External PHYs.
- Configurable operation as standard Ethernet or EtherCAT MainDevice.

Both MACs are intended to support standard Ethernet operation and
EtherCAT MainDevice operation.

Two MACs alone do not guarantee EtherCAT redundancy. Redundancy depends
on the software stack and driver support.

### 6.2 RGMII

Label: PROPOSED

The discussed RGMII clock frequencies are:

| Ethernet rate | RGMII clock |
|---|---:|
| 10 Mbps | 2.5 MHz |
| 100 Mbps | 25 MHz |
| 1000 Mbps | 125 MHz |

RGMII uses DDR signaling over a 4-bit data interface.

The implementation must avoid applying delay twice. Internal MAC delay
and board-level delay must be configured intentionally.

### 6.3 MAC data path and DMA

Label: PROPOSED

The discussed MAC integration includes:

- TX and RX DMA descriptors.
- AXI4 master data access.
- AXI4-Lite register control.
- QoS and arbitration integration.

The detailed descriptor format, buffer ownership, interrupt behavior,
DMA coherency and error handling remain to be specified.

### 6.4 EtherCAT MainDevice

Label: PROPOSED

The MAC is expected to support EtherCAT MainDevice traffic using raw
Ethernet frames.

EtherCAT uses EtherType 0x88A4. The MAC and its receive filtering must
not reject EtherCAT traffic through an IP-only filtering policy.

A separate EtherCAT Slave Controller (ESC) is not mandatory for
MainDevice operation.

EtherCAT Distributed Clocks are implemented by SubDevices. MAC
timestamping is not a substitute for Distributed Clock functionality.

Hardware timestamping was discussed as a proposal only; it is not
selected.

## 7. Security Management Subsystem

### 7.1 Security processor and local resources

Label: SELECTED

The owner-selected security architecture includes:

- A dedicated isolated 32-bit RISC-V security core.
- Its own 64 KiB ROM.
- Its own 64 KiB SRAM.
- A dedicated eFuse resource.
- AES-128 and AES-256 support.
- SHA-256 support, mandatory.
- An asymmetric cryptography accelerator in the security domain.
- A dedicated separate secure AXI interconnect.

The asymmetric cryptography accelerator is part of the discussed security
architecture. Its algorithms and exact implementation remain open.

### 7.2 Secure interconnect

Label: SELECTED for a separate secure AXI interconnect; PROPOSED for
detailed parameters

The discussed secure AXI interface parameters are:

| Parameter | Direction |
|---|---|
| Data width | 32-bit |
| Address width | 32-bit |
| Outstanding reads | 2 |
| Outstanding writes | 2 |

Only explicitly authorized secure connections are to be present on the
secure AXI interconnect.

The application AXI interconnect must not provide access to:

- Security ROM.
- Security SRAM.
- eFuse.
- Cryptographic key management.
- Security interrupt controller.

The exact hardware access-control implementation and its verification
remain to be specified.

### 7.3 Secure boot sequence

Label: PROPOSED

The discussed secure boot sequence is:

1. Always-on domain becomes active.
2. Security ROM and eFuse resources become available to the security core.
3. Security core accesses OSPI NOR through the authorized secure path.
4. Security core authenticates the boot image.
5. Security core authorizes release of the C910 reset.
6. C910 initializes DDR4 and PSRAM.
7. Remaining SoC subsystems are initialized.
8. Linux and Kritva software start.

The security core starts first. The immutable ROM authenticates the boot
image and authorizes C910 release.

The security core must have an authorized OSPI NOR access path before
the application fabric is active.

C910 reset release must be hardware-controlled by the security domain.

### 7.4 Secure address space

Label: PROPOSED

The secure address space is separate from the application address space.

Numerical address ranges may overlap between the two address spaces
without conflict because they are isolated by separate buses and address
spaces. This separation must be explicit in the architecture and
interconnect documentation.

The following secure map was discussed as a proposal. It is not frozen.

| Secure region | Proposed address range |
|---|---|
| Security ROM | 0x00000000-0x0000FFFF |
| Security SRAM | 0x00010000-0x0001FFFF |
| OSPI NOR secure aperture | 0x10000000-0x1FFFFFFF |
| AES | 0x20000000 |
| SHA | 0x20010000 |
| Asymmetric cryptography | 0x20020000 |
| eFuse | 0x20030000 |
| Key management | 0x20040000 |
| Security control | 0x20050000 |
| Security interrupt controller | 0x20060000 |
| Security timer/watchdog | 0x20070000 |
| OSPI registers | 0x20080000 |

The base addresses and address windows are proposals only.

### 7.5 Security items not yet specified

Label: OPEN

The following remain open:

- Hash and signature formats.
- Signature algorithms.
- Root-key provisioning.
- Anti-rollback policy and implementation.
- Recovery and authenticated recovery procedure.
- Debug lifecycle and debug authorization.
- eFuse programming and access-control lifecycle.
- Security fault reporting and response.
- Cryptographic accelerator register interfaces.
- Key-management interface and policy.

Raw secrets must not be exposed through ordinary application interfaces.
The detailed eFuse operation and status interface remains to be specified.

## 8. Peripheral subsystem

### 8.1 Owner-requested peripheral counts

Label: SELECTED for the requested counts

The owner-requested peripheral counts are:

| Peripheral | Count | Label |
|---|---:|---|
| PWM | 16 | SELECTED |
| GPIO | 32 | SELECTED |
| General-purpose timers | 4 | SELECTED |
| UART | 4 | SELECTED |
| I2C masters | 4 | SELECTED |
| SPI master | 1 | SELECTED |
| SPI slave | 1 | SELECTED |
| I2S masters | 2 | SELECTED |

The counts are selected. Detailed peripheral features and implementation
parameters are not thereby selected.

### 8.2 Peripheral implementation details

Label: PROPOSED / OPEN

The following details remain to be defined:

- PWM resolution, frequency, polarity and complementary-output behavior.
- GPIO interrupt and debounce capabilities.
- General-purpose timer width and capture/compare features.
- UART FIFO depth, baud-rate support and DMA integration.
- I2C speed modes, FIFO and DMA support.
- SPI modes, FIFO and transfer-length behavior.
- I2S sample rates, data widths, channel configuration and clocking.
- Pin multiplexing and package pin assignment.

Dedicated pins were assumed for initial architectural counting.
Pinmux and final pin allocation were deferred.

## 9. Application interconnect architecture

### 9.1 Application AXI fabrics

Label: SELECTED for the four-fabric architecture concept; PROPOSED for
widths, frequencies and detailed topology

The owner agreed to four application AXI fabrics.

The discussed functional partitioning is:

| Fabric | Main role | Discussed data width | Discussed frequency |
|---|---|---:|---:|
| AXI-0 | Main system, CPU and memory | 128-bit | 400-600 MHz |
| AXI-1 | AI and vision: ISP, NPU and camera | 256-bit | 400-600 MHz |
| AXI-2 | Multimedia and high-speed IO: display, Ethernet and storage | 128-bit | 400-600 MHz |
| AXI-3 | General peripherals, control and DMA | 64-bit | 400-600 MHz |

A nominal 500 MHz operating point was discussed.

These widths and frequencies are proposals, not owner-selected
requirements.

### 9.2 Theoretical fabric bandwidth

Label: PROPOSED calculations

The theoretical per-direction bandwidth at the nominal 500 MHz point is:

| Fabric | Data width | Theoretical bandwidth |
|---|---:|---:|
| AXI-0 | 128-bit | 8 GB/s |
| AXI-1 | 256-bit | 16 GB/s |
| AXI-2 | 128-bit | 8 GB/s |
| AXI-3 | 64-bit | 4 GB/s |

The corresponding theoretical bandwidth at the discussed frequency
range is:

| Fabric | At 400 MHz | At 600 MHz |
|---|---:|---:|
| AXI-0 | 6.4 GB/s | 9.6 GB/s |
| AXI-1 | 12.8 GB/s | 19.2 GB/s |
| AXI-2 | 6.4 GB/s | 9.6 GB/s |
| AXI-3 | 3.2 GB/s | 4.8 GB/s |

These are theoretical interface calculations, not measured system
bandwidth or guaranteed sustained throughput.

### 9.3 Proposed master placement

Label: PROPOSED

The discussed master placement is:

| Master or subsystem | Proposed fabric |
|---|---|
| C910 AXI master | AXI-0 |
| ISP, NPU and camera DMA | AXI-1 |
| Display, Ethernet and storage DMA | AXI-2 |
| Peripheral and I2S DMA | AXI-3 |

Local SRAM paths should connect to the relevant subsystem fabric where
appropriate. Camera frame-pool, ISP and NPU local-memory transfers should
not be forced through DDR4.

### 9.4 Memory Access Crossbar

Label: PROPOSED

A separate Memory Access Crossbar (MAX) was recommended to avoid
serializing all memory access through AXI-0.

The proposed MAX has four fabric ingress ports. This is not selected
and remains to be specified.

The MAX is expected to support:

- Read and write arbitration.
- QoS.
- Address decode.
- Outstanding transaction handling.
- Burst handling.
- Error handling.
- Access protection.

The exact relationship between the four AXI fabrics, MAX and DDR4
controller ingress ports remains open.

Four fabric ingress ports do not establish the number of DDR4 controller
ports.

### 9.5 AXI-to-APB interconnects

Label: SELECTED for count; PROPOSED for detailed parameters and routing

The owner agreed to two AXI-to-APB interconnects.

The discussed APB bridge direction is:

- 32-bit APB data width.
- 200-250 MHz target frequency.
- APB-0 peripheral address region around 0x40000000.
- APB-1 control address region around 0x41000000.

These detailed parameters and address regions are proposals.

The C910 path to APB peripherals through AXI-0 and the bridge arrangement
has not been defined completely.

### 9.6 Application address map

Label: PROPOSED

The following 40-bit application address map was discussed:

| Region | Proposed address range |
|---|---|
| System SRAM | 0x00000000-0x000FFFFF |
| Camera frame pool | 0x10000000-0x10FFFFFF |
| ISP SRAM | 0x11000000-0x11FFFFFF |
| NPU SRAM | 0x12000000-0x13FFFFFF |
| Reserved | 0x14000000-0x1FFFFFFF |
| Peripherals | 0x40000000-0x4FFFFFFF |
| NOR | 0x60000000-0x6FFFFFFF |
| PSRAM | 0x70000000-0x7FFFFFFF |
| DDR4 | 0x10_0000_0000-0x1F_FFFF_FFFF |

The frame-pool address aperture is 16 MiB. The usable frame-pool capacity
selected by the owner is 6 MiB. The aperture is not the physical memory
capacity.

The address windows for ISP SRAM and NPU SRAM are apertures, not selected
physical memory capacities.

The DDR4 address window reserves 64 GiB of address space. It does not
select a 64 GiB physical DDR4 device.

The application address width remains unconfirmed against the exact
C910 configuration.

Cacheability, coherency, security attributes, read/write/execute
permissions and IOMMU requirements remain open.

### 9.7 Application AXI and APB control access

Label: OPEN

The application interconnect must define the C910-to-APB access path.

A proposed path is:

C910 -> AXI-0 -> AXI routing or bridge -> AXI-to-APB -> APB-0/APB-1

This is a proposal only. Routing, decode, access control, bridge
placement and error response behavior remain open.

## 10. Clock, reset, power and interrupt architecture

### 10.1 Clock frequency directions

Label: PROPOSED

The discussed clock directions are:

| Subsystem | Discussed frequency |
|---|---:|
| C910 | 1.0-1.2 GHz target |
| NPU | 800 MHz target |
| ISP | 600 MHz |
| Security core | 200-400 MHz |
| AXI fabrics | 400-600 MHz |
| APB | 200-250 MHz |
| PSRAM controller | 200-400 MHz |
| DPI pixel clock | 74.25 MHz |

The DDR4 PHY requires dedicated PLL/DLL and calibration support.

These frequencies are targets or architecture proposals, not verified
timing results.

### 10.2 PLL architecture

Label: PROPOSED

The discussed PLL architecture is:

- Four integer PLLs.
- Two fractional PLLs.

The exact PLL allocation, frequency plan, jitter, clock relationships
and feasibility remain to be established.

### 10.3 DVFS

Label: SELECTED for C910 and NPU DVFS support; PROPOSED for implementation

DVFS support for C910 and NPU was agreed.

The implementation requires clock and voltage control. PMIC selection,
voltage rails, transition sequencing, operating points and power-state
policy remain open.

### 10.4 Power domains

Label: PROPOSED

Seven logical power domains were discussed:

- AON.
- SEC.
- CPU.
- MEM.
- AI.
- MEDIA.
- IO.

These are logical domains and do not necessarily imply seven separate
voltage rails.

The physical power-domain implementation and rail partitioning remain
open.

### 10.5 Reset domains

Label: PROPOSED

The discussed reset-domain partition is:

- AON.
- SEC.
- CPU.
- MEM.
- AI.
- ISP.
- DISP.
- IO.

Reset behavior is expected to use asynchronous assertion and synchronous
deassertion.

The security domain must be able to control C910 reset release.
A C910 warm reset must not reset the security domain.

The complete reset tree, reset sources, reset dependencies and
subsystem-specific reset behavior remain to be specified.

### 10.6 Interrupt architecture

Label: PROPOSED / OPEN

The discussed interrupt architecture includes:

- An application interrupt controller, with PLIC or AIA selection
  dependent on the C910 integration.
- 128 application external interrupt sources as a CPU-side direction.
- Four harts in the discussed C910 cluster.
- A separate security interrupt controller with 32 sources.
- An always-on interrupt controller with 8-16 wake sources.

The exact C910 PLIC/CLINT versus AIA integration remains open.

Critical thermal, power and tamper faults require hardware response
independent of application CPU execution.

### 10.7 CDC and RDC

Label: PROPOSED

Clock-domain crossing and reset-domain crossing verification are
mandatory engineering activities.

The design must use appropriate synchronizers, asynchronous FIFOs and
reset synchronizers for the relevant crossings.

Unsafe multi-bit synchronization must not be used.

CDC/RDC checks and documented waivers are required.

The exact clock-domain matrix, reset-domain matrix, synchronizer
implementation and waiver criteria remain to be established.

## 11. Toolchain and evidence architecture

Label: PROPOSED

The engineering toolchain discussed for Nexus includes:

| Tool | Intended role |
|---|---|
| Icarus Verilog | Lightweight RTL simulation |
| Verilator | Lint, compiled simulation and co-simulation |
| Yosys | RTL synthesis |
| OpenLane 2 | Block-level physical-design flow |
| OpenROAD | Physical-design backend |
| Renode | Kritva Nexus Simulator / virtual-platform simulation |
| GTKWave | Waveform viewing |
| OpenOCD and vendor tools | Board bring-up and debug, as required |

The toolchain choices and their repository implementation belong to
KOS-NEXUS-002. This architecture draft records the discussed direction
but does not establish that all tools have been installed, qualified
or selected for every block.

### 11.1 Simulation and co-simulation

Label: PROPOSED

Renode is the Kritva Nexus Simulator workstream.

Renode is a virtual-platform simulator. It is not equivalent to a
cycle-accurate C910 model.

Verilator co-simulation can connect selected actual RTL blocks to the
simulator environment.

A Renode CPU model must not be treated as C910 validation without
confirming ISA, privilege, MMU and other relevant compatibility.
It must not be treated as cycle-accurate validation of C910 timing,
cache behavior or performance.

### 11.2 RTL reuse and technology wrappers

Label: PROPOSED

The same functional RTL is intended to be reusable across simulation,
FPGA and ASIC contexts.

The discussed wrapper structure is:

- technology/generic
- technology/fpga
- technology/asic

Technology-dependent memory, clock, reset, scan and MBIST implementation
must be mapped through suitable wrappers.

Examples discussed include:

- Generic memory models for simulation.
- FPGA block RAM mapping for FPGA implementation.
- ASIC SRAM macro mapping for ASIC implementation.

The exact wrapper APIs and technology-specific implementation remain
to be defined.

### 11.3 FPGA prototyping

Label: PROPOSED / OPEN

FPGA prototyping is part of the engineering plan.

The FPGA board selection remains open.

The C910 RTL and DDR PHY suitability for the selected FPGA platform must
be verified.

An alternative RISC-V CPU on FPGA may validate platform interfaces, but
does not count as C910 validation.

FPGA synthesis and place-and-route results are distinct from tests
performed on a programmed FPGA board.

### 11.4 OpenLane scope

Label: PROPOSED

OpenLane 2 and OpenROAD are intended for block-level physical-design
work where the required technology collateral, memory macros,
constraints and tool support are available.

The discussion does not establish that the complete Nexus SoC can be
implemented through OpenLane.

### 11.5 RTL module design guidance

Label: PROPOSED

The discussed RTL module-size guidance is:

- Target: 300-800 lines.
- More than 1000 lines: review.
- More than 1500 lines: consider decomposition.

These are review guidelines, not hard limits.

Module review should consider responsibility, clock domains, complexity,
ports, state, FSMs, fanout and verification requirements.

Each module specification is expected to include:

- Module ID and name.
- Subsystem.
- Purpose.
- Requirements.
- Ports.
- Clock and reset domains.
- CDC behavior.
- Reset behavior.
- Register and data interfaces.
- Parameters.
- Technology dependencies.
- Verification requirements.
- Synthesis and physical-design concerns.

### 11.6 Evidence classification

Label: PROPOSED

The discussed evidence classification is:

| Activity | Evidence category |
|---|---|
| RTL lint | Software |
| Yosys synthesis | Software |
| FPGA synthesis and place-and-route | Software |
| OpenLane runs | Software |
| Icarus simulation | Simulation |
| Verilator simulation | Simulation |
| Renode simulation | Simulation |
| RTL co-simulation | Simulation |
| Tests on a programmed FPGA board | Physical |

OpenLane DRC, LVS and STA results were discussed as software evidence
pending explicit owner confirmation of the evidence policy.

Evidence records should identify:

- Target: RTL, FPGA or ASIC.
- Tool and version.
- Configuration.
- Source commit.
- CI run.

This is a proposed local evidence approach. It does not establish a
Kritva V2 status schema or a V2 programme mapping.

## 12. Open issues and architecture gaps

The following items remain open. The gap identifiers are retained as
canonical identifiers and must not be renumbered.

### NX-ARCH-GAP-001 - C910-to-APB access path

The C910 access path to APB peripherals through AXI-0 is not fully
defined.

The proposed path is:

C910 -> AXI-0 -> AXI routing or bridge -> AXI-to-APB -> APB-0/APB-1

The routing, decode, access control, bridge placement and error behavior
must be resolved.

### NX-ARCH-GAP-002 - Secure and application address spaces

The secure and application address maps contain overlapping numerical
ranges in the discussion.

The architecture must explicitly document that these are separate
address spaces on separate interconnects, and define the isolation
boundary and permitted access paths.

### NX-ARCH-GAP-003 - C910 application address width

The proposed 40-bit application address width has not been confirmed
against the exact C910 RTL configuration.

The selected C910 configuration and address-width compatibility must
be verified before the application address map is frozen.

### NX-ARCH-GAP-004 - DDR4 controller ingress

The DDR4 controller ingress topology and number of upstream ports
remain open.

The four application AXI fabrics and a proposed four-ingress MAX do not
establish the DDR4 controller port count.

### Additional open issues

#### CPU and application interconnect

- Exact C910 RTL release and configuration.
- Confirmation of cache sizes and CPU cluster configuration.
- Confirmation of AXI interface parameters against C910 RTL.
- PLIC/CLINT versus AIA integration.
- Application address-map attributes: cacheability, coherency, security
  and read/write/execute permissions.
- IOMMU requirements.
- AXI routing, decode, QoS, outstanding transactions and error behavior.

#### Memory

- DDR4 width and capacity.
- DDR4 controller port count and ingress topology.
- PSRAM protocol, mode, capacity and bandwidth.
- OSPI NOR device and controller details.
- Memory arbitration and bandwidth allocation.
- Frame-pool bank count, width, port organization and ECC implementation.
- ISP SRAM and NPU SRAM physical organization.
- Memory macro selection and MBIST implementation.

#### Camera, ISP and NPU

- Camera electrical interface and capture details.
- Exact ISP pipeline and stage ordering.
- Bayer halo requirements.
- ISP tile size selection.
- ISP-to-NPU interface details.
- NPU architecture and implementation.
- NPU model and tensor-format requirements.
- Frame-buffer release-latency bound.
- Buffer-borrowing policy.
- DDR use for optional intermediates and recording.
- Subsystem power budgets and measured workload performance.

#### Display and multimedia

- DPI electrical and pin configuration.
- Final pixel-format selection.
- Compositor implementation and framebuffer policy.
- Display DMA coherency and bandwidth margin.
- Underflow behavior and recovery.
- DRM/KMS integration details.

#### Ethernet and EtherCAT

- External PHY selection.
- MAC register and descriptor interfaces.
- DMA buffer coherency.
- Hardware timestamping decision.
- EtherCAT stack and driver support.
- Redundancy implementation and verification.
- RGMII delay configuration at MAC and board level.

#### Security

- Signature and hash formats.
- Asymmetric cryptographic algorithms.
- Root-key provisioning.
- Anti-rollback policy.
- Recovery behavior.
- Debug lifecycle and authorization.
- eFuse programming and access control.
- Secure address-map finalization.
- Security interrupt and fault-response details.
- Secure boot failure handling.

#### Peripherals

- PWM capabilities and timing.
- GPIO interrupt behavior.
- Timer width and features.
- UART FIFO, baud-rate and DMA details.
- I2C speed modes and DMA details.
- SPI modes and FIFO details.
- I2S sample rates, widths and clocking.
- Pinmux and package pin assignment.

#### Clock, reset and power

- PLL allocation and feasibility.
- Clock source and clock-tree architecture.
- Jitter requirements.
- DVFS operating points and voltage sequencing.
- PMIC and rail selection.
- Power-domain implementation.
- Reset sources and reset sequencing.
- Clock-domain and reset-domain matrices.
- CDC/RDC waiver policy.
- Independent hardware response to critical faults.

#### Toolchain, FPGA and physical design

- Tool versions and qualified configurations.
- FPGA board selection.
- C910 RTL compatibility with FPGA target.
- DDR PHY availability and suitability.
- Renode CPU model compatibility.
- RTL co-simulation boundary.
- Technology wrapper interfaces.
- SRAM macro and technology collateral availability.
- OpenLane block-level scope and supported targets.
- FPGA and ASIC implementation constraints.
- Evidence metadata and acceptance policy.

#### Programme and governance boundary

Kritva Nexus is outside the Kritva V2 plan and is planned for V3.

Nexus has no V2 programme registration, no V2 status.json and no V2
programme mapping.

NX-M0 through NX-M8 are local Nexus engineering milestones. Any future
mapping to Kritva V3 must be established through the V3 planning process.

All Nexus owner and reviewer roles are Dinesh.

This draft is PROPOSED and is not an approved or frozen architecture
baseline.
