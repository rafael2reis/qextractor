import unittest
import globoquotes

class TestGloboQuotes(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load(self):
        print("test_load")

        corpus = globoquotes.load("GloboQuotes/corpus-globocom-cv.txt")

        print("len corpus: ", len(corpus))
        print("len 0: ", len(corpus[0]))
        print("corpus[0]", len(corpus[0]), " corpus[0][0]=", len(corpus[0][0]))

        #[print(x) for x in corpus[0]]

        self.assertTrue(len(corpus) == 551 and len(corpus[0]) == 774)

if __name__ == '__main__':
    unittest.main()