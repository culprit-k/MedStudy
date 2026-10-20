"""Integrity checks for MedStudy's local question banks and illustration assets."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = ROOT / "data" / "questions.json"
VISUAL_PATH = ROOT / "data" / "visual_questions.json"
README_PATH = ROOT / "README.md"
EXPECTED_SUBJECTS = {
    "Anatomy",
    "Physiology",
    "Biochemistry",
    "Pathology",
    "Microbiology",
    "Pharmacology",
}


class QuestionBankIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = json.loads(CORE_PATH.read_text(encoding="utf-8"))
        cls.visual = json.loads(VISUAL_PATH.read_text(encoding="utf-8"))
        cls.readme = README_PATH.read_text(encoding="utf-8")

    def test_core_bank_has_expected_subjects_and_documented_count(self):
        self.assertEqual(set(self.core), EXPECTED_SUBJECTS)
        self.assertTrue(all(isinstance(items, list) for items in self.core.values()))
        total = sum(len(items) for items in self.core.values())
        self.assertEqual(total, 120, "Update the README and this assertion when the starter bank grows")
        self.assertIn("growing educational starter set", self.readme)
        self.assertIn("question bank", self.readme.lower())

    def test_core_questions_have_valid_schema_and_answer_keys(self):
        required = ("id", "question", "answer", "explanation")
        for subject, questions in self.core.items():
            for index, item in enumerate(questions):
                with self.subTest(subject=subject, index=index):
                    for field in required:
                        self.assertIsInstance(item.get(field), str)
                        self.assertTrue(item[field].strip())
                    options = item.get("options")
                    self.assertIsInstance(options, list)
                    self.assertGreaterEqual(len(options), 2)
                    self.assertTrue(all(isinstance(option, str) and option.strip() for option in options))
                    self.assertEqual(len(options), len(set(options)), "Options should not be duplicated")
                    self.assertIn(item["answer"], options)

    def test_all_question_ids_are_unique_across_banks(self):
        ids = []
        for questions in self.core.values():
            ids.extend(item.get("id") for item in questions)
        ids.extend(item.get("id") for item in self.visual)
        self.assertTrue(all(isinstance(question_id, str) and question_id.strip() for question_id in ids))
        self.assertEqual(len(ids), len(set(ids)), "Question IDs must be unique across both banks")

    def test_visual_questions_have_valid_schema_and_local_assets(self):
        required = ("id", "subject", "level", "image", "image_caption", "question", "answer", "explanation", "pearl")
        self.assertGreater(len(self.visual), 0)
        for index, item in enumerate(self.visual):
            with self.subTest(index=index):
                for field in required:
                    self.assertIsInstance(item.get(field), str)
                    self.assertTrue(item[field].strip())
                options = item.get("options")
                self.assertIsInstance(options, list)
                self.assertGreaterEqual(len(options), 2)
                self.assertTrue(all(isinstance(option, str) and option.strip() for option in options))
                self.assertEqual(len(options), len(set(options)), "Options should not be duplicated")
                self.assertIn(item["answer"], options)
                asset_path = (ROOT / item["image"]).resolve()
                self.assertTrue(asset_path.is_relative_to(ROOT.resolve()), "Image paths must stay within the repository")
                self.assertTrue(asset_path.is_file(), f"Missing visual-question asset: {item['image']}")


if __name__ == "__main__":
    unittest.main()
