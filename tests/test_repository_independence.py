"""Standalone repository contract tests. Standard library only, no network access."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StandaloneRepositoryTests(unittest.TestCase):
    def test_all_canonical_entrypoints_exist(self):
        required = [
            "README.md", "AGENTS.md", "CLAUDE.md",
            "CODING_AGENT_START_HERE.md", "SiliconForge_Working_SYNC.md",
            "docs/00_MISSION_AND_BOUNDARIES.md",
            "docs/09_ACCEPTANCE_TEST_MATRIX.md",
            "docs/10_CODING_AGENT_EXECUTION_ORDER.md",
            "docs/14_PARALLEL_EXPLORATION_ARCHITECTURE.md",
            "docs/15_PARALLEL_EXPLORATION_ACCEPTANCE.md",
            "docs/16_PARALLEL_EXPLORATION_IMPLEMENTATION.md",
            "docs/17_STANDALONE_REPOSITORY_CONTRACT.md",
            "contracts/parallel_exploration_acceptance.json",
            "contracts/exploration_event.schema.json",
            "config/exploration_policy.json",
            "src/siliconforge/runtime.py",
            "src/siliconforge/mcp_server.py",
            "src/siliconforge/harness.py",
            "tests/test_runtime.py",
            "skills/rtl-owner/SKILL.md",
            "skills/verification-owner/SKILL.md",
            "skills/formal-owner/SKILL.md",
            "skills/ppa-owner/SKILL.md",
            "skills/eda-environment-owner/SKILL.md",
            "simulator/SiliconForge_Autonomy_Simulator_v2.html",
        ]
        for rel in required:
            with self.subTest(path=rel):
                self.assertTrue((ROOT / rel).is_file(), f"missing local file: {rel}")

    def test_no_dependency_on_any_prior_repo(self):
        # Keep the forbidden legacy basename constructed so this test does
        # not itself create a false match in a repository-wide text scan.
        legacy = "codex" + "_" + "coding"
        forbidden = (
            "caseykcc0124/" + legacy,
            "github.com/caseykcc0124/" + legacy,
            legacy + "/SiliconForge",
        )
        suffixes = {".md", ".py", ".json", ".toml", ".yaml", ".yml", ".txt", ".ini", ".cfg", ".sh", ".ps1"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts or path.suffix not in suffixes:
                continue
            relative = path.relative_to(ROOT)
            data = path.read_text(encoding="utf-8")
            for word in forbidden:
                with self.subTest(path=str(relative), pattern=word):
                    self.assertNotIn(word, data, f"cross-repo reference found in {relative}")

    def test_no_git_submodule_or_required_local_symlink(self):
        self.assertFalse((ROOT / ".gitmodules").exists(), "external Git submodules are forbidden")
        for path in ROOT.rglob("*"):
            if ".git" in path.parts:
                continue
            self.assertFalse(path.is_symlink(), f"local source cannot depend on symlink: {path}")

    def test_acceptance_is_complete_and_local(self):
        original = (ROOT / "docs/09_ACCEPTANCE_TEST_MATRIX.md").read_text(encoding="utf-8")
        canonical = (ROOT / "docs/15_PARALLEL_EXPLORATION_ACCEPTANCE.md").read_text(encoding="utf-8")
        counts = {"A0": 18, "A1": 8, "A2": 7, "A3": 7, "A4": 6, "A5": 7, "A6": 7}
        for phase, n in counts.items():
            for i in range(1, n + 1):
                self.assertIn(f"{phase}-{i:02d}", original)
        self.assertEqual(sum(counts.values()), 60)
        tracker = json.loads((ROOT / "contracts/parallel_exploration_acceptance.json").read_text(encoding="utf-8"))
        cases = tracker["cases"]
        required_ids = [f"E{i:02d}" for i in range(1, 21)]
        self.assertEqual([case["case_id"] for case in cases], required_ids)
        self.assertEqual(tracker["existing_required"], 60)
        self.assertEqual(tracker["extension_required"], 20)
        self.assertEqual(tracker["total_required"], 80)
        self.assertTrue(all(c["required"] for c in cases))
        self.assertTrue(all(c["status"] == "NOT_RUN" for c in cases))
        for ident in required_ids:
            self.assertIn(ident, canonical)

    def test_status_points_only_to_this_repo(self):
        status = (ROOT / "SiliconForge_Working_SYNC.md").read_text(encoding="utf-8")
        self.assertRegex(status, r"(?m)^repo:\s+caseykcc0124/SiliconForge$")
        self.assertIn('architecture_baseline: "3.1"', status)
        self.assertIn("E_cases_not_run: 20", status)

if __name__ == "__main__":
    unittest.main()
