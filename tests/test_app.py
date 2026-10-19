import unittest

from streamlit.testing.v1 import AppTest


class AppSmokeTests(unittest.TestCase):
    def test_dashboard_renders_without_exceptions(self):
        app = AppTest.from_file("app.py", default_timeout=15).run()
        self.assertEqual(len(app.exception), 0, str(app.exception))
        self.assertTrue(any("Learn medicine" in str(item.value) for item in app.markdown))


if __name__ == "__main__":
    unittest.main()
