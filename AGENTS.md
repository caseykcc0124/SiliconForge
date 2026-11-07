# SiliconForge Coding Agent Contract

> **External Coding Agent environment override:** The current remote Coding Agent reads GitHub with Chrome/Computer Use, downloads source through GitHub's ZIP interface, develops with LOCAL Git only, and can edit on GitHub **only** `SiliconForge_Working_SYNC.md` using the Web UI. It cannot use GitHub Git Clone/Pull/Push, submit PRs, or upload arbitrary source files. For its initial instruction read the Sync file directly; AGENTS.md is not assumed auto-loaded remotely. See `docs/18_BROWSER_ZIP_CODING_AGENT_HANDOFF.md`.

Read in order: README.md, docs/00_MISSION_AND_BOUNDARIES.md, docs/01_ARCHITECTURE_AND_OWNERSHIP.md, docs/02_EVENT_RUNTIME_PROTOCOL.md, docs/09_ACCEPTANCE_TEST_MATRIX.md, docs/10_CODING_AGENT_EXECUTION_ORDER.md and SiliconForge_Working_SYNC.md. Other numbered specifications are normative within their domain. Docs v3 supersede historical v2.x docs.

## Nonnegotiable architecture

- Main Agent is a human communication interface, **not** a technical arbiter or mandatory event hop.
- Engineering events route deterministically to the owning domain. Owners choose P-Stack methods and communicate with peers via durable events.
- Persistent Runtime is independent of user Codex / Claude Code sessions. NO custom chat CLI.
- EDA Environment Owner owns image versions, PDK/license compliance and reproducible toolchains; other owners cannot install/upgrade tools on their own.
- PASS requires actual tool evidence with matching design/spec/constraints/toolchain fingerprints, never narrative claims.
- Do not modify rules, tests, scope, budgets, workflows or permissions just to make a run pass.
- No external publication or unauthorized external calls; no importing proprietary artifacts into a public repo.
- No autonomous modification of the Super Agent Runtime / control plane from an engineering owner.

## Work pattern

1. Inspect repository and sync state. Avoid parallel overlapping edits; preserve existing work.
2. Make a bounded plan for the current milestone, then work autonomously through it.
3. Implement and **run** tests. Report executed/not executed separately; attach exact commands, counts, commits, environment and evidence paths.
4. If blocked, troubleshoot using available authorized tools and bounded retries. Escalate only a true policy/engineering ambiguity or budget violation.
5. Update `SiliconForge_Working_SYNC.md` on start, after each meaningful gate/commit/obstacle, and at least every 15 minutes while actively running; keep timestamps honest. Avoid empty heartbeat-only commits more frequently than 15 minutes.
6. Never claim implementation of later milestones from mock/unit tests. Each milestone has independent gates.
7. Work with Git branches and commits **only inside the local workspace** obtained through a GitHub ZIP download. The external agent cannot Push, open PRs, or update other GitHub source files. It uses GitHub Browser editing only for the authoritative Sync file; source integration/PR belongs to a separate authorized Integrator after actual artifact bytes have been transferred. Never represent a local commit as a remote commit.

## Reply to human

Always include phase, actual implemented changes, **local Git commit distinguished from verified GitHub source commit**, commands/tests and pass/fail count, concrete evidence, resource usage when available, remaining risks, approvals required, and next executable work. Explicitly differentiate MOCK, STUB, EXPERIMENTAL and REAL EDA.

## Mandatory v3.1: Multi-Owner Parallel Exploration

Before coding or architectural decisions, read `CODING_AGENT_START_HERE.md`, `docs/14_PARALLEL_EXPLORATION_ARCHITECTURE.md`, `docs/15_PARALLEL_EXPLORATION_ACCEPTANCE.md` and `docs/16_PARALLEL_EXPLORATION_IMPLEMENTATION.md`. These extend, and do not replace, the A0–A6 baseline. **Existing 60 required cases + E01–E20 = 80 required cases.**

- Domain Role is not a singleton Owner. The Runtime instantiates multiple Owner Instances with independent work leases per exploration branch and Ticket.
- P-Stack stays inside each Domain Owner Instance. The Runtime, not Main, maintains Branch Lineage DAG, event fan-out, fork admission, budgets, watchdog, recovery and merge provenance.
- Same Requirement can yield Performance, Low Power and Area candidates concurrently, each isolated with real Git branch/worktree and separately pinned Simulation, Formal, Synthesis and PPA evidence.
- Every accepted merge yields a new SHA requiring fresh relevant gates. An Owner must not copy another candidate's PASS, auto-promote a candidate, force main, or use false PPA comparability.
- Branch spawn must have bounded explicit hypothesis, stop criterion and quota. One blocked branch must not stop healthy branches.
- Implement A0X/A3X/A4X/A5X/A6X at the milestones specified by docs/16. Never create another framework or overwrite the existing Working Sync state.



## Standalone repository source-of-truth (mandatory)

Use only the current repository for SiliconForge source code, specifications, contracts, skills, acceptance trackers, Git activity and Working Sync. There is no alternate SiliconForge repository to clone or synchronize. Read `docs/17_STANDALONE_REPOSITORY_CONTRACT.md`; run `python -m unittest discover -s tests -v` before milestone claims. External Codex/Claude and open EDA tools are execution dependencies, not cross-repository SiliconForge source dependencies. All eventual remote changes and PRs belong here, but the external Coding Agent itself is **not** expected to create PRs or push changes. It must hand off an accessible ZIP/Patch artifact to an authorized Integrator; if no handoff channel exists, explicitly report pending transfer.
