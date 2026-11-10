# Kritva Nexus RTL Design Standard

| Property | Value |
|---|---|
| Document ID | KNX-RTL-STD-001 |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Engineering Standard |
| Status | APPROVED (SELECTED by NX-DEC-023; the section 19 check plan and the section 20 defaults stay PROPOSED) |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 1.0.1 |
| Last Updated | 2026-11-10 |
| Authority | AUTHORITATIVE for Kritva Nexus RTL design rules |
| Related Tasks / Milestones | KOS-NEXUS-020; NX-M1 |
| Related Documents | [NX-DEC-023](../decisions/NX-DEC-023.md) (approval); [NX-REQ-082 to 091](../requirements/REQUIREMENTS.md); [system architecture](../architecture/SYSTEM_ARCHITECTURE.md); [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md); [acceptance criteria](../ACCEPTANCE_CRITERIA.md) (AC-030 to AC-033) |

## Purpose

This standard sets the RTL design and implementation rules for Kritva Nexus: naming, file and module organisation, coding, reset and clock policy, the common RTL library, clock-domain crossings, low-power and clock gating, memory wrappers, latches, lint and sign-off. Its aim is RTL that is reusable, technology-portable, verifiable and ready for integration.

It is a design-control document. A passing check does not establish functional correctness, timing closure, power sign-off or release readiness. It reports no evidence: lint, synthesis, simulation and coverage results belong in the evidence records of the tasks that produce them, with target, tool and version, configuration revision, source commit and run ID.

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.0.0-draft | 2026-11-09 | Imported from the draft KNX-RTL-STD-001 v1.0.0 and corrected: sections renumbered and cross-references fixed; stable rule IDs and an enforcement column added; the weight and credit model moved to an informative annex that does not apply to Nexus; roles set to the interim all-owner arrangement; one file-length policy; copyright holder and licence fixed in the source header; the open methodology decisions each given a proposed default or a deciding procedure; automated compliance checks defined (section 19). |
| 1.0.1-draft | 2026-11-10 | Correction pass after an external ChatGPT review of the merged draft: waiver cross-reference fixed; permanent rule IDs added for the specification (SPC) and low-power (LPW) rules; every A-rule mapped to a check, phase or review-only disposition (section 19.1); result states reconciled for the manifest (19.2, 19.4); clock-source classification, clock muxes, dividers and generated clocks, reset identification and polarity, and array counting defined (19.3, MEM-002); the provisional status of the clock-gating figures stated in full; negative fixtures required (19.6); library wording made future tense; a waiver cannot replace an owner decision record (18.3). |
| 1.0.1 | 2026-11-10 | Approved by the owner as NX-DEC-023 (SELECTED), all rules, with the section 19 check plan and the section 20 defaults left PROPOSED and the clock-gating figures provisional. The rule text is the reviewed 1.0.1-draft text; only the status, authority, label wording and approval table changed. |

## 1. Scope and applicability

This standard applies to synthesizable design RTL: SoC top-level and integration logic, reusable IP blocks, subsystems and interconnect components, and wrappers around memories, clocks, resets, power and technology cells, including packages and interfaces, and RTL changes made in maintenance or integration.

Testbenches, assertions, formal properties, scripts and generated verification sources follow the verification rules of the repository. The file-length limits of section 6 apply to design RTL; verification sources may adopt separate limits.

Nothing here creates RTL, a directory or a tool. Directories such as `rtl/` and `technology/` are added only when a real task needs them (AGENTS.md rule 3), and no check in section 19 exists until a task implements it.

## 2. Normative language, rule identifiers and labels

| Term | Meaning |
|---|---|
| SHALL / MUST | Mandatory |
| SHALL NOT / MUST NOT | Prohibited |
| SHOULD | Expected practice; a deviation needs a recorded reason and review |
| MAY | Optional |

**Rule identifiers.** Every rule has a permanent identifier `KNX-RTL-<CAT>-NNN`. Checker output, waivers, reviews and requirement rows cite these identifiers. A removed rule is marked RETIRED and its identifier is never reused. Categories: SPC specification entry, NAM naming, FIL file and module organisation, DOC source header, COD coding, RST reset, CLK clock and clock gating, LPW low-power RTL, LIB common library and technology abstraction, CDC clock-domain crossings, LAT latches, MEM memory, VER lint and verification, INT integration, GOV review, exceptions and change control.

**Enforcement column.** A automated: a check can decide it from source or tool output, so it is a candidate for CI (section 19). T tool-assisted: a tool produces a report that a reviewer judges. R review only. CI cannot establish that a design is functionally correct or safe: for example, finding a reset synchroniser instance does not prove that every reset release is synchronised correctly.

**Labels.** The standard follows the repository labels. The rules of this document were approved by the owner as NX-DEC-023 and are SELECTED, so they are mandatory for design RTL. The automated compliance checks of section 19 and the methodology defaults of section 20 are PROPOSED, and the clock-gating figures are provisional until section 20 selects them. A PROPOSED item changes by change request; a SELECTED item changes by change request and a new decision record (section 18.4). OPEN means no default exists yet.

A requirement is not satisfied because a design document mentions it; evidence must show implementation and review.

## 3. Design principles

1. Specification first: a feature or IP has a specification before it is reported as implemented.
2. Modular design with explicit interfaces: ports, widths, protocols, clocks and resets are documented at every boundary.
3. Portable RTL: functional RTL does not name foundry or library cells.
4. Common infrastructure: shared CDC, reset, clock-gating, FIFO and memory structures come from the approved common RTL library.
5. Low power by design: avoid unnecessary switching and identify clock-gating opportunities early.
6. Verification by construction: requirements, assertions, coverage points and tests are planned with the RTL.
7. DFT awareness: RTL supports the approved scan, test-clock and memory-test method once it is defined.
8. Traceability from requirement to RTL, test, report, review and accepted commit.
9. Controlled exceptions: unusual constructs and deviations are recorded in a waiver (section 18.3).

