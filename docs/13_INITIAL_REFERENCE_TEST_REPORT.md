# 13. Initial reference / evidence boundaries

The original project-delivery ZIP was locally tested with 22 Python stdlib reference unit tests before repository publication. Those test results apply to the original A0 **reference** code at its local source revision only. They do **not** constitute full A0-01–A0-18 acceptance, and not a single real Cadence-like EDA or Codex Owner E2E has yet been accepted.

Canonical gate: docs/09_ACCEPTANCE_TEST_MATRIX.md. Each new remote commit must be re-tested from the actual cloned remote tree and report exactly the tests executed on that tree. Do not reuse historical test counts after modifying source.

Known gaps include complete crash/lease fencing and audit recovery, authenticated MCP and identity ACLs, actual runtime-owned harness processes, real pinned EDA jobs, independent formal/evidence gates, low-interruption notifications and PDCA deployment experiments.

A milestone is VERIFIED only when every relevant acceptance test has independently reproducible evidence tied to the implementation commit.
