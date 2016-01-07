import unittest
import xml.dom.minidom
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

        with open(file_name) as file:
            contents = file.read()
        assert_that(contents, sample_string)

    def test_should_save_task_to_default_file(self):
        taskBody = 'Task body'
        self.builder.taskBody = taskBody

        self.builder.save()

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, equal_to(taskBody))

    def test_should_have_task_tag_on_top_level(self):
        self.builder.createTemplate()

        contents = self.builder.taskBody
        assert_that(contents, starts_with('<Task>'))
        assert_that(contents, ends_with('</Task>'))

    def test_should_have_subtasks_and_datastreams_elements(self):
        self.builder.createTemplate()

        contents = xml.dom.minidom.parseString(self.builder.taskBody)
        subtasksElements = contents.getElementsByTagName('Subtasks')
        datasetsElements = contents.getElementsByTagName('Datasets')
        assert_that(subtasksElements.length, equal_to(1))
        assert_that(datasetsElements.length, equal_to(1))

    @unittest.skip('wip')
    def test_should_have_main_subtask_element(self):
        self.builder.createTemplate()

        contents = self.builder.taskBody
        assert_that(contents, contains_string('<Subtask name="Main">\n</Subtask>'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
