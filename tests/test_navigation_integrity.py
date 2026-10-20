"""Static integrity checks for MedStudy's page navigation and runtime data files."""
import ast
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "app.py"


def navigation_options(source: str) -> list[str]:
    """Extract the label list passed to the sidebar navigation radio without importing Streamlit."""
    match = re.search(
        r'page\s*=\s*st\.radio\(\s*"YOUR WORKSPACE"\s*,\s*(\[[\s\S]*?\])\s*,\s*key="navigation"',
        source,
    )
    if not match:
        raise AssertionError("Could not find the registered sidebar navigation list")
    options = ast.literal_eval(match.group(1))
    if not isinstance(options, list) or not all(isinstance(item, str) for item in options):
        raise AssertionError("The sidebar navigation options must be a list of strings")
    return options


def routed_page_labels(source: str) -> set[str]:
    """Collect exact-match and grouped page labels handled by app.py's rendering branches."""
    labels = set(re.findall(r'\b(?:if|elif)\s+page\s*==\s*["\']([^"\']+)["\']', source))
    for match in re.finditer(r'\b(?:if|elif)\s+page\s+in\s*(\[[\s\S]*?\])\s*:', source):
        values = ast.literal_eval(match.group(1))
        if isinstance(values, list) and all(isinstance(item, str) for item in values):
            labels.update(values)
    return labels


class NavigationIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = APP_PATH.read_text(encoding="utf-8")
        cls.options = navigation_options(cls.source)
        cls.routed = routed_page_labels(cls.source)

    def test_navigation_labels_are_unique(self):
        self.assertEqual(len(self.options), len(set(self.options)), "Sidebar navigation labels must be unique")

    def test_every_navigation_label_has_a_rendering_route(self):
        missing = sorted(set(self.options) - self.routed)
        self.assertEqual(missing, [], f"Navigation labels without a rendering route: {missing}")

    def test_retired_heavy_simulator_is_not_in_primary_navigation(self):
        self.assertNotIn("Tissue Interaction Lab", self.options)
        self.assertNotIn("Hands-on Skills Lab", self.options)
        self.assertNotIn('if page == "Tissue Interaction Lab":', self.source)
        self.assertIn("Image Quiz", self.options)
        self.assertIn("Teacher AI", self.options)

    def test_app_runtime_data_files_exist_and_are_valid_json(self):
        paths = (
            "data/questions.json",
            "data/visual_questions.json",
            "data/image_library.json",
            "data/hospital_training.json",
        )
        for relative in paths:
            with self.subTest(path=relative):
                path = ROOT / relative
                self.assertTrue(path.is_file(), f"Missing runtime data file: {relative}")
                import json
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertIsNotNone(payload, f"Empty JSON payload: {relative}")


if __name__ == "__main__":
    unittest.main()
