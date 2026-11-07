# 08. Implementation plan, milestones and dependencies

Milestones are objective gates, not time promises. Within authorized scope Coding Agent should implement, test, fix and continue automatically, rather than repeatedly asking the user for routine decisions.

| Gate | Build | Evidence to close |
|---|---|---|
| A0 | SQLite WAL immutable events, idempotence, outbox, routing, leases, bounded retry, peer, watchdog, ticket replay | All A0-01…A0-18 executed PASS on clean checkout |
| A1 | Native Codex/Claude skills and authenticated MCP gateway, Harness Adapter, notification persistence | All A1-01…A1-08, no custom chat CLI |
| A2 | EDA Environment Owner, pinned profile, APB CRC32 RTL and golden model, cocotb/Verilator, formal, synthesis | Real commands, source/profiles hashes, complete A2 tests |
| A3 | Verification and RTL Codex Owners, waveform-TDD, peer repair, independent gate, restart | Actual injected RTL defect fixed with Main offline, A3 all PASS |
| A4 | Spec revision impact + PPA Owner bounded Arena; OpenROAD | A4 actual candidates, formal correctness, no stale release |
| A5 | Read-only Dashboard, audit traces, Notification Outbox, PDCA A/B sandbox | A5 all PASS, no production auto-promotion |
| A6 | Multi-IP chaos, security, quotas, restart reliability, distribution | A6 all PASS on real integrated system |

## Dependencies
A0 blocks all later gate closures. A1 harness and A2 EDA preparations can proceed in separate worktrees once A0 contracts are frozen. A3 needs A1 auth and A2 real baseline. A4 relies on A3 independent integrated evidence. A5 read projections can begin early, but it closes after real traces exist. A6 only tests frozen credible acceptance.

## Per-work unit deliverables
Description/ADR, code commit, actual executed test counts and commands, logs and artifacts, environment/version hashes, known risks, next work and updated SiliconForge_Working_SYNC.md. Distinguish implemented, simulated and proposed. No end-to-end 'PASS' from Mock EDA.

## Architecture economy
Initial deployment: Python standard library Runtime, SQLite WAL, modular components, Git worktree isolation and Docker EDA tools, optional FastAPI for MCP/REST, TypeScript/React Web Dashboard once telemetry is real. No Redis, Kafka, vector DB, microservices or custom agent scripting framework without measured need and ADR.

## Target repository
src/siliconforge/{runtime.py,ingress.py,router.py,scheduler.py,mcp_server.py,harness/,eda/,owners/,evidence/,telemetry/}; config/, contracts/, skills/, tests/, simulator/, docs/, SiliconForge_Working_SYNC.md.

## Coding Agent execution order
Perform gap audit against docs/09, select smallest safe next work, implement and execute tests, publish evidence and Git commit, update sync and proceed. Stop only for human approval, explicit budget wall, or proven blocker. Never quietly expand scope.

## v3.1 required branch exploration gates

The established A0–A6 architecture remains authoritative. Extend it with:

| Insertion gate | Required implementation and evidence |
|---|---|
| A0X after A0 | Exploration/Branch Registry, lineage DAG, multiple Owner Instances per Role, candidate-scoped routing/leases/quotas, crash replay and state transitions |
| A3X in A1/A3 | Native Codex/Claude Owner Instances, actual Git worktrees, branch isolation, branch-specific P-Stack workflows, job registration and conflict-safe commits |
| A4X in A2/A4 | CRC32 Performance/Low Power/Area concurrent tracks, independent real Simulation/Formal/Synthesis/PPA, nested fork, Pareto, controlled merge and post-merge gates |
| A5X in A5 | Dashboard Branch DAG, per-instance traces, compare/merge view and PDCA of discarded variants |
| A6X in A6 | Multi-branch crash/recovery, stale evidence protection, no-progress watchdog, branch fairness, cost ceilings |

See docs/14–16 for event/state/data-model requirements. Existing 60 A0–A6 cases remain; E01–E20 are 20 new required cases. **Total: 80**. Do not reduce earlier test coverage or claim development success by counting branches/commits.

