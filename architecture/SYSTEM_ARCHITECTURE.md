# Kritva Nexus System Architecture

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-ARCH-001 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Architecture |
| Status | DRAFT (partial; not reviewed or approved) |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.4.0-draft |
| Last Updated | 2026-11-07 |
| Authority | INPUT (not AUTHORITATIVE until the owner approves it) |
| Related Tasks / Milestones | KOS-NEXUS-006; NX-M1 |
| Related Documents | [A0 integration draft](A0_INTEGRATION_DRAFT.md); [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md); [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) |

## Purpose

This document is the top-level system architecture of the Nexus SoC, owned by this repository. It consolidates the A0 integration draft, which is an input and a reconstruction of a working discussion, into one document that traces to the requirements register and the decision records. It is written for the owner, reviewers and the engineers who will write the interconnect, memory and address-map documents (KOS-NEXUS-007 and 008). It does not replace those documents and does not contain RTL, numeric performance results or implementation evidence.

## 1. Scope and status

This document so far covers the document rules, the system context, the domain map and a section for every domain in section 4. The interface register and the open-issues register (AC-012) are added in later pull requests of KOS-NEXUS-006; until a topic has a section here, the A0 draft section named in the domain map is the only description of it, and it is PROPOSED.

Detailed interconnect, memory and address-map content belongs to KOS-NEXUS-007 and 008. Subsystem microarchitecture and RTL are out of scope.

## 2. Rules for this document

1. Every architecture statement carries one label: `SELECTED` (recorded owner decision, with a decision record), `PROPOSED` (a recommendation, including every one from an AI tool) or `OPEN` (needs engineering definition). A statement without a label is not part of the architecture.
2. A SELECTED statement names its decision record (NX-DEC-NNN). A PROPOSED or OPEN statement names its requirement (NX-REQ-NNN) or gap (NX-ARCH-GAP-NNN).
3. Where this document and the requirements register or a decision record differ, the register or record wins and this document is corrected.
4. Numeric parameters stay PROPOSED unless the requirement is SELECTED. Owner-selected values are only those in the register: 6 MiB frame pool, 720p60 at 1280x720 over parallel DPI, three composition layers, 64 KiB security ROM and SRAM, the four application AXI fabrics, the two AXI-to-APB interconnects and the peripheral counts.
5. Evidence stays separate. Renode results are not evidence of C910 timing, cache behaviour or cycle accuracy; a substitute CPU on FPGA is labelled a substitute; lint, Yosys, FPGA synthesis and OpenLane results are `software` evidence, simulation results are `simulation` evidence and `physical` is reserved for programmed-board results.

## 3. System context

Nexus is the application-processing and AI SoC of the Kritva robotics platform and interfaces with Kritva Edge over EtherCAT (PROPOSED, NX-REQ-040, NX-REQ-041; the SELECTED part is two independent Ethernet MACs, NX-DEC-007). Nexus is outside the Kritva Program V2 plan and is planned for the V3 plan.

External interfaces named in the register: DDR4 (SELECTED, NX-DEC-001), Octal SPI PSRAM (SELECTED, NX-DEC-002), OSPI NOR boot medium (SELECTED, NX-DEC-003), camera inputs (PROPOSED, NX-REQ-042), a parallel DPI display (SELECTED, NX-DEC-005), two Ethernet MACs (SELECTED, NX-DEC-007) and board-level peripherals (counts SELECTED, NX-DEC-020).

## 4. Domain map

