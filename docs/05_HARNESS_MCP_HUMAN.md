# 05. Native Codex/Claude Code, MCP, human notifications

## Entry path
User opens normal Codex or Claude Code in repository and chats naturally. AGENTS.md/CLAUDE.md + SiliconForge Skill explain how to use MCP. Do not implement an sf chat CLI or a replacement harness. The native human session is optional and independent of always-on Runtime. Main Agent has status, explanation, event submission and human approval capabilities but never replaces Domain Owner judgments.

## MVP MCP contract
- sf_get_status(project_id?,ip_id?,ticket_id?): read persisted state and last evidence.
- sf_submit_event(event_type,project_id,ip_id,payload,idempotency_key): validate actor + create durable event, return event_id and ticket_id; never directly run RTL in Main.
- sf_get_evidence(ticket_id,revision?): return immutable manifest references and credibility.
- sf_send_message(recipient_owner,ticket_id,request_type,artifact_refs,completion_contract): durable peer communication; route directly to target owner.
- sf_get_activity(ticket_id,cursor?): ordered and causal event+owner+tool activity.
- sf_subscribe(project_id,ticket_id,notification_types): persist notification preference.
- sf_get_notifications(since_id?,unread_only?): idempotent query/pull.
- sf_submit_approval(approval_id,decision,nonce): authenticated approved human only; reject replay.
- sf_control_ticket(ticket_id,action,reason): pause/resume/cancel within role/policy.

All mutations are authorized by authenticated actor identity, project membership, command capability, request nonce and audit trail. Owner identity is not inferred from untrusted prompt content. Example MCP skeleton in src/ is intentionally DEV ONLY until authentication and policy pass A1.

## Harness adapters
Owner Harness Adapter API: start(owner,ticket,checkpoint,policy), resume(run_id), interrupt(run_id), collect_output(run_id), checkpoint(run_id), shutdown(run_id). Every run stores harness/model/effort/skill version, input/output summary, token/cost, task limits and terminal state. Switching sessions/harnesses cannot reset ticket budget or evidence. Owner should relinquish model compute while EDA job waits.

## Notifications
Runtime writes durable Notification Outbox for completion, approval-needed, persistent blocker and policy violation. Dashboard shows events; native harness reconnect retrieves unread and optionally uses supported hooks; optional external webhook or OS push is separate. Do not design model busy-poll loop. Unsupported push channel must not lose notice. Human may ask Owner directly via gateway for technical judgment but cannot silently change original mandate.

## Verification
A1-01 to A1-08 from docs/09, include native Codex and Claude status, authenticated event equivalence, unauthorized writes rejected, closing frontend does not stop Runtime, notification retained, model switch restores same Ticket.
