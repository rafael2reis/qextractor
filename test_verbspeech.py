import verbspeech
import unittest

class TestVerbspeech(unittest.TestCase):
    _db = None

    @classmethod
    def setUpClass(cls):
        cls._db = verbspeech.DataBase()
        #[print(e) for e in cls._db.db]
        
    def tearDown(self):
        pass

    """def testLoad(self):
        lb = verbspeech.load("Label/Label-Delaf_pt_v4_1.dic")
        #[ print(e) for e in lb ]
        print("length: ", len(lb))

        self.assertEqual(len(lb), 11618)"""

    def testSearchDissemos(self):
        self.assertTrue(self._db.search("dissemos"))

    def testSearchAfirmou(self):
        self.assertTrue(self._db.search("afirmou"))

    def testSearchExplicaram(self):
        self.assertTrue(self._db.search("explicaram"))

    def testConverter(self):
        conv = verbspeech.Converter(self._db)

        a = [["disse", "V"], ["Pedro", "NPROP"], ["pulou", "V"]]
        result = [["disse", "VSAY"], ["Pedro", "NPROP"], ["pulou", "V"]]

        conv.vsay(a, tokenIndex = 0, posIndex = 1)

        self.assertEqual(a, result)

if __name__ == '__main__':
    unittest.main()