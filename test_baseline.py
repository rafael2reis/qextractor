import baseline
import globoquotes
import unittest

class TestBaseline(unittest.TestCase):
    
    def setUp(self):
        self.corpus = globoquotes.load("GloboQuotes/corpus-globocom-cv.txt")

    def tearDown(self):
        pass

    def test_detoken(self):

        sne = [ e[0] for e in self.corpus[0] ]

        text, tr = baseline.detoken(sne)
        print(len(text))
        self.assertEqual(len(text), 3781)

    def test_firstLetterUpperCase(self):
        s = [["Guilherme"],["disse"],["a"], ["Maria"]]
        resp = [1,0,0,1]

        uc = baseline.firstLetterUpperCase(s)

        self.assertEqual(uc, resp)

    def test_verbSpeechNeighb(self):
        s = [["disse", "VSAY"], ["o", "XX"], ["juiz", "ABC"], ["de", "PREP"], ["o", "ART"]]
        resp = [1,1,1,0,0]

        vsn = baseline.verbSpeechNeighb(s)

        self.assertEqual(resp, vsn)

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

        # Sentence that fits in the second regular expression rule:
        qs = baseline.quotationStart(self.corpus[231])
        qe = baseline.quotationEnd(self.corpus[231], qs)

        self.assertTrue(True)

    def test_quoteBounds(self):
        # Sentence that fits in the first regular expression rule:
        qs = baseline.quotationStart(self.corpus[0])
        qe = baseline.quotationEnd(self.corpus[0], qs)
        qb = baseline.quoteBounds(qs, qe)
        for i in range(len(qe)):
            print(self.corpus[0][i][0], "\t", qs[i], qe[i], qb[i])

        # Sentence that fits in the second regular expression rule:
        qs = baseline.quotationStart(self.corpus[231])
        qe = baseline.quotationEnd(self.corpus[231], qs)
        qb = baseline.quoteBounds(qs, qe)
        for i in range(len(qe)):
            print(self.corpus[231][i][0], "\t", qs[i], qe[i], qb[i])

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()