| Domain | Contents | Label | Records | A0 draft |
|---|---|---|---|---|
| Application CPU | Xuantie C910 direction; RV64 quad-core cluster; C910 DVFS | PROPOSED CPU (CPU IP and configuration); SELECTED DVFS | NX-REQ-001, 055, 056; NX-DEC-018 (PROPOSED); NX-DEC-016 | Section 2 |
| Application interconnect | Four AXI fabrics, Memory Access Crossbar, two AXI-to-APB interconnects, application address map | SELECTED counts; PROPOSED roles, widths and map | NX-DEC-014, NX-DEC-015; NX-REQ-049 to 053 | Section 9 |
| Memory | DDR4, Octal SPI PSRAM, OSPI NOR boot | SELECTED media; PROPOSED controller targets; OPEN DDR4 ingress | NX-DEC-001 to 003; NX-REQ-030, 064, 065 | Section 4 |
| AI and vision | Camera inputs, 6 MiB frame pool, ISP, NPU, NPU DVFS | SELECTED frame-pool capacity and NPU DVFS; PROPOSED the rest | NX-DEC-004, NX-DEC-017; NX-REQ-042 to 047 | Section 3 |
| Multimedia and connectivity | 720p60 parallel DPI display, three composition layers, two Ethernet MACs, EtherCAT MainDevice, peripherals | SELECTED display mode, layers, MAC count, peripheral counts; PROPOSED EtherCAT, RGMII, compositor | NX-DEC-005 to 007, NX-DEC-020; NX-REQ-040, 041, 048 | Sections 5, 6 and 8 |
| Security | Isolated 32-bit RISC-V core, 64 KiB ROM and SRAM, eFuse, AES, SHA-256, separate secure AXI | SELECTED; PROPOSED accelerator, boot sequence, secure map; OPEN address-space separation | NX-DEC-008 to 013, NX-DEC-019; NX-REQ-033 to 039, 054; NX-REQ-028 | Section 7 |
| Always-on, clock, reset, power, interrupt | Always-on domain, PLLs, power and reset domains, interrupts, CDC and RDC, DVFS | SELECTED DVFS; PROPOSED PLL, domains and targets; OPEN always-on definition and interrupt architecture | NX-DEC-016, NX-DEC-017; NX-REQ-031, 057 to 063, 066 | Section 10 |

## 5. Application CPU

| Item | Statement | Label | Records |
|---|---|---|---|
| CPU IP | The application CPU subsystem uses the Xuantie C910, RV64. The exact RTL release and configuration are not confirmed. | PROPOSED | NX-REQ-001, NX-DEC-018 |
| Cluster | One cluster of four cores with 64 KB L1 instruction and data caches per core and a shared 1 MB L2; 1.0 to 1.2 GHz is a target, not a timing result. | PROPOSED | NX-REQ-055 |
| CPU interface | AXI4, 128-bit data, 8 outstanding reads and 8 outstanding writes; the 40-bit address width is unconfirmed. | PROPOSED | NX-REQ-056 |
| Address width | The application address width is confirmed against the selected C910 configuration before the address map is frozen. | OPEN | NX-REQ-029, NX-ARCH-GAP-003 |
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
| AXI-3 | General peripherals, control and DMA | 64-bit | Peripheral and I2S DMA |

A separate Memory Access Crossbar with four fabric ingress ports is PROPOSED (NX-REQ-049) to avoid serialising memory access through AXI-0; its relationship to the DDR4 controller ports is OPEN (NX-REQ-030, NX-ARCH-GAP-004), and four ingress ports do not establish the DDR4 port count. The two AXI-to-APB interconnects are proposed at 32-bit APB data width and 200 to 250 MHz (NX-REQ-052).

The path from the C910 to the APB peripherals (C910, AXI-0, routing or bridge, AXI-to-APB, APB-0 or APB-1) is a proposal and is OPEN (NX-REQ-027, NX-ARCH-GAP-001): routing, decode, access control, bridge placement and error response are not defined. The application address map is PROPOSED (NX-REQ-053) and is held by KOS-NEXUS-008, not copied here. Its apertures are not memory capacities: the 16 MiB frame-pool aperture is not the owner-selected 6 MiB capacity, and the DDR4 window does not select a DDR4 device size. Cacheability, coherency, security attributes, permissions and IOMMU needs are OPEN.

## 7. External memory

| Memory | Role | Label | Records |
|---|---|---|---|
| DDR4 | Primary system memory for Linux and applications, NPU models and large activations, display framebuffers and DMA buffers | SELECTED role | NX-REQ-002, NX-DEC-001 |
| Octal SPI PSRAM | Secondary memory | SELECTED role | NX-REQ-003, NX-DEC-002 |
| OSPI NOR | Primary boot medium: boot firmware, bootloader and recovery, configuration and authenticated updates | SELECTED role | NX-REQ-004, NX-DEC-003 |

