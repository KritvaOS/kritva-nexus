# kritva-nexus

> Kritva Nexus is the planned ASIC/FPGA SoC engineering repository for KritvaOS: architecture, RTL, verification, a Renode-based simulator, FPGA prototyping and block-level physical design, in one place.

| Property | Value |
|---|---|
| Project | KritvaOS |
| Repository | `KritvaOS/kritva-nexus` |
| Repository Type | Platform (PROPOSED; outside the V2 plan, planned for V3) |
| Visibility Class | Not yet decided |
| GitHub Setting | Not verified (owner to attest) |
| Lifecycle Status | PLANNING |
| Repository Owner | Dinesh |
| Technical Owner | Dinesh (interim, not independent) |
| Security Owner | Dinesh (program Security Owner, D-032 in kritva-program) |
| Architecture | Not yet defined |
| Datasheet | [datasheet/NEXUS_DATASHEET.md](datasheet/NEXUS_DATASHEET.md) (DERIVED, DRAFT; preliminary planning summary of the requirements register) |
| Milestones | [planning/MILESTONE.md](planning/MILESTONE.md) (PROPOSED) |
| Tasks | [planning/TASKS.md](planning/TASKS.md) (PROPOSED) |
| Acceptance Criteria | [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) (PROPOSED) |
| Status Reporting | [planning/MILESTONE_STATUS.md](planning/MILESTONE_STATUS.md) (hand-maintained; no central status) |
| License | [LICENSE](LICENSE) (Apache License 2.0) |

## 1. Purpose and Scope

This repository will own the engineering of the Kritva Nexus SoC:

- the architecture, requirements and decision records for the SoC;
- technology-independent RTL, with FPGA and ASIC mapping wrappers kept separate from it;
- RTL verification (lint, simulation, regression, CDC and RDC analysis, coverage);
- the Kritva Nexus Simulator: a Renode-based platform simulation, with Verilator co-simulation of selected RTL blocks;
- FPGA prototyping of a reduced Nexus configuration;
- block-level synthesis and OpenLane physical design;
- the reproducible tool environment, CI entry points and the evidence they produce.

It does not own: the program baseline, task weights, approvals, accepted progress or consolidated status (these belong to kritva-program); third-party IP sources and licences (the repository will record their status, not host unlicensed IP); a claim of production signoff, since results from open-source flows are implementation evidence only.

Nothing in this repository is implemented yet. Every capability named in this README is PLANNED or PROPOSED unless a table below says otherwise.

## 2. Position in the KritvaOS Ecosystem

