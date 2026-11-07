# 12. Public repository and Git-backed agent synchronization

Canonical repository: https://github.com/caseykcc0124/SiliconForge
Canonical branch: main

## Current external Coding Agent access

The current Coding Agent cannot Git Clone/Pull/Push on GitHub. It may read GitHub files through Chrome/Computer Use; obtain the complete Repository through **Code → Download ZIP**; use Git locally after extracting the ZIP; and use the GitHub **web editor only for `SiliconForge_Working_SYNC.md`**. Remote source integration and PRs require a distinct authorized Integrator and actual code artifact transfer. See `docs/18_BROWSER_ZIP_CODING_AGENT_HANDOFF.md`.

## Working protocol
The single machine-readable status entry is SiliconForge_Working_SYNC.md on main. Coding Agent updates it on every meaningful engineering transition and at least every 15 minutes during active execution. Heartbeats are independent of real progress; never set last_progress_at_utc solely because a status update was written.

Changes include **LOCAL Git commit clearly distinguished from any verified remote GitHub source commit or PR**, actually executed commands, real passed/failed/not-run counts, artifacts and hashes, active owner, current workstream, blocker ID, actionable next step, time UTC and approval needed. Preserve recent audit entries. Keep changes to the working file focused; do not overwrite another concurrent owner's status without checking branch head.

## Commit workflow
For this Coding Agent, work in **Local** Git branches/worktrees, run tests and prepare a ZIP/Patch artifact; **do not attempt a GitHub PR, Push or mass source edit**. The Agent edits only the Sync file on GitHub through the web browser. A separate GitHub Integrator can submit an actual PR once it has received and reviewed the artifact. Do not force-push main or rewrite journal evidence. Ensure merge and CI proof before claiming a milestone.

## Status reader
Read canonical main synchronization file, check updated_at_utc and last_progress_at_utc, compare latest commit and actual repository changes, identify stale/no-progress work. Do not treat an agent's prose report as verified acceptance. The Coding Agent may autonomously resolve authorized technical issues but only human can approve scope change, unapproved external service/PDK or public publication.

## Bootstrapping
Initial repository content is a **reference and specification baseline**, not production-autonomous EDA. Review docs/09 and docs/10 in the browser, download GitHub ZIP to Local, run tests on the extracted snapshot, then complete A0 acceptance and proceed through A1–A6. First sync can be NOT_STARTED despite commits that upload docs. Do not mistake docs upload for functional progress.

## Collaboration
Use PRs/Issues for substantial design disputes and review, not human as peer message ferry. Use an Event Journal in the Runtime for live engineering state; Git status file is a higher-level durable summary, not a replacement for event storage.
