import json
import unittest
from pathlib import Path
from siliconforge.runtime import ROUTES,OWNER_SET

ROOT=Path(__file__).resolve().parents[1]
class SpecIntegrityTests(unittest.TestCase):
    def test_routes_match_kernel(self):
        configured=json.loads((ROOT/"config/routes.json").read_text())["routes"]
        self.assertEqual(configured,{k:list(v) for k,v in ROUTES.items()})
        self.assertTrue(all(o in OWNER_SET for os in configured.values() for o in os))
    def test_schemas_load(self):
        schemas=list((ROOT/"contracts").glob("*.schema.json"))
        self.assertGreaterEqual(len(schemas),6)
        for path in schemas:
            s=json.loads(path.read_text())
            self.assertEqual(s["type"],"object")
            self.assertTrue(s["required"])
    def test_acceptance_ids(self):
        text=(ROOT/"docs/09_ACCEPTANCE_TEST_MATRIX.md").read_text()
        for phase,n in (("A0",18),("A1",8),("A2",7),("A3",7),("A4",6),("A5",7),("A6",7)):
            for i in range(1,n+1):
                self.assertIn(f"{phase}-{i:02d}",text)
    def test_native_harness(self):
        p=json.loads((ROOT/"config/harness_policy.json").read_text())
        self.assertIn("codex",p["human_interfaces"])
        self.assertIn("claude_code",p["human_interfaces"])
        self.assertNotIn("siliconforge_custom_cli",p["human_interfaces"])
if __name__=="__main__":
    unittest.main()
