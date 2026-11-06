# KOS-NEXUS-001 Establish repository structure and engineering conventions

| Property | Value |
|---|---|
| Milestone | NX-M0 |
| Status | NOT_STARTED (proposed; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | none |
| Workstream | INFRA |
| Readiness | IMPLEMENTABLE |
| Proposal status | PROPOSED |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007. |
| Deliverables | The files above. The Makefile (kritva-sense pattern) defines the common targets; each target not yet implemented prints that it is not implemented and exits 3. |
| Acceptance evidence | None yet. Merge commit SHA, pull request, CI run IDs, review record. Evidence type: software. |

Objective: Give the repository the files and checks that the V2 Acceptance Standard requires of every Kritva repository, so that later work can be reviewed and reported.

Scope: `README.md`, `AGENTS.md`, `ACCEPTANCE_CRITERIA.md`, `SECURITY.md`, `CONTRIBUTING.md`, `LICENSE`, `Makefile`, `.gitignore`, `.github/CODEOWNERS`, `.github/kritva-gate.json`, `.github/PULL_REQUEST_TEMPLATE.md`, the workflows `secret-scan`, `commit-message-check`, `pr-acceptance-gate` and `readme-check`, `scripts/` (docs_check, check_readme, security and pipeline checks), `tests/` for those scripts, and `planning/` with TASKS, MILESTONE, MILESTONE_STATUS, REVIEW_CHECKLIST, GIT_COMMIT_STEP and CHANGELOG.

Out of scope: Tool environments (Icarus, Verilator, Yosys, OpenLane, Renode, FPGA), RTL, other CI workflows, `status/status.json` (Nexus is not registered in kritva-program), any directory for unbaselined work.

Inputs: kritva-program `ACCEPTANCE_STANDARD.md`, README and document-header standards, and the common files of kritva-sense (the format source).

Verification method: Review against the standard; `make check` once implemented; README check; secret-scan and commit-message-check workflows once present.

Progress note: Drafts of `README.md`, `AGENTS.md` and `ACCEPTANCE_CRITERIA.md` exist in the working tree and are not committed. The state stays `NOT_STARTED` until Dinesh starts the task.
