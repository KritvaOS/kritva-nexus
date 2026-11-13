# Kritva Nexus System Architecture

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-ARCH-001 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Architecture |
| Status | DRAFT (partial; not reviewed or approved) |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.20.0-draft |
| Last Updated | 2026-11-13 |
| Authority | INPUT (not AUTHORITATIVE until the owner approves it) |
| Related Tasks / Milestones | KOS-NEXUS-006; NX-M1 |
| Related Documents | [A0 integration draft](A0_INTEGRATION_DRAFT.md); [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md); [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) |

## Purpose

This document is the top-level system architecture of the Nexus SoC, owned by this repository. It consolidates the A0 integration draft, which is an input and a reconstruction of a working discussion, into one document that traces to the requirements register and the decision records. It is written for the owner, reviewers and the engineers who will write the interconnect, memory and address-map documents (KOS-NEXUS-007 and 008). It does not replace those documents and does not contain RTL, numeric performance results or implementation evidence.

## 1. Scope and status

This document covers the document rules, the system context, the domain map and a section for every domain in section 4. The interface register (section 13) and the open-issues register (section 14) are the artefacts for AC-012; whether they meet it is for the owner's review. The sections name the A0 draft section for each topic; where this document is silent on a detail, the A0 draft is the only description of it and that detail is PROPOSED or OPEN.

Detailed interconnect, memory and address-map content belongs to KOS-NEXUS-007 and 008. Subsystem microarchitecture and RTL are out of scope.

## 2. Rules for this document

1. Every architecture statement carries one label: `SELECTED` (recorded owner decision, with a decision record), `PROPOSED` (a recommendation, including every one from an AI tool) or `OPEN` (needs engineering definition). A statement without a label is not part of the architecture.
2. A SELECTED statement names its decision record (NX-DEC-NNN). A PROPOSED or OPEN statement names its requirement (NX-REQ-NNN) or gap (NX-ARCH-GAP-NNN).
3. Where this document and the requirements register or a decision record differ, the register or record wins and this document is corrected.
4. Numeric parameters stay PROPOSED unless the requirement is SELECTED. Owner-selected values are only those in the register: 6 MiB frame pool, 720p60 at 1280x720 over parallel DPI, three composition layers, 64 KiB security ROM and SRAM, the four application AXI fabrics, the two AXI-to-APB interconnects, the C910-to-APB route and behaviour, the peripheral counts and the DMA controller with 32 channels.
5. Evidence stays separate. Renode results are not evidence of C910 timing, cache behaviour or cycle accuracy; a substitute CPU on FPGA is labelled a substitute; lint, Yosys, FPGA synthesis and OpenLane results are `software` evidence, simulation results are `simulation` evidence and `physical` is reserved for programmed-board results.
6. A PROPOSED item is changed by a change request: a pull request that edits it with a changelog entry. A SELECTED item also needs a new decision record.

## 3. System context

Nexus is the application-processing and AI SoC of the Kritva robotics platform and interfaces with Kritva Edge over EtherCAT (PROPOSED, NX-REQ-040, NX-REQ-041; the SELECTED part is two independent Ethernet MACs, NX-DEC-007). Nexus is outside the Kritva Program V2 plan and is planned for the V3 plan.

External interfaces named in the register: DDR4 (SELECTED, NX-DEC-001), Octal SPI PSRAM (SELECTED, NX-DEC-002), OSPI NOR boot medium (SELECTED, NX-DEC-003), camera inputs (PROPOSED, NX-REQ-042), a parallel DPI display (SELECTED, NX-DEC-005), two Ethernet MACs (SELECTED, NX-DEC-007) and board-level peripherals (counts SELECTED, NX-DEC-020).

## 4. Domain map

| Domain | Contents | Label | Records | A0 draft |
|---|---|---|---|---|
| Application CPU | Xuantie C910 direction; RV64 quad-core cluster; C910 DVFS | PROPOSED CPU (CPU IP and configuration); SELECTED DVFS | NX-REQ-001, 055, 056; NX-DEC-018 (PROPOSED); NX-DEC-016 | Section 2 |
| Application interconnect | Four AXI fabrics, Memory Access Crossbar, two AXI-to-APB interconnects, application address map | SELECTED counts, C910-to-APB route and behaviour; PROPOSED roles, widths and map | NX-DEC-014, NX-DEC-015, NX-DEC-021, NX-DEC-022; NX-REQ-049 to 053, 067 to 075 | Section 9 |
| Memory | DDR4, Octal SPI PSRAM, OSPI NOR boot | SELECTED media; PROPOSED controller targets, DDR4 width and ingress | NX-DEC-001 to 003; NX-REQ-030, 064, 065, 076 to 078 | Section 4 |
| AI and vision | Camera inputs, 6 MiB frame pool, ISP, NPU, NPU DVFS | SELECTED frame-pool capacity and NPU DVFS; PROPOSED the rest | NX-DEC-004, NX-DEC-017; NX-REQ-042 to 047 | Section 3 |
| Multimedia and connectivity | 720p60 parallel DPI display, three composition layers, two Ethernet MACs, EtherCAT MainDevice, peripherals | SELECTED display mode, layers, MAC count, peripheral counts; PROPOSED EtherCAT, RGMII, compositor | NX-DEC-005 to 007, NX-DEC-020; NX-REQ-040, 041, 048 | Sections 5, 6 and 8 |
| DMA | General-purpose DMA controller with 32 channels on AXI-3 | SELECTED controller and channel count; PROPOSED placement and features | NX-DEC-025; NX-REQ-092 to 100 | Not in the A0 draft |
| Security | Isolated 32-bit RISC-V core, 64 KiB ROM and SRAM, eFuse, AES, SHA-256, separate secure AXI | SELECTED, including the secure map and the address-space separation; PROPOSED accelerator, boot sequence | NX-DEC-008 to 013, NX-DEC-019, NX-DEC-030; NX-REQ-033 to 039, 054; NX-REQ-028 | Section 7 |
| Always-on, clock, reset, power, interrupt | Always-on domain, PLLs, power and reset domains, interrupts, CDC and RDC, DVFS | SELECTED DVFS; PROPOSED PLL, domains and targets; OPEN always-on definition and interrupt architecture | NX-DEC-016, NX-DEC-017; NX-REQ-031, 057 to 063, 066 | Section 10 |

