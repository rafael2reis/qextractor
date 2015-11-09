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

def createInput():
    corpus = globoquotes.load("GloboQuotes/corpus-globocom-cv.txt")
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

    fluc = baseline.firstLetterUpperCase(s)
    vsn = baseline.verbSpeechNeighb(s)

    quotes = wisinput.interval(qb)
    coref = wisinput.coref(quotes, s, corefIndex=7)

    k = 0
    for e in quotes:
        print(e, coref[k])
        k += 1