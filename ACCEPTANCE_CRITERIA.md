# Acceptance Criteria: kritva-nexus

Standard: kritva-program `v2/planning/ACCEPTANCE_STANDARD.md` (commit not pinned, UNVERIFIED). Nexus is outside the Kritva Program V2 plan and is planned for the V3 plan; it is not registered in kritva-program, so nothing here is a baseline commitment, carries a weight or earns credit. This document is PROPOSED (not approved). Owner and reviewer: Dinesh (interim, not independent). Where a criterion cannot be tested yet, it is listed in section 12, not invented. Related: [README.md](README.md), [AGENTS.md](AGENTS.md), [planning/TASKS.md](planning/TASKS.md).

## 1. Purpose and Scope

**Owns:** acceptance conditions for Nexus architecture documents, requirements, IP assessments, RTL, technology-mapping wrappers, verification, the Kritva Nexus Simulator (Renode and Verilator co-simulation), FPGA prototypes, block-level synthesis and OpenLane physical design, SoC integration and the engineering release baseline.

**Does not own:** the program baseline, task weights, approvals, accepted progress or consolidated status (kritva-program); production signoff, silicon validation or manufacturing readiness; the licences or availability of third-party IP, which are recorded here but decided elsewhere.

## 2. Normative Dependencies

| Dependency | Version or commit | State |
|---|---|---|
| kritva-program `v2/planning/ACCEPTANCE_STANDARD.md` (task definition of done, milestone closure, test gates, commit format, tags, required files, status contract) | Commit not pinned | UNVERIFIED pin; to be recorded when the standards commit is pinned (owner decision 9) |
| kritva-program `schema/status.schema.json`, schema 2.0 | Commit not pinned | UNVERIFIED pin |
| kritva-program document header and README standards | Commit not pinned | UNVERIFIED pin |
| kritva-program registration and task baseline | Not applicable | Not registered: Nexus is planned for the V3 plan |

Where this document and the pinned standard differ, the standard wins and this document is corrected.

## 3. Acceptance Criteria

Criterion IDs are permanent. "Verified by" names the check that decides the criterion; a check that does not exist yet is shown in the state column.

### 3.1 Governance and repository

| ID | Criterion (testable) | Verified by | State |
|---|---|---|---|
| AC-001 | The repository contains the files required by ACCEPTANCE_STANDARD section 7: `ACCEPTANCE_CRITERIA.md`; `planning/` with TASKS, MILESTONE, MILESTONE_STATUS, REVIEW_CHECKLIST, GIT_COMMIT_STEP and CHANGELOG, and one `tasks/<ID>/TASK.md` per registered task; `AGENTS.md`, `SECURITY.md`, `CONTRIBUTING.md`, `LICENSE`, `Makefile`; `.github/CODEOWNERS`; `.github/workflows/secret-scan.yml` and `commit-message-check.yml` | `make check` | `make check` NOT_IMPLEMENTED |
| AC-002 | No empty directory and no placeholder task exists. Every directory holds baselined work, and every task in `planning/TASKS.md` has a stable ID and a defined deliverable | `make check`, review | NOT_IMPLEMENTED |
| AC-003 | Every proposed task is marked PLANNING_ONLY or NOT_STARTED, carries no weight and no credit statement, and is not reported as active until the owner starts it | Review | Review only |
| AC-004 | Every commit in a pull request follows `type(scope): summary` with exactly one `Task:` or `Tasks:` footer, uses only IDs from the task record or `Tasks: None (reason)` on docs and chore commits, and carries no AI-session trailer | `python3 scripts/security/check_commit_format.py` once adopted | Not adopted |
| AC-005 | The secret-scan workflow passes on the closing commit and no allowlist entry was added without an owner decision | `secret-scan` workflow | Workflow not present |
| AC-006 | `README.md` passes the kritva-program README check and a manual review against the README review checklist; the README contains no task counts, percentages or gate states | README check, review | Check script not vendored |
| AC-007 | Every detailed human-maintained Markdown document carries the Kritva document header, and no document is marked APPROVED without the approval the program records | Review | Review only |

### 3.2 Architecture and requirements

| ID | Criterion (testable) | Verified by | State |
|---|---|---|---|
| AC-010 | Every architecture decision is labelled SELECTED, PROPOSED or OPEN, and no decision is SELECTED without a recorded owner decision | Review | Review only |
| AC-011 | Every requirement has a stable ID and is traced to an architecture element and to a verification method or an approved disposition | Review of the requirements register | Register not defined |
| AC-012 | Every interface and assumption between subsystems is documented, and unresolved items are listed in an architecture open-issues register with an owner and a status | Review | Register not defined |
| AC-013 | The application and secure address spaces are documented as separate address spaces, with independent decode and access control, and no overlap is presented as a conflict or hidden | Review | Open item NX-ARCH-GAP-002 |
| AC-014 | The path from the application CPU to the APB peripherals is defined end to end, including bridge placement | Review | Open item NX-ARCH-GAP-001 |
| AC-015 | The application address width is confirmed against the configured CPU and all DMA masters before the address map is marked SELECTED | Review | Open item NX-ARCH-GAP-003 |
| AC-016 | The number and width of memory-access ports into the DDR4 controller are derived from documented bandwidth requirements | Review, analysis | Open item NX-ARCH-GAP-004 |

