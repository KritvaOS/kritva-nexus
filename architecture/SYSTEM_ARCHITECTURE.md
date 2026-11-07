# Kritva Nexus System Architecture

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-ARCH-001 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Architecture |
| Status | DRAFT (partial; not reviewed or approved) |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.2.0-draft |
| Last Updated | 2026-11-07 |
| Authority | INPUT (not AUTHORITATIVE until the owner approves it) |
| Related Tasks / Milestones | KOS-NEXUS-006; NX-M1 |
| Related Documents | [A0 integration draft](A0_INTEGRATION_DRAFT.md); [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md); [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) |

## Purpose

This document is the top-level system architecture of the Nexus SoC, owned by this repository. It consolidates the A0 integration draft, which is an input and a reconstruction of a working discussion, into one document that traces to the requirements register and the decision records. It is written for the owner, reviewers and the engineers who will write the interconnect, memory and address-map documents (KOS-NEXUS-007 and 008). It does not replace those documents and does not contain RTL, numeric performance results or implementation evidence.

## 1. Scope and status

This document so far covers the document rules, the system context, the domain map and the application CPU, application interconnect and external memory sections. The remaining domain sections (AI and vision, multimedia and connectivity, security, always-on, clock, reset, power and interrupt), the interface register and the open-issues register (AC-012) are added in later pull requests of KOS-NEXUS-006; until a topic has a section here, the A0 draft section named in the domain map is the only description of it, and it is PROPOSED.

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

## 8. Open architecture gaps

The four gaps below are open and are kept under their canonical identifiers. They are not resolved by this document. The wider open-issues register with owners follows in a later pull request.

| Gap | Subject | Requirement |
|---|---|---|
| NX-ARCH-GAP-001 | C910 to APB access path | NX-REQ-027 |
| NX-ARCH-GAP-002 | Secure and application address spaces | NX-REQ-028 |
| NX-ARCH-GAP-003 | C910 application address width | NX-REQ-029 |
| NX-ARCH-GAP-004 | DDR4 controller ingress | NX-REQ-030 |
