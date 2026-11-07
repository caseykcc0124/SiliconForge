# 06. Observability, communication records, Dashboard and PDCA

## Five authoritative durable record types
1. Immutable Event Journal: ingested event, route, delivery, ACK, causation and provenance.
2. Communication Ledger: typed human/peer requests, sender, recipient, completion contract, response/refusal, deadlines and artifacts.
3. Execution Trace: Owner turns, P-Stack subworkers, EDA command, model and tool use, waits, cost, heartbeat and stop.
4. Decision & Evidence Record: selected strategy, alternatives, constraints, candidate hashes and objective results.
5. Improvement Ledger: failure motif, hypotheses, baseline, proposed skill/policy changes, A/B/rollback evaluation.

All records correlate via trace_id, event_id, ticket_id, owner_run_id, causation_id, project_id and immutable engineering revisions. The Event Journal is source of truth; OpenTelemetry is an exporter, not a dependency for work delivery.

## Dashboard
Mission overview; owners/run/lease activity; Communication + Event Trace graph; Simulation/Formal/Synthesis/PPA evidence; resource and failure analytics; PDCA experiment board. Read views can be rebuilt after crash, do not perform engineering decisions.

## Structured failure taxonomy
SPEC_AMBIGUOUS, SIM_ASSERTION, RTL_BUG, GOLDEN_MODEL_CONFLICT, FORMAL_COUNTEREXAMPLE, FORMAL_UNKNOWN, TIMING_VIOLATION, ENV_DRIFT, RESOURCE_EXHAUSTED, NO_PROGRESS, POLICY_DENIED, STALE_EVIDENCE, HARNESS_FAILURE, UNAUTHORIZED_WORK. Store immutable error signature + seed + reproducer and root-cause confidence, not generic prose only.

## PDCA
Plan: identify repeated failure and quantify baseline cases/cost. Do: create new Skill/policy candidate in sandbox. Check: independent frozen-corpus A/B, including safety and expense. Act: explicit authorized promotion or reject/rollback. Improvement Owner cannot mutate live production router/policies. Success trajectories as well as failure patterns can become reusable tests, but not automatic model training.

## Retention
Audit records immutable with privacy filtering and redacted secrets; large raw traces and waveforms retained as content-addressed artifacts. Store evidence hashes, not all tool logs inline in Ticket. Support export and replay without leaking sensitive design.

## v3.1 exploration observability

In addition to linear Event Trace, the Dashboard must reconstruct a Branch DAG: Requirement → Exploration → Branch/Parent → Candidate/Commit → Owner Instance → EDA Jobs/Evidence → Comparison/Pareto → Merge/Promotion. Store branch/owner IDs, fork SHA, lineage edge, cost/quota, stale spec marker, merge decision and new-SHA re-gate outcomes. PDCA must retain losing branches' hypotheses, failure signatures and resource use. Event Journal and immutable Engineering Evidence remain authoritative, not a decorative graph. See E19, docs/14–16.