The NOR and the PSRAM are separate devices with separate controllers. The operating targets are PROPOSED: DDR4-3200 (NX-REQ-064) and a PSRAM controller at 200 to 400 MHz (NX-REQ-065). DDR4 data width and capacity, the PSRAM protocol, mode and capacity, and the NOR device are not selected. The 200 MHz OSPI x8 figure in the A0 draft is an example calculation, not a requirement. The secure boot path must reach the NOR before the application fabrics and the C910 are active (PROPOSED, NX-REQ-038). The DDR4 ingress topology and port count are OPEN (NX-REQ-030, NX-ARCH-GAP-004), and memory arbitration and bandwidth allocation are not defined.

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
| Secure address map | A separate secure address space with the proposed map of A0 draft section 7.4. | PROPOSED | NX-REQ-054 |
| Address-space separation | The secure and application address spaces are separate, with independent decode and access control; the isolation boundary, the permitted access paths and the treatment of overlapping numerical ranges are not yet defined. | OPEN | NX-REQ-028, NX-ARCH-GAP-002 |

The security domain is described here as an architecture direction. Root-key provisioning, anti-rollback policy, recovery behaviour, debug lifecycle and authorisation, eFuse programming and access control, secure boot failure handling and the security interrupt and fault-response details are OPEN. No security claim is made from this document: it contains no threat model, no verification result and no hardware validation.

## 11. Always-on, clock, reset, power and interrupts

| Item | Statement | Label | Records |
|---|---|---|---|
| DVFS | DVFS is supported for the C910 subsystem and for the NPU. Operating points and voltage sequencing are OPEN. | SELECTED | NX-REQ-017, NX-REQ-018, NX-DEC-016, NX-DEC-017 |
| Always-on domain | The responsibilities of the always-on domain and its interfaces to reset, wake-up, security and power control are not defined. | OPEN | NX-REQ-031 |
| Interrupt controllers | An application controller with 128 external sources, a security controller with 32 sources and an always-on controller with 8 to 16 wake sources; the PLIC versus AIA choice is undecided. | OPEN | NX-REQ-057 |
| PLLs | Four integer PLLs and two fractional PLLs; allocation and feasibility are not verified. | PROPOSED | NX-REQ-058 |
| Frequency targets | C910 1.0 to 1.2 GHz, NPU 800 MHz, ISP 600 MHz, security core 200 to 400 MHz, AXI fabrics 400 to 600 MHz, APB 200 to 250 MHz, PSRAM controller 200 to 400 MHz and DPI pixel clock 74.25 MHz. These are targets, not timing results. | PROPOSED | NX-REQ-059 |
| Power domains | Seven logical domains: AON, SEC, CPU, MEM, AI, MEDIA and IO; the implementation is not defined. | PROPOSED | NX-REQ-060 |
| Reset domains | Eight domains: AON, SEC, CPU, MEM, AI, ISP, DISP and IO, with asynchronous assertion and synchronous deassertion. Reset sources and sequencing are OPEN. | PROPOSED | NX-REQ-061 |
| CDC and RDC | Every clock-domain and reset-domain crossing uses a suitable synchroniser, asynchronous FIFO or reset synchroniser and is covered by CDC and RDC checks with documented waivers. | PROPOSED | NX-REQ-062 |
| Critical faults | Critical thermal, power and tamper faults have a hardware response independent of application CPU execution; the response is not defined. | PROPOSED | NX-REQ-063 |
| SoC power | A total power target of 10 to 20 W. This is a target, not an estimate or a measurement. | PROPOSED | NX-REQ-066 |

The clock source and clock-tree architecture, jitter requirements, PMIC and rail selection, the clock-domain and reset-domain matrices and the CDC and RDC waiver policy are OPEN.

## 12. Open architecture gaps

The four gaps below are open and are kept under their canonical identifiers. They are not resolved by this document. The wider open-issues register with owners follows in a later pull request.

| Gap | Subject | Requirement |
|---|---|---|
| NX-ARCH-GAP-001 | C910 to APB access path | NX-REQ-027 |
| NX-ARCH-GAP-002 | Secure and application address spaces | NX-REQ-028 |
| NX-ARCH-GAP-003 | C910 application address width | NX-REQ-029 |
| NX-ARCH-GAP-004 | DDR4 controller ingress | NX-REQ-030 |