## 5. Application CPU

| Item | Statement | Label | Records |
|---|---|---|---|
| CPU IP | The application CPU subsystem uses the Xuantie C910, RV64. The exact RTL release and configuration are not confirmed. | PROPOSED | NX-REQ-001, NX-DEC-018 |
| Cluster | One cluster of four cores with 64 KB L1 instruction and data caches per core and a shared 1 MB L2; 1.0 to 1.2 GHz is a target, not a timing result. | PROPOSED | NX-REQ-055 |
| CPU interface | AXI4, 128-bit data, 8 outstanding reads and 8 outstanding writes; the 40-bit application address width is SELECTED (NX-DEC-026) and its confirmation against the C910 configuration is OPEN. | PROPOSED | NX-REQ-056 |
| Address width | The application address width is 40 bits. | SELECTED | NX-REQ-101, NX-DEC-026 |
| Address width confirmation | The owner confirmed the 40-bit width for the C910 (NX-DEC-030) and for every other application master (NX-DEC-031); the RTL evidence source is not recorded (NX-ARCH-OI-001), and the procedure is in section 4 of MEMORY_ARCHITECTURE. | SELECTED | NX-REQ-029, NX-DEC-031 |
| DVFS | The clock and power subsystem supports DVFS for the C910 subsystem. | SELECTED | NX-REQ-017, NX-DEC-016 |
| Interrupts and timers | 128 external sources, 16 inter-processor interrupts, a shared 64-bit timebase, a 32.768 kHz RTC, per-hart timer compare and TAP debug; PLIC/CLINT versus AIA is undecided. | PROPOSED, with the controller choice OPEN | NX-REQ-057 |
| Power and test support | Clock gating, power gating, hardware performance counters, scan test and MBIST for applicable memories are expected; the implementation is not frozen. | PROPOSED | A0 draft 2.4 |

The C910 is a direction, not a selected IP decision. A substitute CPU used for FPGA validation is labelled a substitute and is never reported as C910 validation.

## 6. Application interconnect

The architecture has four application AXI fabrics (SELECTED, NX-REQ-015, NX-DEC-014) and two AXI-to-APB interconnects (SELECTED, NX-REQ-016, NX-DEC-015). The partition below is PROPOSED (NX-REQ-050, NX-REQ-051); widths and the 400 to 600 MHz range are proposals, and the theoretical bandwidth figures in the A0 draft are interface arithmetic, not sustained throughput.

| Fabric | Role | Proposed width | Proposed masters |
|---|---|---|---|
| AXI-0 | Main system, CPU and memory | 128-bit | C910 |
| AXI-1 | AI and vision | 256-bit | ISP, NPU, camera DMA |
| AXI-2 | Multimedia and high-speed IO | 128-bit | Display, Ethernet and storage DMA |
| AXI-3 | General peripherals, control and DMA | 64-bit | DMA controller (peripheral and I2S DMA) |

A separate Memory Access Crossbar with four fabric ingress ports is PROPOSED (NX-REQ-049) to avoid serialising memory access through AXI-0; the proposal is one 256-bit AXI4 port from the crossbar to the DDR4 controller, derived for a x32 DDR4-3200 interface (NX-REQ-030, NX-REQ-076 to NX-REQ-078, NX-ARCH-GAP-004), and the sizing assumptions are changed only by change request. The two AXI-to-APB interconnects are proposed at 32-bit APB data width and 200 to 250 MHz (NX-REQ-052).

The route from the C910 to the APB peripherals is SELECTED (NX-REQ-067, NX-DEC-021): the C910 reaches APB-0 and APB-1 through AXI-0, an AXI fabric bridge from AXI-0 to AXI-3, AXI-3 decode and the AXI-to-APB interconnects. The behaviour of the path (error response, timeout, masters, bridge structure, access control, ordering, bursts and reset) is also SELECTED (NX-REQ-068 to NX-REQ-075, NX-DEC-022) and is held in the interconnect specification; NX-ARCH-GAP-001 is closed. The timeout value, recovery and the bridge buffering limits are OPEN (NX-ARCH-OI-033, NX-ARCH-OI-034). The application address map is PROPOSED (NX-REQ-053) and is held by KOS-NEXUS-008, not copied here. Its apertures are not memory capacities: the 16 MiB frame-pool aperture is not the owner-selected 6 MiB capacity, and the DDR4 window does not select a DDR4 device size. Cacheability, coherency, security attributes, permissions and IOMMU needs are OPEN.

### DMA controller

A general-purpose DMA controller with 32 independent channels is SELECTED (NX-REQ-092, NX-DEC-025). Its placement and features are PROPOSED (NX-REQ-093 to NX-REQ-100); the owner's feature list is adapted to AXI terms, as listed in NX-DEC-025.

