# 10. Coding Agent implementation order, bounded autonomy and mandatory reporting

> **Current external Coding Agent I/O restriction**: Browser reads GitHub, Code → Download ZIP for local source acquisition, Local Git only, and GitHub Web Edit to `SiliconForge_Working_SYNC.md` only. **No remote Git clone/fetch/pull/push, no agent-created GitHub PR, no source upload capability.** Source integration is a separate responsibility after an accessible ZIP/Patch Bundle is handed off. `docs/18_BROWSER_ZIP_CODING_AGENT_HANDOFF.md` and the top of Sync override Git/PR requirements below for this agent.

## Mission handed to the Coding Agent

Build and verify **SiliconForge** from this repository. The goal is a continuously recoverable, event-driven autonomous chip-development framework with deterministic Super Agent Runtime, independent domain owners powered by replaceable native coding harnesses, P-Stack practices inside owners, controlled real EDA execution, and objective evidence. The point is **maximum autonomy with minimal human interruption and explicit failure bounds**, not producing many files or endlessly running. The existing `simulator/` is solely an architecture demonstration.

### Required reading before editing

Read `README.md`, `AGENTS.md`, docs 00–09, `SiliconForge_Working_SYNC.md`, all schemas and route/policy config. Historical v2.2 docs are reference only. Create a concrete gap table against the v3 acceptance IDs. Do not silently reinterpret architecture or omit the user-harness native integration.

### Work mode

Proceed autonomously from A0 through successive milestones in order, respecting dependencies and human approval boundaries. Start with **A0 and its 18 tests**, then A1 Codex + Claude Code native integration, A2 toolchain, A3 real verification repair, A4 PPA/spec, A5 observability/PDCA, A6 hardening. Finish available work in each cycle; do not stop after plans, TODOs or scaffolds if objective tests can be implemented. If an EDA dependency fails, attempt only bounded authorized alternatives and record what was attempted, why it failed and reproducible next steps.

### Nonnegotiable acceptance rules

- A checkpoint that says 'test 19/19' must list test IDs, commands, actual execution environment and logs; no inherited claims from earlier chats.
- `simulation passed` requires running Verilator/cocotb and evidence; `formal passed` requires the proper checker; `PPA improved` requires comparable tool reports. Mock tests are named MOCK.
- A single integration test cannot replace all per-module contract gates.
- A failure should lead to diagnosis and bounded repair, never to quietly deleting failing tests, rewriting the golden model or spawning an entirely new framework.
- Do not conflate engineering Ticket completion, individual Agent Turn completion and EDA Job completion.
- Environment Owner, not each Domain Owner, controls EDA installation.
- No automatic public release or CI auto-merge without approved policy.

### Git workflow and sync channel

The public repo's `main` is the authoritative published baseline. **This Coding Agent** downloads it as ZIP via Chrome, works with Local Git branches only, and cannot upload source or create GitHub PRs. The Agent edits **only `SiliconForge_Working_SYNC.md` through the GitHub web editor**. A web edit of Sync is a status update, not a source-code commit. Any eventual GitHub source submission is done by a separate authorized Integrator who has actually received the ZIP/Patch artifact. **Never race-overwrite the Sync file**; re-read the live web page and resolve conflicts before saving. Refresh source before every status update. Append critical updates to the progress section (or use changelog file with immutable events for larger history), don't rewrite passed/failed history.

Mandatory sync times:
1. On starting a coding session (set mission state and plan).
2. After each meaningful code commit, acceptance test or environment status change.
3. On true BLOCKED/WAITING_FOR_HUMAN/PAUSED transitions immediately.
4. At least every 15 minutes during active work with a heartbeat (but never an unbounded commit loop if no progress).
5. Before ending the current turn, with exact next executable action.

Maintain ISO UTC `updated_at_utc` separate from `last_progress_at_utc`. Heartbeat cannot refresh progress timestamp unless objective progress occurred. Do not imply a status-polling service exists merely because the markdown is present. External watchdog will read it; a developer agent must actually commit updates while working.

### Required output after each milestone

```
Phase: A0..A6
Mission state: ACTIVE / WAITING_FOR_TOOL / BLOCKED / WAITING_FOR_HUMAN / VERIFIED
Commit / PR / branch: exact IDs
Implemented: bullet list with file paths
Execution: commands actually run; test IDs PASS/FAIL/BLOCKED/NOT_RUN
Evidence: reproducible hashes / logs / screenshots / tool versions
Budget and resource usage: model tokens, tool wall time where available
Risks and policy requests: narrowly scoped
Next action: one executable step and owner
```

### Canonical A0 execution task

