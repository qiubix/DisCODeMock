import os
import unittest
from DisCODeRunner import DisCODeRunner


class TestDisCODeRunner(unittest.TestCase):
    def setUp(self):
        self.runner = DisCODeRunner()

    def test_discode_exists_on_path(self):
        path = os.environ['PATH']
        self.assertEqual("DisCODe" in path, True)

    def test_if_discode_installed(self):
        self.assertEqual(self.runner.run(), "WARNING: Configuration file config.xml not found.")


if __name__ == '__main__':
    unittest.main()
