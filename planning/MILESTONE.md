# Milestones: kritva-nexus

Source: this repository (`planning/MILESTONE.md`, hand-maintained). Nexus is outside the Kritva Program V2 plan and is planned for the V3 plan; it is not registered in kritva-program and its milestones are not program milestones. Dates are not set. A milestone closes only through an approved COMPLETION_RECORD.md. Owner and reviewer: Dinesh (interim, not independent). Execution state is in [MILESTONE_STATUS.md](MILESTONE_STATUS.md); tasks are in [TASKS.md](TASKS.md); criteria are in [../ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md).

## Purpose

This document defines the proposed repository milestones for Kritva Nexus, their outcomes and testable exit conditions, and records the risks, architecture gaps, external IP dependencies, blockers and owner decisions that affect them. It is a planning record. Nexus is outside the V2 plan and is not registered in kritva-program, so nothing here is a baseline commitment, carries a weight, or earns credit.

## 1. Rules for these milestones

- **Names.** Repository milestones are `NX-M0` to `NX-M8`. They are local identifiers and are not program milestone IDs.
- **Program mapping.** Every milestone has `Program milestone mapping: Not mapped`. No mapping is inferred from similar names or order. In particular, `NX-M6` is not assumed to map to the program milestone V2-M6, which is on HOLD. A mapping, if any, is decided for the V3 plan when it exists; none is made now.
- **Status.** Every milestone is `PROPOSED`. Execution state is reported in [MILESTONE_STATUS.md](MILESTONE_STATUS.md), where every milestone is currently `NOT_STARTED`.
- **No dates.** No target date exists, and none is implied by the order of milestones.
- **No dependency fields.** Repository milestones carry no `depends_on` field. Each milestone gives its prerequisites in prose, in one sentence format that creates no program dependency.
- **Tasks.** A milestone lists only registered Stage 1 tasks from `TASKS.md`. Catalogue candidates are not listed against a milestone, even where they are expected to contribute later. A milestone with no registered task says so.
- **Named exit-condition groups.** Where a milestone holds a recognisable sub-goal (simulator foundation, FPGA foundation, prototype), it is a named group of exit conditions inside that milestone. It is not a separate milestone ID.
- **Closure.** A milestone closes only through an approved `COMPLETION_RECORD.md`. All tasks being marked complete, a merge, a passing run or a tag does not close a milestone.
- **Evidence for every exit condition.** Each exit condition is testable, is linked to acceptance criteria in `ACCEPTANCE_CRITERIA.md` where they exist, and is supported by identifiable evidence stating: target (`RTL`, `simulator`, `FPGA` or `ASIC`), tool name and version, configuration revision, source commit, CI run or report reference, and result with review disposition.

### 1.1 Wording of results

A result is described only with wording its evidence supports. The word "validated" is not used without saying what was validated.

| Evidence | Wording |
|---|---|
| Renode test passes | Simulator functional test passed |
| Verilator co-simulation passes | RTL and platform co-simulation passed |
| FPGA synthesis completes | FPGA implementation flow completed |
| FPGA bitstream generated | Bitstream generation completed |
| FPGA programmed and tested on a board | FPGA hardware test passed |
| Actual board test with measurements | Hardware behaviour demonstrated under the tested conditions |
| Yosys or OpenLane run | Tool flow completed (software evidence; no silicon or board claim) |

A simulator result never establishes physical hardware validation, and an OpenLane run never implies a successful silicon implementation.

## 2. Milestone summary

| ID | Name | Program milestone mapping | Status | Registered Stage 1 tasks |
|---|---|---|---|---|
| NX-M0 | Repository and engineering foundation | Not mapped | PROPOSED | KOS-NEXUS-001 |
| NX-M1 | Architecture baseline | Not mapped | PROPOSED | KOS-NEXUS-006, KOS-NEXUS-007, KOS-NEXUS-008, KOS-NEXUS-084 |
| NX-M2 | IP and subsystem specifications | Not mapped | PROPOSED | KOS-NEXUS-018, KOS-NEXUS-019 |
| NX-M3 | RTL foundation | Not mapped | PROPOSED | None registered |
| NX-M4 | Subsystem implementation | Not mapped | PROPOSED | None registered |
| NX-M5 | Subsystem verification | Not mapped | PROPOSED | None registered |
| NX-M6 | Block-level physical design | Not mapped | PROPOSED | None registered |
| NX-M7 | SoC integration and prototype | Not mapped | PROPOSED | None registered |
| NX-M8 | Engineering release baseline | Not mapped | PROPOSED | None registered |

