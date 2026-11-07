# SiliconForge Working Sync

**Purpose:** Git-backed handoff contract among the human project owner, Coding Agent(s), and status-review assistant. This is a current status snapshot plus a concise audit trail, not an autonomous scheduling service.

## IMPORTANT: External Coding Agent must use Browser + ZIP + Local Git + Sync-only

**This section is the direct task and communication contract for the current external Coding Agent. Read it first. The Agent CANNOT run Git commands against GitHub, CANNOT clone/pull/push the remote repository, and CANNOT write any remote source file other than this Sync file via the GitHub web editor. It CAN use local Git on its own machine.**

1. **Read task**: Open THIS FILE using Chrome/Computer Use. Other GitHub files, including `AGENTS.md` and `docs/`, may be read using Browser when needed; do not assume they have been automatically loaded.
2. **Acquire code when necessary**: Open `https://github.com/caseykcc0124/SiliconForge` in the Browser; choose **Code → Download ZIP**, download and extract into the Coding Agent's own Local workspace. This is the permitted whole-repository input method. **Do not run `git clone`, `git fetch` or `git pull` on GitHub.**
3. **Work locally**: Develop and test in that Local directory. Local `git init`, Local branches and Local commits are allowed, but they are **NOT GitHub commits** and are not proof that remote source has changed. The ZIP is a snapshot without `.git` history.
4. **Report progress**: In the Browser, edit only `SiliconForge_Working_SYNC.md` and save it through GitHub Web UI. Report the current baseline revision, local code status, exact tests, SHA of produced artifact, blocker, and next local action. **Do not claim a Sync Web edit means code was uploaded.**
5. **Deliver actual source**: When implementation is ready, prepare a Local ZIP/Patch Bundle containing changed source, tests, manifests and raw evidence, with baseline SHA and SHA256. The Agent currently has **no verified direct transfer path for this bundle**. Mark `LOCAL_IMPLEMENTED_PENDING_ARTIFACT_TRANSFER` until an authorized, accessible channel is available. A separate GitHub Integrator may commit actual source only **after receiving and verifying those bytes**. If no transfer path exists, state this blocker accurately. Do not tell the human that GitHub source was updated.
6. **Never attempt**: remote Git Clone/Pull/Push, GitHub PR creation as a required Coding Agent step, edits to other GitHub files via the Browser, reading another SiliconForge repository, or unbounded test/framework expansion.
7. **Engineering goals**: SiliconForge v3.1 remains the event-driven Super Agent Runtime with specialized P-Stack Domain Owners, native Codex/Claude Harness interfaces and real EDA verification. Multiple Owner Instances may concurrently explore one Requirement with Performance/Low Power/Area Git worktrees, nested forks, independent candidate evidence, Pareto selection and verified Merge. Existing A0–A6 **60 required cases** and E01–E20 **20 required cases** give **80**. A0 is NOT_VERIFIED; no new E case is PASS by writing this instruction.
8. **Sync frequency**: On start, material progress, test changes, blocked, and final report. During active work update/heartbeat at least once per 15 minutes where Browser UI permits; distinguish heartbeat timestamp from last actual engineering progress. Re-read the page before editing to avoid overwriting another editor.

If a separate doc says 'Clone the repo', 'Push commit', or 'Create PR', **that step is for an authorized GitHub Integrator or a different environment**. For this Coding Agent, the transport contract in this section overrides it. Full procedure in `docs/18_BROWSER_ZIP_CODING_AGENT_HANDOFF.md`.

## MACHINE-READABLE STATUS

