import wisinput
import baseline
import globoquotes
import unittest

class TestWisInput(unittest.TestCase):
    
    def setUp(self):
        self.corpus = globoquotes.load("GloboQuotes/corpus-globocom-cv.txt")

    def tearDown(self):
        pass

    def testInterval(self):
        qs = baseline.quotationStart(self.corpus[0])
        qe = baseline.quotationEnd(self.corpus[0], qs)
        qb = baseline.quoteBounds(qs, qe)
        inte1 = wisinput.interval(qb, 0)

        resp1 = [(1, 10),(54, 55),(63, 65),(83, 84),(100, 128),(172, 181),(185, 186),(209, 211),(246, 249),(293, 294),(302, 329),(331, 426),(464, 466),(479, 493),(585, 634),(654, 699),(736, 737),(743, 772)]

        #[ print(k, v) for k, v in enumerate(qb) ]
        #[ print(e) for e in inte1 ]

        qs = baseline.quotationStart(self.corpus[231])
        qe = baseline.quotationEnd(self.corpus[231], qs)
        qb = baseline.quoteBounds(qs, qe)
        inte2 = wisinput.interval(qb, 0)

        resp2 = [(48, 51),(73, 88),(90, 123),(241, 244),(320, 333),(337, 390),(393, 420),(542, 560),(563, 568),(572, 686),(689, 715),(717, 721),(762, 769),(772, 786),(790, 840),(843, 852),(856, 922),(925, 959),(963, 1045),(1080, 1101),(1103, 1104),(1108, 1201),(1204, 1227),(1250, 1297),(1300, 1316),(1347, 1351),(1353, 1401),(1404, 1419),(1423, 1506),(1509, 1526),(1530, 1593)]

        #[ print(k, v) for k, v in enumerate(qb) ]
        #[ print(e) for e in inte2 ]

        self.assertTrue(inte1 == resp1 and inte2 == resp2)

    def test_corefAnnotated(self):
        quotes = [[1,2],[6,8]]
        s = [['O', 'O'],\
            ['r1+', 'O'],\
            ['r1+', 'O'],
            ['O', 'O'],
            ['O', 'ref00'],
            ['O', 'O'],
            ['r1-', 'O'],
            ['r1-', 'O'],
            ['r1-', 'O']]
        gpqIndex = 0
        corefIndex = 1

        answer = [[4],[4]]

        coref = wisinput.corefAnnotated(quotes, s, gpqIndex, corefIndex)

        self.assertEqual(coref, answer)

if __name__ == '__main__':
    unittest.main()