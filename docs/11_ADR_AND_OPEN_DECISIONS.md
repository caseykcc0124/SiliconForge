# 11. Architecture Decision Record and unresolved choices

## Accepted
ADR-001 Runtime deterministic event-driven, never an LLM central arbiter.
ADR-002 Domain Owner is durable ticket/identity, not a permanent Codex process.
ADR-003 P-Stack skill orchestration is local to each Domain Owner.
ADR-004 User chooses native Codex or Claude Code; shared MCP gateway and optional hooks; no custom chat CLI.
ADR-005 Simulation/Formal/PPA are evidence sources with exact version fingerprints.
ADR-006 EDA Environment Owner exclusively manages pinned toolchain profiles.
ADR-007 Main Agent serves human inquiry and authorized intent translation only.
ADR-008 Event Journal/Peer Ledger/Decision/Trace/PDCA persist independently of UI.
ADR-009 Safety and budget gates are host-side, not prompt-only.
ADR-010 Start SQLite WAL + modular backend + isolated workers, scale only on evidence.

## Open with conservative defaults
1. Model/effort by Owner: begin with Codex as common Harness with configurable policy; no hidden automatic premium-model escalation.
2. Human approval thresholds: all spec acceptance changes, scope expansion, publishing, new paid resources, external access and unapproved environment changes require explicit authenticated approval.
3. Per-ticket budget and max retries: bounded configurable development values, visible in UI and log; crossing limit stops ticket, not all IPs.
4. Toolchain: approved open-source images only, no third-party proprietary PDK until license review.
5. Notification channels: durable outbox + on-resume sync first; desktop/webhook push is optional.
6. Autonomous PDCA: proposal and sandbox experiments allowed; production policy auto-promotion forbidden.
7. Security: local-dev MCP is read/write only in isolated development, not safe for network exposure without auth/ACL/nonce.

Changes require ADR, evidence-based impact analysis, updated tests and versioned policy. No autonomous Owner may decide these global issues.
