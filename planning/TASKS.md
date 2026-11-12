# Tasks: kritva-nexus

Task IDs use the prefix `KOS-NEXUS`. Nexus is outside the Kritva Program V2 plan and is planned for the V3 plan: it is not registered in kritva-program, no task here is baselined and no task carries a weight, credit or accepted progress. A task earns acceptance only through the owner's approval bound to immutable evidence, never from this file. Status vocabulary: NOT_STARTED, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, CHANGES_REQUESTED, ACCEPTED, DEFERRED, CANCELLED. The owner and reviewer of every task is Dinesh (interim, not independent).

Stage 1 is the smallest set needed for the Nexus planning-baseline proposal. Further candidates live in [TASK_CATALOGUE.md](TASK_CATALOGUE.md) and are promoted into this file one batch at a time after the owner accepts them. Registered IDs are never renumbered or reused; a task that is no longer needed becomes CANCELLED or DEFERRED.

| Task | Title | Status | Milestone | Acceptance |
|---|---|---|---|---|
| KOS-NEXUS-001 | Establish repository structure and engineering conventions | NOT_STARTED (proposed) | NX-M0 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md); [task](../tasks/KOS-NEXUS-001/TASK.md) |
| KOS-NEXUS-006 | Consolidate top-level system architecture | ACCEPTED (accepted by the owner on 2026-11-09 as a repository task only; no weight or credit; proposed, not baselined) | NX-M1 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md); [task](../tasks/KOS-NEXUS-006/TASK.md) |
| KOS-NEXUS-007 | Define application AXI and memory access architecture | IN_PROGRESS (started by the owner; proposed, not baselined) | NX-M1 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md); [task](../tasks/KOS-NEXUS-007/TASK.md) |
| KOS-NEXUS-008 | Define memory and address-map architecture | IN_PROGRESS (started by the owner; proposed, not baselined) | NX-M1 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md); [task](../tasks/KOS-NEXUS-008/TASK.md) |
| KOS-NEXUS-084 | Establish requirements register and architecture decision records | ACCEPTED (accepted by the owner on 2026-11-07 as a repository task only; no weight or credit; proposed, not baselined; new task) | NX-M1 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md); [task](../tasks/KOS-NEXUS-084/TASK.md) |
| KOS-NEXUS-085 | Write the Nexus preliminary datasheet | IN_PROGRESS (started by the owner; proposed, not baselined; new task) | NX-M1 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md); [task](../tasks/KOS-NEXUS-085/TASK.md) |
| KOS-NEXUS-020 | Define RTL coding and module conventions | IN_PROGRESS (started by the owner; proposed, not baselined) | NX-M1 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md); [task](../tasks/KOS-NEXUS-020/TASK.md) |
| KOS-NEXUS-018 | Establish external and internal IP inventory | NOT_STARTED (proposed) | NX-M2 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md); [task](../tasks/KOS-NEXUS-018/TASK.md) |
| KOS-NEXUS-019 | Define IP integration and licensing status | NOT_STARTED (proposed) | NX-M2 | [ACCEPTANCE_CRITERIA.md](../ACCEPTANCE_CRITERIA.md); [task](../tasks/KOS-NEXUS-019/TASK.md) |

Dependency: the central baseline has no dependency field and Nexus has no central baseline, so dependencies are recorded in each `tasks/*/TASK.md`. A task moves out of NOT_STARTED only when the owner starts it. A commit that implements a task carries the footer `Task: KOS-NEXUS-nnn`.
