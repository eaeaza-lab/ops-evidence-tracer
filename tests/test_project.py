import json
from pathlib import Path
import unittest

import app


ROOT = Path(__file__).resolve().parents[1]


class ProjectSkeletonTests(unittest.TestCase):
    def test_required_project_files_exist(self):
        for name in ("SPEC.md", "PLANS.md", "README.md", "AGENTS.md", ".nightshift.json"):
            self.assertTrue((ROOT / name).is_file(), name)

    def test_runner_configuration_uses_allowed_test_command(self):
        config = json.loads((ROOT / ".nightshift.json").read_text(encoding="utf-8"))
        self.assertEqual(config["check"], ["python -m unittest discover -s tests"])

    def test_handler_is_available_and_offline_health_is_declared(self):
        self.assertTrue(issubclass(app.EvidenceTracerHandler, object))
        self.assertIn('"mode":"offline"', app.EvidenceTracerHandler.do_GET.__code__.co_consts)

    def test_synthetic_issue_scenario_is_planned(self):
        spec = (ROOT / "SPEC.md").read_text(encoding="utf-8")
        self.assertIn("quantity conflicts", spec)
        self.assertIn("missing links", spec)


if __name__ == "__main__":
    unittest.main()
