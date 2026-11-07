# 04. EDA environment and objective engineering evidence

## Baseline device
APB CRC32 Engine with explicit register map, APB read/write transaction semantics, reset behavior, polynomial/reflect/initial XOR settings, completion timing and a documented reference algorithm. Do not select a large SoC for first real demonstration. AES-128 and tiny MCU are later benchmarks.

## Environment ownership
A dedicated EDA Environment Owner manages toolchain profiles with immutable image digest, Verilator, cocotb, Yosys, SymbiYosys, OpenROAD, optional SystemC versions, PDK/standard-cell library license/sha, constraints and smoke-test reference. All other Owners request work through centralized EDA Runner using an approved toolchain_profile_id. Direct installs, version drift and unapproved tools are denied and audited.

## Job contract
job_id, project_id, ip_id, ticket_id, requesting_owner, source_commit, spec_sha, test_suite/property_set, tool_name, toolchain_profile_digest, constraints_digest, input_artifact_refs, allowed_execution_time, memory_limit, output_contract, correlation_id, callback_event_key.

## Evidence manifest
source/spec SHA, exact command, tool and image digest, input hashes, constraints, libraries, execution timestamps and exit status, raw stdout/stderr digests, simulation seed, waveform reference, formal proof/counterexample and status, netlist hash, area/timing metrics, parser version, derived report, reviewer and lineage. A parser crash/missing raw report yields UNVERIFIED. No PASS from mocked EDA or human/model narrative.

## Required gates
1. Source+spec+toolchain+constraints fingerprint matches candidate.
2. Simulation regression really executed, expected failures reproduced, no applicable failures remain.
3. Formal mandatory properties pass; UNKNOWN/timeouts are not PASS.
4. Yosys netlist actual synthesis output is preserved.
5. PPA comparisons run consistent constraints, report metrics with provenance.
6. Integration gate independently checks all required evidence and published artifact revision.
7. External or public publication of restricted IP/tool data is prohibited.

## Benchmark path
A2: baseline actual tool runs with vectors; A3: deliberately inject reset-state RTL defect, regression goes red, owner repair, independent re-run green with exact SHA and offline Main; A4: tightened clock target, bounded candidate Arena and full rechecks. Show costs and number of iterations. Same-failure watchdog must stop rather than regenerate unrelated tests/frameworks.
