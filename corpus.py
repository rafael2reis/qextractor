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
    speechVerbs = SpeechVerbs()
    c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt", speechVerbs)

    p = c.next()
    while p:
        f = findPattern(p, speechVerbs)
        #if f:
        #    return

        p = c.next()

def findPattern(p, speechVerbs):
    if p.speechVerb:
        allNodes = p.nodes
        speechNodes = p.speechNodes

        for verbNode in speechNodes:
            acc, subj = searchAccSubj(allNodes, verbNode)

            if (acc and subj 
                and (verbNode.speechVerb in speechVerbs.pattern1
                        or verbNode.speechVerb in speechVerbs.pattern2)):
                print(p.sentence)
                print("O QUE: " + acc.text())
                print("QUEM: " + subj.text() + '\n')

                return True
    return False

def searchAccSubj(allNodes, verbNode):
    accNode = None
    subjNode = None

    for node in allNodes:
        
        if (node.level == verbNode.parent.level 
            and node.parent == verbNode.parent.parent):
            if node.type == 'ACC':
                accNode = node
            elif node.type == 'SUBJ':
                subjNode = node

    return accNode, subjNode

class CorpusAd:
    """
    Class that represents a corpus in the AD format.

    In order to creat an object of this class, you must
    pass a fileName to the constructor.
    """

    def __init__(self, fileName=None, speechVerbs=None):
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

        if speechVerbs:
            self.verbs = speechVerbs
        else:
            self.verbs = SpeechVerbs()

    def next(self):
        p = Piece()

        p.sentence = self.getSentenceDescription()

        if not p.sentence:
            return None

        lastNode = Node()
        lastNode.child = []
        while not self.isSentenceEnd():

            if self.isValidLevel():
                currLevel = self.getCurrentLevel()

                newNode = Node()
                newNode.child = []
                newNode.level = currLevel
                newNode.line = self.i

                newNode.type, newNode.stype, newNode.txt = self.getInfo()

                speechVerb = self.getSpeechVerb(newNode.stype)
                newNode.speechVerb = speechVerb

                if currLevel > lastNode.level: # Child from lastNode
                    newNode.parent = lastNode
                elif currLevel == lastNode.level: # Sibbling of lastNode
                    newNode.parent = lastNode.parent
                else: #currLevel < previousLevel
                    newNode.parent = lastNode.parent
                    while newNode.parent.level >= newNode.level:
                        newNode.parent = newNode.parent.parent
                newNode.parent.child.append(newNode)

                lastNode = newNode
                p.nodes.append(newNode)

                if speechVerb:
                    p.speechVerb = speechVerb
                    p.speechNodes.append(newNode)

                #print('node: ' + str(newNode.line) + ' ' + newNode.txt + ' ' + str(len(newNode.child)))

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
            return info, None, info
        else:
            m = re.search(r'(?P<TYPE>.+):(?P<TAIL>.+)$', info)
            txt = ''
            if info.find(")") > 0:
                n = re.search(r'\)( *)(?P<TEXT>[^ ]*)$', info)
                txt = n.group('TEXT').strip()

            return m.group('TYPE'), m.group('TAIL'), txt

    def getSpeechVerb(self, s):
        if s and re.match(r'.*v-fin\(\'\w+\'', s):
            m = re.search(r'.*v-fin\(\'(?P<VERB>\w+)\'', s)
            v = m.group('VERB')

            if v in self.verbs.all:
                return v
        return ''

class SpeechVerbs:
    def __init__(self):
        self.verbs = self.loadSpeechVerbs()
        self.all = self.verbs[0]
        self.pattern1 = self.verbs[1]
        self.pattern2 = self.verbs[2]

    def loadSpeechVerbs(self):
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

    def __len__(self):
        return len(self.verbs)

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
        self.txt = ''

    def text(self):
        t = self.txt
        if t:
            t = ' ' + t

        for c in self.child:
            t += c.text()

        return t

class InvalidArgumentException(Exception):
    pass
