# NX-DEC-032: address-map-check is a required check

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's answer "Keep address-map-check as required check", stated in the project chat on 2026-11-13 and relayed to this repository; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-13 |
| Requirements | None (repository working rule) |
| Task | [KOS-NEXUS-008](../tasks/KOS-NEXUS-008/TASK.md) |
| Evidence | `.github/workflows/address-map-check.yml`; `scripts/check_address_maps.py`; the required-check lists of [AGENTS.md](../AGENTS.md) and [CONTRIBUTING.md](../CONTRIBUTING.md) |

Context: The address-map-check workflow runs the checker tests and the checker on every pull request and push to main, and until now it was not one of the required checks (secret-scan, commit-message-check, pr-acceptance-gate). The owner decided to keep it as a required check.

Decisions:

1. A pull request merges only when address-map-check passes, in addition to the three existing required checks. Owner: keep address-map-check as required check.
2. AGENTS.md, CONTRIBUTING.md and README.md list the check as required. The branch-protection setting is a GitHub repository setting that the pull request cannot change: the owner or an administrator adds the status check `address-map-check` to the protection of `main`, and until that is done the requirement is documented and not enforced by GitHub.
3. The check is structural. It does not show that a base, size or attribute is right, and a PASS is not an approval.

Alternatives considered: Leave it as a non-required check that reviewers read. The owner chose to require it.

Rationale: Owner answer as listed. No further rationale was recorded.

Consequences: A change to the address maps, to the checker, to the register identifiers or to the tables of ADDRESS_MAP.md that breaks the check blocks the merge. A pull request that touches nothing the check reads still runs it, because the workflow has no path filter. If the workflow is renamed, the required status check name must change with it.

## History

| Date | Change |
|---|---|
| 2026-11-13 | Record created with label SELECTED. |
