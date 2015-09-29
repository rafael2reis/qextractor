import unittest
import corpus
from corpus import CorpusAd

class TestCorpus(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInitSuccess(self):
        c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt")

        self.assertEqual(len(c.raw), 177483)

    def testInitFailNone(self):
        self.assertRaises(corpus.InvalidArgumentException, CorpusAd, None)

    def testInitFailInvalid(self):
        self.assertRaises(IOError, CorpusAd, "invalid.txt")

    def testNext(self):
        c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt")

        p = c.next()
        c.next()
        c.next()
        c.next()

        print(p.nodes)

        self.assertNotEqual(p, None)

    def testLoadSpeechVerbs(self):
        verbs = corpus.loadSpeechVerbs()

        self.assertEqual(len(verbs[1]), 210)

    def testHasSpeechVerb(self):
        c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt")

        v = c.getSpeechVerb("==========MV:v-fin('dizer' <fs-subst> <nosubj> PR 3S IND)é")
        self.assertEqual(v, 'dizer')

    def testAnnotate(self):
        corpus.annotate()
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()