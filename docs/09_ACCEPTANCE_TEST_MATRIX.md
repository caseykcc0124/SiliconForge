# 09. Acceptance matrix, objective proof required

**No milestone is completed merely because tests were written, a mock was animated, a response said PASS, or a GitHub PR exists.** Evidence must refer to the executed implementation, actual commit and profile. The following IDs are traceable acceptance requirements.

## A0: control plane, deterministic without LLM

| ID | Test | Expected result |
|---|---|---|
| A0-01 | Ingest accepted SIM.FAILED | One immutable event, direct Verification delivery, no Main Agent dependency |
| A0-02 | Re-ingest same source/idempotency key/payload | Same event ID, one delivery, no duplicate run |
| A0-03 | Same key different payload | Reject conflict, original remains unchanged |
| A0-04 | Crash after event commit before worker starts | Recovery claims committed delivery, event not lost |
| A0-05 | Worker lease expires | New lease token can claim; stale ACK rejected |
| A0-06 | Direct Verification → RTL Peer Request | One typed peer message and direct RTL inbox delivery |
| A0-07 | Owner waits for EDA | Persistent WAITING state, no LLM busy polling |
| A0-08 | EDA completion event | Causal links preserved, waiting Owner awakened |
| A0-09 | Two IPs, one blocked | Other continues to independently complete |
| A0-10 | Duplicate failure signature with no progress | Watchdog blocks bounded task, emits reason and PDCA candidate |
| A0-11 | Unauthorized Owner/workstream crossing | Policy denies and journals reason |
| A0-12 | Stale spec/toolchain evidence promotion attempt | Integration gate refuses; requires updated evidence |
| A0-13 | Simulated user exits harness | Event and Owner work persist |
| A0-14 | Event/peer/decision journal replay | Dashboard projection reconstructs same ordered history |
| A0-15 | Route unknown or ambiguous | Dead letter; no guessing or fallback to Main |
| A0-16 | Attempt editing immutable journal row | Database rejects mutation |
| A0-17 | Delivery attempts exhausted | Dead letter, no unbounded retry |
| A0-18 | Idle and then new event | New work begins, original history retained |

## A1: native harness and secure gateway

| ID | Test | Expected result |
|---|---|---|
| A1-01 | Open normal Codex in repo and request status | Skill/MCP returns persisted data; no custom CLI |
| A1-02 | Open Claude Code and request same status | Same contract and IDs; adapter differences isolated |
| A1-03 | Submit spec change through MCP and Dashboard | Identical router/events semantics with distinct verified actors |
| A1-04 | Unauthenticated request | Denied, audited, zero effects |
| A1-05 | Authenticated actor outside project | Denied, audited, zero effects |
| A1-06 | Replay approval nonce / attempt privileged command | Denied, cannot bypass human mandate |
| A1-07 | Close/reopen native harness | Notifications and ticket state preserved without global stoppage |
| A1-08 | Switch Owner harness after checkpoint | No loss of ticket, causality or evidence; model policy enforced |

## A2: real EDA baseline

| ID | Test | Expected result |
|---|---|---|
| A2-01 | Environment Owner creates image | pinned digest + version reports and smoke tests |
| A2-02 | Verification job from RTL Owner | only approved EDA profile executes, no local install |
| A2-03 | Simulate CRC32 known vectors and APB transactions | real cocotb/Verilator report + waveform with source SHA |
| A2-04 | Formal mandatory properties | real proof/failed/unknown results, no timeout counted PASS |
| A2-05 | Yosys synthesis/netlist | actual netlist and report, reproducible command |
| A2-06 | Induce environment drift | dependent job waits; new approved profile restores it |
| A2-07 | Raw report missing or parser fails | UNVERIFIED, no artifact promotion |

## A3: autonomous real bug repair loop

| ID | Test | Expected result |
|---|---|---|
| A3-01 | Introduce APB CRC32 reset defect | independent real regression red, failure reproducer saved |
| A3-02 | Verification Owner requests repair | typed peer event directly to RTL Owner, evidence refs present |
| A3-03 | RTL Owner patch in isolated worktree | explicit diff, local red→green repro, source commit |
| A3-04 | Independent Verification and Formal Owners re-run | merged SHA, actual tools and required properties pass |
| A3-05 | Close Main harness during run | recovery and final evidence with zero manual forwarding |
| A3-06 | Kill worker midway | no lost event, bounded retry and no duplicate promotion |
| A3-07 | Same broken patch repeatedly regenerated | watchdog stops and identifies non-progress; no new framework spawned |