| Item | Statement | Label | Records |
|---|---|---|---|
| Controller | A general-purpose DMA controller with 32 independent channels offloads bulk data movement from the C910. | SELECTED | NX-REQ-092, NX-DEC-025 |
| Placement | The controller is the peripheral and I2S DMA master on AXI-3 and its registers are reached through the AXI-to-APB interconnects; the camera, display, Ethernet and storage DMA masters stay on their own fabrics. | PROPOSED | NX-REQ-093 |
| Transfer types | Memory-to-memory, memory-to-peripheral, peripheral-to-memory and peripheral-to-peripheral. | PROPOSED | NX-REQ-094 |
| Transfer modes | Burst transfers with a configurable length and a limit on consecutive bursts, no bus locking; one-beat-per-arbitration transfers; background transfers at the lowest priority level. | PROPOSED | NX-REQ-095 |
| Addressing and width | Increment, decrement and fixed addressing; 8, 16, 32 and 64-bit data widths within the 64-bit AXI-3. | PROPOSED | NX-REQ-096 |
| Scatter-gather | Chains of descriptors held in memory. | PROPOSED | NX-REQ-097 |
| Arbitration | Configurable per-channel priority, round-robin among equal priorities, the "NPU and other DMA" QoS class on its AXI traffic. | PROPOSED | NX-REQ-098 |
| Completion and errors | An interrupt on completion or error only; a DECERR or SLVERR response stops the channel and is reported per channel. | PROPOSED | NX-REQ-099 |
| Low-power operation | Configured transfers can continue while the C910 cluster is in a low-power state; the DMA power domain and wake-up conditions are defined with the power-domain and always-on definitions. | PROPOSED | NX-REQ-100 |

Memory-to-memory copies cross AXI-3 (64-bit) and the Memory Access Crossbar; their throughput is not quantified, and the DDR4 sizing of section 4 of the interconnect specification has no DMA line. Peripheral request mapping, descriptor format, coherency and the DMA power domain are NX-ARCH-OI-035.

## 7. External memory

| Memory | Role | Label | Records |
|---|---|---|---|
| DDR4 | Primary system memory for Linux and applications, NPU models and large activations, display framebuffers and DMA buffers | SELECTED role | NX-REQ-002, NX-DEC-001 |
| Octal SPI PSRAM | Secondary memory | SELECTED role | NX-REQ-003, NX-DEC-002 |
| OSPI NOR | Primary boot medium: boot firmware, bootloader and recovery, configuration and authenticated updates | SELECTED role | NX-REQ-004, NX-DEC-003 |

The NOR and the PSRAM are separate devices with separate controllers. The operating targets are PROPOSED: DDR4-3200 (NX-REQ-064) and a PSRAM controller at 200 to 400 MHz (NX-REQ-065). DDR4 is proposed as one x32 channel with capacity chosen at board level (NX-REQ-076); the PSRAM protocol, mode and capacity, and the NOR device are not selected. The 200 MHz OSPI x8 figure in the A0 draft is an example calculation, not a requirement. The secure boot path must reach the NOR before the application fabrics and the C910 are active (PROPOSED, NX-REQ-038). The DDR4 ingress is one 256-bit port and memory arbitration uses four QoS classes with bandwidth budgets, all PROPOSED (NX-REQ-030, NX-REQ-077, NX-REQ-078).

## 8. AI and vision

| Item | Statement | Label | Records |
|---|---|---|---|
| Camera inputs | Four simultaneous cameras at up to 640x640 and 10 FPS each, Bayer RAW10 and RAW12 input; the electrical interface and capture details are not defined. | PROPOSED | NX-REQ-042 |
| Frame pool | The camera frame pool provides 6 MiB of usable capacity. The bank count, width, port organisation and ECC implementation are not defined. | SELECTED capacity | NX-REQ-005, NX-DEC-004 |
| Frame drop | When no frame buffer is available, the complete frame is dropped; a partially captured frame is never exposed as valid. | PROPOSED | NX-REQ-043 |
| Frame release | A source frame is released after source consumption, independently of inference completion; the release-latency bound and buffer-borrowing policy are OPEN. | PROPOSED | NX-REQ-044 |
| ISP | Bayer input through unpacking, black-level, defect-pixel, lens-shading, demosaic, white-balance, colour-correction and gamma stages, RGB output by default; stage ordering, halo requirements and tile size are not specified. | PROPOSED | NX-REQ-045 |
| NPU | Four homogeneous clusters, INT8 inputs and weights, INT32 accumulators, a peak target of 8 TOPS INT8. The target is not a measured result; the NPU microarchitecture and model and tensor-format requirements are not defined. | PROPOSED | NX-REQ-046 |
| Local memories | The path uses a camera frame pool, an ISP local SRAM and an NPU local SRAM, and its normal path does not need DDR intermediate storage. ISP and NPU SRAM sizes and organisation are not selected. | PROPOSED | NX-REQ-047 |
| NPU DVFS | The clock and power subsystem supports DVFS for the NPU. | SELECTED | NX-REQ-018, NX-DEC-017 |

On the application interconnect the ISP, NPU and camera DMA are proposed on AXI-1 (NX-REQ-051). Frame-pool, ISP and NPU local-memory transfers are not forced through DDR4, and DDR4 stays available for models, large activations and optional intermediates (the use of DDR for optional intermediates and recording is OPEN). Workload and power figures in the A0 draft are PROPOSED derived calculations, and no performance, power or area result exists for the AI and vision path. The SoC power target is PROPOSED (NX-REQ-066) and is held in the clock, power and reset section.

## 9. Multimedia and connectivity

| Item | Statement | Label | Records |
|---|---|---|---|
| Display mode | 720p60: 1280x720 at 60 Hz over a parallel DPI interface. DPI electrical and pin configuration and the pixel format are not defined. | SELECTED | NX-REQ-006, NX-DEC-005 |
| Composition | Three composition layers. | SELECTED | NX-REQ-007, NX-DEC-006 |
| Compositor | Three independent framebuffers in DDR4 with alpha composition, z-order control, atomic update at Vsync and underflow detection; underflow recovery is OPEN. | PROPOSED | NX-REQ-048 |
| Ethernet MACs | Two independent Ethernet MACs. | SELECTED | NX-REQ-008, NX-DEC-007 |
| Ethernet interface | 10/100/1000 Mbps over RGMII with external PHYs; PHY selection and RGMII delay configuration are OPEN. | PROPOSED | NX-REQ-040 |
| EtherCAT | Both MACs support EtherCAT MainDevice operation using raw Ethernet frames, and receive filtering does not reject EtherType 0x88A4. Hardware timestamping, redundancy and the stack are OPEN. | PROPOSED | NX-REQ-041 |
| Peripherals | 16 PWM channels, 32 GPIO, four general-purpose timers, four UARTs, four I2C masters, one SPI master, one SPI slave and two I2S masters. Only the counts are selected. | SELECTED counts | NX-REQ-019 to NX-REQ-026, NX-DEC-020 |

