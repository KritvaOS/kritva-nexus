# Git Commit Step: kritva-nexus

1. `git switch -c <type>/<short-name>` from an up-to-date `main`.
2. Commit with the format below; one task per commit.
3. `make check` (and the applicable gates), then push the branch and open a PR.
4. Merge after required checks and the owner's approval on the current head. Merge method: merge commit.
5. Tag only after the approved merge: `git tag -a vX.Y.Z -m "..."`; a tag does not close a milestone.

```text
type(scope): summary of at most 90 characters [optional KOS-NEXUS-NNN]

Task: KOS-NEXUS-001
```

Several tasks: `Tasks: KOS-NEXUS-001, KOS-NEXUS-006`. A docs or chore commit that implements no task: `Tasks: None (reason)`. Use `.github/PULL_REQUEST_TEMPLATE.md` for the PR text. No AI-session trailer or link in any commit.