Nexus is an engineering repository. It reports implementation facts and evidence; it does not award itself program progress. Plan, baseline, approvals and status live in [kritva-program](https://github.com/KritvaOS/kritva-program).

Registration state: by owner decision, Nexus is outside the Kritva Program V2 plan and is planned for the V3 plan. It is not registered as a workstream in kritva-program, and no Nexus tasks are baselined. Until a V3 registration is recorded, all Nexus plans are PROPOSED planning material with no weight and no credit. Dinesh holds every owner and reviewer role for this repository (interim, not independent).

## 3. Architecture

The working architecture, named System Architecture A0 (integration draft), is PROPOSED and not yet written into this repository. In outline it has an application domain (a quad-core application CPU cluster, four AXI fabrics, external memory, AI and vision blocks, multimedia and I/O, two APB bridges), an independent security domain with its own 32-bit RISC-V processor and secure AXI, and an always-on management domain. Which choices are SELECTED, PROPOSED or open is recorded per decision in the architecture documents once they exist.

| Architecture document | Status |
|---|---|
| System architecture and index | Not yet defined |
| Interconnect, memory, address map | Not yet defined |
| Clock, reset, CDC and RDC | Not yet defined |
| Security architecture | Not yet defined |
| Simulator architecture | Not yet defined |

A document that is planned but not written has no link here. Open items that must be resolved before an architecture freeze include DDR4 interface width and capacity, memory-access port architecture, AXI configuration, cache coherency, local SRAM capacity, application address width against the selected CPU configuration, and the physical pin inventory.

## 4. Documents to Read First

| Document | Label, status | What it answers |
|---|---|---|
| [LICENSE](LICENSE) | REFERENCE, in force | Under what terms the repository may be used |
| This README | REFERENCE (navigation), DRAFT | What the repository is for and what exists |
| [AGENTS.md](AGENTS.md) | AUTHORITATIVE for repository working rules, DRAFT | Who decides, what agents must not change, commit and evidence rules |
| [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) | AUTHORITATIVE for acceptance, PROPOSED | What makes a task, gate or milestone acceptable |
| [planning/TASKS.md](planning/TASKS.md) | INPUT (read by program tooling), PROPOSED | Which Stage 1 tasks are proposed and their details |
| [planning/TASK_CATALOGUE.md](planning/TASK_CATALOGUE.md) | REFERENCE, PROPOSED | Future task candidates, not registered tasks |
| [planning/MILESTONE.md](planning/MILESTONE.md) | INPUT, PROPOSED | Milestones, exit conditions, risks, architecture gaps, owner decisions |
| [planning/MILESTONE_STATUS.md](planning/MILESTONE_STATUS.md) | EVIDENCE, PROPOSED | Reported execution state of each milestone |
| [planning/REVIEW_CHECKLIST.md](planning/REVIEW_CHECKLIST.md) | INPUT, PROPOSED | What a reviewer checks on every pull request |
| [planning/GIT_COMMIT_STEP.md](planning/GIT_COMMIT_STEP.md) | INPUT, PROPOSED | Branch, commit, merge and tag steps and the commit format |
| [planning/CHANGELOG.md](planning/CHANGELOG.md) | EVIDENCE, PROPOSED | Record of changes to the repository |
| [CONTRIBUTING.md](CONTRIBUTING.md) | REFERENCE, DRAFT | How to contribute |
| [SECURITY.md](SECURITY.md) | AUTHORITATIVE for reporting, DRAFT | How to report a vulnerability |

The A0 integration draft is in [architecture/A0_INTEGRATION_DRAFT.md](architecture/A0_INTEGRATION_DRAFT.md) as a PROPOSED import. The consolidated system architecture is being written in [architecture/SYSTEM_ARCHITECTURE.md](architecture/SYSTEM_ARCHITECTURE.md) (DRAFT, partial).

## 5. Repository Structure and File Responsibilities

Directories are added only when the work they hold is baselined. Empty folders and placeholder tasks are not created. Planned paths are shown in code format because they do not exist yet.

| Path | Responsibility | Label, status | Edit by hand? |
|---|---|---|---|
| [LICENSE](LICENSE) | Apache License 2.0 text | REFERENCE, IMPLEMENTED | Yes, by owner decision only |
| `README.md` | Navigation hub | REFERENCE, DRAFT | Yes |
| [AGENTS.md](AGENTS.md) | Rules for agents and contributors | AUTHORITATIVE for repository working rules, DRAFT | Yes |
| [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) | Testable acceptance criteria | AUTHORITATIVE for acceptance, PROPOSED | Yes, new versions only |
| `planning/` | Task, milestone and review records | MIXED; see the files below | Per file |
| [planning/TASKS.md](planning/TASKS.md) | Proposed Stage 1 tasks, read by the PR gate | INPUT, PROPOSED | Yes, keep the table layout |
| [tasks/](tasks/KOS-NEXUS-001/TASK.md) | One `TASK.md` per Stage 1 task | INPUT, PROPOSED | Yes |
| [planning/TASK_CATALOGUE.md](planning/TASK_CATALOGUE.md) | Future task candidates | REFERENCE, PROPOSED | Yes |
| [planning/MILESTONE.md](planning/MILESTONE.md) | Milestone definitions, risks, gaps, owner decisions | INPUT, PROPOSED | Yes |
| [planning/MILESTONE_STATUS.md](planning/MILESTONE_STATUS.md) | Reported milestone execution state | EVIDENCE, PROPOSED | Yes, until a generator exists |
| [planning/REVIEW_CHECKLIST.md](planning/REVIEW_CHECKLIST.md), [planning/GIT_COMMIT_STEP.md](planning/GIT_COMMIT_STEP.md), [planning/CHANGELOG.md](planning/CHANGELOG.md) | Review, commit-step and change records | INPUT, PROPOSED | Yes |
| [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) | Contribution and security-reporting rules | REFERENCE, DRAFT | Yes (SECURITY.md by owner only) |
| [planning/CLAUDE_SESSIONS.md](planning/CLAUDE_SESSIONS.md) | Claude session identifiers of Claude-assisted commits, one consolidated file (NX-DEC-028) | REFERENCE, DRAFT | Yes, by every Claude-assisted commit |
| [Makefile](Makefile) | Make targets; unimplemented gates exit 3 | INPUT, DRAFT | Yes, by owner only |
| `.github/` | CODEOWNERS, gate configuration, PR template, workflows | INPUT, DRAFT | Yes, by owner only |
| `scripts/` and `tests/` | Repository checks (README, links, commit format, PR gate) and their tests | INPUT, DRAFT | Yes, by owner only |
| `architecture/` | SoC architecture, address maps, clock, reset, CDC, security | AUTHORITATIVE for architecture, PLANNED | Yes |
| [architecture/README.md](architecture/README.md) | Index of the architecture documents | REFERENCE, DRAFT | Hand-maintained |
| [architecture/A0_INTEGRATION_DRAFT.md](architecture/A0_INTEGRATION_DRAFT.md) | A0 integration draft imported from a discussion (a reconstruction, not an original document) | INPUT, PROPOSED | Addenda only |
| [architecture/SYSTEM_ARCHITECTURE.md](architecture/SYSTEM_ARCHITECTURE.md) | Consolidated top-level system architecture (KOS-NEXUS-006), partial | INPUT, DRAFT | Hand-maintained |
| [requirements/REQUIREMENTS.md](requirements/REQUIREMENTS.md) | Traceable requirements register | AUTHORITATIVE for requirements, PROPOSED | Yes |
| [decisions/DECISIONS.md](decisions/DECISIONS.md) | Decision index and records `NX-DEC-NNN.md` with alternatives and rationale | EVIDENCE, PROPOSED | Append only |
| [standards/RTL_DESIGN_STANDARD.md](standards/RTL_DESIGN_STANDARD.md) | Kritva Nexus RTL design standard (KOS-NEXUS-020), rules with stable IDs and the planned compliance checks | AUTHORITATIVE for RTL design rules, SELECTED (NX-DEC-023) | Yes, by change request |
| [datasheet/NEXUS_DATASHEET.md](datasheet/NEXUS_DATASHEET.md) | Preliminary planning datasheet of 8 to 12 pages (KOS-NEXUS-085): blocks, consolidated features, external interfaces, internal connectivity and per-block feature list, each row traced to NX-REQ IDs; the PDF is generated and not committed | DERIVED (not AUTHORITATIVE), DRAFT | Yes |
| [datasheet/nexus_external_interfaces.svg](datasheet/nexus_external_interfaces.svg) | External interface diagram used by the datasheet | DERIVED, DRAFT | Yes |
| [datasheet/nexus_internal_connectivity.svg](datasheet/nexus_internal_connectivity.svg) | Internal AXI and security connectivity diagram used by the datasheet | DERIVED, DRAFT | Yes |
| `rtl/` | Synthesizable, technology-independent RTL | AUTHORITATIVE for implementation, NOT YET IMPLEMENTED | Yes |
| `technology/` | Generic, FPGA and ASIC mapping wrappers | AUTHORITATIVE for technology mapping, NOT YET IMPLEMENTED | Yes |
| `verification/` | Test plans, testbenches, assertions, CDC and RDC plans | AUTHORITATIVE for verification, NOT YET IMPLEMENTED | Yes |
| `simulator/` | Kritva Nexus Simulator (Renode platform, co-simulation, firmware tests) | AUTHORITATIVE for the simulator, NOT YET IMPLEMENTED | Yes |
| `fpga/` | Board configuration, projects, constraints, bring-up tests | AUTHORITATIVE for FPGA prototyping, NOT YET IMPLEMENTED | Yes |
| `synthesis/` and `physical_design/` | Yosys and OpenLane configuration, constraints, reports | MIXED, NOT YET IMPLEMENTED | Per file |
| `tools/` | Pinned tool versions and setup | INPUT, NOT YET IMPLEMENTED | Yes |
| `evidence/` | Commit-linked simulation, synthesis, FPGA and PD reports | EVIDENCE, NOT YET IMPLEMENTED | Append only |
| `status/status.json` | Task-level status in program schema 2.0 | GENERATED, PLANNED | No |
| `.github/workflows/` | CI checks | INPUT, PLANNED | Yes |

## 6. Toolchain and Development Workflow

The toolchain is PROPOSED. No tool version is pinned and no script or Makefile exists yet, so there are no commands to run.

| Tool | Purpose | Version | Check |
|---|---|---|---|
| Icarus Verilog | Smoke and directed RTL simulation | Not yet pinned | Not yet defined |
| Verilator | Lint, regression simulation, coverage, co-simulation with Renode | Not yet pinned | Not yet defined |
| Yosys | Synthesis checks, latch and hierarchy checks | Not yet pinned | Not yet defined |
| OpenLane 2 with OpenROAD | Block-level physical design (ASIC-oriented) | Not yet pinned | Not yet defined |
| Renode | Platform simulation (the Kritva Nexus Simulator) | Not yet pinned | Not yet defined |
| FPGA toolchain | Prototyping; board and vendor flow not selected | Not yet selected | Not yet defined |
| GTKWave | Waveform inspection | Not yet pinned | Not yet defined |

| Command | Effect | Needs | Preview |
|---|---|---|---|
| None exist yet | Not applicable | Not applicable | Not applicable |

Intended separation of evidence: RTL simulation and Verilator regression show RTL behaviour; the Renode simulator shows software-visible platform behaviour, not CPU timing or cycle accuracy; FPGA results show behaviour of synthesized RTL on a board; OpenLane results show block-level implementation under a configured technology. None of these is presented as another's evidence, and none is production signoff.

## 7. Dependencies and Interfaces

| Dependency | Direction | Kind | Contract | State |
|---|---|---|---|---|
| kritva-program | upstream | governance | Standards followed (acceptance, README, commit format); no registration in V2 | Standards only; V3 registration planned |
| Application CPU RTL (Xuantie C910 direction) | upstream | build | Source, licence and FPGA/ASIC suitability | UNVERIFIED |
| DDR4 controller and PHY | upstream | build | IP strategy and integration model | UNVERIFIED |
| NPU and ISP implementation | internal or upstream | build | Own versus external IP boundary | UNVERIFIED |
| Open-source tools listed in section 6 | upstream | build | Pinned versions and configuration | PLANNED |
| ASIC technology collateral and macros for OpenLane | upstream | build | Availability for each block | UNVERIFIED |
| FPGA prototyping board | upstream | build | Resources, DDR, I/O, debug, licensing | Not selected |

## 8. Milestones and Implementation Plan

| Item | Document | Status and meaning of dates |
|---|---|---|
| Milestones | [planning/MILESTONE.md](planning/MILESTONE.md) | PROPOSED; no dates exist and none is implied |
| Milestone status | [planning/MILESTONE_STATUS.md](planning/MILESTONE_STATUS.md) | Repository-reported state, not acceptance |
| Roadmap | Not yet defined | Not applicable |

Repository milestones carry an `NX-` prefix to avoid confusion with program milestones and are not mapped to any program milestone; any mapping is a V3-plan decision. The workstreams are: architecture, IP, RTL, verification, simulator (SIM), FPGA, physical design, integration, infrastructure and release. The first stage is the repository and tool foundation, the architecture baseline and the IP assessment. One small self-contained RTL block is intended to be taken through the whole flow before any large subsystem is started. The CPU, ISP and NPU RTL are not the starting point.

## 9. Tasks and Acceptance Criteria

Tasks are recorded in [planning/TASKS.md](planning/TASKS.md) and acceptance criteria in [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md), following the kritva-program V2 Acceptance Standard. The task prefix is `KOS-NEXUS`. The tasks listed there are Stage 1 candidates, each with a record under `tasks/`; future candidates are held in [planning/TASK_CATALOGUE.md](planning/TASK_CATALOGUE.md) and are not valid task IDs until promoted. Nothing is registered in kritva-program (Nexus is planned for V3), weighted or credited, and an ID is not reused or invented outside the repository's task record.

Work is not accepted because code, a commit, a merged pull request or a local test exists. A task is done only under the standard's definition of done, and a milestone closes only through an approved `COMPLETION_RECORD.md`.

## 10. Status Reporting and Program Integration

Nexus is outside the V2 plan, so it has no `status/status.json` and reports nothing to kritva-program; status is the hand-maintained [planning/MILESTONE_STATUS.md](planning/MILESTONE_STATUS.md). Four things are kept apart: execution (what this repository reports), evidence (commit, result and scope, using the types software, simulation or physical), acceptance (decided by the program's approval records, not by this repository) and release readiness (the applicable gates). Evidence mapping: lint, Yosys, FPGA synthesis and place-and-route, and OpenLane results are software; Icarus, Verilator, Renode and co-simulation are simulation; physical means programmed-board results only (see [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md)).

## 11. Build, Test, Regression and Validation

| Check | Command | Effect | Runs in CI? | Expected |
|---|---|---|---|---|
| Repository structure | `make check` | Required files exist; commit-message checker tests pass | No (not yet wired) | Implemented |
| Documentation links | `make docs-check` | Relative Markdown links resolve | No | Implemented |
| README structure | `make check-readme` | README metadata, topics and links | Yes (`readme-check`) | Implemented |
| Lint | `make lint` | Not applicable | No | Exit 3, NOT_IMPLEMENTED |
| Unit, integration, regression, all tests, acceptance | `make test-unit`, `make test-integration`, `make test-regression`, `make test`, `make acceptance` | Not applicable | No | Exit 3, NOT_IMPLEMENTED |

A target not yet implemented exits with code 3 (NOT_IMPLEMENTED) and is never a pass.

## 12. Git Workflow and Review

The Kritva commit standard (`type(scope): summary` with one `Task:` or `Tasks:` footer, merge-commit method) applies, as set out in [planning/GIT_COMMIT_STEP.md](planning/GIT_COMMIT_STEP.md). The `commit-message-check`, `secret-scan`, `pr-acceptance-gate` and `readme-check` workflows are defined in `.github/workflows/`; that they are enabled and required in the GitHub settings is not verified. Work on a branch and open a pull request; no push to `main`. Commit messages carry no AI-session trailers or session links. Review is by Dinesh (interim, not independent); see [planning/REVIEW_CHECKLIST.md](planning/REVIEW_CHECKLIST.md).

## 13. Safety and Security

This is not a repository that moves hardware today. The security subsystem, secure boot and isolation boundaries are architecture topics and are PROPOSED; none is implemented or validated. Simulation, FPGA runs and open-source physical-design runs are implementation evidence only and do not establish production readiness or security assurance.

Reporting route: see [SECURITY.md](SECURITY.md); the GitHub private reporting setting is not verified. Send vulnerability or secret-exposure reports privately to the Security Owner named above, and do not post details of an unfixed vulnerability in a public issue or pull request. Never commit credentials, tokens, keys, production data or personal data.

## 14. Release and Versioning

No release exists. Intended scheme: annotated SemVer tags created only after an approved merge and passing required checks, with a completion record, under the kritva-program tag policy. The document version and the release version are separate. The changelog is [planning/CHANGELOG.md](planning/CHANGELOG.md).

## 15. Ownership and Escalation

Dinesh is Repository Owner, Technical Owner (interim), Security Owner and the code owner (see [.github/CODEOWNERS](.github/CODEOWNERS)); review is not independent. A blocker is raised with him.

## 16. Related Repositories and References

- [kritva-program](https://github.com/KritvaOS/kritva-program): plan, baseline, approvals, acceptance standard and status for the program.
- Other KritvaOS repositories: no relationship to Nexus has been verified yet.

## 17. License

Apache License 2.0. See [LICENSE](LICENSE).
