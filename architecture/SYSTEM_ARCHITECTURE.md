# Kritva Nexus System Architecture

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-ARCH-001 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Architecture |
| Status | DRAFT (first part; not reviewed or approved) |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.1.0-draft |
| Last Updated | 2026-11-07 |
| Authority | INPUT (not AUTHORITATIVE until the owner approves it) |
| Related Tasks / Milestones | KOS-NEXUS-006; NX-M1 |
| Related Documents | [A0 integration draft](A0_INTEGRATION_DRAFT.md); [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md); [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md) |

## Purpose

This document is the top-level system architecture of the Nexus SoC, owned by this repository. It consolidates the A0 integration draft, which is an input and a reconstruction of a working discussion, into one document that traces to the requirements register and the decision records. It is written for the owner, reviewers and the engineers who will write the interconnect, memory and address-map documents (KOS-NEXUS-007 and 008). It does not replace those documents and does not contain RTL, numeric performance results or implementation evidence.

## 1. Scope and status of this part

This first part covers the document rules, the system context and the domain map. Domain sections, the interface register and the open-issues register (AC-012) are added in later pull requests of KOS-NEXUS-006; until a topic has a section here, the A0 draft section named in the domain map is the only description of it, and it is PROPOSED.

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

## 5. Open architecture gaps

The four gaps below are open and are kept under their canonical identifiers. They are not resolved by this document. The wider open-issues register with owners follows in a later pull request.

| Gap | Subject | Requirement |
|---|---|---|
| NX-ARCH-GAP-001 | C910 to APB access path | NX-REQ-027 |
| NX-ARCH-GAP-002 | Secure and application address spaces | NX-REQ-028 |
| NX-ARCH-GAP-003 | C910 application address width | NX-REQ-029 |
| NX-ARCH-GAP-004 | DDR4 controller ingress | NX-REQ-030 |