## 4. Specification and design entry

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-SPC-001 | Every SoC feature and reusable IP SHALL have a specification before its implementation is reported as complete. | R |
| KNX-RTL-SPC-002 | The specification SHALL include, at least: purpose, scope and non-goals; architecture and submodule split; port list and interface protocols; register map where applicable; clock and reset domains; power domains and modes where applicable; CDC and RDC inventories; common-library dependencies and versions; low-power and clock-gating plan; file and module plan; verification plan and acceptance criteria; lint, CDC, DFT and coverage targets; integration dependencies, risks and open issues. | R |
| KNX-RTL-SPC-003 | Requirements SHALL carry unique identifiers and a verification method, and a TBD value SHALL NOT be presented as an approved design target. | R |

## 5. Naming and interface rules

### 5.1 Port and signal naming

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-NAM-001 | Every module port SHALL end in a suffix for its direction at that boundary: input `_i`, output `_o`, inout `_io`. This includes clocks, resets, interrupts, test, scan, debug and sideband ports. | A |
| KNX-RTL-NAM-002 | Internal wires, variables, registers and logic signals SHALL NOT end in `_i`, `_o` or `_io`. Parent and child port names need not match, because direction is relative to each module. | A |
| KNX-RTL-NAM-003 | Names of modules, ports, signals, instances and files SHALL be lowercase snake_case, unless a repository-wide convention requires otherwise. | A |
| KNX-RTL-NAM-004 | Names SHOULD describe function and context; vague names such as `temp`, `data1`, `sig` or `enable` SHOULD NOT be used. | R |
| KNX-RTL-NAM-005 | An active-low signal SHALL carry `_n` before the direction suffix: `rst_core_n_i`, `irq_n_o`. | A |

### 5.2 Clock port naming

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-NAM-006 | Every clock port SHALL contain `clk` as a recognisable prefix or suffix. | A |
| KNX-RTL-NAM-007 | The preferred form is `clk_<domain>_<direction suffix>` (`clk_core_i`, `clk_div2_o`). The suffix form `<domain>_clk_i` is permitted only where an approved interface convention requires it; a new IP SHALL NOT mix the two styles. | A (warn) |
| KNX-RTL-NAM-008 | A generated or forwarded clock output SHALL contain `clk` and end in `_o`. | A |
| KNX-RTL-NAM-009 | An internal clock net SHALL contain `clk` and SHALL NOT carry a direction suffix (`clk_core_gated`). | A |
| KNX-RTL-NAM-010 | A clock enable is not a clock and SHALL NOT be named as one (`clk_core_en_i`, `clock_enable`). | A |
| KNX-RTL-NAM-011 | Ambiguous clock names such as `sys_i`, `core_i` or `clock1_i` SHALL NOT be used. | A |

How a checker identifies a clock port is defined in section 19.3; it never relies on a name alone to decide clock semantics.

### 5.3 Other identifiers

| ID | Object | Rule | Enf. |
|---|---|---|---|
| KNX-RTL-NAM-012 | Module | Lower snake_case (`knx_dma_ctrl`) | A |
| KNX-RTL-NAM-013 | RTL file | Name matches the primary module (`knx_dma_ctrl.sv`) | A |
| KNX-RTL-NAM-014 | Instance | Lower snake_case; the `u_` prefix is recommended (`u_dma_ctrl`) | R |
| KNX-RTL-NAM-015 | Parameter and local parameter | Upper snake_case (`DATA_WIDTH`, `STATE_IDLE`) | A |
| KNX-RTL-NAM-016 | Package | Lower snake_case ending `_pkg` | A |
| KNX-RTL-NAM-017 | Interface | Lower snake_case ending `_if` | A |

A repository may refine prefixes but SHALL NOT weaken the port suffix rules.

## 6. RTL file and module organisation

### 6.1 File length

Length is a physical line count: it includes the header, copyright notice, comments and blank lines. It applies to design source files including packages and interfaces, and to generated RTL unless a waiver exists. Line count is one signal of quality, not the only one; a short module with many responsibilities can be worse than a longer, well-structured one.

| ID | Lines | Treatment | Enf. |
|---|---|---|---|
| KNX-RTL-FIL-001 | 300 to 800 | Preferred target (guideline) | R |
| KNX-RTL-FIL-002 | 801 to 1,000 | Acceptable; watch complexity | R |
| KNX-RTL-FIL-003 | Above 1,000 | Warning; design review of the split | A (warn) |
| KNX-RTL-FIL-004 | Above 1,500 | Explicit decomposition review recorded | A (warn) |
| KNX-RTL-FIL-005 | Above 2,000 | Failure; a waiver is required | A (fail) |
| KNX-RTL-FIL-006 | Any | An include file SHALL NOT be used to hide or bypass an oversized source file | T |

This section is the single authority for these thresholds. Other documents, including the A0 draft guidance on module size, refer here; they do not set a competing policy. AC-033 applies the guideline and records each exceedance review.

### 6.2 Module organisation

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-FIL-007 | One primary synthesizable module per file is the default, and the file name matches it. | A (warn) |
| KNX-RTL-FIL-008 | Packages and interfaces SHALL be in separately named files. | A |
| KNX-RTL-FIL-009 | Compilation dependencies SHALL be explicit and documented. | R |
| KNX-RTL-FIL-010 | Unrelated modules SHALL NOT be grouped to reduce file count. | R |

A recommended IP layout is `README.md`, `SPEC.md`, `rtl/`, `tb/`, `tests/`, `formal/`, `constraints/`, `cdc/` and `docs/`. Use the repository's approved structure where one exists, and create no unused directory to match the example.

## 7. Source header

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-DOC-001 | Every design source file (`.v`, `.sv`, and design include files) SHALL begin with the header of Appendix A, before any package, interface or module. | A |
| KNX-RTL-DOC-002 | The copyright line SHALL read `Copyright (c) <YEAR> Kritva Robotics` and the file SHALL carry `SPDX-License-Identifier: Apache-2.0`, matching the repository LICENSE. | A |
| KNX-RTL-DOC-003 | The `Module` field SHALL match the primary module (or the package or interface) declared in the file, and the `File` field the file name. | A |
| KNX-RTL-DOC-004 | The `RTL Standard` field SHALL name `KNX-RTL-STD-001`. | A |
| KNX-RTL-DOC-005 | The header SHALL NOT be removed, shortened to evade the line limit or moved to an include file. | R |
| KNX-RTL-DOC-006 | A header SHALL NOT hold credentials, secrets or personal contact details. | R |
| KNX-RTL-DOC-007 | The `Last Modified` date and the change history do not replace Git history. | R |

