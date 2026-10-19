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

    def test_surface_deformation_uses_correct_plane_axes(self):
        self.assertIn("function deformAt", self.html)
        self.assertIn("function recoverSurface", self.html)
        self.assertIn("deformAt(p,.19,.52)", self.html)
        self.assertIn("pos.getZ(i)-local.z", self.html)
        self.assertIn("pos.setY(i,target)", self.html)
        self.assertNotIn("pos.setZ(i,basePos[i*3+2]-indent[i])", self.html)

    def test_damped_spring_membrane_and_render_loop_exist(self):
        self.assertIn("const stiffness=34,damping=9,coupling=5.5", self.html)
        self.assertIn("const acceleration=-stiffness*indent[i]-damping*velocity[i]", self.html)
        self.assertIn("animate();updateMetrics();", self.html)
        self.assertEqual(self.html.count("animate();updateMetrics();"), 1)
        self.assertNotIn("\\\\nfunction", self.html)

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

    def test_external_body_mesh_has_loader_focus_and_disclosure(self):
        self.assertIn("GLTFLoader.js", self.html)
        self.assertIn("human_posed.glb", self.html)
        self.assertIn('id="bodyModel"', self.html)
        self.assertIn("function setBodyView(show)", self.html)
        self.assertIn("model.rotation.z=-Math.PI/2", self.html)
        self.assertIn("not internal anatomy", self.html)
        self.assertIn("tool.position.set(p.x-.36,p.y+.035,p.z)", self.html)
        self.assertIn("if(dragging&&mode==='explore'){az-=", self.html)
        self.assertIn("CC0 1.0", self.page)


if __name__ == "__main__":
    unittest.main()
