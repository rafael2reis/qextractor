# module globoquotes.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
globoquotes module - Classes and functions to read and process GloboQuotes corpus.

Each line of the corpus must be on the following format:

[features = word, pos, np, ne, ck, clause, gpq, coref, gquotestart, gquoteend, gquote]

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re

POS = 1
NE = 3

def load(file):
    """
    Returns an 3-dim array that stores the "body" feeds from a file in the GloboQuotes format. 
    Each element of the array is given by corpus[x][y][z], where:
    x: is the index of the sentence
    y: is the index of a line in the x-th sentence
    z: is the index of a feature of the y-th line of the x-th sentence

    It discards the feed's titles.
    """
    corpus = []

    with open(file, 'r') as f:
        f.readline() # Reads the header line

        bodyLine = 0
        sentence = []

        for line in f:
            if line.strip() == '':
                continue
            if isNewBody(line):
                if sentence: corpus.append(sentence)
                sentence = []
                bodyLine = 1
            elif isNewTitle(line):
                bodyLine = 0
            elif bodyLine > 0:
                if bodyLine > 1: sentence.append(line.split())
                bodyLine += 1

    return corpus

def isNewBody(line):
    """ Returns True if the given line starts a new feed Body """

    index = getIndex(line)
    if index is not None:
        return index % 2 == 1

    return False

def isNewTitle(line):
    """ Returns True if the given line starts a new feed Title """

    index = getIndex(line)
    if index is not None:
        return index % 2 == 0

    return False

def getIndex(line):
    """ 
    Returns the piece (title or body) index. 
    Each title or body's feed starts with a line #\d+ 
    """

    m = re.search(r'^#(?P<INDEX>\d+)$', line)
    if m:
        return int(m.group('INDEX'))

    return None

class GloboQuotes:

    def __init__(self, file="GloboQuotes/corpus-globocom-cv.txt"):
        self.corpus = load(file)