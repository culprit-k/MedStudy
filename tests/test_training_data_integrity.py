"""Integrity checks for image discovery and virtual-hospital training data."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
IMAGE_LIBRARY_PATH = ROOT / "data" / "image_library.json"
HOSPITAL_PATH = ROOT / "data" / "hospital_training.json"


class TrainingDataIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image_library = json.loads(IMAGE_LIBRARY_PATH.read_text(encoding="utf-8"))
        cls.hospital = json.loads(HOSPITAL_PATH.read_text(encoding="utf-8"))

    def test_image_library_subjects_and_resources_are_well_formed(self):
        library = self.image_library
        self.assertIsInstance(library.get("version"), int)
        self.assertTrue(library.get("note", "").strip())
        subjects = library.get("subjects")
        self.assertIsInstance(subjects, list)
        self.assertGreater(len(subjects), 0)
        names = []
        for index, subject in enumerate(subjects):
            with self.subTest(kind="subject", index=index):
                self.assertTrue(subject.get("name", "").strip())
                self.assertIsInstance(subject.get("query"), str)
                if subject["name"] != "All subjects":
                    self.assertTrue(subject["query"].strip())
                names.append(subject["name"])
        self.assertEqual(len(names), len(set(names)), "Image-library subject names must be unique")

        resources = library.get("resources")
        self.assertIsInstance(resources, list)
        for index, resource in enumerate(resources):
            with self.subTest(kind="resource", index=index):
                for field in ("name", "url", "description", "licence"):
                    self.assertTrue(resource.get(field, "").strip())
                self.assertTrue(resource["url"].startswith("https://"))

    def test_local_image_catalogue_references_existing_repository_assets(self):
        entries = self.image_library.get("local_images")
        self.assertIsInstance(entries, list)
        self.assertGreater(len(entries), 0)
        root = ROOT.resolve()
        for index, item in enumerate(entries):
            with self.subTest(index=index):
                for field in ("title", "path", "caption"):
                    self.assertTrue(item.get(field, "").strip())
                self.assertIsInstance(item.get("subjects"), list)
                self.assertGreater(len(item["subjects"]), 0)
                path = (ROOT / item["path"]).resolve()
                self.assertTrue(path.is_relative_to(root), "Local image path must stay inside the repository")
                self.assertTrue(path.is_file(), f"Missing local image asset: {item['path']}")

    def test_hospital_data_has_education_only_notice_and_expected_sections(self):
        data = self.hospital
        self.assertIsInstance(data.get("version"), int)
        self.assertIn("Fictional scenarios for education only", data.get("notice", ""))
        for key in ("patient_cases", "organ_systems", "microbiology_tests", "or_workflow", "diagnostic_panels"):
            self.assertIsInstance(data.get(key), list, f"{key} must be a list")
            self.assertGreater(len(data[key]), 0, f"{key} must not be empty")

    def test_patient_cases_have_unique_ids_structured_vitals_and_observations(self):
        cases = self.hospital["patient_cases"]
        ids = [case.get("id") for case in cases]
        self.assertTrue(all(isinstance(value, str) and value.strip() for value in ids))
        self.assertEqual(len(ids), len(set(ids)))
        expected_vitals = {"hr", "systolic_bp", "diastolic_bp", "spo2", "rr", "temperature", "pain", "gcs"}
        for index, case in enumerate(cases):
            with self.subTest(index=index):
                for field in ("name", "location", "level", "presentation", "debrief"):
                    self.assertTrue(case.get(field, "").strip())
                vitals = case.get("vitals")
                self.assertIsInstance(vitals, dict)
                self.assertEqual(set(vitals), expected_vitals)
                self.assertTrue(all(isinstance(value, (int, float)) for value in vitals.values()))
                observations = case.get("observations")
                self.assertIsInstance(observations, list)
                self.assertTrue(observations)
                self.assertTrue(all(isinstance(value, str) and value.strip() for value in observations))

    def test_hospital_answer_keys_reference_existing_options(self):
        for collection in ("microbiology_tests", "diagnostic_panels"):
            for index, item in enumerate(self.hospital[collection]):
                with self.subTest(collection=collection, index=index):
                    for field in ("name", "explanation"):
                        self.assertTrue(item.get(field, "").strip())
                    options = item.get("options")
                    self.assertIsInstance(options, list)
                    self.assertGreaterEqual(len(options), 2)
                    self.assertTrue(all(isinstance(option, str) and option.strip() for option in options))
                    answer = item.get("answer")
                    self.assertIsInstance(answer, int)
                    self.assertGreaterEqual(answer, 0)
                    self.assertLess(answer, len(options))
                    if collection == "diagnostic_panels":
                        rows = item.get("results")
                        self.assertIsInstance(rows, list)
                        self.assertTrue(rows)
                        self.assertTrue(all(isinstance(row, list) and len(row) == 3 for row in rows))

    def test_operating_room_workflow_stages_are_populated(self):
        workflow = self.hospital["or_workflow"]
        stage_names = []
        for index, stage in enumerate(workflow):
            with self.subTest(index=index):
                self.assertTrue(stage.get("stage", "").strip())
                items = stage.get("items")
                self.assertIsInstance(items, list)
                self.assertTrue(items)
                self.assertTrue(all(isinstance(item, str) and item.strip() for item in items))
                stage_names.append(stage["stage"])
        self.assertEqual(len(stage_names), len(set(stage_names)))


if __name__ == "__main__":
    unittest.main()