## A4: engineering change and optimization

| ID | Test | Expected result |
|---|---|---|
| A4-01 | Spec changes while jobs run | stale results tracked, not released; new revision triggers impact-based checks |
| A4-02 | PPA target tightened | PPA Owner requests bounded Arena with no central Main judgment |
| A4-03 | Independent candidate competition | same library/corner/constraints, objective ranking, correctness first |
| A4-04 | Candidate passes simulation but fails formal | rejected regardless of superior PPA |
| A4-05 | Candidate fails target after budget | quantified blocked conclusion with evidence, not infinite iterations |
| A4-06 | New PPA candidate merged | required regression/proof/reanalysis on merged SHA |

## A5: observability and PDCA

| ID | Test | Expected result |
|---|---|---|
| A5-01 | Project timeline from Event Journal | ordered causation, leases, owner decisions, actual evidence |
| A5-02 | Query Peer Request | recipient, state, response, deadline and trace linked |
| A5-03 | Query Owner run and model | correct harness/model/skill version and cost metrics |
| A5-04 | Dashboard down then restored | no event loss; projection rebuild consistent |
| A5-05 | Repeated failure motif | PDCA hypothesis with case refs and baseline metrics |
| A5-06 | PDCA candidate | independent A/B test, no production policy auto-change |
| A5-07 | Notification unsupported/undelivered | outbox preserves notice, read on next harness session |

## A6: autonomy and security chaos

| ID | Test | Expected result |
|---|---|---|
| A6-01 | Owner attempts test/gate weakening | host denies, logs policy violation |
| A6-02 | Owner attempts new agent/framework spawn | denied without explicit mandate |
| A6-03 | Owner tries unauthorized external publish | denied; public repo contains no restricted artifact |
| A6-04 | Model switch tries to bypass budget | total ticket budget enforced across sessions |
| A6-05 | Database/process crash during lease and callback | recovery preserves event causality and fences stale workers |
| A6-06 | Three projects plus environment drift | isolation/fairness, bounded resources, no global fatal stop |
| A6-07 | Production acceptance test is modified to green | fail review and CI integrity control |

## Passing evidence format

For each ID record `test_id`, `milestone`, `implementation_commit`, `command`, `started_utc`, `ended_utc`, `environment_digest`, `actual_result`, `objective_artifact_paths`, `log_digest`, `independent_reviewer`, `limitations`. `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN` are distinct. An A0 deterministic simulation never counts as an A3 real-EDA PASS.

## First real milestone acceptance checklist

A0 must run from a clean checkout using Python stdlib, generate an actual report, and meet all *implemented* A0 reference tests. `A0-07`–`A0-15` may require later A0 implementation beyond initial reference and must not be marked PASS from a conceptual model. A0 complete only after **all 18** test IDs have executed and passed with evidence. Do not release an A0 badge based solely on the included scaffold test count.

## v3.1 additive E01–E20 acceptance

The A0–A6 acceptance IDs above (18 + 8 + 7 + 7 + 6 + 7 + 7 = **60 Required Cases**) remain unchanged. The additional [E01–E20 matrix](15_PARALLEL_EXPLORATION_ACCEPTANCE.md) contains **20 new Required Cases**, giving **80 total**.

The new cases include simultaneous Owner Instances, nested forks, branch-scoped event routing, git worktree isolation, cross-branch evidence rejection, parallel real EDA, Pareto comparability, managed merge and re-gate, budget-limited spawning, restart recovery, and DAG/PDCA reconstruction.

Machine-readable tracker: [contracts/parallel_exploration_acceptance.json](../contracts/parallel_exploration_acceptance.json). All E cases are `NOT_RUN` until executed with matching evidence. Tests written but not run do not count as PASS. Mock/Stub may verify early contracts but cannot satisfy real Harness/EDA requirements.

