"""Validate dynamic supervisor instruction channel without requiring remote Git."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]

class SupervisorWorkOrderContractTests(unittest.TestCase):
    def test_directive_version_and_stable_url(self):
        doc=(ROOT/"docs/19_SUPERVISOR_WORK_ORDER.md").read_text(encoding="utf-8")
        self.assertRegex(doc,r"DIRECTIVE_ID: SF-DIR-\d{8}-\d{2}")
        self.assertIn("SiliconForge_Working_SYNC.md",doc)
        self.assertIn("每 15 分鐘",doc)
        self.assertIn("G0：A0 CLOSE",doc)
        self.assertIn("G7：A6 + A6X",doc)
        self.assertIn("GitHub Web Edit",doc)
    def test_sync_points_to_current_supervisor_version(self):
        directive=(ROOT/"docs/19_SUPERVISOR_WORK_ORDER.md").read_text(encoding="utf-8")
        sync=(ROOT/"SiliconForge_Working_SYNC.md").read_text(encoding="utf-8")
        match=re.search(r"^> \*\*DIRECTIVE_ID: ([\w-]+)\*\*",directive,re.M)
        self.assertIsNotNone(match)
        self.assertIn("current_directive_id: "+match.group(1),sync)
        self.assertIn("docs/19_SUPERVISOR_WORK_ORDER.md",sync)
        self.assertIn("last_seen_directive_id:",sync)
        self.assertIn("directive_application_state:",sync)
    def test_agent_guidance_requires_active_session_poll(self):
        for path in ("AGENTS.md","CODING_AGENT_START_HERE.md","docs/10_CODING_AGENT_EXECUTION_ORDER.md","docs/18_BROWSER_ZIP_CODING_AGENT_HANDOFF.md"):
            with self.subTest(file=path):
                content=(ROOT/path).read_text(encoding="utf-8")
                self.assertIn("docs/19_SUPERVISOR_WORK_ORDER.md",content)
                self.assertIn("15",content)
        work=(ROOT/"docs/19_SUPERVISOR_WORK_ORDER.md").read_text(encoding="utf-8")
        self.assertIn("ACTIVE_SESSION_ONLY",work)
        self.assertIn("不能",work)
        self.assertIn("80",work)
if __name__=="__main__":
    unittest.main()
