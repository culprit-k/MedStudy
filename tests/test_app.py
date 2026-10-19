import json
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).parents[1]
APP_FILE = ROOT / "app.py"


class AppSmokeTests(unittest.TestCase):
    def test_dashboard_renders_without_exceptions(self):
        app = AppTest.from_file(str(APP_FILE), default_timeout=30).run()
        self.assertEqual(len(app.exception), 0, str(app.exception))
        self.assertTrue(any("Learn medicine" in str(item.value) for item in app.markdown))

    def test_question_bank_schema_and_answer_keys(self):
        data = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))
        self.assertEqual(set(data), {"Anatomy", "Physiology", "Biochemistry", "Pathology", "Microbiology", "Pharmacology"})
        all_ids = []
        for subject, questions in data.items():
            self.assertGreaterEqual(len(questions), 10, subject)
            for question in questions:
                self.assertTrue(question.get("id"), subject)
                self.assertTrue(question.get("question"), subject)
                self.assertGreaterEqual(len(question.get("options", [])), 2, question.get("id"))
                self.assertIn(question.get("answer"), question.get("options", []), question.get("id"))
                self.assertTrue(question.get("explanation"), question.get("id"))
                all_ids.append(question["id"])
        self.assertEqual(len(all_ids), len(set(all_ids)), "Question IDs must be unique")

    def test_visual_question_assets_exist(self):
        visuals = json.loads((ROOT / "data" / "visual_questions.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(visuals), 5)
        for item in visuals:
            self.assertIn(item["answer"], item["options"], item["id"])
            self.assertTrue((ROOT / item["image"]).is_file(), item["image"])

    def test_new_learning_areas_are_in_app_source(self):
        source = APP_FILE.read_text(encoding="utf-8")
        for label in ["Exam Arena", "Visual Lab", "Clinical Cases", "OSCE Studio", "Research & EBM", "Teacher AI"]:
            self.assertIn(label, source)

    def test_hospital_training_catalog_has_all_lab_curricula(self):
        data = json.loads((ROOT / "data" / "hospital_training.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data.get("patient_cases", [])), 4)
        self.assertGreaterEqual(len(data.get("organ_systems", [])), 8)
        self.assertGreaterEqual(len(data.get("microbiology_tests", [])), 8)
        self.assertGreaterEqual(len(data.get("or_workflow", [])), 4)
        self.assertGreaterEqual(len(data.get("diagnostic_panels", [])), 5)
        for test in data["microbiology_tests"]:
            self.assertTrue(test.get("name"))
            self.assertGreaterEqual(len(test.get("options", [])), 2)
            self.assertIn(test.get("answer"), range(len(test["options"])))
            self.assertTrue(test.get("explanation"))
        for panel in data["diagnostic_panels"]:
            self.assertTrue(panel.get("results"))
            self.assertIn(panel.get("answer"), range(len(panel.get("options", []))))

    def test_interactive_3d_anatomy_viewer_uses_detailed_atlas(self):
        source = APP_FILE.read_text(encoding="utf-8")
        for label in ["render_3d_anatomy_viewer", "components.iframe", "https://nqwrc.github.io/3d-anatomy/", "Source code and model credits", "licence before any redistribution"]:
            self.assertIn(label, source)
        viewer = source[source.index("def render_3d_anatomy_viewer"):source.index("def render_hospital_monitor")]
        self.assertNotIn("THREE.SphereGeometry", viewer)
        self.assertIn("components.iframe", viewer)

    def test_virtual_hospital_workspace_is_integrated(self):
        source = APP_FILE.read_text(encoding="utf-8")
        for label in ["Virtual Hospital", "Operating theatre", "Microbiology bench", "Diagnostics lab", "render_hospital_monitor", "render_simulation_scene", "Patient scenario", "Team safety view"]:
            self.assertIn(label, source)

    def test_medical_image_library_catalog_is_complete_and_local_assets_exist(self):
        catalog = json.loads((ROOT / "data" / "image_library.json").read_text(encoding="utf-8"))
        subjects = catalog.get("subjects", [])
        names = [item["name"] for item in subjects]
        self.assertGreaterEqual(len(subjects), 25)
        self.assertEqual(len(names), len(set(names)), "Image-library subjects must be unique")
        self.assertEqual(names[0], "All subjects")
        self.assertGreaterEqual(len(catalog.get("local_images", [])), 5)
        for item in catalog["local_images"]:
            self.assertTrue((ROOT / item["path"]).is_file(), item["path"])
            self.assertTrue(item.get("subjects"), item["title"])
        self.assertGreaterEqual(len(catalog.get("resources", [])), 3)

    def test_image_library_feature_is_in_navigation_and_uses_attribution_metadata(self):
        source = APP_FILE.read_text(encoding="utf-8")
        for text in ["Medical Image Library", "search_wikimedia_images", "LicenseShortName", "Saved image references"]:
            self.assertIn(text, source)


if __name__ == "__main__":
    unittest.main()
