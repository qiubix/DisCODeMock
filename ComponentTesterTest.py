from hamcrest import *
import unittest

from ComponentTester import ComponentTester


class TestComponentTester(unittest.TestCase):
    def setUp(self):
        self.defaultFileName = 'test_tasks/test_task.xml'

    def test_component_tester_running(self):
        assert_that(ComponentTester(), is_not(None))

    def test_adds_proper_component_to_task(self):
        tester = ComponentTester()
        tester.setComponent('Summator', 'CvBasic:Sum')

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string('<Component bump="0" name="Summator" priority="1" type="CvBasic:Sum"/>'))

    def test_adds_generator_to_components(self):
        tester = ComponentTester()
        tester.addGenerator('SampleGenerators:CvMatGenerator')

        with open(self.defaultFileName) as file:
            contents = file.read()
        assert_that(contents, contains_string(
            '<Component bump="0" name="Generator" priority="1" type="SampleGenerators:CvMatGenerator"/>'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
