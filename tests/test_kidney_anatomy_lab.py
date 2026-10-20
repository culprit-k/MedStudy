"""Regression checks for the interactive kidney anatomy component."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "app.py"
COMPONENT_PATH = ROOT / "components" / "kidney_anatomy_lab.html"
DOC_PATH = ROOT / "docs" / "KIDNEY_ANATOMY_LAB.md"


class KidneyAnatomyLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = APP_PATH.read_text(encoding="utf-8")
        cls.html = COMPONENT_PATH.read_text(encoding="utf-8")
        cls.docs = DOC_PATH.read_text(encoding="utf-8") if DOC_PATH.is_file() else ""

    def test_skills_lab_uses_standalone_kidney_component(self):
        self.assertIn('ROOT / "components" / "kidney_anatomy_lab.html"', self.app)
        self.assertIn('organ_lab_html = organ_lab_path.read_text(encoding="utf-8")', self.app)
        self.assertIn("components.html(organ_lab_html, height=730, scrolling=False)", self.app)
        self.assertTrue(COMPONENT_PATH.is_file())

    def test_real_cc0_kidney_model_and_fallback_are_configured(self):
        self.assertIn("https://cdn.3dassets.dev/assets/38958/v1/model.glb", self.html)
        self.assertIn("https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js", self.html)
        self.assertIn('model.name="CC0 anatomical kidney model"', self.html)
        self.assertIn("The built-in 3D kidney fallback remains available", self.html)
        self.assertIn("CC0", self.docs)
        self.assertIn("3dassets.dev", self.docs)

    def test_anatomy_and_tissue_landmark_controls_are_wired(self):
        for element_id in (
            "cameraMode",
            "instrumentMode",
            "anatomyToggle",
            "surfaceToggle",
            "sutureDrill",
            "reset",
            "assetStatus",
        ):
            with self.subTest(element_id=element_id):
                self.assertIn(f'id="{element_id}"', self.html)
        for landmark in ("Renal cortex", "Renal pyramids", "Renal pelvis", "Renal artery", "Renal vein", "Ureter"):
            with self.subTest(landmark=landmark):
                self.assertIn(landmark, self.html)
        self.assertIn("pointermove", self.html)
        self.assertIn("Alignment drill", self.html)

    def test_external_model_and_internal_overlay_limitations_are_disclosed(self):
        self.assertIn("internal overlay is schematic and not registered to the source mesh", self.html)
        self.assertIn("not real suturing technique", self.html)
        self.assertIn("not force feedback", self.html)
        self.assertIn("not a validated", self.docs.lower())

    def test_component_has_no_accidental_python_string_delimiter(self):
        self.assertFalse(self.html.rstrip().endswith('"""'))
        self.assertIn("function loadExternalKidney()", self.html)
        self.assertIn("requestAnimationFrame(animate)", self.html)


if __name__ == "__main__":
    unittest.main()