### 3.3 IP management

| ID | Criterion (testable) | Verified by | State |
|---|---|---|---|
| AC-020 | Every external or internal IP block has a record of source, ownership, licence, availability and integration status, and is classified as developed here, integrated, or placeholder only | Review of the IP register | Register not defined |
| AC-021 | Any substitute IP used for validation (for example a different RISC-V core on FPGA) is labelled as a substitute and is never reported as validation of the selected IP | Review | Review only |

### 3.4 RTL

| ID | Criterion (testable) | Verified by | State |
|---|---|---|---|
| AC-030 | RTL is synthesizable and passes Verilator lint with zero unexplained errors and zero unexplained warnings; each justified warning has a recorded reason | `make lint` | NOT_IMPLEMENTED |
| AC-031 | Yosys synthesis completes with no unintended latch, no unresolved module and no unexplained warning | Synthesis run | NOT_IMPLEMENTED |
| AC-032 | Functional RTL contains no technology-specific cell instance; technology-specific mapping is confined to separate wrapper layers | Review, structural check | Check not defined |
| AC-033 | Every significant RTL module has a recorded purpose, interface, clock domain, reset domain and verification boundary; module-size guidelines are applied and each exceedance has a recorded review | Review | Guidelines not defined |
| AC-034 | A register map is defined separately from its implementation, and the implementation matches it | Review, test | Not defined |

### 3.5 Verification

| ID | Criterion (testable) | Verified by | State |
|---|---|---|---|
| AC-040 | Directed tests pass, include negative cases, and are reproducible from a clean checkout | `make test-unit` | NOT_IMPLEMENTED |
| AC-041 | Subsystem and integration tests pass with the same test list on every run | `make test-integration` | NOT_IMPLEMENTED |
| AC-042 | The regression suite passes unchanged before and after any change to a public interface; a fixed defect adds a regression test | `make test-regression` | NOT_IMPLEMENTED |
| AC-043 | Every mandatory requirement maps to a test or to an explicitly approved verification disposition; assertion and coverage evidence is reviewed and each unresolved coverage gap is recorded | Review of traceability | Not defined |
| AC-044 | Where the same behaviour is checked in RTL simulation, the Kritva Nexus Simulator and on FPGA, the three checks share one functional test definition and a disagreement is investigated and recorded | Review | Not applicable until more than one environment exists |

## 4. Interface and API Compatibility

- Interface changes (ports, protocol options, register maps, address maps, interrupt allocations) are versioned and recorded in the changelog.
- A breaking interface change needs a MAJOR version, a changelog entry and an approved decision.
- Units, widths, reset values and byte order are stated for every register and port in the owning specification.
- Interfaces to external IP are written down as integration contracts with the IP version they were checked against.

## 5. Test Gates

The common make targets are required by the V2 Acceptance Standard. A target that is not implemented prints that it is not implemented and exits with code 3 (`NOT_IMPLEMENTED`); it never exits 0. A gate is `NOT_APPLICABLE` only through a structured, approved disposition.

| Gate | Command | Required result | Current state |
|---|---|---|---|
| Structure and planning files | `make check` | Exit 0; structure, planning files and commit-format self-test valid | NOT_IMPLEMENTED (no Makefile) |
| Lint | `make lint` | Exit 0; AC-030 met | NOT_IMPLEMENTED |
| Unit | `make test-unit` | Exit 0; all tests pass | NOT_IMPLEMENTED |
| Integration | `make test-integration` | Exit 0; all tests pass | NOT_IMPLEMENTED |
| Regression | `make test-regression` | Exit 0; suite unchanged and all pass | NOT_IMPLEMENTED |
| Aggregate | `make test` | Exit 0; unit, integration and regression together | NOT_IMPLEMENTED |
| Documentation | `make docs-check` | Exit 0; links and generated documents current | NOT_IMPLEMENTED |
| Acceptance | `make acceptance` | Exit 0; every automatable criterion in this file passes | NOT_IMPLEMENTED |

No coverage threshold is set. Coverage requirements are set later per subsystem and verification plan, and approved exclusions are documented.

## 6. Simulator Gates (RTL simulation and the Kritva Nexus Simulator)

