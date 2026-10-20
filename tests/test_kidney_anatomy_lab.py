"""Regression checks for the self-contained kidney teaching scene."""
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

    def test_kidney_has_bean_shape_and_named_teaching_structures(self):
        self.assertIn("medialNotch", self.html)
        self.assertIn('kidneySurface.name="Kidney outer surface"', self.html)
        for label in ("Renal cortex", "Renal pyramids", "Renal pelvis", "Ureter",
                      "Renal artery", "Renal vein", "Superior major calyx"):
            with self.subTest(label=label):
                self.assertIn(label, self.html)

    def test_controls_are_present_and_wired(self):
        for control in ("cameraMode", "instrumentMode", "anatomyToggle",
                        "surfaceToggle", "sutureDrill", "reset", "next", "show"):
            with self.subTest(control=control):
                self.assertIn(f'id="{control}"', self.html)
                self.assertRegex(self.html, "getElementById\\(['\"]" + control + "['\"]\\)")
        self.assertIn("function setAnatomyVisible(show)", self.html)
        self.assertIn("function setSurfaceVisible(show)", self.html)
        self.assertIn("function setInteractionMode(next)", self.html)
        self.assertIn("drillActive=true", self.html)
        self.assertIn("drillStep++", self.html)

    def test_model_does_not_download_an_unverified_external_mesh(self):
        self.assertIn("built-in kidney teaching model", self.html.lower())
        self.assertNotIn("cdn.3dassets.dev", self.html)
        self.assertNotIn("loadExternalKidney();", self.html)
        self.assertIn("Built-in kidney teaching model loaded", self.html)

    def test_limitations_are_disclosed(self):
        self.assertIn("schematic", self.html.lower())
        self.assertIn("not a clinically validated mesh", self.html.lower())
        self.assertIn("not a sourced, segmented, clinically validated 3d kidney mesh", self.docs.lower())


if __name__ == "__main__":
    unittest.main()