```yaml
schema_version: "1.0"
project: SiliconForge
repo: caseykcc0124/SiliconForge
branch: main
sync_branch: main
sync_commit: "6fe2c6b243adf399420fbfb9815c807a0ff728cb"
architecture_baseline: "3.1"
coding_agent_transport:
  acquisition: GITHUB_WEB_DOWNLOAD_ZIP
  github_read: BROWSER_COMPUTER_USE
  github_write: WEB_EDIT_SINGLE_SYNC_FILE
  only_remote_editable_file: SiliconForge_Working_SYNC.md
  remote_git_clone_pull_push: UNSUPPORTED
  git_scope: LOCAL_ONLY
  remote_source_delivery: NOT_AVAILABLE_FROM_CODING_AGENT
  local_artifact_transfer: NOT_ESTABLISHED
  actual_source_on_github_updated_by_agent: false
mission_state: ACTIVE
phase: A0
owner_agent: Codex_local_A0
updated_at_utc: "2026-11-07T16:37:46Z"
last_progress_at_utc: "2026-11-07T16:37:46Z"
last_heartbeat_at_utc: "2026-11-07T16:37:46Z"
latest_commit: "6fe2c6b243adf399420fbfb9815c807a0ff728cb"
latest_pr: null
current_task: "A0 acceptance gap audit and implementation, see GitHub Issue #1"
next_action: "Coding Agent: follow Issue #1 and docs/10; audit existing A0-01..A0-18, then implement v3.1 docs/14-16 E01..E20 using A0X/A3X/A4X/A5X/A6X gates."
next_action_owner: Coding Agent
blockers: []
human_approval_required: []
policy_flags:
  allow_auto_public_release: false
  allow_auto_merge: false
  allow_unapproved_framework_expansion: false
  allow_unapproved_eda_tool_install: false
  allow_owner_control_plane_edit: false
acceptance_baseline:
  original_A0_to_A6_required: 60
  new_E01_to_E20_required: 20
  total_required: 80
  exploration_extension_status: SPEC_PUBLISHED_AWAITING_IMPLEMENTATION
  E_cases_passed: 0
  E_cases_failed: 0
  E_cases_not_run: 20
  exploration_policy_file: config/exploration_policy.json
  exploration_acceptance_file: contracts/parallel_exploration_acceptance.json
  exploration_spec: docs/14_PARALLEL_EXPLORATION_ARCHITECTURE.md
exploration_metrics:
  groups_implemented: NOT_VERIFIED
  parallel_owner_instances_verified: false
  nested_git_fork_verified: false
  cross_branch_evidence_gate_verified: false
  post_merge_real_eda_regate_verified: false
milestones:
  A0: NOT_VERIFIED
  A1: NOT_STARTED
  A2: NOT_STARTED
  A3: NOT_STARTED
  A4: NOT_STARTED
  A5: NOT_STARTED
  A6: NOT_STARTED
actual_tests:
  a0_reference_tests: "GITHUB_ACTIONS_REFERENCE_22_PASSED_NOT_FULL_A0_ACCEPTANCE"
  reference_ci_run: "https://github.com/caseykcc0124/SiliconForge/actions/runs/42354537870"
  real_eda_tests: NOT_RUN
  native_harness_tests: NOT_RUN
last_evidence:
  - "GitHub main 6fe2c6b243adf399420fbfb9815c807a0ff728cb; 54 tracked files; A0 reference CI 22/22 PASS"
``` 

## v3.1 specification and acceptance synchronization

- Canonical GitHub repository is `caseykcc0124/SiliconForge`. All source, specifications, agent instructions, acceptance records and status updates are maintained here; no alternate source repository is required.
- v3.1 adds multi-instance Domain Owners, simultaneous exploration branches and nested forks, branch-scoped event/EDA evidence, Pareto comparison, controlled merge and post-merge real EDA re-gating.
- Original A0–A6 acceptance remains 60 cases. New E01–E20 adds 20 cases; total required 80. **All newly added E cases are NOT_RUN**; this is a specification handoff, not implementation progress.
- Coding Agent must update exploration/branch/owner/merge IDs and Git SHA / toolchain fingerprint for every substantive event. Heartbeat does not imply a new verified branch or EDA result.

## Repository-independence verification (spec and reference only)

- Verified the canonical source tree includes the local Coding Agent entrypoint, AGENTS/CLAUDE guidance, docs/00–17, config, contracts, skills, src, tests, simulator and Working Sync.
- Added standalone check `tests/test_repository_independence.py` to the existing local test suite; full CI result remains pending until GitHub Actions finishes. No external SiliconForge source checkout is permitted.
- This change concerns canonical documentation and test coverage only. A0 remains NOT_VERIFIED; real harness, EDA, parallel-exploration work and all E01–E20 are NOT_RUN.

## Engineering status summary

- Initial architecture and implementation plan have been prepared. **22 local reference tests passed**, but the full A0 matrix is not complete; no autonomous Codex/Claude Code or real EDA milestone has been validated.
- The included reference Runtime and simulator are explicitly non-production and must be evaluated under the current acceptance IDs. Local reference tests do not qualify as all A0 acceptance cases. See `docs/13_INITIAL_REFERENCE_TEST_REPORT.md`.
- Public GitHub Repository is live at https://github.com/caseykcc0124/SiliconForge. The initial 54-file baseline has been published and the reference CI passed. **A0 milestone remains NOT_VERIFIED.**

## Sync update protocol

