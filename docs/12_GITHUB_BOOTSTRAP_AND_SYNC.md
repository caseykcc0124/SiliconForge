# 12. Public repository and Git-backed agent synchronization

Canonical repository: https://github.com/caseykcc0124/SiliconForge
Canonical branch: main

## Working protocol
The single machine-readable status entry is SiliconForge_Working_SYNC.md on main. Coding Agent updates it on every meaningful engineering transition and at least every 15 minutes during active execution. Heartbeats are independent of real progress; never set last_progress_at_utc solely because a status update was written.

Changes include exact commit/PR link, actually executed commands, real passed/failed/not-run counts, artifacts and hashes, active owner, current workstream, blocker ID, actionable next step, time UTC and approval needed. Preserve recent audit entries. Keep changes to the working file focused; do not overwrite another concurrent owner's status without checking branch head.

## Commit workflow
Work in branch/worktree for substantive implementation; run unit tests, create evidence and open PR for review where mandated. The sync file on main may be updated by authorized agent or synchronization service. Do not force-push main or rewrite journal evidence. Ensure merge and CI proof before claiming a milestone.

## Status reader
Read canonical main synchronization file, check updated_at_utc and last_progress_at_utc, compare latest commit and actual repository changes, identify stale/no-progress work. Do not treat an agent's prose report as verified acceptance. The Coding Agent may autonomously resolve authorized technical issues but only human can approve scope change, unapproved external service/PDK or public publication.

## Bootstrapping
Initial repository content is a **reference and specification baseline**, not production-autonomous EDA. Review docs/09 and docs/10, run tests on a clean clone, then complete A0 acceptance and proceed through A1–A6. First sync can be NOT_STARTED despite commits that upload docs. Do not mistake docs upload for functional progress.

## Collaboration
Use PRs/Issues for substantial design disputes and review, not human as peer message ferry. Use an Event Journal in the Runtime for live engineering state; Git status file is a higher-level durable summary, not a replacement for event storage.
