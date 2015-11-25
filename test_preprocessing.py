import preprocessing
import unittest

class TestPreprocessing(unittest.TestCase):
        
    def tearDown(self):
        pass

    def test_createInput(self):
    	preprocessing.createInput()

    	self.assertTrue(True)

    def test_createInputTest(self):
    	preprocessing.createInput(fileName="qextractor_input_test.csv", createTest=True)

    	self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()