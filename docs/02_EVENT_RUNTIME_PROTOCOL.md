# 02. Event-driven autonomous runtime contract

## End-to-end cycle
Producer (human MCP, Git, EDA Runner, timer, peer) → authenticated ingress → schema/source/policy checks → journal transaction + outbox delivery → deterministic route by event type, project, IP and version → durable Domain Ticket → scheduler leases Owner → Owner chooses P-Stack skill/workers/EDA job → result artifact + event → same ingress → next Owner or Evidence Gate. No busy-polling LLM and no Main Agent arbitration.

## Required event fields
event_id, event_type, schema_version, project_id, ip_id, ticket_id, source_kind, source_actor_id, identity_verified, idempotency_key, occurred_at_utc, received_at_utc, producer_revision, spec_sha, source_sha, toolchain_profile_digest, parent_event_id, causation_id, correlation_id, trace_id, payload, artifact_refs, authorization_policy_version.

## Atomic delivery
In a DB transaction: append immutable event, enforce (producer,idempotency_key) uniqueness, create affected deliveries/outbox messages and ticket transition. Same key + same payload returns existing event; same key + conflicting payload fails. Never mark handled before commit. Unknown or ambiguous routing goes to dead letter with reason, never automatically to Main.

## Work state machines
Event: RECEIVED → VALIDATED → ROUTED → DELIVERED → ACKED or DEAD_LETTER.
Ticket: NOT_STARTED → READY → ACTIVE → WAITING_FOR_RUN/WAITING_FOR_ENV/WAITING_FOR_PEER/WAITING_FOR_HUMAN → READY → VERIFYING → VERIFIED or BLOCKED/CANCELLED.
Delivery: READY → LEASED → ACKED; expired LEASED → READY up to retry cap; then DEAD_LETTER.

## Leases / recovery
Claim requires monotonic lease_token, worker_id and expiry. All writes/ACK/promotions are fenced by current token; stale workers cannot commit. On restart recovery scans committed unacked delivery and expired leases. EDA execution is async and persists job_id, state, environment, source revision and callback key; EDA.RUN_COMPLETED wakes waiting owner from journal. Owner session checkpoint is serializable and survives model/harness switch.

## Invalidation
New Spec Revision changes an evidence epoch; ongoing jobs may finish for diagnosis but stale evidence cannot close new revision. Recompute impact-based tests, not all checks indiscriminately. New events received after IDLE resume system. One blocked project cannot stop unrelated projects.

## Concrete SIM failure route
SIM.REGRESSION_FAILED → verification. Verification stores reproducer and creates typed REPAIR_REQUEST to rtl. RTL assesses failure and does bounded waveform-TDD fix; RTL.PATCH_READY routes to verification, formal, integration subscribers. EDA runner emits real results. Only independent pass with matching fingerprint reaches Integration closure. Repeated unchanged failure signature triggers bounded no-progress stop plus PDCA case.

## Tests
A0-01 to A0-18 in docs/09; include crash injection between journal and delivery, duplicate callbacks, partitioned IPs, stale lease, replay and Main-offline tests. Reference implementation is not a production-proven runtime.