Stage 1 defines the Nexus planning baseline. It does not authorise implementation of the complete SoC.

## 3. Milestone definitions

### NX-M0 Repository and engineering foundation

**Outcome.** The repository, governance files, toolchain strategy and CI conventions are established, with a reproducible initial RTL and tool flow.
**Workstreams involved.** INFRA, FPGA (tool environment only).
**Registered Stage 1 tasks.** KOS-NEXUS-001.
**Prerequisites.** Owner review of the Nexus planning proposal. These are descriptive execution prerequisites and do not create additional program dependency relationships.

| Exit condition | Criteria |
|---|---|
| The files required by the V2 Acceptance Standard (the common-file set of kritva-sense) exist, with no empty folder and no placeholder task | AC-001, AC-002 |
| The eight common make targets exist; each target not yet implemented exits 3 and none prints a pass | Section 5 of the criteria |
| The secret-scan and commit-message-check workflows run and pass on the closing commit | AC-004, AC-005 |
| Tool versions for Icarus, Verilator, Yosys and OpenLane are pinned and recorded, and a smoke example for each runs from a clean checkout, or the blocker is recorded with its reason | AC-031, AC-050 |
| The FPGA toolchain setup is documented as reproducible without choosing a board; the Renode environment is documented | AC-060 (tool setup part) |
| The status-reporting path is documented; no `status/status.json` exists while Nexus is outside the V2 plan | Section 10 of the criteria |
| An approved `COMPLETION_RECORD.md` exists | Milestone closure rule |

### NX-M1 Architecture baseline

**Outcome.** The system architecture, requirements and interfaces are documented, with every decision labelled and every open item registered.
**Workstreams involved.** ARCH, RTL (coding conventions only).
**Registered Stage 1 tasks.** KOS-NEXUS-006, KOS-NEXUS-007, KOS-NEXUS-008, KOS-NEXUS-084.
**Prerequisites.** Owner approval of the architecture work and the four A0 gaps (section 5) accepted as the open-issue register. These are descriptive execution prerequisites and do not create additional program dependency relationships.

| Exit condition | Criteria |
|---|---|
| Architecture documents cover the CPU subsystem, memory, ISP and NPU, display, Ethernet, security, peripherals, AXI and APB interconnect, address maps, clock, reset, power and interrupt, CDC and RDC, RTL partitioning, and the simulator and FPGA-prototype architecture | AC-010, AC-012 |
| Every decision is SELECTED, PROPOSED or OPEN, and none is SELECTED without a recorded owner decision | AC-010 |
| The requirements register and decision records exist, with traceability to architecture and a verification method | AC-011 |
| The application and secure address spaces are documented as separate spaces | AC-013 |
| The CPU-to-APB path, the application address width and the memory-access port architecture are resolved, or each is left OPEN with an owner | AC-014, AC-015, AC-016 |
| The architecture review is recorded and the owner has approved it; the architecture is not described as frozen before the documents are reconciled and reviewed | AC-007, AC-010 |
| An approved `COMPLETION_RECORD.md` exists | Milestone closure rule |

### NX-M2 IP and subsystem specifications

**Outcome.** The IP inventory, availability and licensing assessment, interface contracts and integration assumptions are defined, so that implementation scope is realistic.
**Workstreams involved.** IP, ARCH, FPGA (board evaluation and selection).
**Registered Stage 1 tasks.** KOS-NEXUS-018, KOS-NEXUS-019.
**Prerequisites.** The NX-M1 architecture outcome, or owner direction to proceed in parallel. These are descriptive execution prerequisites and do not create additional program dependency relationships.

| Exit condition | Criteria |
|---|---|
| Every IP block has a record of source, ownership, licence, availability and integration status, classified as developed here, integrated or placeholder | AC-020 |
| Substitute IP planned for validation is named as a substitute | AC-021 |
| Interface specifications, clock and reset interface definitions, register-map specifications, DMA and memory interface definitions, and integration and verification assumptions are written for every in-scope block | AC-012, AC-034 |
| The FPGA prototyping board is chosen by an owner decision, or the choice is recorded as open with the reasons | Owner decision |
| An approved `COMPLETION_RECORD.md` exists | Milestone closure rule |

