import unittest
from DisCODeRunner import DisCODeRunner


class TestDisCODeRunner(unittest.TestCase):
    def setUp(self):
        self.runner = DisCODeRunner()

    def test_discode_exists_on_path(self):
        import os
        discodeExecutable = 'discode'

        def isExe(filepath):
            return os.path.isfile(filepath) and os.access(filepath, os.X_OK)

        discodeExists = False
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            discodePath = os.path.join(path, discodeExecutable)
            if isExe(discodePath):
                discodeExists = True

        self.assertEqual(discodeExists, True)

    def test_if_discode_runs(self):
        message = self.runner.run()
        # self.assertEqual(message, "WARNING: Configuration file config.xml not found.")
        self.assertEqual(message, "\x1b[33mWARNING: \x1b[00mConfiguration file config.xml not found.\n")


if __name__ == '__main__':
    unittest.main()