The display, Ethernet and storage DMA masters are proposed on AXI-2, and the peripheral and I2S DMA masters on AXI-3 (NX-REQ-051). The peripheral features (PWM resolution, GPIO interrupt behaviour, timer width, FIFO depths, speed modes, I2S rates and clocking), the pinmux and the package pin assignment are not selected; dedicated pins were assumed only for the initial counting. The pixel clock and timing totals, and the display and Ethernet traffic figures in the A0 draft, are PROPOSED derived calculations and not requirements. DRM/KMS integration, display DMA coherency and Ethernet DMA buffer coherency are OPEN.

## 10. Security

| Item | Statement | Label | Records |
|---|---|---|---|
| Security core | A dedicated, isolated 32-bit RISC-V security core. | SELECTED | NX-REQ-009, NX-DEC-008 |
| Local memory | 64 KiB of ROM and 64 KiB of SRAM for the security core. | SELECTED | NX-REQ-010, NX-REQ-011, NX-DEC-009, NX-DEC-010 |
| eFuse | A dedicated security eFuse resource; programming and access control are not defined. | SELECTED | NX-REQ-012, NX-DEC-011 |
| Cryptography | AES-128 and AES-256, and SHA-256. | SELECTED | NX-REQ-013, NX-REQ-014, NX-DEC-012, NX-DEC-013 |
| Asymmetric accelerator | An asymmetric cryptography accelerator; its algorithms, signature and hash formats are not defined. | PROPOSED | NX-REQ-035 |
| Secure interconnect | A dedicated, separate secure AXI interconnect. Its 32-bit data and address widths and 2 outstanding reads and writes are proposals. | SELECTED concept; PROPOSED parameters | NX-REQ-032, NX-DEC-019; NX-REQ-033 |
| Application exclusion | The application AXI interconnect gives no access to the security ROM, security SRAM, eFuse, key management or security interrupt controller. | PROPOSED | NX-REQ-034 |
| Secure boot | The security core starts first, authenticates the boot image from OSPI NOR using the immutable ROM and authorises C910 reset release before the application subsystems are initialised; an authorised NOR access path is usable before the application fabrics and the C910 are active. | PROPOSED | NX-REQ-036, NX-REQ-038 |
| Reset control | C910 reset release is hardware-controlled by the security domain, and a C910 warm reset does not reset the security domain. | PROPOSED | NX-REQ-037 |
| Secret exposure | Raw secrets are not exposed through ordinary application interfaces. | PROPOSED | NX-REQ-039 |
| Secure address map | A separate secure address space with the map held in architecture/maps/secure_map.yaml (derived from A0 draft section 7.4). | SELECTED | NX-REQ-054, NX-DEC-030 |
| Address-space separation | The secure and application address spaces are separate address spaces on separate interconnects, with independent decode and access control. This is the architectural statement; the secure map is NX-REQ-054, the separation is NX-REQ-028 and the application exclusion is NX-REQ-034. | SELECTED | NX-REQ-054, NX-REQ-028, NX-DEC-030 |
| Controlled crossings | The boundary between the security and application domains has exactly two controlled crossings: a security-core access path into one application window and one application-to-security mailbox. | SELECTED | NX-REQ-105, NX-DEC-027 |
| Boot window scope and mailbox rule | The security core reaches System SRAM only and never DDR4; the mailbox window keeps the C910-to-APB rule that secure resources are unreachable and is the only security-related window on that path. | SELECTED | NX-REQ-109, NX-REQ-110, NX-DEC-029 |
| Boot window and mailbox | The window is the System SRAM region reached through a secure-to-application bridge; the mailbox has a window in each address space. Both are default-deny, every other security resource is unreachable, overlapping ranges are not conflicts, and the attachment and mailbox details are defined in NX-REQ-113 to NX-REQ-115. | SELECTED | NX-REQ-106, NX-REQ-107, NX-REQ-108, NX-DEC-030 |
| Crossing details | The bridge is one AXI master port on AXI-3 that forwards only the boot-window alias and answers every other address itself; the mailbox is one register block with request and response buffers of 256 bytes, one outstanding request, a security-side allow-list check and one interrupt in each direction. | SELECTED | NX-REQ-113, NX-REQ-114, NX-REQ-115, NX-DEC-033 |

The security domain is described here as an architecture direction. Root-key provisioning, anti-rollback policy, recovery behaviour, debug lifecycle and authorisation, eFuse programming and access control, secure boot failure handling and the security interrupt and fault-response details are OPEN. No security claim is made from this document: it contains no threat model, no verification result and no hardware validation.

## 11. Always-on, clock, reset, power and interrupts

