# Review Checklist: kritva-nexus

- [ ] Task ID and acceptance criteria exist and are unchanged by this PR (or changed under change control).
- [ ] Commit headers follow `type(scope): summary` and each has exactly one `Task:` or `Tasks:` footer (`Tasks: None (reason)` only on docs or chore). The PR uses the PR template.
- [ ] No AI-session trailer, link, secret or production data.
- [ ] Required checks passed on the exact PR head: secret-scan, commit-message-check, plus the gates that apply.
- [ ] No unimplemented gate is reported as a pass (exit 3 is NOT_IMPLEMENTED, never PASS).
- [ ] Each architecture decision is labelled SELECTED, PROPOSED or OPEN; none is promoted to SELECTED without the owner's recorded decision.
- [ ] Evidence names the target (RTL, FPGA or ASIC), tool version, configuration revision, commit SHA and CI run ID.
- [ ] Interfaces and address maps are versioned; a breaking change has a MAJOR bump, changelog entry and recorded decision.
- [ ] Changelog and documentation updated; evidence references are commit SHAs and CI run IDs.
- [ ] Reviewer is Dinesh (interim, not independent); this is stated in the PR, and no approval is claimed that was not given on the current head.
- [ ] Nexus stays outside the V2 plan: no kritva-program registration, `status/status.json`, program milestone mapping or progress number is added.
