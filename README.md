# SiliconForge

**Autonomous Chip Engineering Framework | Architecture & Delivery Baseline v3.1**

Status: **SPECIFICATION / A0 REFERENCE IMPLEMENTATION**. No production autonomous EDA flow has been demonstrated. Existing `simulator/` is a deterministic **mock**, not evidence of working Codex or Verilator.

## Intent

An engineering event, such as a new specification, RTL change, regression failure, formal counterexample, PPA target revision or toolchain drift, must reach its domain owner **without passing through a human Main Agent**. That owner uses domain-specialized P-Stack practices, a replaceable coding-agent harness, controlled EDA tools and evidence gates. Tool and peer outcomes create durable new events. Human intervention is reserved for explicit policy boundaries or exhausted, explainable engineering blockers.

**Control plane:** deterministic Super Agent Runtime. **Domain decisions:** autonomous domain owners. **Execution:** Codex/Claude Code and EDA runners. **Human interface:** native Codex/Claude Code via skills + MCP + project guidance, with Web Dashboard as observability. **Not** a custom chat CLI.

## Read in order

1. [`docs/00_MISSION_AND_BOUNDARIES.md`](docs/00_MISSION_AND_BOUNDARIES.md), what to build and what not to build
2. [`docs/01_ARCHITECTURE_AND_OWNERSHIP.md`](docs/01_ARCHITECTURE_AND_OWNERSHIP.md), decisions and module boundaries
3. [`docs/02_EVENT_RUNTIME_PROTOCOL.md`](docs/02_EVENT_RUNTIME_PROTOCOL.md), durable autonomous event loop
4. [`docs/03_PSTACK_DOMAIN_WORKFLOWS.md`](docs/03_PSTACK_DOMAIN_WORKFLOWS.md), exact owner skill behavior
5. [`docs/04_EDA_EVIDENCE_AND_ENVIRONMENT.md`](docs/04_EDA_EVIDENCE_AND_ENVIRONMENT.md), technical verification and toolchain owner
6. [`docs/05_HARNESS_MCP_HUMAN.md`](docs/05_HARNESS_MCP_HUMAN.md), Codex/Claude Code integration and notifications
7. [`docs/06_OBSERVABILITY_PDCA.md`](docs/06_OBSERVABILITY_PDCA.md), traces and improvement loop
8. [`docs/07_SAFETY_AND_RESOURCE_GATES.md`](docs/07_SAFETY_AND_RESOURCE_GATES.md), autonomy guardrails
9. [`docs/08_IMPLEMENTATION_PLAN.md`](docs/08_IMPLEMENTATION_PLAN.md), incremental deliveries
10. [`docs/09_ACCEPTANCE_TEST_MATRIX.md`](docs/09_ACCEPTANCE_TEST_MATRIX.md), proof of completion
11. [`docs/10_CODING_AGENT_EXECUTION_ORDER.md`](docs/10_CODING_AGENT_EXECUTION_ORDER.md), exact handoff instruction
12. [`SiliconForge_Working_SYNC.md`](SiliconForge_Working_SYNC.md), progress and communications contract

The historical v2.2 RFC lives in `docs/reference` for traceability. **v3 docs and acceptance matrix supersede prior proposals** when there are conflicts.

## Local A0 reference tests

```bash
python -m unittest discover -s tests -v
python -m siliconforge.demo   # requires PYTHONPATH=src or editable installation
```

Recommended editable installation: `python -m pip install -e .`. A0 tests use only the Python standard library; real Codex/MCP/EDA connectors are future milestones.

## GitHub workflow

The canonical standalone repository is `caseykcc0124/SiliconForge`. Work should proceed on topic branches with pull requests and CI, subject to the authorized publishing rules. Coding Agent updates `SiliconForge_Working_SYNC.md` on meaningful progress and at least once per 15 minutes while actively developing, and commits it to GitHub without inventing test outcomes. Track the authoritative sync file on `main` via integration commits/PR merges or explicitly approved dedicated status branch if PR work is ongoing. See `docs/10_CODING_AGENT_EXECUTION_ORDER.md`.

## Reference materials

DeepSeek [dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) informs Trigger/Ticket/Mandate/recovery concepts. [P-Stack design methods](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/04-design.md) inform `architect/arena/swarm/interrogate` **inside** owners. Cadence ChipStack is an aspirational engineering capability reference, not an implementation dependency.

## License and scope

No open-source license is assigned yet; the repository being public does not imply permission to reuse external proprietary code. Do not import confidential chip data, PDK assets, company specifications, model credentials, or source material you do not have permission to publish. Select a license only after owner approval.

## v3.1 extension: concurrent design exploration

SiliconForge supports **multiple Owner Instances for each Domain Role**, not one singleton per specialty. A single Requirement may fork into Performance, Low Power and Area candidates, with nested Git branch/worktree exploration, independent EDA validation, a traceable Pareto comparison, controlled merge and mandatory merged-SHA re-verification.

The canonical [Coding Agent entry point](CODING_AGENT_START_HERE.md) includes the updated work order. Read [Parallel Exploration Architecture](docs/14_PARALLEL_EXPLORATION_ARCHITECTURE.md), [E01–E20 Additional Acceptance](docs/15_PARALLEL_EXPLORATION_ACCEPTANCE.md), and [Implementation Mapping](docs/16_PARALLEL_EXPLORATION_IMPLEMENTATION.md). Policy: [config/exploration_policy.json](config/exploration_policy.json).

**The original A0–A6 60 cases remain mandatory. The 20 new E cases bring the project to 80 Required Acceptance cases.** Documentation publication is not implementation acceptance.



## Fully standalone repository

This repository is the **only** SiliconForge source, specification, acceptance and status authority. A clean clone includes the local source, tests, skills, config, contracts, simulator, 60 original A0–A6 cases and 20 new E cases. It does not rely on another SiliconForge repository or external archive for its own implementation baseline. See [Standalone Repository Contract](docs/17_STANDALONE_REPOSITORY_CONTRACT.md). The A0 local test suite now includes independence and acceptance-integrity tests: `python -m unittest discover -s tests -v`.
