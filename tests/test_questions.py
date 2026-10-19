import json
import unittest
from pathlib import Path

DATA_FILE = Path(__file__).parents[1] / "data" / "questions.json"


class QuestionBankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with DATA_FILE.open(encoding="utf-8") as file:
            cls.questions = json.load(file)

    def test_expected_subjects_exist(self):
        expected = {
            "Anatomy", "Physiology", "Biochemistry",
            "Pathology", "Microbiology", "Pharmacology",
        }
        self.assertTrue(expected.issubset(self.questions.keys()))

    def test_question_records_are_complete(self):
        seen_ids = set()
        for subject, items in self.questions.items():
            self.assertTrue(items, f"{subject} should contain at least one question")
            for item in items:
                with self.subTest(question=item.get("id", "unknown")):
                    for field in ("id", "question", "options", "answer", "explanation"):
                        self.assertIn(field, item)
                    self.assertNotIn(item["id"], seen_ids, "Question IDs must be unique")
                    seen_ids.add(item["id"])
                    self.assertGreaterEqual(len(item["options"]), 2)
                    self.assertEqual(len(item["options"]), len(set(item["options"])))
                    self.assertIn(item["answer"], item["options"])
                    self.assertTrue(item["question"].strip())
                    self.assertTrue(item["explanation"].strip())
                    self.assertIsInstance(item["options"], list)

    def test_question_bank_has_at_least_one_question_per_subject(self):
        self.assertGreaterEqual(sum(len(items) for items in self.questions.values()), 30)

    def test_each_subject_has_questions(self):
        for subject, items in self.questions.items():
            with self.subTest(subject=subject):
                self.assertGreaterEqual(len(items), 3)


if __name__ == "__main__":
    unittest.main()
