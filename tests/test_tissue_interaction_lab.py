"""Static smoke tests for the browser-based tissue interaction prototype.

These tests check expected controls and code paths; they do not validate medical realism.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "components" / "realistic_tissue_interaction_lab.html"
PAGE = ROOT / "pages" / "3_Tissue_Interaction_Lab.py"
APP = ROOT / "app.py"
README = ROOT / "README.md"
DOCS = ROOT / "docs" / "TISSUE_INTERACTION_LAB.md"


class TissueInteractionLabSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = COMPONENT.read_text(encoding="utf-8")
        cls.page = PAGE.read_text(encoding="utf-8")
        cls.app = APP.read_text(encoding="utf-8")
        cls.readme = README.read_text(encoding="utf-8")
        cls.docs = DOCS.read_text(encoding="utf-8")

    def test_documentation_discloses_model_limits(self):
        self.assertIn("Tissue Interaction Lab", self.readme)
        self.assertIn("not a realistic or clinically validated surgical simulator", self.readme)
        self.assertIn("mass-spring membrane approximation", self.docs)
        self.assertIn("not literature-derived measurements", self.docs)

    def test_main_navigation_routes_to_tissue_lab(self):
        self.assertIn('"Tissue Interaction Lab"', self.app)
        self.assertIn('st.switch_page("pages/3_Tissue_Interaction_Lab.py")', self.app)
        self.assertIn("Tissue interaction lab", self.app)
        self.assertIn("adjustable spring parameters", self.app)

    def test_home_card_button_uses_registered_navigation_target(self):
        self.assertIn('"Tissue Interaction Lab"', self.app)
        self.assertIn('key=f"home_{target}"', self.app)
        self.assertIn('on_click=jump, args=(target,)', self.app)

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
        self.assertIn("const gx=(local.x+2.9)/5.8*segmentX,gz=(local.z+2.05)/4.1*segmentZ", self.html)
        self.assertIn("pos.setY(i,target)", self.html)
        self.assertNotIn("pos.setZ(i,basePos[i*3+2]-indent[i])", self.html)

    def test_damped_spring_membrane_and_render_loop_exist(self):
        self.assertIn("stiffness=34,damping=9,coupling=5.5", self.html)
        self.assertIn("physicsEngine.step(dt)", self.html)
        self.assertIn("TissuePhysicsEngine", self.html)
        self.assertIn("animate();updateMetrics();", self.html)
        self.assertEqual(self.html.count("animate();updateMetrics();"), 1)
        self.assertNotIn("\\\\nfunction", self.html)

    def test_shared_physics_engine_is_loaded_and_tested(self):
        engine = (ROOT / "components" / "tissue_physics_engine.js").read_text(encoding="utf-8")
        tests = (ROOT / "tests" / "tissue_physics_engine.test.js").read_text(encoding="utf-8")
        self.assertIn("TissuePhysicsEngine", engine)
        self.assertIn("Substep large frame times", engine)
        self.assertIn("node --test tests/tissue_physics_engine.test.js", (ROOT / ".github" / "workflows" / "tissue-lab-ci.yml").read_text(encoding="utf-8"))
        self.assertIn("bounded under repeated large contacts", tests)

    def test_collision_engine_and_labelled_proxy_feedback_are_integrated(self):
        self.assertIn("anatomy_collision_engine.js", self.html)
        self.assertIn("AnatomyCollisionEngine.deepestProxyContact", self.html)
        self.assertIn('id="contactState"', self.html)
        self.assertIn('id="structureState"', self.html)
        engine = (ROOT / "components" / "anatomy_collision_engine.js").read_text(encoding="utf-8")
        self.assertIn("function pointPlaneContact", engine)
        self.assertIn("function pointSphereContact", engine)
        self.assertIn("illustrative collision proxy", self.html)
        self.assertIn("deepestSweptProxyContact(lastToolPoint,p,anatomyProxies)", self.html)
        self.assertIn("lastToolPoint=p", self.html)
        self.assertIn("Swept proxy contact", self.html)
        self.assertIn("function sweptSphereContact", engine)
        self.assertIn("function deepestSweptProxyContact", engine)

    def test_reset_and_layer_controls_exist(self):
        self.assertIn('id="reset"', self.html)
        self.assertIn('id="layers"', self.html)

    def test_physics_controls_are_wired_to_model_parameters(self):
        self.assertIn('id="stiffnessSlider"', self.html)
        self.assertIn('id="dampingSlider"', self.html)
        self.assertIn('id="couplingSlider"', self.html)
        self.assertIn("stiffness=Number(e.target.value)", self.html)
        self.assertIn("damping=Number(e.target.value)", self.html)
        self.assertIn("coupling=Number(e.target.value)", self.html)

    def test_limitations_are_disclosed(self):
        self.assertIn("not a realistic or ", self.page)
        self.assertIn("validated surgical simulator", self.page)
        self.assertIn("not biomechanically calibrated", self.html)

    def test_anatomy_reference_and_physics_roadmap_exist(self):
        self.assertIn("Anatomy reference", self.page)
        self.assertIn("components.iframe", self.page)
        self.assertIn("SOFA", self.page)
        self.assertIn("No finite-element tissue physics", self.page)

    def test_membrane_has_bounded_deformation_and_fixed_rim(self):
        self.assertIn("maxDisplacement:.18", self.html)
        self.assertIn("boundaryWidth:2", self.html)
        self.assertIn("applyIndentation(gx,gz,amount", self.html)

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
