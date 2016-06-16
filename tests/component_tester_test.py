import time
import unittest
from os.path import isfile
from subprocess import call

from hamcrest import *

from discoderunner import ComponentTester


class TestComponentTester(unittest.TestCase):
    def setUp(self):
        self.defaultFileName = 'data/test_tasks/test_task.xml'
        if isfile(self.defaultFileName):
            call(['rm', self.defaultFileName])

    def test_component_tester_running(self):
        assert_that(ComponentTester(), is_not(None))

    def test_should_save_to_default_file_on_init(self):
        tester = ComponentTester()

        assert_that(isfile(self.defaultFileName), is_(True))

    def test_should_create_task_template_on_init(self):
        tester = ComponentTester()

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, starts_with('<Task>'))
        assert_that(contents, ends_with('</Task>\n'))
        assert_that(contents, contains_string('<Subtasks>'))
        assert_that(contents, contains_string('</Subtasks>'))
        assert_that(contents, contains_string('<Subtask name="Main"'))
        assert_that(contents, contains_string('<DataStreams/>'))

    def test_should_create_task_with_default_executor_on_init(self):
        tester = ComponentTester()

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string('<Executor name="Processing" period="1"/>'))

    def test_should_add_proper_component_to_task(self):
        tester = ComponentTester()

        tester.setComponent('Summator', 'CvBasic:Sum')

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string('<Component bump="0" name="Summator" priority="1" type="CvBasic:Sum"/>'))

    def test_should_add_generator_to_components(self):
        tester = ComponentTester()

        tester.addGenerator('SampleGenerators:CvMatGenerator')

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string(
                '<Component bump="0" name="Generator" priority="1" type="SampleGenerators:CvMatGenerator"/>'))

    def test_should_add_generator_with_specific_name_to_components(self):
        tester = ComponentTester()

        tester.addGenerator('SampleGenerators:CvMatGenerator', 'AnotherGenerator')

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string(
            '<Component bump="0" name="AnotherGenerator" priority="1" type="SampleGenerators:CvMatGenerator"/>'))

    def test_should_add_sink(self):
        tester = ComponentTester()
        tester.addSink('SampleGenerators:CvMatSink')

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string(
                '<Component bump="0" name="Sink" priority="1" type="SampleGenerators:CvMatSink"/>'))

    def test_should_add_new_datastream(self):
        tester = ComponentTester()

        tester.addDataStream('First', 'out_data', 'Second', 'in_data')

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string('<Source name="First.out_data">\n\t\t\t<sink>Second.in_data</sink>'))

    def test_should_run_discode(self):
        tester = ComponentTester()
        tester.resetTerminationStatements()
        if isfile(self.defaultFileName):
            call(['rm', self.defaultFileName])

        tester.start()

        output = tester.getOutput()
        assert_that(output, contains_string('\x1b[33mWARNING: \x1b[00mConfiguration file config.xml not found.\n'))

    def test_should_run_task_with_default_name(self):
        tester = ComponentTester()
        tester.resetTerminationStatements()
        print(call(['pwd']))
        if isfile(self.defaultFileName):
            call(['rm', self.defaultFileName])

        tester.start()

        output = tester.getOutput()
        assert_that(output, contains_string('Configuration: File \'' + self.defaultFileName + '\' doesn\'t exist.'))

    @unittest.skip('integration test skipped!')
    def test_should_run_specific_task(self):
        tester = ComponentTester()
        tester.resetTerminationStatements()
        tester.taskName = 'SequenceViewer.xml'

        tester.start()
        time.sleep(.500)
        tester.runner.kill()

        output = tester.getOutput()
        assert_that(output, contains_string('Kopiowanie TASKA!'))

    @unittest.skip('integration test skipped!')
    def test_should_stop_discode_manually(self):
        tester = ComponentTester()
        tester.resetTerminationStatements()
        tester.start()
        time.sleep(5)

        tester.stop()

        output = tester.getOutput()
        assert_that(output, contains_string('Finishing DisCODe.'))
        assert_that(output, contains_string('Server stoped.'))

    @unittest.skip('integration test skipped!')
    def test_should_stop_on_termination_statement(self):
        tester = ComponentTester()
        tester.taskName = 'data/SequenceViewer.xml'
        tester.addTerminationStatement('ERROR')
        tester.start()
        time.sleep(.500)

        output = tester.getOutput()
        assert_that(output, contains_string('Finishing DisCODe.'))
        assert_that(output, contains_string('Server stoped.'))

    @unittest.skip('integration test skipped!')
    def test_should_stop_on_error_by_default(self):
        tester = ComponentTester()
        tester.taskName = 'data/SequenceViewer.xml'
        tester.start()
        time.sleep(.500)

        output = tester.getOutput()
        assert_that(output, contains_string('Finishing DisCODe.'))
        assert_that(output, contains_string('Server stoped.'))

    def test_should_have_default_generators_installed(self):
        import os
        discode_dcl_dir = os.environ['DISCODE_DCL_DIR']
        dependencyPath = discode_dcl_dir + '/SampleGenerators/dist'
        assert_that(dependencyPath, is_not(empty))

    def test_should_have_cvbasic_sum_component_installed(self):
        import os
        discode_dcl_dir = os.environ['DISCODE_DCL_DIR']
        libPath = discode_dcl_dir + '/CvBasic/dist/lib/libSum.so'
        print(libPath)
        assert_that(isfile(libPath), is_(True))

    @unittest.skip('integration test skipped!')
    def test_should_check_component_output(self):
        tester = ComponentTester()
        # print('adding generator...')
        tester.addGenerator('SampleGenerators:CvMatGenerator', 'Generator1')
        tester.addGenerator('SampleGenerators:CvMatGenerator', 'Generator2')
        # print('adding component...')
        tester.setComponent('Summator', 'CvBasic:Sum')
        # print('adding component...')
        tester.addSink('SampleGenerators:CvMatSink')
        tester.addDataStream('Generator1', 'out_img', 'Summator', 'in_img1')
        tester.addDataStream('Generator2', 'out_img', 'Summator', 'in_img2')
        tester.addDataStream('Summator', 'out_img', 'Sink', 'in_img')
        tester.addTerminationStatement('END OF SEQUENCE')
        # print('Task body:')
        # print(tester.taskBuilder.getTaskBody())

        tester.start()

        output = tester.getOutput()
        # print(output)
        # print('finished printing output')
        assert_that(output, contains_string('[2, 2, 2, 2;\n  2, 2, 2, 2;\n  2, 2, 2, 2]'))

    @unittest.skip('problem capturing stdout in test')
    def test_should_print_output_in_debug_mode(self):
        tester = ComponentTester()
        tester.taskName = 'data/SequenceViewer.xml'

        tester.setDebugMode(True)

        from io import StringIO
        import sys
        try:
            out = StringIO()
            sys.stdout = out

            tester.start()
            # time.sleep(5)

            output = out.getvalue().strip()
            assert_that(output, contains_string('\x1b[33mWARNING: \x1b[00mConfiguration file config.xml not found.\n'))
        finally:
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main(warnings='ignore', verbosity=2)