The external Coding Agent edits **only this file via GitHub Web UI**. Its local Git commits are local-only and must be reported as `local_git_commit`, never as an uploaded GitHub commit or PR. Each web-edited status update must include meaningful task state, exact tests and evidence, local artifact transfer state, progress timestamp, currently running/blocked activities, next executable step and any human approval. A real remote source commit SHA may be recorded only after an authorized Integrator has independently published and verified the actual source. Update upon each meaningful change and at least every 15 minutes during active execution. Idle heartbeat must not imply engineering progress. Use `WAITING_FOR_HUMAN` only when no authorized route forward exists. Update to `VERIFIED` only after all acceptance IDs for the phase have actual evidence. Avoid reporting 'CI GREEN' when CI has not actually run.

### Required states

`NOT_STARTED`, `ACTIVE`, `WAITING_FOR_TOOL`, `WAITING_FOR_ENV`, `WAITING_FOR_HUMAN`, `BLOCKED`, `VERIFYING`, `VERIFIED`, `CANCELLED`. After A0, use real test case IDs in `actual_tests`.

### Progress log, newest first

| UTC timestamp | Agent | Phase/state | Commit or PR | Executed evidence | Next |
|---|---|---|---|---|---|
| 2026-11-07T08:14:54Z | Architecture handoff | A0 / NOT_STARTED | [6fe2c6b](https://github.com/caseykcc0124/SiliconForge/commit/6fe2c6b243adf399420fbfb9815c807a0ff728cb) | Public repository has 54 files; [GitHub CI 22/22 reference PASS](https://github.com/caseykcc0124/SiliconForge/actions/runs/42354537870); formal A0 acceptance NOT_RUN | Coding Agent starts [Issue #1](https://github.com/caseykcc0124/SiliconForge/issues/1) |
| 2026-11-07T06:35:15Z | Architect | A0 / NOT_STARTED | Local-only | 22/22 stdlib reference tests passed; no production EDA or full A0 acceptance | Coding Agent to begin A0 gap audit |

## Human decisions and messages

| UTC | Request / decision | Owner | Status | Evidence |
|---|---|---|---|---|
| 2026-11-07 | Create a new **public** GitHub repository and use this sync file | Human sponsor / GitHub connector | VERIFIED | https://github.com/caseykcc0124/SiliconForge |

## Blocker escalation format

When genuinely blocked, append `blocker_id`, owner, attempted fixes, machine-readable failure signature, logs/artifacts, why further autonomous work would violate scope/policy, specific decision requested, and alternative tasks still possible. Do not ask the human to manually ferry normal peer messages.

## External Coding Agent local A0 execution

```yaml
external_coding_agent:
  transport: BROWSER_ZIP_LOCAL_GIT
  github_write_scope: SiliconForge_Working_SYNC.md_ONLY
  input_zip_baseline_sha: efe183b726de8392371b4271bb57ea5cf3d76f2b
  input_zip_sha256: 9ceeaa748872bbe77c5a1b61480a343266a753a9f1d3a52c40b71abb369eefdc
  local_workspace_state: ACTIVE
  local_git_commit: 0ce2b25
  code_artifact_state: NOT_CREATED
  code_artifact_access: UNAVAILABLE
  remote_source_integrated_commit: null
  tests_executed:
    - command: PYTHONPATH=src python -m unittest discover -s tests -v
      result: PASS
      count: 58
      scope: CURRENT_LOCAL_SUITE_NOT_FULL_A0
  next_action: Complete scoped Runtime, lease expiry, durable wait/wake, ingress policy and evidence rejection; execute A0-01 through A0-18.
```

2026-11-07T16:37:46Z. Downloaded main through Chrome Code -> Download ZIP and initialized local-only Git. Original 30 reference tests passed. Read-only audit reproduced expired lease ACK, stranded final lease, unknown-route loss and same-project IP scope gaps. Core repairs and boundary modules are in progress. A0 remains NOT_VERIFIED; real EDA, native harness and E01-E20 remain NOT_RUN. No remote source file has been changed. Local source artifact transfer is not established; this does not block authorized local A0 work.



2026-11-07T16:37:46Z. Local checkpoint. Full stdlib suite 58/58 PASS, independently rerun by Luna reviewer. Executable tests/run_a0_acceptance.py has per-ID raw logs, source hashes and JSON under .audit/a0-acceptance; currently 17 A0 checks pass and A0-14 remains NOT_VERIFIED. Independent review continues on peer boundaries and canonical envelope completeness, so full A0 remains NOT_VERIFIED. A separate Luna worker is implementing immutable ordered history reconstruction. Changes remain uncommitted; local_git_commit stays baseline 0ce2b25. Source artifact NOT_CREATED and transfer UNAVAILABLE. Next finish replay and boundary review, rerun acceptance at committed local revision, then A0X. REAL EDA/native harness/E01-E20 NOT_RUN. No remote source changes or new approval requests.

