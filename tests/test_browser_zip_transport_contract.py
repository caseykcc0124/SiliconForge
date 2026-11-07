"""Protect the external Coding Agent's actual Browser/ZIP/local-Git workflow."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BrowserZipTransportTests(unittest.TestCase):
    def test_sync_is_self_contained_first_entrypoint(self):
        sync = (ROOT / "SiliconForge_Working_SYNC.md").read_text(encoding="utf-8")
        self.assertIn("## IMPORTANT: External Coding Agent", sync)
        self.assertIn("Code → Download ZIP", sync)
        self.assertIn("GITHUB_WEB_DOWNLOAD_ZIP", sync)
        self.assertIn("WEB_EDIT_SINGLE_SYNC_FILE", sync)
        self.assertIn("git_scope: LOCAL_ONLY", sync)
        self.assertIn("local_artifact_transfer: NOT_ESTABLISHED", sync)
        self.assertIn("Source Integrated", sync) if "Source Integrated" in sync else self.assertIn("GitHub source", sync)

    def test_canonical_guidance_has_transport_override(self):
        for rel, phrase in [
            ("AGENTS.md", "External Coding Agent environment override"),
            ("CODING_AGENT_START_HERE.md", "GitHub Clone"),
            ("docs/10_CODING_AGENT_EXECUTION_ORDER.md", "Current external Coding Agent I/O restriction"),
            ("docs/12_GITHUB_BOOTSTRAP_AND_SYNC.md", "Current external Coding Agent access"),
            ("docs/17_STANDALONE_REPOSITORY_CONTRACT.md", "Download ZIP"),
            ("docs/18_BROWSER_ZIP_CODING_AGENT_HANDOFF.md", "GitHub → Local"),
        ]:
            with self.subTest(file=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn(phrase, text)

    def test_no_local_git_commit_can_be_remote_verified(self):
        policy = (ROOT / "docs/18_BROWSER_ZIP_CODING_AGENT_HANDOFF.md").read_text(encoding="utf-8")
        self.assertIn("Local Git", policy)
        self.assertIn("Local Code Implemented", policy)
        self.assertIn("Source Integrated on GitHub", policy)
        self.assertIn("Local Artifact", policy)
        self.assertIn("不得聲稱程式碼已同步", policy)

if __name__ == "__main__":
    unittest.main()
