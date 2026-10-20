"""Regression checks for the standalone kidney anatomy teaching scene."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "components" / "kidney_anatomy_lab.html"
APP = ROOT / "app.py"
DOCS = ROOT / "docs" / "KIDNEY_ANATOMY_LAB.md"


class KidneyAnatomyLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = COMPONENT.read_text(encoding="utf-8")
        cls.app = APP.read_text(encoding="utf-8")
        cls.docs = DOCS.read_text(encoding="utf-8") if DOCS.is_file() else ""

    def test_component_is_loaded_by_hands_on_lab(self):
        self.assertIn('ROOT / "components" / "kidney_anatomy_lab.html"', self.app)
        self.assertIn('organ_lab_html = organ_lab_path.read_text(encoding="utf-8")', self.app)
        self.assertIn('replace("__STATION__", json.dumps(skill))', self.app)
        self.assertIn("components.html(organ_lab_html, height=730, scrolling=False)", self.app)

    def test_single_organ_does_not_depend_on_the_old_remote_pair_asset(self):
        self.assertIn("function makeKidneyGeometry()", self.html)
        self.assertIn('kidneySurface.name="Single kidney outer surface"', self.html)
        self.assertIn("No twin-kidney tray asset or remote organ mesh is required.", self.html)
        self.assertNotIn("https://cdn.3dassets.dev/assets/38958/v1/model.glb", self.html)
        self.assertNotIn("function loadExternalKidney()", self.html)
        self.assertIn("originally", self.docs.lower())
        self.assertIn("procedurally authored geometry", self.docs.lower())

    def test_cutaway_parts_and_hilum_are_named_for_learning(self):
        for label in (
            "Renal cortex", "Renal medulla", "renal pyramid", "Renal column",
            "Minor calyx", "Superior major calyx", "Middle major calyx",
            "Inferior major calyx", "Renal pelvis", "Ureter",
            "Renal artery", "Renal vein", "Single kidney outer surface",
        ):
            with self.subTest(label=label):
                self.assertIn(label.lower(), self.html.lower())
        self.assertIn("function kidneyShape(scale=1)", self.html)
        self.assertIn("medialNotch", self.html)
        self.assertIn("medial hilum", self.docs.lower())

    def test_touch_controls_are_present_and_wired(self):
        controls = (
            "surfaceView", "cutawayView", "cameraMode", "instrumentMode",
            "anatomyToggle", "surfaceToggle", "cortexLayer", "pyramidsLayer",
            "collectingLayer", "vesselsLayer", "sutureDrill", "reset",
            "next", "show", "zoomIn", "zoomOut",
        )
        for control in controls:
            with self.subTest(control=control):
                self.assertIn(f'id="{control}"', self.html)
                self.assertIn(f'byId("{control}")', self.html)
        self.assertIn("function applyView()", self.html)
        self.assertIn("function setView(mode)", self.html)
        self.assertIn("function setInteractionMode(mode)", self.html)
        self.assertIn("drillActive=true", self.html)
        self.assertIn("attempts++", self.html)
        self.assertIn("successful++", self.html)
        self.assertIn('addEventListener("pointermove"', self.html)
        self.assertIn('addEventListener("pointerup"', self.html)

    def test_safety_and_asset_licensing_limits_are_documented(self):
        self.assertIn("not clinically validated", self.html.lower())
        self.assertIn("not a clinically validated anatomical reference", self.docs.lower())
        self.assertIn("does not have validated mesh collision", self.docs.lower())
        self.assertIn("exact file's licence", self.docs.lower())
        self.assertIn("not a measure of surgical competence", self.docs.lower())


if __name__ == "__main__":
    unittest.main()
