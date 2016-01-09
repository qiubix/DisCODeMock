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

        contents = self.builder.getTaskBody()
        assert_that(contents, starts_with('<Task>'))
        assert_that(contents, ends_with('</Task>\n'))

    def test_should_have_subtasks_and_datastreams_elements(self):
        self.builder.createTemplate()

        contents = xml.dom.minidom.parseString(self.builder.getTaskBody())
        subtasksElements = contents.getElementsByTagName('Subtasks')
        datasetsElements = contents.getElementsByTagName('DataStreams')
        assert_that(subtasksElements.length, equal_to(1))
        assert_that(datasetsElements.length, equal_to(1))

    def test_should_have_main_subtask_element(self):
        self.builder.createTemplate()

        contents = self.builder.getTaskBody()
        assert_that(contents, contains_string('<Subtask name="Main"/>'))

    def test_should_create_executor(self):
        self.builder.createTemplate()
        executorName = 'Custom executor'
        executorPeriod = 2
        self.builder.addExecutor(executorName, executorPeriod)

        contents = self.builder.getTaskBody()
        assert_that(contents,
                    contains_string('<Executor name="' + executorName + '" period="' + str(executorPeriod) + '"/>'))

    def test_should_create_default_executor(self):
        self.builder.createTemplate()
        self.builder.addDefaultExecutor()

        contents = self.builder.getTaskBody()
        assert_that(contents, contains_string('<Executor name="Processing" period="1"/>'))

    def test_should_add_component_to_default_executor(self):
        self.builder.createTemplate()
        self.builder.addDefaultExecutor()
        name = 'Sequence'
        componentType = 'CvBasic:Sequence'
        priority = 1
        bump = 0
        self.builder.addComponent(name, componentType, priority, bump)

        contents = self.builder.getTaskBody()
        dom = xml.dom.minidom.parseString(self.builder.getTaskBody())
        components = dom.getElementsByTagName('Component')
        assert_that(components.length, equal_to(1))
        component = components.item(0)
        assert_that(component.getAttribute('name'), equal_to(name))
        assert_that(component.getAttribute('type'), equal_to(componentType))
        assert_that(component.getAttribute('priority'), equal_to(str(priority)))
        assert_that(component.getAttribute('bump'), equal_to(str(bump)))
        assert_that(contents,
                    contains_string('<Component'
                                    ' bump="' + str(bump) + '"'
                                    ' name="' + name + '"'
                                    ' priority="' + str(priority) + '"'
                                    ' type="' + componentType + '"'
                                                       '/>'))

    def test_should_add_component_with_default_attribute_values(self):
        self.builder.createTemplate()
        self.builder.addDefaultExecutor()
        name = 'Sequence'
        componentType = 'CvBasic:Sequence'
        self.builder.addComponent(name, componentType)

        dom = xml.dom.minidom.parseString(self.builder.getTaskBody())
        component = dom.getElementsByTagName('Component').item(0)
        assert_that(component.getAttribute('name'), equal_to(name))
        assert_that(component.getAttribute('type'), equal_to(componentType))
        assert_that(component.getAttribute('priority'), equal_to('1'))
        assert_that(component.getAttribute('bump'), equal_to('0'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
