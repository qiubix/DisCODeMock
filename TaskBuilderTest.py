import unittest
from hamcrest import *
from subprocess import call
from TaskBuilder import TaskBuilder


class TaskBuilderTest(unittest.TestCase):
    def test_should_create_file_with_specific_name(self):
        file_name = 'test_tasks/test_task.xml'
        sample_string = 'sample string'
        call(['rm', 'test_tasks/test_task.xml'])
        builder = TaskBuilder()
        builder.fileName = file_name

        builder.writeToFile(sample_string)

        file = open(file_name)
        assert_that(file.read(), sample_string)


if __name__ == '__main__':
    unittest.main(verbosity=2)
