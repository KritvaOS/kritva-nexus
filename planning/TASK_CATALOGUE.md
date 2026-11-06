# Kritva Nexus Task Catalogue

Entries in this catalogue are planning candidates. They are not registered tasks, are not valid for commit-footer validation, have no assigned weights and do not contribute to accepted program progress. Promotion into `planning/TASKS.md` requires owner (Dinesh) review and approval.

Candidate milestone assignments are provisional. They do not establish any mapping to kritva-program milestones, and Nexus is outside the V2 plan (planned for V3) and not registered in kritva-program. The catalogue uses no task states: the registered task lifecycle belongs to `planning/TASKS.md`. Every entry here has the same descriptive metadata, candidate stage `PLANNING_ONLY`.

Candidate IDs are the identifiers used in the planning discussion and are kept unchanged when a candidate is promoted. They are not renumbered to close gaps. Six identifiers (KOS-NEXUS-001, 006, 007, 008, 018 and 019) were promoted to `planning/TASKS.md` as Stage 1 candidates and are not repeated here; Stage 1 also holds the new KOS-NEXUS-084.

Each candidate has one primary milestone. A candidate that spans two milestones says so in the notes. Candidate titles and deliverables are L1 and L2 outlines; they are decomposed further after the simulator platform and the FPGA board are chosen.

## 1. How to read an entry

| Column | Meaning |
|---|---|
| Candidate ID | Stable planning identifier, not a registered task ID |
| Title | Concise description of the work |
| Workstream | INFRA, ARCH, RTL, VERIF, SIM, FPGA, PD, INTEGRATION or RELEASE |
| Milestone | Primary proposed repository milestone `NX-M0` to `NX-M8`, provisional |
| Deliverable | Expected engineering outcome |
| Notes | Dependencies, secondary milestone or evidence caution |

## 2. Candidates by workstream

### Infrastructure (INFRA)

| Candidate ID | Title | Workstream | Milestone | Deliverable | Notes |
|---|---|---|---|---|---|
| KOS-NEXUS-002 | Establish Icarus and Verilator tool environment | INFRA | NX-M0 | Reproducible simulation environment | - |
| KOS-NEXUS-003 | Establish Yosys synthesis environment | INFRA | NX-M0 | Reproducible synthesis environment | - |
| KOS-NEXUS-004 | Establish OpenLane 2 environment and example flow | INFRA | NX-M0 | Reproducible physical-design example | Technology collateral availability must be checked first |
| KOS-NEXUS-005 | Establish CI and status reporting | INFRA | NX-M0 | CI workflows and status schema | Nexus is not registered in kritva-program (V3 plan); no `status/status.json` is created while that holds |

### Architecture (ARCH)

| Candidate ID | Title | Workstream | Milestone | Deliverable | Notes |
|---|---|---|---|---|---|
| KOS-NEXUS-009 | Define clock, reset and power architecture | ARCH | NX-M1 | Clock, reset and power documents | - |
| KOS-NEXUS-010 | Define interrupt architecture | ARCH | NX-M1 | Interrupt specification | - |
| KOS-NEXUS-011 | Define security management architecture | ARCH | NX-M1 | Security specification | - |
| KOS-NEXUS-012 | Define CPU subsystem architecture | ARCH | NX-M1 | CPU specification | - |
| KOS-NEXUS-013 | Define ISP and camera architecture | ARCH | NX-M1 | ISP specification | - |
| KOS-NEXUS-014 | Define NPU subsystem architecture | ARCH | NX-M1 | NPU specification | - |
| KOS-NEXUS-015 | Define display architecture | ARCH | NX-M1 | Display specification | - |
| KOS-NEXUS-016 | Define Ethernet and EtherCAT architecture | ARCH | NX-M1 | Ethernet specification | - |
| KOS-NEXUS-017 | Define peripheral subsystem architecture | ARCH | NX-M1 | Peripheral specification | - |
| KOS-NEXUS-069 | Define clock-domain architecture | ARCH | NX-M1 | Clock-domain architecture and domain register | - |
| KOS-NEXUS-070 | Define reset-domain architecture | ARCH | NX-M1 | Reset-domain architecture and domain register | - |
| KOS-NEXUS-071 | Establish CDC crossing register | ARCH | NX-M1 | CDC crossing register | - |
| KOS-NEXUS-072 | Define RTL hierarchy and partitioning | ARCH | NX-M1 | RTL partitioning guidelines and module hierarchy | - |

### RTL implementation (RTL)