### NX-M3 RTL foundation

**Outcome.** Common RTL infrastructure and first synthesizable blocks exist, with a simulator foundation, CDC infrastructure and the methodologies the later milestones use.
**Workstreams involved.** RTL, VERIF, SIM, FPGA, PD.
**Registered Stage 1 tasks.** None registered.
**Prerequisites.** NX-M1 architecture decisions for the blocks concerned and the NX-M0 tool environments. These are descriptive execution prerequisites and do not create additional program dependency relationships.

| Exit condition | Criteria |
|---|---|
| Common RTL, reset and clock-domain-crossing conventions, AXI and APB infrastructure, basic register blocks and interrupt and timer foundations pass Verilator lint and Yosys synthesis checks | AC-030, AC-031 |
| The CDC synchronizer, asynchronous FIFO and reset-synchronization libraries pass their tests, including overflow, underflow and reset-release behaviour | AC-082, AC-083, AC-084 |
| Functional RTL and technology-specific mapping are kept in separate layers | AC-032 |
| Icarus smoke tests and the Verilator regression pass for the declared subset | AC-050, AC-051 |
| Block-level synthesis and OpenLane methodologies are written, and the verification frameworks and the assertion, coverage, CDC and RDC strategies exist | AC-070 (methodology part), AC-043 |

**Named exit-condition group: simulator foundation.**

| Exit condition | Criteria |
|---|---|
| The Renode platform description, CPU and memory configuration, address map and interrupt model match the approved address map | AC-052, AC-053 |
| The first firmware boot reaches a defined checkpoint and a UART functional model passes its test | AC-054, AC-055 |
| One Verilated peripheral is connected to Renode through co-simulation and passes the same test as its functional model | AC-056 |
| Simulator tests run automatically and report pass or fail | AC-057 |

### NX-M4 Subsystem implementation

**Outcome.** The major subsystem RTL is implemented, and selected blocks run in the simulator and on the FPGA.
**Workstreams involved.** RTL, SIM, FPGA, IP.
**Registered Stage 1 tasks.** None registered.
**Prerequisites.** NX-M3 foundations, NX-M2 IP decisions for the blocks concerned, and the FPGA board decision for the FPGA group. These are descriptive execution prerequisites and do not create additional program dependency relationships.

Suggested implementation order (a proposal, not a commitment that every block is built from scratch): system control, reset and interrupt infrastructure; AXI and APB interconnect and system memory interfaces; security management; peripherals; Ethernet and storage; display; camera and ISP; NPU integration; CPU subsystem integration.

| Exit condition | Criteria |
|---|---|
| Each implemented subsystem passes the eight subsystem gates | Section 9.1 of the criteria |
| Subsystem tests pass, and each significant module has a recorded purpose, interface, clock domain, reset domain and verification boundary | AC-040, AC-041, AC-033 |
| Selected RTL blocks are available to the simulator and the FPGA flows, and selected RTL peripherals are connected to Renode | AC-056 |

**Named exit-condition group: FPGA foundation.**

| Exit condition | Criteria |
|---|---|
| A board is selected, the toolchain is installed and a minimal FPGA project with clock and reset builds | AC-060, AC-061 |
| The bitstream is programmed and the UART, GPIO and timer tests are run on the board, with the results recorded | AC-062 |

### NX-M5 Subsystem verification

**Outcome.** Verification of the implemented subsystems is closed against requirements, with correlated RTL and software-visible tests.
**Workstreams involved.** VERIF, SIM, FPGA, RTL.
**Registered Stage 1 tasks.** None registered.
**Prerequisites.** NX-M4 implementations for the subsystems concerned. These are descriptive execution prerequisites and do not create additional program dependency relationships.

| Exit condition | Criteria |
|---|---|
| Unit and subsystem regressions, interface protocol checks, reset and interrupt tests, DMA and memory-access tests and security-isolation tests pass | AC-040, AC-041, AC-042 |
| CDC and RDC analysis is reviewed with no unexplained critical violation | AC-080, AC-081, AC-082, AC-085 |
| Every mandatory requirement maps to a test or an approved disposition; coverage evidence is reviewed and each gap recorded | AC-043 |
| RTL, simulator and FPGA tests share functional test definitions where more than one environment exists, and differences are recorded | AC-044 |
| Firmware simulation and automated simulator regression run reproducibly | AC-057 |