1. Review current `src/siliconforge/runtime.py` and tests; identify which A0 IDs are truly proven. Preserve functioning behavior.
2. Finish event envelope JSON Schema validation; verified identity at ingress boundary, direct route and actor permissions; durable Owner ticket; delivery fencing; atomic decision/next-events; payload size/rate limits; no-progress watchdog; request state machine; read-side replay.
3. Add explicit A0 tests for every A0-01..18, including process restart against file-backed SQLite. Run standard library tests and write machine-readable evidence JSON with commit hash.
4. Review Source/Ingress trust so no external untrusted endpoint is writable without proper auth. A0 in-process mock may remain local only.
5. Demonstrate user harness is not needed for domain routing. Do not build GUI or chat terminal in A0.
6. Record final LOCAL results in Sync, including ZIP/Patch artifact hash and whether transfer to an Integrator actually occurred. Do not claim a PR or remote source update. Start A1 only when relevant A0 requirements are truly achieved and the next stage is accessible.

### No false-block policy

If a requested cloud service cannot be reached, continue on local A0 work where possible. Record a true blocker with evidence and a specific approval/input request only if the milestone **cannot** continue. Do not request the human to relay every Owner/Worker status; peers communicate through Runtime. Local worktree/code changes must stay within the authorized scope. GitHub remote source must be reported NOT_INTEGRATED until an authorized Integrator verifies actual delivered artifact bytes.

### First message to another Coding Agent (copyable)

> Read `AGENTS.md`, `docs/00_MISSION_AND_BOUNDARIES.md`, `docs/01_ARCHITECTURE_AND_OWNERSHIP.md`, `docs/02_EVENT_RUNTIME_PROTOCOL.md`, `docs/08_IMPLEMENTATION_PLAN.md`, `docs/09_ACCEPTANCE_TEST_MATRIX.md`, `docs/10_CODING_AGENT_EXECUTION_ORDER.md`, and `SiliconForge_Working_SYNC.md`. Implement and objectively verify milestones in order. The Super Agent Runtime handles event lifecycle while each Domain Owner makes domain engineering decisions through P-Stack skills. The user talks to SiliconForge through native Codex/Claude Code + MCP/Skills, not a custom CLI. Keep EDA Environment ownership centralized and evidence gates independent. Update and commit `SiliconForge_Working_SYNC.md` on progress and every 15 minutes during active work. Start by auditing A0 IDs and implementing missing ones, do not stop after a plan. Never claim real EDA from mock tests. Use a PR and report exact commits/test evidence.

## v3.1 mandatory execution amendment

**This repository is now the canonical home for all SiliconForge execution instructions.** Follow [CODING_AGENT_START_HERE.md](../CODING_AGENT_START_HERE.md), [14｜Exploration Architecture](14_PARALLEL_EXPLORATION_ARCHITECTURE.md), [15｜Acceptance](15_PARALLEL_EXPLORATION_ACCEPTANCE.md), [16｜Implementation](16_PARALLEL_EXPLORATION_IMPLEMENTATION.md). Do not create a second repository, fetch alternative SiliconForge source trees, or start a new project. The current repository contains every required implementation entrypoint.

Do not model RTL, Verification, Formal, PPA, Spec or any Domain Role as a globally single Owner instance. The deterministic Runtime may run many instances of the same Role, independently scoped to `exploration_id`, `branch_id`, `ticket_id` and `lease_epoch`. P-Stack `arena` and `swarm` stay inside each Owner Instance, while Runtime maintains the inter-branch DAG, routing, budgets, stop conditions and durable state.

Implement A0X immediately after core A0: Branch Registry, ID schema, Router/Outbox Fanout, lease fencing, lineage and bounded Fork admission. Implement A3X for real Git Branch/Worktree/Owner instance isolation, including direct peer requests and model/harness switching. Implement A4X for the real three-way APB CRC32 exploration with independent EDA evidence and nested fork; select Pareto candidates and require an explicit MergeProposal, conflict handling, a new merge SHA and complete re-gate. Implement A5X/A6X for visual DAG/PDCA and multi-branch reliability.

**Acceptance:** existing 60 A0–A6 cases + 20 E cases = **80 required**. E20 must prove three independent paths genuinely overlap in time, one descendant fork exists, at least one failure was contained, and all final results use real tool fingerprints. Source-branch `PASS` never transfers to merge result. Quotas bound all branches; lack of measurable engineering progress stops further expansion. Continue autonomously within policies, record exact commands, commits, logs and EDA/environment digests; update the canonical `SiliconForge_Working_SYNC.md` every meaningful transition and at least every 15 minutes while active.

When blocked, give a narrow explicit reason and a next executable action. Do not ask the human to manually relay normal peer results. Do not declare completion from mock or textual claims.



## Standalone enforcement

Before reporting any milestone, execute `python -m unittest discover -s tests -v` from a clean **GitHub Download ZIP extract** of this repository (with necessary local environment setup) and verify the standalone checks in `docs/17_STANDALONE_REPOSITORY_CONTRACT.md`. No source, test or instruction may be fetched from another SiliconForge repository as a prerequisite. All future work and status must remain here.
