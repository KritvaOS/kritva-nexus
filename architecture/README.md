# Nexus Architecture Documents

| Property | Value |
|---|---|
| Document ID | KOS-NEXUS-ARCH-INDEX |
| Repository | `KritvaOS/kritva-nexus` |
| Document Type | Architecture |
| Status | DRAFT |
| Owner | Dinesh |
| Reviewer / Approver | Dinesh (interim, not independent) |
| Version | 0.1.0-draft |
| Last Updated | 2026-11-08 |
| Authority | REFERENCE |
| Related Tasks / Milestones | KOS-NEXUS-006; NX-M1 |
| Related Documents | [requirements](../requirements/REQUIREMENTS.md); [decisions](../decisions/DECISIONS.md) |

## Purpose

This is the index of the architecture documents in this repository. It lists each document, its status and its authority, so a reader knows which one to open and which one is only an input. It states no architecture itself.

## Documents

| Document | Content | Authority | Status |
|---|---|---|---|
| [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) | Consolidated top-level system architecture: domains, interface register and open-issues register | INPUT (not AUTHORITATIVE until the owner approves it) | DRAFT |
| [A0_INTEGRATION_DRAFT.md](A0_INTEGRATION_DRAFT.md) | A0 integration draft imported from a discussion; a reconstruction, not an original document; changed by dated addenda only | INPUT | PROPOSED |

## Reading order and rules

Read the system architecture first; use the A0 draft only for detail the system architecture leaves out, and treat that detail as PROPOSED or OPEN. Where a document differs from the [requirements register](../requirements/REQUIREMENTS.md) or a [decision record](../decisions/DECISIONS.md), the register or record wins. Interconnect, memory and address-map documents (KOS-NEXUS-007 and 008) are added to this index when they exist.