A checker can test that a field is present and well formed (for example a valid requirement or specification reference); it cannot show that the reference describes the implementation, which stays a review item.

## 8. RTL coding rules

### 8.1 Logic and signals

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-COD-001 | Sequential logic SHALL use `always_ff` with nonblocking assignments. | A |
| KNX-RTL-COD-002 | Combinational logic SHALL use `always_comb` with blocking assignments. | A |
| KNX-RTL-COD-003 | Combinational outputs SHALL be assigned on every path (see section 13). | A |
| KNX-RTL-COD-004 | A signal SHALL NOT have multiple drivers, and procedural multiple drivers are avoided. | A |
| KNX-RTL-COD-005 | Widths, signedness and casts SHALL be explicit; implicit nets, ambiguous sizing and unintended truncation are avoided. | A (lint) |
| KNX-RTL-COD-006 | Parameter ranges and legal combinations SHALL be defined and checked. | R |
| KNX-RTL-COD-007 | FSM default and illegal-state recovery SHALL be explicit; states, reset state and transitions are documented. | R |
| KNX-RTL-COD-008 | Design RTL SHALL NOT use simulation-only constructs, `force` and `release`, delays or testbench-only constructs. | A |
| KNX-RTL-COD-009 | Pipeline stages, arithmetic widths, saturation and overflow behaviour, latency, backpressure, ordering, arbitration and simultaneous-event behaviour SHALL be specified. | R |

State encoding is chosen for implementation and verification reasons; no encoding is assumed best everywhere.

### 8.2 Reset

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-RST-001 | All resets and reset controls in functional RTL SHALL be active-low. | A (name) and T (use) |
| KNX-RTL-RST-002 | An active-low reset port SHALL follow `rst_<domain>_n_i` (`rst_core_n_i`). | A |
| KNX-RTL-RST-003 | An active-high reset is an exception; a waiver SHALL give the rationale, affected modules, reset-domain impact, CDC and RDC implications and verification evidence. Where an external component supplies one, polarity conversion is made at one defined integration boundary with an approved implementation. | A (waiver) |
| KNX-RTL-RST-004 | Every state element that needs a reset SHALL have a documented reset value and strategy; datapath and memory are not reset without a functional, safety or implementation reason. | R |
| KNX-RTL-RST-005 | Reset assertion and deassertion behaviour SHALL be defined for each reset domain. | R |
| KNX-RTL-RST-006 | An asynchronous reset deassertion SHALL be synchronised with the approved common-library reset structure where the reset method requires it, and a reset synchroniser SHALL NOT be reimplemented inside an IP. | A (instance) and R |
| KNX-RTL-RST-007 | Reset-domain crossings SHALL be reviewed separately from data CDC (section 10). | R |

### 8.3 Clock edge and clock gating

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-CLK-001 | Sequential functional RTL SHALL use the positive clock edge. Negative-edge and dual-edge sequential logic are not permitted without a waiver. | A |
| KNX-RTL-CLK-002 | A clock-edge waiver SHALL identify the clock and registers, timing intent, generated-clock and STA implications, CDC, RDC and DFT impact and verification evidence. | A (waiver) |
| KNX-RTL-CLK-003 | Clock gating SHALL use the approved common-library clock-gating abstraction and mapping flow. | A |
| KNX-RTL-CLK-004 | A hand-written combinational clock gate (for example `assign gated_clk = clk & enable`) SHALL NOT be used. A checker flags any clock net used as a data operand of a logic expression or assignment outside an approved library module. | A |
| KNX-RTL-CLK-005 | Gating enable logic SHALL meet the approved glitch-free implementation rules. | R |
| KNX-RTL-CLK-006 | Scan and test enable override SHALL be supported and verified as the DFT method requires. | T |
| KNX-RTL-CLK-007 | Generated clocks and clock-gating checks SHALL be correct in timing constraints and reports. | T |
| KNX-RTL-CLK-008 | Gating fanout, granularity, enable source and exceptions SHALL be documented (register in Appendix C). | R |
| KNX-RTL-CLK-009 | Clock-gating metrics SHALL report numerator, denominator, percentage, exclusions and evidence per metric, SHALL NOT be added together, and are provisional until section 20 decisions STD-D-001 and STD-D-002 are selected. | T |
| KNX-RTL-CLK-010 | Clock multiplexers, clock dividers and other generated-clock structures SHALL come from approved library modules; any other logic that produces a clock SHALL carry a waiver. | A |

The imported draft listed proposed targets of 99% (single), 80% (dual) and above 60% (quad) clock gating. They stay provisional planning figures until the classes (STD-D-001), the eligible denominator and the exclusions (STD-D-002) are approved; none of them is an auditable sign-off metric before then, and compliance is not claimed from RTL intent but from mapped synthesis reports.

## 9. Common RTL library and technology abstraction

### 9.1 Library as the technology boundary

Kritva Nexus is to have one approved common RTL library of reviewed abstractions for shared infrastructure: single-bit level synchronisers, pulse and event synchronisers, request and acknowledge CDC handshakes, asynchronous FIFOs and multi-bit CDC structures, reset synchronisers, clock-gating wrappers, memory wrappers, tie-high and tie-low cells, isolation, retention and level-shifter abstractions, and DFT and scan wrappers, as the SoC needs them. No module of that library exists yet; the tasks that create them are KOS-NEXUS-021 and KOS-NEXUS-073 to KOS-NEXUS-078 in the [task catalogue](../planning/TASK_CATALOGUE.md).