| ID | Criterion (testable) | Verified by | State |
|---|---|---|---|
| AC-050 | Icarus smoke simulation passes for the declared supported test subset | Simulation run | NOT_IMPLEMENTED |
| AC-051 | Verilator simulation regression passes for the declared mandatory test suite | Simulation run | NOT_IMPLEMENTED |
| AC-052 | The Renode platform description matches the documented simulator architecture and the approved address map for CPU, memory, peripherals and interrupts | Review, test | Not defined |
| AC-053 | The supported ISA and privilege configuration of the simulated CPU is documented and compatible with the intended firmware, and differences from the selected CPU implementation are listed | Review | Not defined |
| AC-054 | Firmware runs to a defined checkpoint and produces the expected result | Simulator test | Not defined |
| AC-055 | Peripheral and interrupt models pass register and interrupt functional tests | Simulator test | Not defined |
| AC-056 | A Verilated RTL peripheral connected through co-simulation passes the same functional tests as its functional model | Co-simulation test | Not defined |
| AC-057 | Simulator tests run reproducibly and report pass or fail | Simulator regression | Not defined |
| AC-058 | No simulator result is presented as evidence of CPU timing, cache behaviour or cycle accuracy | Review | Review only |

## 7. FPGA Gates

Two acceptance levels are kept separate.

| ID | Criterion (testable) | Verified by | Evidence type | State |
|---|---|---|---|---|
| AC-060 | FPGA implementation complete: synthesis and place-and-route complete within the selected device's resources and constraints, with no unexplained critical warning; reports are reviewed | Tool run, review | software | Board not selected |
| AC-061 | The bitstream is generated and its source commit, tool version and configuration are recorded | Build record | software | Board not selected |
| AC-062 | FPGA hardware validation complete: the bitstream is programmed on the named board and the required tests (for example clock and reset, UART, GPIO, timer, interrupt, boot) are executed with results recorded | Board test | physical | Board not selected |
| AC-063 | Any substitute CPU used on FPGA is named as a substitute in every report | Review | Not applicable | Review only |

A successful FPGA synthesis or place-and-route run is not hardware validation, and is never reported as such.

## 8. Physical-Design Gates (Yosys and OpenLane)

| ID | Criterion (testable) | Verified by | Evidence type | State |
|---|---|---|---|---|
| AC-070 | Technology collateral, macro models and constraints needed for a block are confirmed available before the block is claimed physically implementable; otherwise the block is recorded as blocked | Review | Not applicable | Not defined |
| AC-071 | The configured OpenLane flow completes for the block and produces the required synthesis, floorplan, placement, clock-tree, routing, timing, area and physical-check reports | Flow run | software | Not defined |
| AC-072 | Every critical timing, DRC or LVS failure is either fixed or has a structured waiver (approver, scope, rationale, expiry or review condition); none is reported as PASS | Review | Not applicable | Review only |
| AC-073 | Clock-tree and reset implementation and technology mapping are reviewed as explicit acceptance items for every block taken through physical design | Review | Not applicable | Not defined |
| AC-074 | Physical-design reports state the target (ASIC), flow configuration and tool version, and are never presented as FPGA validation | Review | Not applicable | Review only |

No numeric timing, slack, frequency or area threshold is set until architecture, IP availability and feasibility assessment define one.

## 9. CDC and RDC Gates

| ID | Criterion (testable) | Verified by | State |
|---|---|---|---|
| AC-080 | Every clock domain and reset domain has a unique identifier in a domain register | Review | Register not defined |
| AC-081 | Every asynchronous crossing is listed in a crossing register with a documented strategy, and every crossing is registered at its destination | Review, structural check | Register not defined |
| AC-082 | No related multi-bit control or data signal is synchronised bit by bit; each such crossing uses a handshake, stable-data transfer or asynchronous FIFO | Review, structural check | Check not defined |
| AC-083 | FIFO overflow, underflow and reset behaviour is verified for every asynchronous FIFO | Simulation | Not defined |
| AC-084 | Reset assertion and release are verified for every clock domain, including domain-specific sequencing | Simulation | Not defined |
| AC-085 | CDC and RDC reports contain no unexplained critical violation; each waiver has rationale and reviewer approval | Review | Not defined |

Icarus, Verilator and Yosys are not a complete CDC or RDC signoff solution. Structural checks and assertions in the open-source flow are partial evidence only, and a dedicated checker is evaluated when required.

### 9.1 Subsystem gates

No RTL subsystem is implementation-complete unless all eight gates hold.

