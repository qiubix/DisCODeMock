from hamcrest import *
import unittest

from ComponentTester import ComponentTester


class TestComponentTester(unittest.TestCase):
    def test_component_tester_running(self):
        assert_that(ComponentTester(), is_not(None))


if __name__ == '__main__':
    unittest.main(verbosity=2)
