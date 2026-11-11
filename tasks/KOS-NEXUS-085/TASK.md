# KOS-NEXUS-085 Write the Nexus preliminary datasheet

| Property | Value |
|---|---|
| Milestone | NX-M1 |
| Status | IN_PROGRESS (started by Dinesh on 2026-11-11; proposed, not baselined; Nexus is outside the V2 plan and is not registered in kritva-program) |
| Weight | none (no baseline; Nexus is planned for the V3 plan) |
| Depends on | KOS-NEXUS-006, KOS-NEXUS-007, KOS-NEXUS-084 |
| Workstream | ARCH |
| Readiness | PLANNABLE |
| Proposal status | PROPOSED |
| Owner and reviewer | Dinesh (interim, not independent) |
| Acceptance | [ACCEPTANCE_CRITERIA.md](../../ACCEPTANCE_CRITERIA.md): AC-010 and AC-011 apply to the label and traceability of every datasheet row; no datasheet-specific criterion exists yet. The datasheet has its own review and approval record; the approval of the RTL standard (NX-DEC-023) does not cover it. |
| Deliverables | `datasheet/NEXUS_DATASHEET.md` (single editable source) and `datasheet/nexus_block_diagram.svg`. A PDF is generated from the source and is not committed. |
| Acceptance evidence | None yet. Merge commit SHA, pull request, review record. Evidence type: software. |

Objective: Give readers a 3 to 6 page preliminary planning datasheet that lists the Nexus blocks, a consolidated feature summary and the individual features of each block, derived from the requirements register and decision records.

Agreed format (reviewed with ChatGPT before writing):

- Folder `datasheet/`, source `NEXUS_DATASHEET.md` with the Kritva document header (ID KOS-NEXUS-DS-001, Status DRAFT, Authority DERIVED), diagram `nexus_block_diagram.svg`. The folder is added in the pull request that adds the first file, not before.
- The document states that it is a derived, non-authoritative summary and that the requirements register and approved decision records win on any conflict. It carries the title and footer "PRELIMINARY PLANNING DATASHEET, NOT A PRODUCT SPECIFICATION" and names the source commit it summarises.
- Every feature row has the NX-REQ identifiers it restates, its label (SELECTED, PROPOSED or OPEN) and a value or description that adds nothing to the register. A row without a settled value reads TBD (OPEN) or PRELIMINARY (PROPOSED). The wording is "planned" or "proposed", not an unqualified "supports". No measured, timing, power, area, FPGA, achieved-performance or IP-availability claim appears; a planning figure is labelled theoretical or proposed and cites its requirement.
- Layout, 3 to 6 pages, a limit and not a target: page 1 overview, consolidated feature summary and block diagram; page 2 application CPU, interconnect and memory; page 3 AI and vision; page 4 multimedia, connectivity and peripherals; page 5 security and always-on, clock, reset and power; page 6 open items, status disclaimer and revision history.
- The PDF is generated on demand and in CI to check the page count (failing above 6 pages), and attached to a release with the source commit recorded; it is not committed to `main`. The generation script and CI check live under owner-only paths and are a later step, not part of the first datasheet pull request.

Open items stay visible: the address-map and address-width gaps (NX-ARCH-GAP-002 and NX-ARCH-GAP-003) are not hidden in the open-items page; every dependent feature shows as OPEN until KOS-NEXUS-008 settles them, and the datasheet is updated then.

Out of scope: the PDF generation script and CI check, any change to a requirement or decision, any new technical value, and any distribution as an approved document before its own approval record exists.

Inputs: [architecture/SYSTEM_ARCHITECTURE.md](../../architecture/SYSTEM_ARCHITECTURE.md), [architecture/INTERCONNECT_SPECIFICATION.md](../../architecture/INTERCONNECT_SPECIFICATION.md), [requirements/REQUIREMENTS.md](../../requirements/REQUIREMENTS.md), [decisions/DECISIONS.md](../../decisions/DECISIONS.md).

Verification method: Review that every row traces to an NX-REQ ID with the register label and adds no value; page count checked once the generator exists.

Progress note: the first draft is [datasheet/NEXUS_DATASHEET.md](../../datasheet/NEXUS_DATASHEET.md) with the block diagram [datasheet/nexus_block_diagram.svg](../../datasheet/nexus_block_diagram.svg), linked from the README. A test render fitted six A4 pages. It has no approval record, the PDF generation script and CI page-count check are still to do under owner-only paths, and the task stays IN_PROGRESS until the owner moves it to review.
