# NX-DEC-020: Peripheral instance counts

| Property | Value |
|---|---|
| Label | SELECTED |
| Decided by | Dinesh, as relayed in the A0 discussion; confirmed by approval of the pull request that adds this record |
| Date | Not recorded (the decision predates this repository) |
| Requirements | NX-REQ-019, NX-REQ-020, NX-REQ-021, NX-REQ-022, NX-REQ-023, NX-REQ-024, NX-REQ-025, NX-REQ-026 |
| Task | [KOS-NEXUS-084](../tasks/KOS-NEXUS-084/TASK.md) |
| Evidence | Owner wording as relayed; the A0 draft is imported at [A0_INTEGRATION_DRAFT.md](../architecture/A0_INTEGRATION_DRAFT.md) (a reconstruction, not an original document) |

Context: Fix the number of instances of each general peripheral: 16 PWM, 32 GPIO, 4 general-purpose timers, 4 UART, 4 I2C masters, 1 SPI master, 1 SPI slave and 2 I2S masters.

Alternatives considered: Other counts; no alternatives recorded.

Rationale: Owner stated the counts. No further rationale recorded. Grouped in one record because the owner stated them together; the counts are SELECTED, nothing else about the peripherals is.

Consequences: Features, FIFO depths, clocking and register maps of each peripheral are not decided here.

Owner wording: Counts as listed in the Context line.

## History

| Date | Change |
|---|---|
| 2026-11-07 | Record created from the A0 discussion for KOS-NEXUS-084 with label SELECTED. |
