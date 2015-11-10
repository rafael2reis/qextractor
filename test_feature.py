import feature
import unittest
import globoquotes

class TestFeature(unittest.TestCase):
    _corpus = None

    @classmethod
    def setUpClass(cls):
        cls._corpus = globoquotes.load("GloboQuotes/corpus-globocom-cv.txt")
        
    def tearDown(self):
        pass

    def test_create(self):
        pass

    def test_pos(self):
        m = [["NPROP"], ["NPROP"], ["PROADJ"], ["N"], ["PREP"]]
        pos = feature.pos(m, 0)

        self.assertEqual(len(pos), 4)

    def test_columns(self):
        pass

if __name__ == '__main__':
    unittest.main()