### 9.2 Rules

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-LIB-001 | CDC, reset-synchroniser, clock-gate, FIFO and memory structures SHALL be instantiated from modules listed in the approved library manifest (section 19.4). | A |
| KNX-RTL-LIB-002 | Designers SHALL use the real approved module names and versions and SHALL NOT invent local substitutes. | A |
| KNX-RTL-LIB-003 | Feature and IP functional RTL SHALL NOT instantiate foundry or standard-cell library cells; technology cells are reached through approved wrappers or the approved mapping flow. | A |
| KNX-RTL-LIB-004 | Technology-specific `ifdef` branches, cell mappings and simulation models SHALL be owned and reviewed in the common library or the technology layer, and technology names SHALL NOT appear in portable IP interfaces. | A (flag) and R |
| KNX-RTL-LIB-005 | Each IP SHALL record its common-library dependencies (function, approved module, library commit, use, evidence). | R |
| KNX-RTL-LIB-006 | All synchronous and asynchronous FIFOs SHALL be library FIFOs. A locally coded dual-clock memory and pointer synchroniser is prohibited. A configuration the library lacks goes to a library enhancement request, or to a waiver reviewed for CDC and RDC. | A |
| KNX-RTL-LIB-007 | The library FIFO specification SHALL define depth and width limits, clocking mode, reset behaviour, full, empty and almost flag semantics, overflow and underflow behaviour, read latency, simultaneous read and write behaviour and parameter legality. | R |
| KNX-RTL-LIB-008 | Behavioural models SHALL suit simulation and SHALL NOT hide unknown or unsafe behaviour. | R |

A deviation from any LIB rule is a waiver (section 18.3) with a portability, verification and implementation impact assessment.

## 10. Clock-domain and reset-domain crossings

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-CDC-001 | Every asynchronous crossing SHALL be listed in a CDC inventory (Appendix B format). | R |
| KNX-RTL-CDC-002 | A crossing SHALL use an approved library structure suited to its semantics. | A (instance) and T |
| KNX-RTL-CDC-003 | Multi-bit data SHALL NOT be synchronised bit by bit where coherency is needed. | T |
| KNX-RTL-CDC-004 | Pulse crossings SHALL state event-rate assumptions and whether loss is allowed. | R |
| KNX-RTL-CDC-005 | Handshake crossings SHALL state data stability, request and acknowledge behaviour and reset interaction. | R |
| KNX-RTL-CDC-006 | Asynchronous FIFOs SHALL state depth, overflow and underflow behaviour and flag semantics. | R |
| KNX-RTL-CDC-007 | Reconvergence and related-signal coherency SHALL be assessed. | T |
| KNX-RTL-CDC-008 | Synchroniser depth and MTBF assumptions SHALL follow the approved CDC method. | R |
| KNX-RTL-CDC-009 | A CDC waiver SHALL give rationale, owner, reviewer and approval reference. | A (waiver) |
| KNX-RTL-CDC-010 | CDC and RDC acceptance needs a reviewed inventory, tool reports, resolved blockers and approved waivers. A percentage cannot override an unsafe crossing or unresolved blocker. | R |

The crossing is reviewed even when the source contains a two-flop synchroniser: reconvergent paths, multi-bit data and reset-domain crossings need more than structure detection. RDC: source and destination reset domains, sequencing assumptions, protection structures and tool findings are documented separately. CDC and RDC tool availability is unverified (STD-D-009), so until a tool exists these rules are review-only.

## 11. Low-power RTL

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-LPW-001 | Each IP SHALL identify idle and inactive conditions, clock-gating opportunities and enable conditions, operand-isolation opportunities, always-on logic and wake-up paths, retention and isolation needs, test-mode clock behaviour, and power modes and transitions. | R |
| KNX-RTL-LPW-002 | Where applicable, the IP SHALL provide the low-power evidence: clock-gating inference and mapped-cell report, gating simulation or assertion results, test-mode override verification, generated-clock and timing checks, activity-based power analysis, power-intent (UPF) checks for isolation and retention, and wake-up and state-restoration verification. This evidence is reported under the evidence rules in the introduction. | T |

## 12. Lint and quality gate

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-VER-001 | Lint is a mandatory gate (AC-030): the approved configuration is run at the required review points. | A |
| KNX-RTL-VER-002 | Critical and error findings SHALL be resolved before acceptance; warnings are fixed or carry a reviewed waiver (rule, location, rationale, owner, approval). | A |
| KNX-RTL-VER-003 | A lint report SHALL be tied to the RTL commit. | A |

## 13. Latch inference and approval

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-LAT-001 | Every inferred or explicitly coded latch requires prior documented approval. | A |
| KNX-RTL-LAT-002 | The exception for a latch inside an approved integrated clock-gating cell is scoped to the exact approved library module and instance. It SHALL NOT exempt a whole file or module, and it does not permit general-purpose latch inference in functional RTL. | A |
| KNX-RTL-LAT-003 | Without approval, the following are prohibited: incomplete combinational assignment that infers a latch; explicit level-sensitive latch coding; a latch used as an ad-hoc CDC synchroniser or data-holding structure; direct latch-cell instantiation in functional RTL. | A |
| KNX-RTL-LAT-004 | An approval records latch ID, RTL location, purpose, alternatives considered, timing, CDC and RDC, DFT, power, implementation, owner, approver and approval reference (a waiver entry, section 18.3). | A (waiver) |
| KNX-RTL-LAT-005 | The synthesised latch inventory SHALL match the approved inventory, excluding approved clock-gate internals. | A |

A checker treats three cases differently: an intentional latch inside an approved clock gate, an unintended inferred data latch, and a latch-like structure that appears after synthesis.

## 14. Memory inference and memory wrappers

### 14.1 Array rule

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-MEM-001 | An RTL array larger than the threshold SHALL be implemented through an approved common memory wrapper and SHALL NOT be coded as an ordinary array with the intent of inferring a large flip-flop bank. | A |
| KNX-RTL-MEM-002 | The threshold applies to each array and is exceeded when its depth is greater than 1,024 words or its capacity (depth multiplied by width, in bits) is greater than 32 Kib. This threshold is PROPOSED (STD-D-013): the imported draft defined 1K entries as 1,024 addressable words independent of width and asked the owner to confirm it, and the added capacity limit is a proposal. A review rule covers collections of arrays that each stay under the threshold. Counting (all evaluated after elaboration): a word is one addressable entry; depth is the product of all unpacked dimension sizes of the array; width is the packed bit width of one entry; capacity is depth multiplied by width in bits. A parameterised array is evaluated for every parameter value actually instantiated; an array inside a generate construct is counted per elaborated instance and not summed across instances; a multidimensional array counts as one array. | A |
| KNX-RTL-MEM-003 | A smaller array MAY use inferred storage, subject to synthesis, area, power, timing and design review, and MAY still be required to use a wrapper where the method requires it. | R |
| KNX-RTL-MEM-004 | A fallback flip-flop implementation of a large array, or an array outside a wrapper, requires a waiver with area, power, timing, verification and DFT impact. | A (waiver) |

