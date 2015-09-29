# module corpus.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
corpus module - Classes and functions to read and process corpus data.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re

def annotate():
    c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt")

    p = c.next()
    while p:
        if p.speechVerb:
            print(p.sentence)
        p = c.next()

class CorpusAd:
    """
    Class that represents a corpus in the AD format.

    In order to creat an object of this class, you must
    pass a fileName to the constructor.
    """

    def __init__(self, fileName=None):
        """
        Receives a fileName as an argument. The fileName must be
        a valid corpus in the AD format.
        """
        if not fileName:
            raise InvalidArgumentException('You must inform a valid fileName!')

        with open(fileName, 'r') as f:
            self.raw = f.readlines()
        self.i = 0 # Index of the last line read. It'll be used in the "next" method.
        self.rawLen = len(self.raw)

        self.verbs = loadSpeechVerbs()

    def next(self):
        p = Piece()

        p.sentence = self.getSentenceDescription()

        if not p.sentence:
            return None

        lastNode = Node()
        while not self.isSentenceEnd():

            if self.isValidLevel():
                currLevel = self.getCurrentLevel()

                newNode = Node()
                newNode.level = currLevel
                newNode.line = self.i

                newNode.type, newNode.stype = self.getInfo()

                speechVerb = self.getSpeechVerb(newNode.stype)

                if currLevel > lastNode.level: # Child from lastNode
                    newNode.parent = lastNode
                    lastNode.child.append(newNode)
                elif currLevel == lastNode.level: # Sibbling of lastNode
                    newNode.parent = lastNode.parent
                    newNode.parent.child.append(newNode)
                else: #currLevel < previousLevel
                    newNode.parent = lastNode.parent
                    while newNode.parent.level >= newNode.level:
                        newNode.parent = newNode.parent.parent

                lastNode = newNode
                p.nodes.append(newNode)

                if speechVerb:
                    p.speechVerb = speechVerb
                    p.speechNodes.append(newNode)

            self.i += 1

        return p

    def isSentenceBegin(self):
        return self.raw[self.i] == "<s>\n"

    def isSentenceDescription(self):
        return re.match(r'^CF\d+-\d+' , self.raw[self.i])

    def getSentenceDescription(self):
        while self.i < self.rawLen and not self.isSentenceBegin():
            self.i += 1

        if self.i >= self.rawLen:
            return None

        while not self.isSentenceDescription():
            self.i += 1

        m = re.search(r'^CF\d+-\d+\w* (?P<SENT>.+)$', self.raw[self.i])
        s = m.group('SENT')

        return s

    def isSentenceEnd(self):
        return self.raw[self.i] == "</s>\n"

    def isValidLevel(self):
        return re.match(r'^=+' , self.raw[self.i])

    def getCurrentLevel(self):
        levels = re.findall('=', self.raw[self.i])
        return len(levels)

    def getInfo(self):
        info = re.sub(r'=+', "", self.raw[self.i]).replace("\n", "")
        
        if len(info) == 1 or info.find(":") == -1:
            return info, None
        else:
            m = re.search(r'(?P<TYPE>.+):(?P<TAIL>.+)$', info)
            return m.group('TYPE'), m.group('TAIL')

    def getSpeechVerb(self, s):
        if s and re.match(r'.*v-fin\(\'\w+\'', s):
            m = re.search(r'.*v-fin\(\'(?P<VERB>\w+)\'', s)
            v = m.group('VERB')

            if v in self.verbs[0]:
                return v
        return ''

def loadSpeechVerbs():
    verbs = [[], [], [], [], [], [], []]
    s = set()
    i = 1
    with open('verbos_dizer_ACDC.txt', 'r') as f:
        for line in f:
            if re.match(r'#(?P<INDEX>\d+)', line):
                m = re.search(r'#(?P<INDEX>\d+)\n', line)
                i = int(m.group('INDEX'))
            else:
                line = line.strip()
                s.add(line)
                verbs[i].append(line)

    verbs[0] = list(s)
    return verbs

class Piece:

    def __init__(self):
        self.start = 0
        self.end = 0
        self.sentence = ""
        self.nodes = []
        self.speechNodes = []
        self.speechVerb = ""

class Node:

    def __init__(self, type=None, stype=None, child=[], parent=None, line=None, level=0):
        self.type = type
        self.stype = stype
        self.child = child
        self.parent = parent
        self.line = line
        self.level = level

class InvalidArgumentException(Exception):
    pass
