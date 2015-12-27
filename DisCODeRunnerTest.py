import os
import unittest
from DisCODeRunner import DisCODeRunner


class TestDisCODeRunner(unittest.TestCase):
    def setUp(self):
        self.runner = DisCODeRunner()

    def test_discode_exists_on_path(self):
        path = os.environ['PATH']
        self.assertEqual("DisCODe" in path, True)

    def test_if_discode_runs(self):
        message = self.runner.run()
        # self.assertEqual(message, "WARNING: Configuration file config.xml not found.")
        self.assertEqual(message, "\x1b[33mWARNING: \x1b[00mConfiguration file config.xml not found.\n")


if __name__ == '__main__':
    unittest.main()