| Item | Statement | Label | Records |
|---|---|---|---|
| DVFS | DVFS is supported for the C910 subsystem and for the NPU. Operating points and voltage sequencing are OPEN. | SELECTED | NX-REQ-017, NX-REQ-018, NX-DEC-016, NX-DEC-017 |
| Always-on domain | The responsibilities of the always-on domain and its interfaces to reset, wake-up, security and power control are not defined. | OPEN | NX-REQ-031 |
| Interrupt controllers | An application controller with 128 external sources, a security controller with 32 sources and an always-on controller with 8 to 16 wake sources; the PLIC versus AIA choice is undecided. | OPEN | NX-REQ-057 |
| Application interrupt controller baseline | A RISC-V PLIC with 128 external sources and a CLINT in APB-1 windows; the AIA is not used in this baseline; the security and always-on controllers and the routing among the three stay open. | SELECTED | NX-REQ-116, NX-DEC-033, NX-ARCH-OI-032 |
| PLLs | Four integer PLLs and two fractional PLLs; allocation and feasibility are not verified. | PROPOSED | NX-REQ-058 |
| Frequency targets | C910 1.0 to 1.2 GHz, NPU 800 MHz, ISP 600 MHz, security core 200 to 400 MHz, AXI fabrics 400 to 600 MHz, APB 200 to 250 MHz, PSRAM controller 200 to 400 MHz and DPI pixel clock 74.25 MHz. These are targets, not timing results. | PROPOSED | NX-REQ-059 |
| Power domains | Seven logical domains: AON, SEC, CPU, MEM, AI, MEDIA and IO; the implementation is not defined. | PROPOSED | NX-REQ-060 |
| Reset domains | Eight domains: AON, SEC, CPU, MEM, AI, ISP, DISP and IO, with asynchronous assertion and synchronous deassertion. Reset sources and sequencing are OPEN. | PROPOSED | NX-REQ-061 |
| CDC and RDC | Every clock-domain and reset-domain crossing uses a suitable synchroniser, asynchronous FIFO or reset synchroniser and is covered by CDC and RDC checks with documented waivers. | PROPOSED | NX-REQ-062 |
| Critical faults | Critical thermal, power and tamper faults have a hardware response independent of application CPU execution; the response is not defined. | PROPOSED | NX-REQ-063 |
| SoC power | A total power target of 10 to 20 W. This is a target, not an estimate or a measurement. | PROPOSED | NX-REQ-066 |

The clock source and clock-tree architecture, jitter requirements, PMIC and rail selection, the clock-domain and reset-domain matrices and the CDC and RDC waiver policy are OPEN.

## 12. RTL partitioning, simulator and prototype architecture

All statements in this section are PROPOSED. No requirement or decision record covers them: tool choices and their repository implementation belong to KOS-NEXUS-002, and none of the tools is installed, qualified or selected for every block by this document. Source: A0 draft section 11.

| Item | Statement | Label |
|---|---|---|
| RTL partitioning | RTL is partitioned along the domains of section 4: application CPU, application interconnect, memory, AI and vision, multimedia and connectivity, security, and always-on, clock, reset and power. Each block has a module specification giving its ID, subsystem, purpose, requirements, ports, clock and reset domains, CDC and reset behaviour, register and data interfaces, parameters, technology dependencies, verification requirements and synthesis and physical-design concerns. | PROPOSED |
| Module size | A module of 300 to 800 lines is the target, more than 1000 lines is reviewed and more than 1500 lines is considered for decomposition. These are review guidelines, not limits. | PROPOSED |
| Technology wrappers | The same functional RTL is intended for simulation, FPGA and ASIC. Memory, clock, reset, scan and MBIST are mapped through wrappers in `technology/generic`, `technology/fpga` and `technology/asic`: generic memory models, FPGA block RAM mapping and ASIC SRAM macro mapping. The wrapper interfaces are not defined. | PROPOSED |
| Kritva Nexus Simulator | The platform simulation is Renode, a virtual-platform simulator that is not a cycle-accurate C910 model. Verilator co-simulation can connect selected RTL blocks to it. A Renode CPU model is not C910 validation until ISA, privilege, MMU and other compatibility are confirmed, and it is never evidence of C910 timing, cache behaviour or performance. Results state whether they come from Renode or from Verilator co-simulation. | PROPOSED |
| FPGA prototype | FPGA prototyping is planned. The board is not selected; C910 RTL and DDR PHY suitability for the chosen FPGA are unverified. A substitute RISC-V CPU on FPGA can validate platform interfaces and is labelled a substitute, never C910 validation. FPGA synthesis and place-and-route results are distinct from tests on a programmed board. | PROPOSED (board selection OPEN) |
| Block-level physical design | OpenLane 2 and OpenROAD are intended for block-level work where the technology collateral, memory macros, constraints and tool support exist. The complete SoC is not established as implementable through OpenLane, and open-source flow results are implementation evidence, not production signoff. | PROPOSED |
| Evidence classification | Lint, Yosys, FPGA synthesis and place-and-route and OpenLane runs (including DRC, LVS and STA) are `software` evidence; Icarus, Verilator, Renode and co-simulation results are `simulation` evidence; `physical` is reserved for programmed-board results. An evidence record states the target (RTL, FPGA or ASIC), the tool and version, the configuration revision, the source commit and the run ID. | PROPOSED (the repository evidence rule in AGENTS.md section 2; the A0 draft left the OpenLane classification to owner confirmation) |

The open items for this section (FPGA board, tool versions, wrapper interfaces, technology collateral, OpenLane scope, co-simulation boundary and evidence metadata policy) are in the open-issues register.

## 13. Interface register

This register lists the interfaces between subsystems that the architecture depends on (AC-012). It records that an interface exists and its label; it does not define signals, protocols or register maps. Those are written in KOS-NEXUS-007 and 008 and the later IP and subsystem specifications. An interface is SELECTED only where the owner's decision covers it.

