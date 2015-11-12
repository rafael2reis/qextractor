import preprocessing
import unittest

class TestPreprocessing(unittest.TestCase):
        
    def tearDown(self):
        pass

    def testCreateInput(self):
    	preprocessing.createInput()

    	self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()