| Candidate ID | Title | Workstream | Milestone | Deliverable | Notes |
|---|---|---|---|---|---|
| KOS-NEXUS-020 | Define RTL coding and module conventions | RTL | NX-M1 | RTL guidelines | Part of the architecture and engineering specification |
| KOS-NEXUS-021 | Implement common RTL infrastructure | RTL | NX-M3 | Common RTL library | - |
| KOS-NEXUS-022 | Implement application AXI/APB infrastructure | RTL | NX-M3 | Interconnect RTL | - |
| KOS-NEXUS-023 | Implement system control and interrupt infrastructure | RTL | NX-M3 | System control RTL | - |
| KOS-NEXUS-024 | Implement security subsystem RTL | RTL | NX-M4 | Security RTL | Possible later decomposition into secure boot, cryptographic peripherals and security control, after IP ownership and boundaries are established |
| KOS-NEXUS-025 | Implement general peripheral RTL | RTL | NX-M4 | Peripheral RTL | - |
| KOS-NEXUS-026 | Integrate CPU subsystem | RTL | NX-M4 | CPU integration | Depends on IP availability and licence assessment |
| KOS-NEXUS-027 | Integrate memory subsystem | RTL | NX-M4 | Memory integration | Depends on DDR4 controller and PHY IP strategy |
| KOS-NEXUS-028 | Integrate ISP and camera subsystem | RTL | NX-M4 | Vision RTL | - |
| KOS-NEXUS-029 | Integrate NPU subsystem | RTL | NX-M4 | NPU integration | - |
| KOS-NEXUS-030 | Implement display subsystem | RTL | NX-M4 | Display RTL | - |
| KOS-NEXUS-031 | Implement Ethernet subsystem | RTL | NX-M4 | Ethernet RTL | - |
| KOS-NEXUS-073 | Develop reusable CDC synchronizer library | RTL | NX-M3 | CDC synchronizer library | - |
| KOS-NEXUS-074 | Develop asynchronous FIFO infrastructure | RTL | NX-M3 | Asynchronous FIFO library | - |
| KOS-NEXUS-075 | Develop reset synchronization infrastructure | RTL | NX-M3 | Reset synchronization library | - |
| KOS-NEXUS-076 | Develop technology-independent memory wrappers | RTL | NX-M3 | Generic memory wrappers | Subsystem-specific mapping follows in NX-M4 |
| KOS-NEXUS-077 | Develop FPGA technology mapping wrappers | RTL | NX-M4 | FPGA mapping wrappers | Needs an FPGA board decision |
| KOS-NEXUS-078 | Develop ASIC technology mapping wrappers | RTL | NX-M4 | ASIC mapping wrappers | Needs technology collateral decision |

### RTL verification (VERIF)

| Candidate ID | Title | Workstream | Milestone | Deliverable | Notes |
|---|---|---|---|---|---|
| KOS-NEXUS-032 | Establish unit-level verification framework | VERIF | NX-M3 | Testbench infrastructure | - |
| KOS-NEXUS-033 | Establish subsystem verification framework | VERIF | NX-M3 | Subsystem test infrastructure | - |
| KOS-NEXUS-034 | Establish assertion and coverage strategy | VERIF | NX-M3 | Assertion and coverage plan | No coverage threshold is set by default |
| KOS-NEXUS-035 | Verify interconnect and memory access | VERIF | NX-M5 | Verification results | - |
| KOS-NEXUS-036 | Verify security isolation and boot controls | VERIF | NX-M5 | Security verification results | - |
| KOS-NEXUS-037 | Verify peripheral and I/O subsystems | VERIF | NX-M5 | Peripheral verification results | - |
| KOS-NEXUS-038 | Verify ISP/NPU data path | VERIF | NX-M5 | Vision verification results | - |
| KOS-NEXUS-039 | Verify display and Ethernet data paths | VERIF | NX-M5 | I/O verification results | - |
| KOS-NEXUS-040 | Establish integration regression | VERIF | NX-M5 | Integration regression results | - |
| KOS-NEXUS-079 | Establish CDC verification methodology | VERIF | NX-M3 | CDC verification methodology | Open-source tools are not CDC signoff tools |
| KOS-NEXUS-080 | Establish RDC verification methodology | VERIF | NX-M3 | RDC verification methodology | - |
| KOS-NEXUS-081 | Establish RTL structural and complexity checks | VERIF | NX-M5 | Structural and complexity check methodology and results | Subsystem analysis and checks |

### Kritva Nexus Simulator (SIM)

| Candidate ID | Title | Workstream | Milestone | Deliverable | Notes |
|---|---|---|---|---|---|
| KOS-NEXUS-048 | Establish Renode simulator environment | SIM | NX-M3 | Installation and version record | - |
| KOS-NEXUS-049 | Define Nexus simulator architecture | SIM | NX-M3 | Simulator architecture document | Explains Renode as a virtual-platform simulator and Verilator co-simulation as real RTL connected to it |
| KOS-NEXUS-050 | Implement Nexus simulator platform description | SIM | NX-M3 | Platform description files (.repl and .resc) | Memory map must match the approved address map |
| KOS-NEXUS-051 | Implement CPU and memory simulator models | SIM | NX-M3 | Platform boot test | CPU model equivalence to the selected CPU is to be verified; no timing claim |
| KOS-NEXUS-052 | Implement peripheral and interrupt models | SIM | NX-M3 | Peripheral tests | - |
| KOS-NEXUS-053 | Establish Verilator co-simulation framework | SIM | NX-M3 | Co-simulation example | - |
| KOS-NEXUS-054 | Integrate selected Nexus RTL peripherals | SIM | NX-M4 | Co-simulation results | Needs RTL blocks from the RTL workstream |
| KOS-NEXUS-055 | Establish firmware simulation and testing | SIM | NX-M5 | Firmware test results | - |
| KOS-NEXUS-056 | Establish automated simulator regression | SIM | NX-M5 | CI results | - |

