# module preprocessing.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
preprocessing module - Prepares the data to the task

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re
import globoquotes
import baseline
import wisinput
import verbspeech
import feature
import csv

INDEX_QB = 10
FILE_NAME = "qextractor_input.csv"

def createInput(fileName=None, createTest=False):
    corpus = globoquotes.load("GloboQuotes/corpus-globocom-cv.txt")
    test = globoquotes.load("GloboQuotes/corpus-globocom-test.txt")
    converter = verbspeech.Converter()

    if not fileName:
        fileName = FILE_NAME

    open(fileName, 'w').close()

    pos = feature.pos(corpus + test, posIndex = 1)
    columns = feature.columns(pos)

    if createTest:
        corpus = test

    i = 0
    for i in range(len(corpus)):
        s = corpus[i]
        qs = baseline.quotationStart(s)
        qe = baseline.quotationEnd(s, qs)
        qb = baseline.quoteBounds(qs, qe)

        converter.vsay(s, tokenIndex = 0, posIndex = 1)

        for k in range(len(s)):
            print(k, s[k][0].ljust(30), s[k][1].ljust(10), s[k][7].ljust(5), qs[k], qe[k], qb[k])

        # Baseline: X
        print("Create bc...")
        bc = baseline.boundedChunk(s)
        print("Create vsn...")
        vsn = baseline.verbSpeechNeighb(s)
        print("Create fluc...")
        fluc = baseline.firstLetterUpperCase(s)

        print("Identifying quotes...")
        quotes = wisinput.interval(qb)

        print("Identifying coreferences...")
        coref, labels = wisinput.coref(s, quotes, corefIndex=7)

        print("Creating features...")
        feat = feature.create(s, quotes=quotes, coref=coref, posIndex=1, corefIndex=7, quoteBounds=qb, bc=bc, vsn=vsn, fluc=fluc)

        print("Binarying features...")
        bfeat = feature.binary(columns, feat)

        # Answer: Y
        print("Output: Creating y...")
        qbA = [ e[INDEX_QB] for e in s ]

        print("Output: Identifying quotes...")
        quotesA = wisinput.interval(qbA)
        print("Output: Quotes = ", len(quotesA))

        print("Output: Identifying coreferences...")
        corefA, labelsA = wisinput.corefAnnotated(s, quotes=quotesA, corefIndex=7, gpqIndex=6)
        print("Output: Coref = ", len(corefA))

        print("Output: Creating features...")
        featA = feature.create(s, quotes=quotesA, coref=corefA, posIndex=1, corefIndex=7, \
                quoteBounds=qbA, bc=bc, vsn=vsn, fluc=fluc, dummy=False)

        print("Output: Binarying features...")
        bfeatA = feature.binary(columns, featA)
        print("Output: bFeat = ", len(bfeatA))

        with open(fileName, 'a', newline='') as csvfile:
            swriter = csv.writer(csvfile, delimiter=';')

            for p in range(len(bfeat)):
                for q in range(len(bfeat[p])):
                    swriter.writerow([i, "x"] + list(quotes[p]) + [labels[p][q]] + bfeat[p][q])

            for p in range(len(bfeatA)):
                for q in range(len(bfeatA[p])):
                    swriter.writerow([i, "y"] + list(quotesA[p]) + [labelsA[p][q]] + bfeatA[p][q])

        print("Done!")
    #k = 0
    #for e in quotes:
    #    print(e, coref[k], bfeat[k])
    #   k += 1