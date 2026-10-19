import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_FILE = Path(__file__).parents[1] / "app.py"


class AppSmokeTests(unittest.TestCase):
    def test_dashboard_renders_without_exceptions(self):
        app = AppTest.from_file(str(APP_FILE), default_timeout=15).run()
        self.assertEqual(len(app.exception), 0, str(app.exception))
        self.assertTrue(any("Learn medicine" in str(item.value) for item in app.markdown))


if __name__ == "__main__":
    unittest.main()