| ID | Interface | Between | Label | Records | Defined by | Owner | Open issue |
|---|---|---|---|---|---|---|---|
| NX-INT-001 | C910 AXI master to AXI-0 | C910, AXI-0 | PROPOSED | NX-REQ-056; NX-REQ-051 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-001 |
| NX-INT-002 | C910 access to APB peripherals through AXI-0, an AXI fabric bridge to AXI-3 and the AXI-to-APB interconnects | C910, AXI-0, AXI-3, AXI-to-APB, APB-0 and APB-1 | SELECTED | NX-REQ-067 to NX-REQ-075; NX-DEC-021; NX-DEC-022; NX-ARCH-GAP-001 (closed) | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-033, NX-ARCH-OI-034 |
| NX-INT-003 | Fabric ingress to the Memory Access Crossbar and the DDR4 controller | AXI-0 to AXI-3, Memory Access Crossbar, DDR4 controller | PROPOSED | NX-REQ-049; NX-REQ-030; NX-REQ-078; NX-ARCH-GAP-004 | KOS-NEXUS-007 | Dinesh | NX-ARCH-GAP-004, NX-ARCH-OI-005 |
| NX-INT-004 | AI and vision masters on AXI-1 | ISP, NPU, camera DMA, AXI-1 | PROPOSED | NX-REQ-051 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-004 |
| NX-INT-005 | Camera, frame pool, ISP local SRAM and NPU local SRAM paths that avoid DDR4 | Camera, ISP, NPU, local memories | PROPOSED | NX-REQ-047 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-007 |
| NX-INT-006 | ISP to NPU data interface | ISP, NPU | OPEN | NX-REQ-045; NX-REQ-046 | A later IP and subsystem task | Dinesh | NX-ARCH-OI-009 |
| NX-INT-007 | Frame ownership and release between capture, ISP and consumers | Camera path, ISP, consumers | PROPOSED | NX-REQ-043; NX-REQ-044 | A later IP and subsystem task | Dinesh | NX-ARCH-OI-011 |
| NX-INT-008 | Display DMA from DDR4 framebuffers on AXI-2 and the parallel DPI output | Display compositor, AXI-2, DDR4, DPI pins | PROPOSED (display mode SELECTED) | NX-REQ-006; NX-REQ-048; NX-REQ-051 | A later IP and subsystem task | Dinesh | NX-ARCH-OI-013, NX-ARCH-OI-014 |
| NX-INT-009 | Ethernet MAC DMA on AXI-2 and the RGMII interface to external PHYs | Ethernet MACs, AXI-2, external PHYs | PROPOSED (MAC count SELECTED) | NX-REQ-008; NX-REQ-040; NX-REQ-041 | A later IP and subsystem task | Dinesh | NX-ARCH-OI-015, NX-ARCH-OI-016 |
| NX-INT-010 | Peripheral and I2S DMA on AXI-3 and the peripheral register access through APB | Peripherals, AXI-3, APB-0 and APB-1 | PROPOSED (counts SELECTED) | NX-REQ-019 to NX-REQ-026; NX-REQ-051 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-022 |
| NX-INT-011 | Secure AXI interconnect between the security core and its local resources | Security core, security ROM, SRAM, eFuse, crypto, secure interrupt controller | SELECTED concept; PROPOSED parameters | NX-REQ-032; NX-REQ-033 | KOS-NEXUS-007 and 008 | Dinesh | NX-ARCH-OI-021 |
| NX-INT-012 | Isolation boundary between the security domain and the application domain | Secure AXI, application AXI | SELECTED | NX-REQ-028; NX-REQ-034; NX-REQ-108; NX-ARCH-GAP-002 | KOS-NEXUS-008 | Dinesh | NX-ARCH-GAP-002 |
| NX-INT-013 | Security core access to OSPI NOR before the application fabrics are active | Security core, OSPI NOR controller | PROPOSED | NX-REQ-036; NX-REQ-038 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-006, NX-ARCH-OI-019 |
| NX-INT-014 | Hardware control of C910 reset release by the security domain | Security domain, C910 reset | PROPOSED | NX-REQ-037 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-019 |
| NX-INT-015 | Always-on domain to reset, wake-up, security and power control | Always-on domain, reset, security, power control | OPEN | NX-REQ-031 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-031 |
| NX-INT-016 | Interrupt routing among the application, security and always-on interrupt controllers | Interrupt controllers, C910, security core, always-on domain | OPEN; SELECTED controller and mailbox lines | NX-REQ-057; NX-REQ-115; NX-REQ-116 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-032, NX-ARCH-OI-002 |
| NX-INT-017 | Clock distribution from the PLLs to the clock domains and the DVFS interfaces | PLLs, clock and power control, C910 and NPU | PROPOSED (DVFS SELECTED) | NX-REQ-017; NX-REQ-018; NX-REQ-058; NX-REQ-059 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-023, NX-ARCH-OI-024 |
| NX-INT-018 | Power-domain and reset-domain boundaries and their crossings | Power and reset domains | PROPOSED | NX-REQ-060; NX-REQ-061; NX-REQ-062 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-025 |
| NX-INT-019 | Critical fault signals to a hardware response | Thermal, power and tamper sources, always-on domain | PROPOSED | NX-REQ-063 | A later IP and subsystem task | Dinesh | NX-ARCH-OI-026 |
| NX-INT-020 | DDR4 controller and PHY to the DDR4 device | DDR4 controller, DDR4 PHY, DDR4 device | SELECTED role; PROPOSED target and width | NX-REQ-002; NX-REQ-064; NX-REQ-076 | A later IP and subsystem task | Dinesh | NX-ARCH-GAP-004, NX-ARCH-OI-005 |
| NX-INT-021 | PSRAM controller to the Octal SPI PSRAM device | PSRAM controller, PSRAM device | SELECTED role; PROPOSED target | NX-REQ-003; NX-REQ-065 | A later IP and subsystem task | Dinesh | NX-ARCH-OI-006 |
| NX-INT-022 | OSPI NOR controller to the NOR device | NOR controller, NOR device | SELECTED role; interface details OPEN | NX-REQ-004 | A later IP and subsystem task | Dinesh | NX-ARCH-OI-006 |
| NX-INT-023 | DMA controller master on AXI-3 and its register access through APB | DMA controller, AXI-3, APB-0 and APB-1 | PROPOSED | NX-REQ-093; NX-REQ-094 | KOS-NEXUS-007 | Dinesh | NX-ARCH-OI-035 |
| NX-INT-024 | Security core access path into the application boot window through a secure-to-application bridge | Security core, secure AXI, application System SRAM | SELECTED | NX-REQ-105; NX-REQ-106; NX-REQ-109; NX-REQ-113 | KOS-NEXUS-008 | Dinesh | NX-ARCH-OI-037 |
| NX-INT-025 | Mailbox between the application domain and the security domain | Mailbox, secure AXI, APB-0 and APB-1 | SELECTED | NX-REQ-105; NX-REQ-107; NX-REQ-110; NX-REQ-114; NX-REQ-115 | KOS-NEXUS-008 | Dinesh | NX-ARCH-OI-037 |

