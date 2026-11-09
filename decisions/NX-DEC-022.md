# NX-DEC-022: Behaviour of the C910-to-APB path

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | The owner's answers to eight questions on the path behaviour, stated in the project chat on 2026-11-09 and relayed to this repository; confirmed by approval of the pull request that adds this record |
| Date | 2026-11-09 |
| Requirements | NX-REQ-068, NX-REQ-069, NX-REQ-070, NX-REQ-071, NX-REQ-072, NX-REQ-073, NX-REQ-074, NX-REQ-075 |
| Task | [KOS-NEXUS-007](../tasks/KOS-NEXUS-007/TASK.md) |
| Evidence | Proposals and trade-offs in [INTERCONNECT_SPECIFICATION.md](../architecture/INTERCONNECT_SPECIFICATION.md) section 3; the route is NX-DEC-021 |

Context: After the owner chose the route for NX-ARCH-GAP-001 (NX-DEC-021), the behaviour of the path was still PROPOSED. The owner was asked eight questions, one per area of section 3.1, and answered as recorded below. Grouped in one record because the answers were given together for one path; each answer has its own requirement.

Decisions:

1. Error mapping: an unmapped address returns DECERR, a denied access returns SLVERR and an APB PSLVERR returns SLVERR, each reaching the C910 as a bus error. Owner: confirm as proposed.
2. Timeout: an access to a hung APB target (one that never asserts PREADY) times out and returns SLVERR. The numeric value, the recovery and whether a timed-out access can complete later are not decided. Owner: timeout returns SLVERR; value OPEN.
3. Masters: only the C910 uses the path. Other masters are out of scope. Owner: C910 only.
4. Bridge structure: one AXI fabric bridge performs both the 128-bit to 64-bit width conversion and the clock-domain crossing, with AXI4 on both sides. Owner: one bridge, AXI4 both sides.
5. Access control: a trusted address-window policy with default-deny, checked before any APB access is issued, with allowed AxPROT attributes set per window; secure resources are unreachable and the application domain cannot change the policy. Owner: confirm as proposed.
6. Ordering: device accesses are strongly ordered per APB target with one outstanding access per target; accesses to different targets may progress independently; buffering limits and backpressure are defined in the bridge specification. Owner: confirm as proposed.
7. Bursts: only single-beat accesses are supported; a burst longer than one beat and any FIXED or WRAP burst returns SLVERR. Owner: single-beat only.
8. Reset: an in-flight access at bridge or peripheral reset completes with SLVERR, and no new access is issued until both sides are out of reset. Owner: confirm as proposed.

Alternatives considered: As set out in the interconnect specification section 3; the owner chose the recommended option in each case except item 4, where the recommendation was to leave the structure OPEN and the owner chose one bridge.

Rationale: Owner answers as listed. No further rationale was recorded.

Consequences: With NX-DEC-021 the path is defined end to end. NX-REQ-027 is superseded by NX-REQ-067 to NX-REQ-075 and NX-ARCH-GAP-001 is closed. Residual items stay OPEN under NX-ARCH-OI-033 (timeout value, recovery and late completion) and NX-ARCH-OI-034 (bridge buffering limits, ID handling, backpressure and the APB protocol version). The route stays subject to the C910 configuration check (NX-ARCH-OI-001). Verification of the path is planned in RTL simulation and has not been run.

## History

| Date | Change |
|---|---|
| 2026-11-09 | Record created for KOS-NEXUS-007 with label SELECTED. |