| Gate | Required evidence |
|---|---|
| Architecture | Module hierarchy and interfaces approved |
| Clock and reset | Clock and reset domains documented |
| CDC and RDC | Crossing register and analysis reviewed |
| RTL quality | Lint and coding review passed |
| Functional | Required simulation regression passed |
| Synthesis | Synthesis and inferred hardware reviewed |
| Technology mapping | FPGA and ASIC abstraction and mapping assumptions documented |
| Physical | Relevant implementation constraints and reports reviewed |

## 10. Evidence Requirements

Evidence points to immutable references: commit SHAs and CI run IDs, never branch names. Each evidence record states:

| Field | Content |
|---|---|
| Repository, task ID, milestone ID | From the task record |
| Source commit and pull request | 40-hex SHA and PR reference |
| Tool name and version | As run |
| Configuration revision | Commit or file hash of the configuration used |
| Target | `target=RTL`, `target=FPGA` or `target=ASIC` |
| Run identifier and result | CI run ID or report hash, and the result |
| Evidence location | Path or URL of the report |
| Reviewer and approval reference | Role, name, date and commit reviewed |

The status schema 2.0 allows only the evidence types below. The schema's enum is not extended.

| Activity | Evidence type | Reason |
|---|---|---|
| Verilator lint | software | Static analysis result |
| Yosys synthesis | software | Tool-generated synthesis result |
| FPGA synthesis, place and route, bitstream build | software | No board validation |
| OpenLane runs, including DRC, LVS and timing reports | software | ASIC-oriented tool-flow result; reclassification needs an explicit owner decision |
| Firmware host build and unit tests | software | Software build and test result |
| Icarus and Verilator simulation | simulation | RTL simulation |
| Renode platform tests | simulation | Platform simulation |
| Renode with Verilator co-simulation | simulation | Combined platform and RTL simulation |
| Programmed FPGA board tests | physical | Measured results on real hardware |

Readiness values describe one task or block, never the whole SoC: PLANNABLE (approach defined well enough to plan), IMPLEMENTABLE (specifications, dependencies, tools and IP available to start) and HARDWARE-BLOCKED (blocked by unavailable IP, FPGA resources, technology collateral or other physical dependency).

Software, simulation and tool-flow acceptance is never reported as hardware, silicon or safety validation.

## 11. Definition of Done

A task is done only when all of the following hold (ACCEPTANCE_STANDARD section 1):

1. It has a stable ID in the repository's task record and testable criteria in this file.
2. The change merged through the approved pull request process.
3. Every required check passed on the exact closing commit.
4. Required reviews are recorded against that commit.
5. Documentation and the changelog are updated.
6. Evidence points to commit SHAs and CI run IDs.
7. No blocking issue was converted into a pass; a waiver is a structured record and is never reported as PASS.
8. Status is reported from the repository's canonical status record, not from commit counts.

Nexus adds: the applicable gates of sections 5 to 9 pass or have approved dispositions, and evidence descriptions state target, tool version and configuration as in section 10.

A milestone closes only through an approved `COMPLETION_RECORD.md` naming the milestone, scope, exact merge and release commits, test runs, tag if any, the disposition of each criterion, deferred work, approvals and evidence. A merge, a passing CI run, a tag or a task marked complete does not close a milestone.

## 12. Known Limitations and Exclusions

No decision ID has been recorded for any item below, because Nexus has no central decision record while it is outside the V2 plan.

| Limitation | Effect | Decision ID |
|---|---|---|
| Nexus is outside the V2 plan (planned for V3); no task is baselined | No criterion here earns credit | None recorded |
| Mapping of OpenLane signoff-style reports to evidence type is undecided | All OpenLane results are software evidence for now | None recorded |
| Open architecture items NX-ARCH-GAP-001 to NX-ARCH-GAP-004 | AC-013 to AC-016 cannot yet be met | None recorded |
| No numeric coverage, timing, slack, frequency or area threshold | These are set after architecture and feasibility work | None recorded |
| CDC and RDC analysis tooling is not signoff grade | Open-source checks are partial evidence only | None recorded |
| Simulator CPU model is not the selected CPU implementation | No timing or cycle-accuracy claim from Renode | None recorded |
| FPGA board and toolchain not selected | Section 7 gates are not testable | None recorded |
| Module-size guidelines and RTL coding guidelines not written | AC-033 is review-only | None recorded |
| Make targets, workflows and the commit checker do not exist | Section 5 gates are NOT_IMPLEMENTED | None recorded |

## 13. Change Control

- Criteria change only through a pull request approved by the owner (Dinesh); new criteria are added as new versions with new IDs.
- Accepted criteria are never edited to fit a result. An accepted criterion is superseded by a new one, and the old record is kept.
- Criterion IDs are never reused.
- Each version change adds a row to the revision table below and a changelog entry.

| Version | Date | Change | Approval |
|---|---|---|---|
| 0.1 | 2026-11-05 | Initial proposed draft | None; PROPOSED |
