import unittest
from DisCODeRunner import DisCODeRunner

class TestDisCODeRunner(unittest.TestCase):

    def setUp(self):
        self.runner = DisCODeRunner()

    def test_nothing(self):
        self.assertEquals(self.runner.run(), 1)

if __name__ == '__main__':
    unittest.main()
