"""Regression checks for the kidney anatomy teaching scene."""
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

    def test_cc0_kidney_mesh_and_procedural_fallback_are_configured(self):
        self.assertIn("https://cdn.3dassets.dev/assets/38958/v1/model.glb", self.html)
        self.assertIn("https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js", self.html)
        self.assertIn("function loadExternalKidney()", self.html)
        self.assertIn("External kidney mesh unavailable", self.html)
        self.assertIn("built-in kidney fallback", self.html.lower())
        self.assertIn("CC0", self.docs)
        self.assertIn("3dassets.dev", self.docs)

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
                self.assertIn("getElementById", self.html)
                self.assertIn(control, self.html)
        self.assertIn("function setAnatomyVisible(show)", self.html)
        self.assertIn("function setSurfaceVisible(show)", self.html)
        self.assertIn("function setInteractionMode(next)", self.html)
        self.assertIn("drillActive=true", self.html)
        self.assertIn("drillStep++", self.html)

    def test_limitations_are_disclosed(self):
        self.assertIn("schematic", self.html.lower())
        self.assertIn("not registered to this mesh", self.html.lower())
        self.assertIn("not a sourced, segmented, clinically validated 3d kidney mesh", self.docs.lower())


if __name__ == "__main__":
    unittest.main()
