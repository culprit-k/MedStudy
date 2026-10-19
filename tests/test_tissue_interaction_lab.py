"""Static smoke tests for the browser-based tissue interaction prototype.

These tests check expected controls and code paths; they do not validate medical realism.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "components" / "realistic_tissue_interaction_lab.html"
PAGE = ROOT / "pages" / "3_Tissue_Interaction_Lab.py"


class TissueInteractionLabSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = COMPONENT.read_text(encoding="utf-8")
        cls.page = PAGE.read_text(encoding="utf-8")

    def test_page_embeds_component(self):
        self.assertIn("components.html", self.page)
        self.assertIn("realistic_tissue_interaction_lab.html", self.page)

    def test_training_modes_exist(self):
        for mode in ("explore", "palpate", "incise", "suture"):
            with self.subTest(mode=mode):
                self.assertIn(f'data-mode="{mode}"', self.html)

    def test_surface_deformation_and_recovery_exist(self):
        self.assertIn("function deformAt", self.html)
        self.assertIn("function recoverSurface", self.html)
        self.assertIn("deformAt(p,.19,.52)", self.html)

    def test_reset_and_layer_controls_exist(self):
        self.assertIn('id="reset"', self.html)
        self.assertIn('id="layers"', self.html)

    def test_limitations_are_disclosed(self):
        self.assertIn("not a realistic or validated surgical simulator", self.page)
        self.assertIn("not biomechanically calibrated", self.html)

    def test_anatomy_reference_and_physics_roadmap_exist(self):
        self.assertIn("Anatomy reference", self.page)
        self.assertIn("components.iframe", self.page)
        self.assertIn("SOFA", self.page)
        self.assertIn("No finite-element tissue physics", self.page)


if __name__ == "__main__":
    unittest.main()