### 14.2 Wrapper catalogue

The common memory library is to provide wrappers for these logical classes. The names are class identifiers in this standard and do not assert that RTL modules exist; real module names, ports and supported configurations are published in the library specification and recorded in the manifest.

| Class | Port and access model | Typical use |
|---|---|---|
| `SP_ROM` | One read port; read-only contents | Firmware, tables, constants |
| `SP_RF` | One access port; behaviour per wrapper contract | Small register banks, local storage |
| `DP_RF` | Two ports; simultaneous access defined | Multi-access register storage |
| `SP_SRAM` | One read and write port | Buffering, data storage |
| `DP_SRAM` | Two ports; supported combinations defined | Shared buffers, multi-client storage |
| `MEMORY` | Parameterised abstraction selecting one approved class; no undocumented behaviour | Common integration and technology mapping boundary |

### 14.3 Wrapper contract and mapping

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-MEM-005 | Each wrapper SHALL document memory type and port count, depth and width, address range behaviour, read latency and output registering, read-during-write and write-during-write behaviour, byte or bit write enables, clocking and port clock relationships, reset behaviour (contents are not assumed reset), initialisation or ROM loading, out-of-range output, ECC or parity, low-power controls, BIST, MBIST and repair requirements, and technology mapping and simulation model behaviour. | R |
| KNX-RTL-MEM-006 | Designers SHALL use only configurations the wrapper contract supports. | R |
| KNX-RTL-MEM-007 | IP RTL SHALL instantiate the technology-independent wrapper and SHALL NOT instantiate a foundry macro (see KNX-RTL-LIB-003). | A |
| KNX-RTL-MEM-008 | A macro SHALL NOT be substituted if its depth, width, port behaviour, latency or collision semantics differ from the wrapper contract; an unsupported configuration is reported by the flow. | T |

### 14.4 Array inventory and verification

Arrays are inventoried at design and synthesis review (array ID, location, depth, width, total bits, intended use, implementation, wrapper class or macro, review status). A source-level structural check is authoritative for whether the abstraction was used; a synthesis memory-inference report is a supporting check that shows what synthesis inferred. Using a wrapper in the source is not proof that the expected macro was mapped.

| ID | Rule | Enf. |
|---|---|---|
| KNX-RTL-MEM-009 | The array inventory SHALL identify arrays above the threshold, smaller arrays better implemented as macros, arrays synthesised to large flip-flop banks, failed inference and differences between wrapper and mapped macro. | T |
| KNX-RTL-MEM-010 | Each memory instance SHALL be verified for its configured behaviour (read and write, address boundaries, back-to-back access, collisions, dual-port access, write enables, reset and power interaction, sleep and wake, ECC or parity, initialisation, BIST and test access, as applicable). Sign-off evidence holds the wrapper configuration, RTL commit, simulation results, mapping report, selected macro and DFT or MBIST evidence. | R |

## 15. Verification and sign-off

Every IP has a verification plan that maps requirements to tests, assertions, coverage and evidence.

| Activity | Requirement | ID |
|---|---|---|
| Lint | Mandatory; clean or reviewed waivers | KNX-RTL-VER-001 |
| Functional simulation | Mandatory for functional behaviour | KNX-RTL-VER-004 |
| Assertions | For applicable protocols and safety properties | KNX-RTL-VER-005 |
| Formal | As the architecture, risk and verification plan require | KNX-RTL-VER-006 |
| Functional coverage | Model, bins, exclusions and denominator in the IP verification plan; no fixed threshold here (STD-D-005) | KNX-RTL-VER-007 |
| Code coverage | Line, expression, statement, branch (case) and toggle reported separately; proposed targets in section 20 (STD-D-004) | KNX-RTL-VER-008 |
| CDC and RDC | Where crossings exist; review-only until a tool exists | KNX-RTL-VER-009 |
| Synthesis | Synthesizability and structural review (AC-031) | KNX-RTL-VER-010 |
| STA | At the integration milestone that defines it | KNX-RTL-VER-011 |
| DFT and low-power review | Where applicable | KNX-RTL-VER-012 |

KNX-RTL-VER-013: acceptance needs every mandatory check to pass or have a formally approved disposition; no accumulated metric overrides a failed mandatory check. Enforcement for VER-004 to VER-013 is T or R.

## 16. SoC integration

Each IP provides an integration package, as applicable: approved specification and port list, register map and address needs, clock and reset requirements, CDC and RDC inventory and reports, common-library dependencies and versions, clock-gating and low-power needs, synthesis constraints and timing assumptions, interrupt and error definitions, DFT requirements, and verification results, waivers and known limitations (KNX-RTL-INT-001, R). SoC integration checks interface compatibility, clock and reset connectivity, address and interrupt allocation, power intent, library version compatibility, DFT connectivity and timing constraints (KNX-RTL-INT-002, R).

## 17. Roles

All roles named in this standard (design authority, RTL, verification, CDC and RDC, low-power and clocking, DFT, integration reviewers) are held by Dinesh as the interim arrangement. This is not independent design review or independent verification, and no approval recorded under it is to be reported as independent. A role changes by change request.

## 18. Review, waivers and change control

### 18.1 Required reviews

KNX-RTL-GOV-001: the review record shows which responsibilities were reviewed (architecture and specification, RTL implementation, verification, CDC and RDC, low-power and clocking, DFT, integration), even when one person holds several roles.

### 18.2 No silent waiver

KNX-RTL-GOV-002: no team or IP may waive a rule silently; every deviation is a waiver under section 18.3.

