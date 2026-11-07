# 07. Guardrails: bounded autonomy in host code

## Mandatory hard controls
Do not rely only on prompts. The host Runtime enforces: per-Ticket total budget, token/model/EDA budget, maximum attempts per signature, max child workers, allowed tools and filesystem/network scopes, source-owner ACL, immutable original specs and acceptance, approval for external publication, exact evidence fingerprint and environment. Main cannot bypass an Owner approval gate.

## No-progress watchdog
Track tuple (ticket, failure_signature, candidate_sha, evidence_hash, test_coverage_delta, quality_delta). Repeated identical failures with no new valid engineering evidence consume bounded retry allowance. A distinct hash is not itself progress. When exceeded, stop affected Ticket, produce diagnostic and PDCA candidate, continue unrelated IPs. Waiting for EDA cannot burn LLM polling tokens.

## Example baseline limits
Set conservative configurable development limits, such as max 3 consecutive same-signature attempts without progress, max 3 Arena candidates per request, max 2 child workers per Owner, finite EDA job timeout, finite wall-clock and all-harness cumulative token budget. These are starting policies, not universal guarantees. Any changes require audited authorization and frozen regression tests.

## Explicit denied actions
- weaken/remove failed tests, proof properties or clock constraint to create green evidence;
- install EDA/PDK versions by random Owner, change image digest without Environment approval;
- spawn a new framework or arbitrary Agents due to one bug;
- bypass denied approval by switching models/harnesses;
- publish IP, private PDK, credentials or restricted artifact to public GitHub;
- mark simulation mock green as an A3 hardware verification pass;
- ignore stale spec/source SHA in evidence gate.

## Stop semantics
PAUSE persists work and releases model compute; BLOCKED records actionable constraint, attempts and evidence, no silent retries; WAITING_FOR_HUMAN only for actual policy/intent decision; VERIFIED only after independent objective gate.

## Acceptance
A0 and A6 tests in docs/09 must cover no-progress stoppage, quota boundaries, stale lease, fault isolation, unauthorized expansion and illegal tool calls.