Assumptions that the interfaces and sections above rest on:

| ID | Assumption | Records | Open issue |
|---|---|---|---|
| NX-ASM-001 | The application address width is 40 bits (SELECTED, NX-DEC-026); the owner confirmed the C910 (NX-DEC-030) and every other application master (NX-DEC-031) at 40 bits; the RTL evidence is not recorded. | NX-REQ-101; NX-REQ-029; NX-ARCH-GAP-003 | NX-ARCH-GAP-003 |
| NX-ASM-002 | The C910 RTL release and configuration meet the cluster and interface parameters proposed in section 5; neither is confirmed. | NX-REQ-055; NX-REQ-056 | NX-ARCH-OI-001 |
| NX-ASM-003 | The DDR4 interface is one x32 channel at DDR4-3200 with a sustained fraction of 70%; the DDR4 address window is not a device size. | NX-REQ-064; NX-REQ-076; NX-REQ-077 | NX-ARCH-OI-005 |
| NX-ASM-004 | Ethernet PHYs are external to the SoC and the PHY is selected at board level. | NX-REQ-040 | NX-ARCH-OI-015 |
| NX-ASM-005 | Dedicated pins were assumed only to count the peripherals; pinmux and package pin assignment are not decided. | NX-REQ-019 to NX-REQ-026 | NX-ARCH-OI-022 |
| NX-ASM-006 | The frequency, bandwidth and power figures are targets or interface arithmetic, with no timing, bandwidth or power result behind them. | NX-REQ-059; NX-REQ-066 | NX-ARCH-OI-012, NX-ARCH-OI-023 |

## 14. Open-issues register

Every unresolved item is listed here with an owner and a status. The owner of every item is Dinesh (interim, not independent). The status is OPEN until the item is resolved. PROPOSED means the item is resolved by a proposal that is not an owner decision; it is changed only by change request. CLOSED means the owner decided it. This document does not turn a PROPOSED item into a decision. The four gaps keep their canonical identifiers and are not renumbered; a closed gap stays in the table with status CLOSED; the other items take NX-ARCH-OI identifiers, which are stable and never reused.