### FPGA prototyping (FPGA)

| Candidate ID | Title | Workstream | Milestone | Deliverable | Notes |
|---|---|---|---|---|---|
| KOS-NEXUS-057 | Evaluate FPGA boards and toolchains | FPGA | NX-M2 | Board evaluation | Depends on whether the CPU and DDR4 IP can be used in an FPGA environment |
| KOS-NEXUS-058 | Select FPGA prototyping board | FPGA | NX-M2 | Owner-approved board decision | Board selection is an owner decision |
| KOS-NEXUS-059 | Establish FPGA development environment | FPGA | NX-M0 | Reproducible tool setup | - |
| KOS-NEXUS-060 | Develop Nexus FPGA top-level wrapper | FPGA | NX-M3 | FPGA top-level RTL | FPGA wrappers stay outside the main synthesizable RTL hierarchy |
| KOS-NEXUS-061 | Define FPGA clock/reset and I/O constraints | FPGA | NX-M3 | Constraints | Needs the selected board |
| KOS-NEXUS-062 | Implement minimal FPGA prototype | FPGA | NX-M4 | Synthesized design | Software evidence only until board tests run |
| KOS-NEXUS-063 | Generate and program initial bitstream | FPGA | NX-M4 | Programming evidence | Needs the selected board |
| KOS-NEXUS-064 | Validate UART, GPIO and timer functionality | FPGA | NX-M4 | Board-level test results | Physical evidence only when run on the board |
| KOS-NEXUS-065 | Integrate RISC-V CPU and memory subsystem | FPGA | NX-M7 | FPGA boot evidence | A substitute CPU, if used, is labelled a substitute |
| KOS-NEXUS-066 | Integrate AXI/APB and interrupt infrastructure | FPGA | NX-M7 | Hardware test results | - |
| KOS-NEXUS-067 | Establish FPGA regression and reporting | FPGA | NX-M5 | Reproducible test reports | Also covers integration regression in NX-M7 |
| KOS-NEXUS-068 | Demonstrate selected Nexus subsystem prototype | FPGA | NX-M7 | Prototype review report | - |

### Physical design (PD)

| Candidate ID | Title | Workstream | Milestone | Deliverable | Notes |
|---|---|---|---|---|---|
| KOS-NEXUS-041 | Establish block-level synthesis methodology | PD | NX-M3 | Synthesis methodology | - |
| KOS-NEXUS-042 | Establish block-level OpenLane methodology | PD | NX-M3 | Physical-design methodology | - |
| KOS-NEXUS-043 | Run first selected block through physical design | PD | NX-M6 | Reviewed physical-design evidence | Blocked for a block whose technology collateral or macro models are unavailable |
| KOS-NEXUS-044 | Establish physical-design reporting and review | PD | NX-M6 | Physical-design report template | - |
| KOS-NEXUS-082 | Establish technology-dependent synthesis mapping | PD | NX-M6 | Technology-dependent synthesis mapping methodology | - |
| KOS-NEXUS-083 | Establish clock-tree and reset implementation methodology | PD | NX-M6 | Clock-tree and reset implementation methodology | - |

### SoC integration (INTEGRATION)

| Candidate ID | Title | Workstream | Milestone | Deliverable | Notes |
|---|---|---|---|---|---|
| KOS-NEXUS-045 | Establish Nexus top-level integration | INTEGRATION | NX-M7 | Top-level RTL | - |
| KOS-NEXUS-046 | Complete integration-level regression | INTEGRATION | NX-M7 | Integration verification evidence | - |

### Engineering release (RELEASE)

| Candidate ID | Title | Workstream | Milestone | Deliverable | Notes |
|---|---|---|---|---|---|
| KOS-NEXUS-047 | Consolidate engineering release evidence | RELEASE | NX-M8 | Release package | - |

## 3. Promotion rules

- The owner reviews a batch of candidates, accepts it, and the batch is added to `planning/TASKS.md` with state `NOT_STARTED` and its criteria in `ACCEPTANCE_CRITERIA.md`. Only then does the ID become valid in a commit footer.
- A promoted candidate keeps its ID. A candidate may be revised, split or dropped before promotion; once an ID is registered it is never renumbered or reused.
- Promotion does not baseline a task in kritva-program, assign a weight or earn credit. Those follow the program's own approval process.
- No candidate is started because it appears here.

## 4. Open points that affect several candidates

- Decided: Nexus is not registered in V2 and goes into the V3 plan; registration details are for V3.
- The mapping of tool results to the status schema evidence types is recorded in `ACCEPTANCE_CRITERIA.md`; OpenLane signoff-style reports stay software evidence until the owner decides otherwise.
- Candidates that depend on external IP (CPU, DDR4 controller and PHY, NPU, ISP) depend on the outcome of the IP inventory and assessment tasks in Stage 1.
- Candidates that depend on a board or on technology collateral are marked in the notes; their readiness is decided at promotion.