### 18.3 Waivers

An exception to a rule is a waiver entry in `rtl/waivers.yml`, created by the task that adds RTL (the file is not created before real RTL exists). Each entry has: rule identifier; exact file and module or instance scope; technical justification; alternatives considered; functional, verification, timing, power, CDC and RDC, DFT and portability impact; compensating controls; risk and mitigation; approver; approval or decision reference; expiry or review condition. A waiver for one IP does not apply to another, a waiver is never global, and an entry that lacks an approver, a reference or a scope fails the check (KNX-RTL-GOV-003). Interim approval by Dinesh is recorded as not independent. A waiver cannot replace an owner decision record: it cannot change a SELECTED decision, and approving a waiver is not approval of this standard.

### 18.4 Change control

KNX-RTL-GOV-004: this standard changes by change request: a pull request that edits the item with a revision-history entry. A change to a SELECTED item also needs a new decision record. A change to a mandatory rule, a threshold or a metric definition needs an impact assessment for IP in progress.

## 19. Automated compliance checks (PROPOSED)

This section describes how the A-rules are checked in CI. It is a proposal: no checker, workflow or toolchain exists yet, and tool choice and pinning belong to KOS-NEXUS-002 and KOS-NEXUS-003. A passing check is software evidence only when it records target, tool and version, configuration revision, source commit and run ID.

### 19.1 Checks, rule mapping and phases

Every A-rule (including A with warn, waiver, name, lint, flag or instance) is mapped to a check below. An A-rule that appears in no row is a defect in this standard. T and R rules are not automated: their tool output or review record is judged by the reviewer and is reported as review-only, never as a CI pass.

| Check | A-rules covered | Method | Phase |
|---|---|---|---|
| Port naming | NAM-001, 002, 005 | Parse module ports with a SystemVerilog parser (proposed: slang) and check every port | 1 |
| Clock and reset naming | NAM-006 to 011, RST-002, name part of RST-001 | Same parse; clock and reset identification as in 19.3 | 1 |
| Identifier conventions | NAM-003, 012, 013, 015, 016, 017, FIL-007, FIL-008 | Same parse: case, module and file names, parameters, packages, interfaces, one primary module per file | 1 |
| Source header and licence | DOC-001 to 004 | Check field presence, format, holder and licence identifier (Appendix A.3) | 1 |
| Maximum file lines | FIL-003 to 005 | Physical line count; warn above 1,000 and 1,500, fail above 2,000 | 1 |
| Clock edge and procedural constructs | CLK-001, COD-001, 002, 008 | Parse: no negedge or dual-edge sequential block, `always_ff` and `always_comb` use, no `force`, `release` or delay in design RTL | 1 |
| Waiver validity | GOV-003; RST-003, CLK-002, LAT-004, MEM-004, CDC-009 and the waiver clause of every LIB rule | Check required fields, scope, approver, reference and expiry (section 18.3) | 1 |
| Lint gate | VER-001 to 003, COD-003, 004, 005 | Lint and elaboration (proposed: Verilator, slang): complete assignment, multiple drivers, undriven signals, width and signedness, report tied to the commit | 2 |
| Unresolved module and black box | LIB-001, 002 | Elaboration reports unresolved modules and unapproved black boxes | 2 |
| Latch inference | LAT-001 to 003, 005 | Lint latch warnings plus a synthesised latch count (proposed: Verilator and Yosys); allow-list only the exact approved clock-gate instance | 2 |
| Common-library dependency | LIB-001 to 004, 006, RST-006, CLK-003, 004, 010, CDC-002 | Instantiated modules resolve to manifest entries; flag foundry cells, technology `ifdef` outside the technology layer, assign-based clock gates, unapproved clock structures and local FIFOs | 2 |
| Memory-wrapper usage | MEM-001, 002, 007 | Source-level array analysis is authoritative; a Yosys memory-inference report is supporting evidence | 2 |
| Use-based reset polarity, CDC and RDC analysis | use part of RST-001; CDC and reset review rules | Dedicated tool when one is available; structure detection alone is not a compliance claim | 3 |

Phase 1 needs no manifest. Phases 2 and 3 are enabled only when their toolchain exists and, for the library and memory checks, the owner has enabled the check.

### 19.2 Result states

A check reports PASS, WARN, FAIL, NOT_APPLICABLE or BLOCKED.

| Condition | Result |
|---|---|
| No RTL file exists | NOT_APPLICABLE (reason `NO_RTL_PRESENT`); no compliance claim is made, and it is never a pass |
| An enabled check cannot run: tool absent or not pinned, manifest file missing or failing its schema | BLOCKED, never PASS |
| RTL exists, the manifest is valid but has no entry for a library-class structure the RTL instantiates | FAIL of the library rule (the RTL uses an unapproved module), not BLOCKED |
| RTL exists, the manifest is valid and empty, and the RTL instantiates no library-class structure | PASS for the library rules only |
| A rule finding with a valid waiver | WARN, reported with the waiver ID |

Each finding names the rule ID, file, line and message, and each run writes a report with tool versions, source commit and run ID.

### 19.3 Identifying clocks, resets and clock structures

A checker classifies every net before applying a rule, and never decides clock or reset semantics from a name alone.

