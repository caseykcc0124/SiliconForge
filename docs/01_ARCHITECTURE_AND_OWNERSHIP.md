# 01. System architecture and ownership

## Canonical topology
Native User Harness (Codex/Claude Code, Skills, AGENTS.md, MCP) and Web Dashboard → authenticated Gateway → deterministic Super Agent Runtime → durable event journal/outbox/router/scheduler/policy/watchdog → independent Domain Owner harness sessions → isolated workers/EDA Runner → objective Evidence Gate → newly emitted events. All journal and message records persist.

## Ownership matrix
| Component | Engineering authority | Cannot do |
|---|---|---|
| Main Agent | interpret authorized human input, status queries, notification summary | decide RTL fixes, select PPA winner, approve specs without human |
| Runtime | receive/validate/dedupe/route events, lease work, stop/resume, enforce budget | infer design root cause or rewrite requirement |
| Spec Owner | interpret requirements, revisions, impact and ambiguity | silently edit acceptance criteria |
| RTL Owner | architecture, bounded patch, local Arena/Workers | weaken tests or global policy |
| Verification Owner | cocotb, regression, repro, coverage, bug classification | approve own unverified fix |
| Formal Owner | assumptions/properties, independent proof/counterexample | count UNKNOWN/TIMEOUT as PASS |
| PPA Owner | bounded candidate comparison on same constraints | select nonfunctional candidate solely for PPA |
| Integration Owner | same-revision evidence bundle, release gate | promote stale or missing evidence |
| EDA Environment Owner | pinned approved profiles/images, tool health and drift | use unauthorized install or PDK |
| Improvement Owner | cross-run metrics, proposal/sandbox A/B | auto-deploy new production policies |

Every Owner holds a stable owner_id, per-Ticket history, assigned rights, local P-Stack parent/worker skills and independent lifecycle. Owner identities are not tied to a long-running LLM conversation. All domain communication is typed Peer Request/Event via Runtime; the Main Agent need not be online.

## Concurrency
One active writer/lease per mutable RTL worktree; parallel candidate worktrees are isolated. Validation and Formal work on exact candidate SHAs. Older revision output is retained historically but cannot satisfy new revision gate. Resource governor limits parallelism and total cost across all workers and harnesses.

## Deployment
Start with a Python modular backend, SQLite WAL with transactions, subprocess workers and pinned containers, a thin MCP/HTTP gateway, and a read-only first Dashboard. No Kafka/Kubernetes/Redis until measured bottlenecks justify ADR. Security boundary: user-to-gateway authentication, owner capabilities, artifact path allowlist, network restrictions and human approval for privileged operations.

## v3.1 multi-instance decision boundary

A `Domain Role` is not a singleton execution Owner. Runtime resolves many independent `owner_instance_id` values per Role and assigns them to branch-scoped Tickets. Instances choose their own domain engineering actions, while the deterministic Exploration Service holds Branch/Lineage Registry, admission, quotas, event routing, recovery and authorized merge. The human Main Agent remains an interface and never decides winning RTL or PPA designs on behalf of other Owners. See docs/14–16.
