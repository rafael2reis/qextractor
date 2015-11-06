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

        sne = [ e[0] for e in self.corpus[0] ]

        text, tr = baseline.detoken(sne)
        print(len(text))
        self.assertEqual(len(text), 3780)

    def test_quotationStart(self):
        # Sentence that fits in the first regular expression rule:
        qs = baseline.quotationStart(self.corpus[0])
        #for i in range(len(qs)):
        #    print(self.corpus[0][i][0], "\t", qs[i])

        # Sentence that fits in the second regular expression rule:
        qs = baseline.quotationStart(self.corpus[231])
        #for i in range(len(qs)):
        #    print(self.corpus[231][i][0], "\t", qs[i])

        self.assertTrue(True)

    def test_quotationEnd(self):
        # Sentence that fits in the first regular expression rule:
        qs = baseline.quotationStart(self.corpus[0])
        qe = baseline.quotationEnd(self.corpus[0], qs)
        for i in range(len(qe)):
            print(self.corpus[0][i][0], "\t", qs[i], qe[i])

        # Sentence that fits in the second regular expression rule:
        qs = baseline.quotationStart(self.corpus[231])
        qe = baseline.quotationEnd(self.corpus[231], qs)
        for i in range(len(qe)):
            print(self.corpus[231][i][0], "\t", qs[i], qe[i])

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()