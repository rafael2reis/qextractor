import baseline
import globoquotes
import unittest

class TestBaseline(unittest.TestCase):
    
    def setUp(self):
        self.corpus = globoquotes.load("GloboQuotes/corpus-globocom-cv.txt")

    def tearDown(self):
        pass

    def test_detoken(self):
        print("test_load")

        text = baseline.detoken(self.corpus[0])
        
        self.assertEqual(len(text), 3741)

    def test_quotationStart(self):
        qs = baseline.quotationStart(self.corpus[0])
        for i in range(len(qs)):
            print(self.corpus[0][i][0], "\t", qs[i])

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()