### NX-M6 Block-level physical design

**Outcome.** Selected RTL blocks are synthesized and taken through the OpenLane flow, with reviewed reports.
**Workstreams involved.** PD, RTL.
**Registered Stage 1 tasks.** None registered.
**Prerequisites.** NX-M3 methodologies and a block with reviewed RTL. These are descriptive execution prerequisites and do not create additional program dependency relationships.

Physical-design execution is judged for each selected block on its own. A block stays blocked where required technology collateral, memory macro models or implementation prerequisites are unavailable, and a generic flow result is not substituted for a valid block-level result.

| Exit condition | Criteria |
|---|---|
| For each selected block, availability of technology collateral, macro models and constraints is confirmed, or the block is recorded as blocked | AC-070 |
| The configured OpenLane flow completes with the required synthesis, floorplan, placement, clock-tree, routing, timing, area and physical-check reports | AC-071 |
| Every critical timing, DRC or LVS failure is fixed or has a structured waiver, and none is reported as a pass | AC-072 |
| Clock-tree and reset implementation and technology mapping are reviewed for each block | AC-073 |
| Reports state the ASIC target, flow configuration and tool version | AC-074 |

### NX-M7 SoC integration and prototype

**Outcome.** The subsystems are integrated at top level, and a reduced Nexus prototype runs in the simulator and on an FPGA.
**Workstreams involved.** INTEGRATION, FPGA, SIM, VERIF.
**Registered Stage 1 tasks.** None registered.
**Prerequisites.** NX-M4 implementations and NX-M5 verification for the blocks concerned, and the resolution of the A0 gaps affecting integration. These are descriptive execution prerequisites and do not create additional program dependency relationships.

| Exit condition | Criteria |
|---|---|
| Top-level RTL is integrated, with address decode, clock and reset, and interrupt integration checked | AC-013, AC-014, AC-015, AC-016 |
| AXI and APB connectivity, memory access and the subsystem integration regression pass | AC-041, AC-042 |
| Integration-level synthesis checks complete | AC-031 |

**Named exit-condition group: Nexus prototype.**

| Exit condition | Criteria |
|---|---|
| A CPU and memory subsystem, the AXI and APB subsystem and boot firmware are integrated on the FPGA, with any substitute CPU named as a substitute | AC-060, AC-063 |
| Interrupt handling and selected DMA and peripheral functions run, with software execution and hardware test results recorded | AC-062 |
| Results are worded as in section 1.1 and not as validation of the selected CPU or of the ASIC | AC-058, AC-063 |

### NX-M8 Engineering release baseline

**Outcome.** The architecture, RTL, verification, simulator, FPGA and physical-design evidence is consolidated into a versioned baseline.
**Workstreams involved.** RELEASE, all others.
**Registered Stage 1 tasks.** None registered.
**Prerequisites.** The earlier milestones that the release covers. These are descriptive execution prerequisites and do not create additional program dependency relationships.

| Exit condition | Criteria |
|---|---|
| Versioned architecture and RTL baselines exist, with a regression summary, a synthesis summary, a physical-design summary, known limitations and open issues, and release notes | Section 11 of the criteria |
| All evidence links to exact commits and CI runs | Section 10 of the criteria |
| An annotated SemVer tag is created only after the approved merge and passing checks, and an approved `COMPLETION_RECORD.md` names it | Tag policy; milestone closure rule |

## 4. Risks

Risks are conditions that may harm the plan. They are not architecture gaps (section 5) and not prerequisites. All are OPEN.

| ID | Topic | Current position | Required action |
|---|---|---|---|
| NX-R01 | Program scope | Nexus is outside the V2 plan and is planned for the V3 plan | Record the V3 scope and registration when the V3 plan exists |
| NX-R02 | CPU RTL availability | Architecture direction selected; usable RTL package, licence and integration form not established | Confirm source, licence and integration package |
| NX-R03 | DDR4 controller and PHY | DDR4 selected architecturally | Establish the controller and PHY IP strategy |
| NX-R04 | NPU implementation | A four-cluster direction exists | Define the RTL and IP implementation strategy |
| NX-R05 | ISP implementation | A functional direction exists | Define internal versus external IP boundaries |
| NX-R06 | OpenLane applicability | Proposed for block-level physical design | Validate technology collateral and macro requirements |
| NX-R07 | Verification capability | Icarus and Verilator are the initial tools | Establish the supported language and assertion subset |
| NX-R08 | Timing closure | Frequency targets exist but are not physically demonstrated | Establish block constraints and the timing methodology |
| NX-R09 | External IP integration | Several subsystems may depend on external IP | Establish the IP inventory and integration models |
| NX-R10 | Full-SoC physical design | Not established | Defer until block-level feasibility is shown |