| ID | Issue | Domain | Requirement | Owner | Status |
|---|---|---|---|---|---|---|---|
| NX-ARCH-GAP-001 | C910 to APB access path: closed by NX-DEC-021 (route) and NX-DEC-022 (behaviour); residual items NX-ARCH-OI-033 and NX-ARCH-OI-034 proposed | AXI fabrics | NX-REQ-067 to NX-REQ-075 (NX-REQ-027 superseded) | Dinesh | CLOSED |
| NX-ARCH-GAP-002 | Secure and application address spaces: separate spaces on separate interconnects, isolation boundary and permitted access paths: closed by NX-DEC-027 (two controlled crossings) and NX-DEC-030 (boundary rules, section 5 of MEMORY_ARCHITECTURE); the attachment stays OPEN as NX-ARCH-OI-037 | Security | NX-REQ-028; NX-REQ-105; NX-REQ-106; NX-REQ-107; NX-REQ-108 | Dinesh | CLOSED |
| NX-ARCH-GAP-003 | C910 application address width: the 40-bit width (SELECTED, NX-DEC-026) is confirmed by the owner for the C910 (NX-DEC-030) and for every other application master (NX-DEC-031); closed, with the RTL evidence source not recorded (NX-ARCH-OI-001) | AXI fabrics | NX-REQ-029 | Dinesh | CLOSED |
| NX-ARCH-GAP-004 | DDR4 controller ingress: resolved by proposal, one 256-bit port for x32 DDR4-3200 | Memory | NX-REQ-030; NX-REQ-076 to NX-REQ-078 | Dinesh | PROPOSED |
| NX-ARCH-OI-001 | Exact C910 RTL release and configuration; cache sizes and cluster configuration; AXI interface parameters against the C910 RTL | CPU and interconnect | None | Dinesh | OPEN |
| NX-ARCH-OI-002 | PLIC/CLINT versus AIA integration | CPU and interconnect | None | Dinesh | OPEN |
| NX-ARCH-OI-003 | Application address-map attributes (cacheability, coherency, security, read/write/execute permissions) and IOMMU requirements: closed by NX-DEC-030 (section 6 of MEMORY_ARCHITECTURE) | CPU and interconnect | NX-REQ-102; NX-REQ-103; NX-REQ-104 | Dinesh | CLOSED |
| NX-ARCH-OI-004 | AXI routing, decode, QoS, outstanding transactions and error behaviour: proposed in the interconnect specification section 6 | CPU and interconnect | NX-REQ-078; NX-REQ-079 | Dinesh | PROPOSED |
| NX-ARCH-OI-005 | DDR4 width and capacity; memory arbitration and bandwidth allocation: proposed in the interconnect specification section 4 | Memory | NX-REQ-076; NX-REQ-077; NX-REQ-078 | Dinesh | PROPOSED |
| NX-ARCH-OI-006 | PSRAM protocol, mode, capacity and bandwidth; OSPI NOR device and controller details | Memory | None | Dinesh | OPEN |
| NX-ARCH-OI-007 | Frame-pool bank count, width, port organisation and ECC implementation; ISP and NPU SRAM physical organisation; memory macro selection and MBIST | Memory | None | Dinesh | OPEN |
| NX-ARCH-OI-008 | Camera electrical interface and capture details | AI and vision | None | Dinesh | OPEN |
| NX-ARCH-OI-009 | ISP pipeline stage ordering, Bayer halo requirements and tile size; ISP-to-NPU interface details | AI and vision | None | Dinesh | OPEN |
| NX-ARCH-OI-010 | NPU architecture and implementation; NPU model and tensor-format requirements | AI and vision | None | Dinesh | OPEN |
| NX-ARCH-OI-011 | Frame-buffer release-latency bound; buffer-borrowing policy; DDR use for optional intermediates and recording | AI and vision | None | Dinesh | OPEN |
| NX-ARCH-OI-012 | Subsystem power budgets and measured workload performance | AI and vision | None | Dinesh | OPEN |
| NX-ARCH-OI-013 | DPI electrical and pin configuration; final pixel format | Display and multimedia | None | Dinesh | OPEN |
| NX-ARCH-OI-014 | Compositor implementation and framebuffer policy; display DMA coherency and bandwidth margin; underflow behaviour and recovery; DRM/KMS integration | Display and multimedia | None | Dinesh | OPEN |
| NX-ARCH-OI-015 | External PHY selection; RGMII delay configuration at MAC and board level | Ethernet and EtherCAT | None | Dinesh | OPEN |
| NX-ARCH-OI-016 | MAC register and descriptor interfaces; DMA buffer coherency; hardware timestamping decision | Ethernet and EtherCAT | None | Dinesh | OPEN |
| NX-ARCH-OI-017 | EtherCAT stack and driver support; redundancy implementation and verification | Ethernet and EtherCAT | None | Dinesh | OPEN |
| NX-ARCH-OI-018 | Signature and hash formats; asymmetric cryptographic algorithms | Security | None | Dinesh | OPEN |
| NX-ARCH-OI-019 | Root-key provisioning; anti-rollback policy; recovery behaviour; secure boot failure handling | Security | None | Dinesh | OPEN |
| NX-ARCH-OI-020 | Debug lifecycle and authorisation; eFuse programming and access control | Security | None | Dinesh | OPEN |
| NX-ARCH-OI-021 | Secure address-map finalisation; security interrupt and fault-response details | Security | None | Dinesh | OPEN |
| NX-ARCH-OI-022 | PWM, GPIO, timer, UART, I2C, SPI and I2S capabilities and timing; pinmux and package pin assignment | Peripherals | None | Dinesh | OPEN |
| NX-ARCH-OI-023 | PLL allocation and feasibility; clock source and clock-tree architecture; jitter requirements | Clock, reset and power | None | Dinesh | OPEN |
| NX-ARCH-OI-024 | DVFS operating points and voltage sequencing; PMIC and rail selection; power-domain implementation | Clock, reset and power | None | Dinesh | OPEN |
| NX-ARCH-OI-025 | Reset sources and sequencing; clock-domain and reset-domain matrices; CDC and RDC waiver policy | Clock, reset and power | None | Dinesh | OPEN |
| NX-ARCH-OI-026 | Independent hardware response to critical faults | Clock, reset and power | None | Dinesh | OPEN |
| NX-ARCH-OI-027 | Tool versions and qualified configurations; evidence metadata and acceptance policy | Toolchain, FPGA and physical design | None | Dinesh | OPEN |
| NX-ARCH-OI-028 | FPGA board selection; C910 RTL compatibility with the FPGA target; DDR PHY availability and suitability | Toolchain, FPGA and physical design | None | Dinesh | OPEN |
| NX-ARCH-OI-029 | Renode CPU model compatibility; RTL co-simulation boundary | Toolchain, FPGA and physical design | None | Dinesh | OPEN |
| NX-ARCH-OI-030 | Technology wrapper interfaces; SRAM macro and technology collateral availability; OpenLane block-level scope and supported targets; FPGA and ASIC implementation constraints | Toolchain, FPGA and physical design | None | Dinesh | OPEN |
| NX-ARCH-OI-031 | Always-on domain definition | Always-on domain | NX-REQ-031 | Dinesh | OPEN |
| NX-ARCH-OI-032 | Interrupt architecture: the application controller baseline (a PLIC and a CLINT) is SELECTED in NX-REQ-116 (NX-DEC-033); the security and always-on controllers and the routing among the three stay open | Clock, reset and interrupts | NX-REQ-057; NX-REQ-116 | Dinesh | OPEN |
| NX-ARCH-OI-033 | C910-to-APB timeout value, recovery and late completion: proposed as 1024 bridge-clock cycles | AXI fabrics | NX-REQ-080 | Dinesh | PROPOSED |
| NX-ARCH-OI-034 | AXI fabric bridge buffering limits, backpressure, ID handling and APB version: proposed | AXI fabrics | NX-REQ-081 | Dinesh | PROPOSED |
| NX-ARCH-OI-035 | DMA controller details: peripheral request and handshake mapping, descriptor format, memory coherency, DMA power domain and wake-up; decided in the DMA specification by PROPOSED defaults, changed by change request | DMA | NX-REQ-093 to NX-REQ-100 | Dinesh | OPEN |
| NX-ARCH-OI-036 | Division of the application peripheral register space (0x00_4000_0000 to 0x00_4FFF_FFFF) among the peripheral instances, including the DMA controller register window and the APB-0 and APB-1 split; closed by NX-DEC-033 (ADDRESS_MAP section 2.1, peripheral_windows.yaml, NX-REQ-112); the register layout of each block stays open | Memory | NX-REQ-053; NX-REQ-112 | Dinesh | CLOSED |
| NX-ARCH-OI-037 | Domain crossings: the application-fabric attachment of the secure-to-application bridge (usable before C910 reset release), the mailbox register layout, message format, interrupt directions and secure-side validation rule; closed by NX-DEC-033 (MEMORY_ARCHITECTURE 5.4 and 5.5); the remaining items are NX-ARCH-OI-038 and NX-ARCH-OI-025, and whether the security core may later reach DDR4 needs a decision record (NX-DEC-027) | Security | NX-REQ-106; NX-REQ-107; NX-REQ-113; NX-REQ-114; NX-REQ-115 | Dinesh | CLOSED |
| NX-ARCH-OI-038 | Mailbox allow-list contents, requester authentication, replay and flood protection and the response to repeated invalid requests; the reset domain of AXI-3 and System SRAM for the boot window (with NX-ARCH-OI-025); the System SRAM attachment point on the fabrics; the width and clock conversion between the secure AXI and AXI-3 | Security | NX-REQ-113; NX-REQ-114 | Dinesh | OPEN |
