import unittest
from hamcrest import *
from subprocess import call

from TaskBuilder import TaskBuilder


class TaskBuilderTest(unittest.TestCase):
    def test_should_create_file_with_specific_name(self):
        file_name = 'test_tasks/sample_test_task.xml'
        sample_string = 'sample string'
        call(['rm', 'test_tasks/sample_test_task.xml'])
        builder = TaskBuilder()
        builder.fileName = file_name

        builder.writeToFile(sample_string)

        file = open(file_name)
        assert_that(file.read(), sample_string)

    def test_should_save_task_to_default_file(self):
        defaultFileName = 'test_tasks/test_task.xml'
        taskBody = 'Task body'
        builder = TaskBuilder()
        builder.taskBody = taskBody

        builder.save()
        file = open(defaultFileName)
        assert_that(file.read(), taskBody)


if __name__ == '__main__':
    unittest.main(verbosity=2)
