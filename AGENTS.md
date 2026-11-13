# AGENTS.md: kritva-nexus

Guidance for AI coding agents and contributors. The program rules live in kritva-program (`AGENTS.md`, `v2/planning/ACCEPTANCE_STANDARD.md`); this file adds the rules for this repository.

## 1. Scope

Kritva Nexus owns the engineering of the Nexus SoC: architecture, requirements, IP assessment, RTL, verification, the Kritva Nexus Simulator (Renode with Verilator co-simulation), FPGA prototyping and block-level physical design. It does not own the program baseline, weights, approvals or gates (kritva-program). Nexus is outside the Kritva Program V2 plan and is planned for the V3 plan; it is not registered in kritva-program. Dinesh holds every owner and reviewer role (interim, not independent). Task IDs use the prefix `KOS-NEXUS`; milestones are `NX-M0` to `NX-M8` and are not program milestones. Workstreams: INFRA, ARCH, IP, RTL, VERIF, SIM, FPGA, PD, INTEGRATION, RELEASE.

## 2. Program rules that apply here

1. This repository reports facts. A commit here never creates credit, and agents do not edit kritva-program records from this repository; a change needed there is written up as a proposal for Dinesh.
2. Simulation, FPGA synthesis and OpenLane results are never described as silicon or hardware validation. Evidence types are `software`, `simulation` and `physical`: lint, Yosys, FPGA synthesis and place-and-route, and OpenLane runs (including DRC, LVS and STA) are `software`; Icarus, Verilator, Renode and co-simulation are `simulation`; `physical` is reserved for programmed-board results. Every evidence description states target (RTL, FPGA or ASIC), tool and version, configuration revision, source commit and run ID.
3. No empty folders, no placeholder tasks, no invented owners, dates, IP availability, licences, PDK or macro availability, FPGA resource figures, timing or evidence. Add directories only when a real task needs them.
4. Architecture decisions carry one label: `SELECTED` (recorded owner decision), `PROPOSED` or `OPEN`. A recommendation from an agent or another AI tool does not make a choice SELECTED. Decision records are append-only.
5. Interfaces and address maps are contract-first and versioned. A breaking change needs a new MAJOR version, a changelog entry and a recorded decision.
6. Keep evidence environments apart: Renode results are not evidence of C910 timing, cache behaviour or cycle accuracy; a substitute CPU on FPGA is labelled a substitute; open-source flow results are implementation evidence, not production signoff. Say whether a result comes from Renode or from Verilator co-simulation.
7. Call the platform simulation the **Kritva Nexus Simulator** (workstream SIM), never emulation.
8. Do not commit IP, PDK files, models or tools whose licence or confidentiality terms forbid it; record source, licence and integration status instead.

## 3. Commits and pull requests

- Commit header: `type(scope): summary` (feat, fix, docs, refactor, test, build, ci, chore, perf, revert, security), at most 90 characters; an optional `[KOS-NEXUS-NNN]` suffix must match the footer.
- Exactly one footer line, `Task: KOS-NEXUS-NNN` or `Tasks: KOS-NEXUS-NNN, KOS-NEXUS-NNN`; a docs or chore commit that implements no task uses `Tasks: None (reason)`. Check with `python3 scripts/security/check_commit_format.py --range origin/main..HEAD`.
- Merge method is a merge commit. PRs use `.github/PULL_REQUEST_TEMPLATE.md`.
- Never add a `Claude-Session:` trailer or a claude.ai session link to a commit or PR description. `commit-message-check` blocks them.
- A commit that Claude helped write also updates [CLAUDE_SESSIONS.md](planning/CLAUDE_SESSIONS.md) in the same commit (a new row for a new session and date, otherwise the Work cell of that row), and ends with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` after the single `Task:` footer (NX-DEC-024, NX-DEC-028). The session identifier is plain text in that file only.
- Open a PR; do not push to `main`; do not force-push shared branches. Required checks: secret-scan, commit-message-check, pr-acceptance-gate and address-map-check (NX-DEC-032). With one owner, the author cannot independently approve: say so in the PR.

## 4. Secrets

Never commit credentials, tokens, keys, production data or personal data. If one is committed by mistake, tell the Security Owner (Dinesh) at once; removing it later does not make it safe. Do not add secret-scan allowlist entries to silence a finding; propose them to the owner.

## 5. Tests

`make check`, `make docs-check`, `make check-readme`, and the gates `lint`, `test-unit`, `test-integration`, `test-regression`, `test`, `acceptance`. An unimplemented target exits 3 (NOT_IMPLEMENTED); do not edit a target to exit 0 to make a gate pass, and never report one as a pass. A fixed defect adds a regression test.

## 6. Tags and milestones

Release tags are annotated SemVer (`vMAJOR.MINOR.PATCH`), created only after the approved merge. A milestone closes only through an approved `COMPLETION_RECORD.md`; a tag, a merge or a passing run does not close it.

## 7. README changes

Run `make check-readme` after editing README.md. It is a structural check only; review the content against the repository as well. The README stays a navigation page: link the document that owns a fact and write no task counts, percentages or gate states in it.

## 8. When unsure

Say what you do not know and ask Dinesh. Prefer leaving an item `OPEN` or `UNVERIFIED` to guessing.
