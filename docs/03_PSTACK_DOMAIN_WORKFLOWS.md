# 03. P-Stack adapted inside each Domain Owner

P-Stack is an **owner-local engineering method**, not the global Super Agent Router. Every Owner is a local parent managing a bounded set of temporary workers with independent worktrees where appropriate. Runtime owns only the cross-domain lifecycle and all resource admission.

## Skills contracts
All skills must specify: trigger event, inputs (spec/source/toolchain/evidence fingerprints), owner authority, bounded subworkers, method, artifacts, pass/fail and retry exit criteria, events to emit, measurable cost. No skill may edit global router/policy/test gates on its own.

### Spec Owner
silicon-architect + design-impact/interrogate. Validate requirement syntax and scope, draft interface/register/clock/reset/latency assumptions, produce spec_revision and impact matrix, route required work to RTL/verification/formal/PPA. Ambiguous semantic requirement is WAITING_FOR_HUMAN with bounded question, not guessed.

### RTL Owner
silicon-architect → waveform-tdd → bounded rtl-arena → design-interrogate → engineering-evidence. The Owner may launch 2 or 3 isolated RTL candidates, but each must satisfy common spec and reproducible tests; independent cross-judge and real EDA gates decide. Do not merge a candidate just because it is smaller or explained convincingly.

### Verification Owner
verification-swarm creates parallel APB protocol, directed functional, random/seeded, reset/corner and testbench/golden-model checks. For failures, first reproduce red condition, preserve seed/waveform/expected/actual/commit, classify model-vs-RTL-vs-environment, send typed peer with a minimal reproducer. Retest patched exact SHA; do not write RTL as a shortcut.

### Formal Owner
formal-interrogate checks whether properties/assumptions accurately represent original spec; use SymbiYosys where supported. Preserve PASS/FAIL/UNKNOWN/TIMEOUT separately. Emit formal counterexample with exact design/constraints, direct request to RTL or Spec as justified. Do not weaken property to turn red green.

### PPA Owner
ppa-arena compares bounded microarchitectures under identical constraints, library, corner, clock, routing settings and resource budget. Correctness gate is mandatory before score; cannot select functionally incorrect fast implementation. Run OpenROAD and/or Yosys; report measured area, timing and explicitly labeled power estimate if available. If infeasible, stop with quantified evidence.

### Integration Owner
engineering-evidence reconciles all required results for same spec_sha/source_sha/toolchain profile, rejects stale/ambiguous/UNKNOWN and signs a verified artifact record. Emit downstream engineering events after closure.

### EDA Environment Owner
toolchain-manager establishes pinned container/profile/PDK/license allowlist and smoke tests, monitors drift and re-validates new profiles. Other owners submit jobs through Runner; never apt/pip-install or alter EDA versions ad hoc. WAITING_FOR_ENV automatically resumes when approved profile is restored.

### Process Improvement Owner
silicon-reflect aggregates event/signature/peer/decision/cost logs, produces PDCA proposal with baseline and A/B test, no unsupervised production policy change.

## Acceptance
Each owner must demonstrate a nontrivial workflow on real outputs, with worker lineage, objective artifacts and bounded retry. README and docs/09 are authoritative.

## v3.1 parallel P-Stack adaptations

The same Domain Role may have concurrent instances for Performance, Low Power and Area candidates. Each has its own P-Stack `arena/swarm/interrogate` run, isolated Git worktree, ticket, evidence, owner lease and stop condition. An RTL instance may fork nested candidates only within the group's approved budget and depth, never silently mutate other branches. Verification/Formal/PPA results belong to exact Candidate/Commit/Spec/Toolchain/Constraints fingerprints; cross-branch PASS reuse is forbidden. The Runtime records their branch DAG and fan-out/fan-in; the P-Stack skills remain local to each Owner Instance. See docs/14–16 and E01–E20.