## 5. Architecture gaps in the A0 draft

These gaps come from review of the A0 integration draft. Each stays OPEN until it is resolved in the architecture documents, which are owned by KOS-NEXUS-006, 007 and 008.

| ID | Issue | Required resolution | Status |
|---|---|---|---|
| NX-ARCH-GAP-001 | The application CPU's access to APB peripherals is not defined end to end | Define the full path from the CPU master through the AXI fabrics and a bridge to APB-0 and APB-1. A path through AXI-0, an AXI routing and bridge stage and an AXI-to-APB bridge is proposed for review, not approved | OPEN |
| NX-ARCH-GAP-002 | The secure 32-bit and application address maps overlap numerically | State that they are separate address spaces on isolated interconnects, with independent decode and access control and no application access to secure ROM, SRAM, eFuse, crypto or security-control registers | OPEN |
| NX-ARCH-GAP-003 | The 40-bit application address width is unconfirmed | Confirm the configured CPU address width and reconcile it with the 40-bit proposal | OPEN |
| NX-ARCH-GAP-004 | The number of memory-access ports into the DDR4 controller is open | Define memory-access-layer to DDR4 connectivity and controller ingress requirements, separating fabric ingress connections, controller ports, internal scheduling and the physical interface | OPEN |

## 6. External IP and platform dependencies

| Dependency | Needed by | State |
|---|---|---|
| Application CPU RTL (Xuantie C910 direction), including FPGA suitability | NX-M2, NX-M4, NX-M7 | UNVERIFIED |
| DDR4 controller and PHY | NX-M2, NX-M4 | UNVERIFIED |
| NPU and ISP implementation | NX-M2, NX-M4 | UNVERIFIED |
| Technology collateral and macro models for OpenLane | NX-M6 | UNVERIFIED |
| FPGA prototyping board and toolchain | NX-M2, NX-M4, NX-M7 | Not selected |
| Renode and Verilator co-simulation support for the interfaces used (AXI4, AXI4-Lite, APB3) | NX-M3 | UNVERIFIED |

## 7. Known blockers

- Nexus is outside the V2 plan (planned for V3), so no task is baselined and no central status source exists.
- External IP availability and licences are unverified.
- The FPGA board is not selected.
- Technology collateral for physical design is unverified.
- The CPU address width and the four A0 gaps are open.
- The make targets, workflows and commit checker do not exist yet.

## 8. Outstanding owner decisions

| # | Decision | Needed for |
|---|---|---|
| 1 | Decided: Nexus is not registered in V2 and goes into the V3 plan; registration details are for the V3 plan | Task baselining, status reporting and credit in V3 |
| 2 | Accept the Stage 1 candidates, including the new KOS-NEXUS-084 | Starting any task |
| 3 | Approve the milestone set, or record changes; any program mapping is a V3 decision | V3 registration |
| 4 | Visibility class of the repository, and the verified GitHub setting | README metadata |
| 5 | Decided: Dinesh holds every owner and reviewer role (interim, not independent) | Reviews and approvals |
| 6 | Adopt the Kritva commit standard formally for this repository, and set the required checks | Commit-format enforcement |
| 7 | Reporting route for security issues, and the content of `SECURITY.md` | Release of the repository |
| 8 | Whether OpenLane signoff-style reports may ever count as physical evidence | Evidence classification |
| 9 | Pin the kritva-program standards commit that this repository follows | Normative dependencies |
| 10 | Select the FPGA board, and confirm CPU and DDR4 IP availability for it | NX-M2 onwards |

## 9. Change control

Milestone definitions change only through a pull request approved by the owner (Dinesh). A milestone is not renumbered or reused. Changes are recorded in `planning/CHANGELOG.md`.
