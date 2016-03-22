import unittest
import xml.dom.minidom
from hamcrest import *
from subprocess import call

from discoderunner import TaskBuilder


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

    def test_should_set_default_executor_period(self):
        self.builder.createTemplate()
        executorName = 'Custom executor'
        self.builder.addExecutor(executorName)

        contents = self.builder.getTaskBody()
        assert_that(contents,
                    contains_string('<Executor name="' + executorName + '" period="1"/>'))

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

    def test_should_add_component_to_specific_executor(self):
        self.builder.createTemplate()
        self.builder.addDefaultExecutor()
        executorName = 'Second'
        self.builder.addExecutor(executorName, 1)
        componentName = 'Sequence'
        componentType = 'CvBasic:Sequence'
        self.builder.addComponentToExecutor(executorName, componentName, componentType)

        dom = xml.dom.minidom.parseString(self.builder.getTaskBody())
        executors = dom.getElementsByTagName('Executor')
        executor = None
        for e in executors:
            if e.getAttribute('name') == executorName:
                executor = e
        if executor is not None:
            assert_that(executor.childNodes.length, equal_to(3))
            component = executor.childNodes.item(1)
            assert_that(component.getAttribute('name'), equal_to(componentName))
            assert_that(component.getAttribute('type'), equal_to(componentType))
            assert_that(component.getAttribute('priority'), equal_to('1'))
            assert_that(component.getAttribute('bump'), equal_to('0'))
        else:
            assert_that(True, equal_to(False))

    def test_should_add_params_to_component(self):
        self.builder.createTemplate()
        self.builder.addDefaultExecutor()
        self.builder.addComponent('First', 'CvBasic:Sequence')
        self.builder.addComponent('Second', 'CvBasic:SIFT')

        secondParamValue = '.*\.jpg'
        firstParamValue = '/some/directory'
        secondParamName = 'sequence.pattern'
        firstParamName = 'sequence.directory'
        self.builder.addParamToComponent('Second', firstParamName, firstParamValue)
        self.builder.addParamToComponent('Second', secondParamName, secondParamValue)

        dom = xml.dom.minidom.parseString(self.builder.getTaskBody())
        component = dom.getElementsByTagName('Component').item(1)
        assert_that(component.childNodes.length, equal_to(5))
        firstParam = component.childNodes.item(1)
        assert_that(firstParam.getAttribute('name'), equal_to(firstParamName))
        assert_that(firstParam.firstChild.data, equal_to(firstParamValue))
        secondParam = component.childNodes.item(3)
        assert_that(secondParam.getAttribute('name'), equal_to(secondParamName))
        assert_that(secondParam.firstChild.data, equal_to(secondParamValue))

    def test_should_add_data_stream(self):
        self.builder.createTemplate()

        sourceName = 'First.out_put'
        sinkName = 'Second.in_put'
        self.builder.addDataStream(sourceName, sinkName)

        dom = xml.dom.minidom.parseString(self.builder.getTaskBody())
        datastreams = dom.getElementsByTagName('Source')
        assert_that(datastreams.length, equal_to(1))
        datastream = datastreams.item(0)
        assert_that(datastream.getAttribute('name'), equal_to(sourceName))
        sink = datastream.childNodes.item(1)
        assert_that(sink.nodeName, equal_to('sink'))
        assert_that(sink.firstChild.data, equal_to(sinkName))

    def test_should_update_data_stream_source(self):
        self.builder.createTemplate()
        sourceName = 'First.out_put'
        sinkName = 'Second.in_put'
        self.builder.addDataStream(sourceName, sinkName)

        newSourceName = 'out_data'
        self.builder.updateSource('First', newSourceName)

        dom = xml.dom.minidom.parseString(self.builder.getTaskBody())
        datastreams = dom.getElementsByTagName('Source')
        assert_that(datastreams.length, equal_to(1))
        datastream = datastreams.item(0)
        assert_that(datastream.getAttribute('name'), equal_to('First.' + newSourceName))
        sink = datastream.childNodes.item(1)
        assert_that(sink.nodeName, equal_to('sink'))
        assert_that(sink.firstChild.data, equal_to(sinkName))

    def test_should_return_true_if_datastream_source_already_exist(self):
        self.builder.createTemplate()
        sourceName = 'First.out_put'
        sinkName = 'Second.in_put'
        self.builder.addDataStream(sourceName, sinkName)

        assert_that(self.builder.hasSource(sourceName), is_(True))

    def test_should_return_false_if_datastream_source_doesnt_exist(self):
        self.builder.createTemplate()

        assert_that(self.builder.hasSource('Any.source'), is_(False))

        sourceName = 'First.out_put'
        sinkName = 'Second.in_put'
        self.builder.addDataStream(sourceName, sinkName)

        assert_that(self.builder.hasSource('Another.out_put'), is_(False))

    def test_should_update_data_stream_sink(self):
        self.builder.createTemplate()
        sourceName = 'First.out_put'
        sinkName = 'Second.in_put'
        self.builder.addDataStream(sourceName, sinkName)

        newComponentName = 'Third'
        newSinkName = 'in_data'
        self.builder.updateSink('Second', newComponentName, newSinkName)

        dom = xml.dom.minidom.parseString(self.builder.getTaskBody())
        datastreams = dom.getElementsByTagName('Source')
        assert_that(datastreams.length, equal_to(1))
        datastream = datastreams.item(0)
        assert_that(datastream.getAttribute('name'), equal_to('First.out_put'))
        sink = datastream.childNodes.item(1)
        assert_that(sink.nodeName, equal_to('sink'))
        assert_that(sink.firstChild.data, equal_to(newComponentName + '.' + newSinkName))


if __name__ == '__main__':
    unittest.main(verbosity=2)
