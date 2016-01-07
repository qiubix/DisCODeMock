import unittest
from hamcrest import *
from subprocess import call

from TaskBuilder import TaskBuilder


class TaskBuilderTest(unittest.TestCase):
    def setUp(self):
        self.defaultFileName = 'test_tasks/test_task.xml'
        self.builder = TaskBuilder()

    def test_should_create_file_with_specific_name(self):
        file_name = 'test_tasks/sample_test_task.xml'
        sample_string = 'sample string'
        call(['rm', 'test_tasks/sample_test_task.xml'])
        self.builder.fileName = file_name

        self.builder.writeToFile(sample_string)

        file = open(file_name)
        assert_that(file.read(), sample_string)

    def test_should_save_task_to_default_file(self):
        taskBody = 'Task body'
        self.builder.taskBody = taskBody

        self.builder.save()

        file = open(self.defaultFileName)
        assert_that(file.read(), taskBody)


if __name__ == '__main__':
    unittest.main(verbosity=2)