- **Clock.** A net is a clock if it is a module input port matching NAM-006, appears in an edge-sensitive event control, or is connected to the clock port or output of an approved library clock structure.
- **Clock sources.** (1) A primary clock port. (2) An approved generated clock: the output of a manifest module of category clock gate, divider or multiplexer. (3) An unapproved generated clock: any other logic output used as a clock, which fails CLK-010 unless it carries a waiver.
- **Clock as data.** A clock net used as an operand of a logic expression or assignment outside an approved library module fails CLK-004. The bodies of manifest modules are not scanned by this rule.
- **Clock muxes, dividers and generated clocks.** They must be approved library modules (CLK-010). The matching generated-clock constraints are a review item (CLK-007).
- **Approved clock-gate exception.** The latch exception of LAT-002 names the exact manifest module and the exact instance (hierarchical path); it covers no other logic in the same module.
- **Reset.** A net is a reset if it matches the reset name pattern, or appears as an asynchronous term in the event control of an `always_ff`, or is the condition of a top-level reset branch of an `always_ff` (an `if` whose branch assigns constants to the block's registers).
- **Polarity.** For a net identified as a reset: a `posedge` asynchronous term, a positive-sense reset condition, or a name without `_n` fails RST-001 or RST-002. A synchronous reset that does not match the top-level pattern is identified by name only, and its polarity in use is review-only.

### 19.4 Approved-module manifest

The approved library is listed in a versioned, machine-readable manifest. It begins as a schema with an empty module list; real module names are added only when the module exists and has been reviewed (no module name is invented here). Each entry has: module name; library category (CDC, reset synchroniser, clock gate, clock divider, clock multiplexer, FIFO, memory wrapper, isolation or level shifter, DFT); interface version; approval status; source location or commit; applicable parameters; clock and reset assumptions; verification status; permitted use. An empty valid manifest is valid; the results in 19.2 apply. A manifest-based check fails only when real RTL violates the policy, and is BLOCKED only when the manifest cannot be read or fails its schema.

### 19.5 Mandatory gate

Creating a workflow does not make it a mandatory gate. After the workflow is added (it lives in the protected `.github/workflows/` path and is added by the owner in its own pull request), the owner confirms in branch protection that the check is a required status check.

### 19.6 Checker fixtures

Each check is built with positive and negative fixtures, and the checker tests run in CI. Minimum negative fixtures: a clock port without `clk`; a clock output without `_o`; a negative-edge flop; an assign-based clock gate; a clock used as a data operand; a clock multiplexer, divider or generated clock not from a library module; an active-high reset port; a `posedge` asynchronous reset term; a reset condition in positive sense; a reset port without `_n`; an inferred latch and an approved clock-gate latch with the wrong instance; an array above the threshold outside a wrapper (including a parameterised and a generate case); a file of 1,001, 1,501 and 2,001 lines; a header with a wrong holder or licence; a waiver with no approver, no scope or an expired review condition; and the result-state cases of 19.2 (no RTL, missing manifest, valid empty manifest with and without a library-class instance).

## 20. Open methodology decisions and proposed defaults

Each decision below was OPEN in the imported draft. Per the owner's rule that nothing stays open, each now has a PROPOSED default or, where the answer depends on facts not yet known, a deciding procedure with no invented value. All are changeable by change request.

| ID | Topic | Proposed default |
|---|---|---|
| STD-D-001 | Single, dual and quad clock gating | The classes are not defined in the source and are not guessed here. The owner defines them before the first clock-gating report. Until then the 99%, 80% and above 60% figures are provisional planning numbers, the classes are independent metrics that are not added together, and each metric is reported as numerator and denominator only. |
| STD-D-002 | Clock-gating denominator | The eligible population is the sequential elements of synthesizable design RTL measured at mapped synthesis. Exclusions are listed in a reviewed register (Appendix C) approved by the owner. |
| STD-D-003 | RTL complexity weight | Not applicable to Nexus: Nexus tasks carry no weight or credit (annex D). Not defined here. |
| STD-D-004 | Statement and case coverage | Code coverage is reported, not credited. The metrics line, expression, statement, branch (case) and toggle are reported separately. Proposed targets carried from the draft: line 90%, expression 60%, statement 90%, branch 90%, toggle 90%; statement and branch each meet 90% separately. Targets are verification goals, not pass criteria, until the owner selects them. |
| STD-D-005 | Functional coverage | The coverage model, bins, exclusions and denominator are stated in each IP verification plan and reviewed; no fixed threshold is set here. |
| STD-D-006 | CDC coverage | The denominator is the crossings in the reviewed CDC inventory and every crossing is classified. Closure means no unresolved or unwaived violation; a percentage is reported but is not the pass criterion. |
| STD-D-007 | DFT-friendly assessment | The checklist is written by a later DFT task. Until then DFT items are review-only and unscored. |
| STD-D-008 | Common RTL library | The library lives in this repository when the first library task starts. The manifest (section 19.4) is the catalogue, versioned by Git commit, owned by Dinesh; its module list is empty until real modules exist. |
| STD-D-009 | Tool baseline | Open-source tools as in the architecture (lint, Yosys, simulation); versions are pinned by KOS-NEXUS-002 and KOS-NEXUS-003. CDC, RDC and DFT tool availability is unverified; those checks are review-only until a tool is confirmed. |
| STD-D-010 | Approval authority | Dinesh holds every role (interim, not independent), section 17. |
| STD-D-011 | Reset and clock exceptions | Approved by Dinesh through a waiver (section 18.3) with the evidence listed in RST-003 and CLK-002. |
| STD-D-012 | Common FIFO catalogue | FIFO modules are manifest entries added when the FIFO library task delivers them; none is named here. |
| STD-D-013 | Memory wrapper threshold | Per array: depth above 1,024 words or capacity above 32 Kib (MEM-002). |

A numeric target used before its decision is selected is reported as provisional, not as final compliance.

## 21. IP RTL compliance checklist

- [ ] Specification exists and the RTL follows the file and module structure (FIL).
- [ ] Ports use `_i`, `_o` and `_io`; clock ports contain `clk`; internal signals have no direction suffix (NAM).
- [ ] Each source file has the Appendix A header with the Kritva Robotics copyright and Apache-2.0 identifier (DOC).
- [ ] No file exceeds 2,000 lines; files above 1,000 and 1,500 lines have a recorded review (FIL).
- [ ] Coding rules and reset strategy are followed; resets are active-low and sequential logic uses the positive edge, or a waiver exists (COD, RST, CLK).
- [ ] FIFOs, CDC, reset synchronisers, clock gates and memory wrappers come from the approved library; no foundry cell is instantiated (LIB).
- [ ] CDC and RDC crossings are inventoried and use approved structures (CDC).
- [ ] Low-power opportunities and clock-gating plan are documented (CLK, section 11).
- [ ] Lint is clean or every waiver is approved (VER).
- [ ] No unapproved latch exists (LAT).
- [ ] Arrays above the threshold use an approved wrapper or have a waiver; memory configuration and mapping are verified (MEM).
- [ ] Verification and coverage evidence is accepted and each code-coverage metric is reported separately (VER).
- [ ] The integration package is complete (INT).
- [ ] The review record shows which responsibilities were reviewed (GOV).

## 22. Approval

| Role | Name | Decision | Date | Evidence / Record |
|---|---|---|---|---|
| Owner and approver of the standard | Dinesh (interim, not independent) | SELECTED (all rules; section 19 and section 20 items PROPOSED) | 2026-11-10 | [NX-DEC-023](../decisions/NX-DEC-023.md) |

The other reviewer roles of the imported draft are held by the same person (section 17); no separate entry is made for them, so the table does not suggest independent approval.

## Appendix A: Mandatory RTL source-file header

### A.1 Applicability

The header is mandatory for every Kritva Nexus Verilog or SystemVerilog design source file (`.v`, `.sv` and design include files where applicable). It appears at the start of the file, before any package, interface or module, and counts toward the line limits.

### A.2 Template

```systemverilog
//==============================================================================
// Copyright (c) <YEAR> Kritva Robotics
// SPDX-License-Identifier: Apache-2.0
//
// Project       : Kritva Nexus
// IP / Feature  : <IP_OR_FEATURE_NAME>
// Subsystem     : <SUBSYSTEM_NAME>
// Module        : <MODULE_NAME>
// File          : <FILE_NAME>
//
// Description   : <CONCISE_FUNCTIONAL_DESCRIPTION>
//
// Specification : <SPEC_DOCUMENT_ID_AND_VERSION>
// RTL Standard  : KNX-RTL-STD-001
//
// Author        : <NAME_OR_TEAM>
// Owner         : <RESPONSIBLE_OWNER>
// Reviewer      : <REVIEWER_OR_TBD>
//
// Created       : YYYY-MM-DD
// Last Modified : YYYY-MM-DD
// Version       : MAJOR.MINOR.PATCH
//
// Dependencies  : <COMMON_LIBRARY_MODULES_OR_PACKAGES>
// Clock(s)      : <CLOCK_DOMAIN_NAMES_OR_NONE>
// Reset(s)      : <ACTIVE_LOW_RESET_NAMES_OR_NONE>
//
// Parameters    : <KEY_CONFIGURATION_PARAMETERS_OR_NONE>
// Notes         : <IMPORTANT_ASSUMPTIONS_OR_NONE>
//
// Change History:
// Date         Version       Author/Owner       Description
// YYYY-MM-DD   0.1.0         <NAME/TEAM>        Initial implementation
//
// Design Rules (summary; the standard is authoritative):
// - Ports use _i, _o and _io; internal signals carry no direction suffix.
// - Clock ports contain clk; resets are active-low; sequential logic is
//   positive-edge unless a waiver exists.
// - CDC, FIFO, clock-gate and memory structures use approved library modules.
// - Latches and arrays above the threshold need approval or an approved wrapper.
// - Maximum file length: 2,000 physical lines, including this header.
//==============================================================================
```

### A.3 Field rules

| Field | Requirement | Checked by CI |
|---|---|---|
| Copyright, SPDX identifier | `Copyright (c) <YEAR> Kritva Robotics` and `SPDX-License-Identifier: Apache-2.0`; the year is the year of creation | Yes, format and values |
| Project | `Kritva Nexus` | Yes |
| IP / Feature | Matches the registered IP or feature name | Presence only |
| Subsystem | Parent subsystem; `N/A` only where appropriate | Presence only |
| Module, File | Match the primary module and the file name | Yes |
| Description | Brief statement of the responsibility | Presence only |
| Specification | Governing specification and version | Format only; the content is reviewed |
| RTL Standard | `KNX-RTL-STD-001` | Yes |
| Author, Owner, Reviewer | Person or team; Reviewer may be `TBD` in development | Presence only |
| Created, Last Modified | ISO date | Format only |
| Version | MAJOR.MINOR.PATCH | Format only |
| Dependencies, Clock(s), Reset(s), Parameters, Notes | As described, or `NONE` | Presence only |
| Change History | Meaningful changes; Git is authoritative | Presence only |

A header for a package or interface names it in the `Module` field (or an explicitly labelled `Design Unit` field used consistently). Specification and standard references are updated when the governing document version changes under its migration policy. An approved deviation from the header format is a waiver.

## Appendix B: Port naming example and CDC inventory format

```systemverilog
module knx_example_ip (
    input  logic        clk_core_i,
    input  logic        rst_core_n_i,
    input  logic        req_valid_i,
    output logic        req_ready_o,
    input  logic [31:0] req_data_i,
    output logic [31:0] rsp_data_o,
    output logic        rsp_valid_o,
    inout  wire         gpio_io
);

    logic        transfer_active;
    logic [31:0] data_reg;

endmodule
```

The example shows naming only and is not a functional implementation.

CDC inventory columns: CDC ID, source domain, destination domain, signal or bus, crossing type, common module, tool result or waiver.

## Appendix C: Clock-gating registers

Opportunity register columns: gate group, clock domain, sequential elements, class (per the definition selected under STD-D-001), enable condition, eligible count, gated count, coverage, exclusion reason.

Metric record fields: IP or feature, clock domain, gate class and its approved definition, eligible and gated elements, excluded elements and exclusion approvals, coverage percentage, synthesis or mapping report, reviewer.

## Appendix D: Informative annex, complexity weight and credit model (not applicable to Nexus)

The imported draft contained a complexity weight and engineering credit model (a weight `W` per IP and up to 12W of credit across RTL implementation, functional verification, code coverage, CDC and DFT). That model does not apply to Kritva Nexus. Nexus tasks carry no weight, percentage credit or programme credit, Nexus is not registered in kritva-program, and weights belong to kritva-program. This annex is kept for historical or future programme reference only. It assigns no weights to rules or tasks, calculates no progress percentage, defines no Nexus task credit, implies no V2 mapping and does not override the repository's task and milestone rules. Any future programme-level tracking needs a separate approval and is not inferred from this standard. The coverage targets that the model used are carried as proposed verification targets in section 20 (STD-D-004), without credit.
