# 00. Mission, origin, non-goals and success

**Normative baseline: v3.0.** SiliconForge is an autonomous, event-driven chip-engineering framework, starting with a tiny APB CRC32 peripheral. Its goal is to complete engineering work with objective evidence and minimum human intervention, not to produce maximum code or maximum agent activity.

## Mandatory architecture
- The deterministic Super Agent Runtime owns the lifecycle of events, leases, routing, budgets, wakeups and recovery.
- Spec, RTL, Verification, Formal, PPA, Integration, EDA Environment and PDCA Domain Owners own their distinct professional decisions and local P-Stack skills.
- A human Main Agent is a conversational interface only; it is never in the mandatory routing or approval path between Domain Owners.
- Tool outputs create durable new events. Domain Tickets survive model turn, shell, session and worker restarts.
- Users use native Codex or Claude Code with AGENTS.md, Skills and MCP, plus a separate Web Dashboard. Do not build a custom chat CLI.
- Use real pinned open EDA tools. Simulation, proof, synthesis and PPA must use reproducible source, spec, constraints and environment fingerprints.

## Hard exclusions
No unbounded loops, unauthorized subagents, new frameworks, license/PDK installs, weakening tests, silently changing specs, bypassing security/publishing gates or claiming mock results are engineering verification. The user chooses approved scope; owners decide within that scope.

## First actual success
Inject an authenticated SIM.REGRESSION_FAILED while the human harness is closed. Verification collects a real reproducer, directly sends an RTL repair request; RTL autonomously patches in isolated worktree; independent real simulation/formal run on a merged SHA and pinned profile; Integration records evidence and closes the ticket. No Main Agent message relay or human re-prompt.

## Human involvement
Only for intention conflict, scope or requirements change outside mandate, expanded access/licensing, budget exhaustion, policy change, authorized publication or a genuinely exhausted engineering blocker. Rejected requests remain rejected across models. Progress means new reproducible evidence, never number of generated files or prompts.

## Results
Measure verified-artifact yield, end-to-end completion, new evidence fingerprints, human interruptions, crash recovery, stall detection, cost per verified result, rejection of invalid candidates and freedom from uncontrolled scope expansion. Milestones A0 to A6 are defined in docs/08 and docs/09.
