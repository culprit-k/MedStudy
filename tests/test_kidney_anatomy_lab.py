"""Regression checks that the old schematic kidney simulator is archived, not in the learner flow."""
from pathlib import Path
import ast
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"


class ArchivedKidneyLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = APP.read_text(encoding="utf-8")

    def test_kidney_simulator_is_not_loaded_by_the_main_app(self):
        self.assertNotIn('ROOT / "components" / "kidney_anatomy_lab.html"', self.app)
        self.assertNotIn('elif page == "Hands-on Skills Lab":', self.app)
        self.assertNotIn("Hands-on Skills Lab", self.app)

    def test_primary_navigation_prioritises_image_learning(self):
        match = re.search(
            r'page\\s*=\\s*st\\.radio\\(\\s*"YOUR WORKSPACE"\\s*,\\s*(\\[[\\s\\S]*?\\])\\s*,\\s*key="navigation"',
            self.app,
        )
        self.assertIsNotNone(match, "Sidebar navigation list must exist")
        options = ast.literal_eval(match.group(1))
        self.assertIn("Image Quiz", options)
        self.assertIn("Teacher AI", options)
        self.assertNotIn("Hands-on Skills Lab", options)
        self.assertNotIn("Tissue Interaction Lab", options)


if __name__ == "__main__":
    unittest.main()
