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

def createInput():
    corpus = globoquotes.load("GloboQuotes/corpus-globocom-cv.txt")
    test = globoquotes.load("GloboQuotes/corpus-globocom-test.txt")
    converter = verbspeech.Converter()

    i = 0
    #for i in range(len(corpus)):
    s = corpus[i]
    qs = baseline.quotationStart(s)
    qe = baseline.quotationEnd(s, qs)
    qb = baseline.quoteBounds(qs, qe)

    converter.vsay(s, tokenIndex = 0, posIndex = 1)
    for k in range(len(s)):
        print(k, s[k][0], s[k][1], s[k][7], qs[k], qe[k], qb[k])

    print("Create bc...")
    bc = baseline.boundedChunk(s)
    print("Create vsn...")
    vsn = baseline.verbSpeechNeighb(s)
    print("Create fluc...")
    fluc = baseline.firstLetterUpperCase(s)

    print("Identifying quotes...")
    quotes = wisinput.interval(qb)
    print("Identifying coreferences...")
    coref = wisinput.coref(quotes, s, corefIndex=7)

    print("Getting POS...")
    pos = feature.pos(corpus + test, posIndex = 1)

    print("Creating features...")
    feat = feature.create(s, quotes=quotes, coref=coref, posIndex=1, corefIndex=7, quoteBounds=qb, bc=bc, vsn=vsn, fluc=fluc)
    columns = feature.columns(pos)

    print("Binarying features...")
    bfeat = feature.binary(columns, feat)

    print("Done!")
    k = 0
    for e in quotes:
        print(e, coref[k], bfeat[k])
        k += 1