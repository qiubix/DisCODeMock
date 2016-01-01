from hamcrest import *
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

        assert_that(discodeExists, equal_to(True))

    def test_if_discode_runs(self):
        message = self.runner.run()
        assert_that(message, contains_string("\x1b[33mWARNING: \x1b[00mConfiguration file config.xml not found.\n"))

    def test_displays_error_when_no_task_specified(self):
        message = self.runner.run()
        assert_that(message, contains_string("ERROR"))
        assert_that(message, contains_string("No task specified!"))

    def test_if_dcl_dir_exists(self):
        import os
        discode_dcl_dir = os.environ['DISCODE_DCL_DIR']
        assert_that(discode_dcl_dir, is_not(empty))

    def test_if_discode_runs_with_task(self):
        self.runner.setTask("CvBasic:SequenceViewer")
        message = self.runner.run()
        assert_that(message, contains_string("Kopiowanie TASKA!"))


if __name__ == '__main__':
    unittest.main()
