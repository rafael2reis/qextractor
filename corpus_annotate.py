# module corpus_annotate.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
corpus module - Functions to process data in the corpus format.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

from corpus import CorpusAd
from corpus import SpeechVerbs

def annotate():
    speechVerbs = SpeechVerbs()
    c = CorpusAd("bosque/Bosque_CF_8.0.ad.txt", speechVerbs)

    p = c.next()
    while p:
        #f = findPattern3(p, speechVerbs)
        f = findPattern1(p, speechVerbs)

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
                print("QUEM: " + subj.text())
                print(verbNode.txt)
                print("O QUE: " + acc.text() + '\n')

                return True
    return False

def findPattern(p, speechVerbs, pattern):
    if p.speechVerb:
        allNodes = p.nodes
        speechNodes = p.speechNodes

        for verbNode in speechNodes:
            acc, subj = searchAccSubj(allNodes, verbNode)

            if pattern(acc, subj, verbNode):
                printQuotation(p, subj, verbNode, acc)

                return True
    return False

def findPattern3(p, speechVerbs):
    if p.speechVerb:
        allNodes = p.nodes
        speechNodes = p.speechNodes

        for verbNode in speechNodes:
            acc, subj = searchAccSubj(allNodes, verbNode)

            if (acc and isValidSubj(subj) and hasChildQue(acc)
                and (verbNode.speechVerb in speechVerbs.pattern3)):
                printQuotation(p, subj, verbNode, acc)

                return True
    return False

def findPattern1(p, speechVerbs):
    """ 
        ACC [word="|»] [word=,] VSAY SUBJ
        ACC [word="|»] [word=,] SUBJ VSAY
    """
    if p.speechVerb:
        allNodes = p.nodes
        speechNodes = p.speechNodes

        for verbNode in speechNodes:
            acc, subj = searchAccSubj(allNodes, verbNode)

            if (acc and isValidSubj(subj) 
                and hasCloseQuotesComma(acc)
                and (verbNode.speechVerb in speechVerbs.pattern1)):
                printQuotation(p, subj, verbNode, acc)

                return True
    return False

def printQuotation(p, subj, verbNode, acc):
    print(p.sentence)
    print("QUEM: " + subj.text())
    print(verbNode.txt)
    print("O QUE: " + acc.text() + '\n')

def hasCloseQuotesComma(acc):
    if acc.next and acc.next.next:
        return acc.next.txt in ("»", "»\"", "\"") and acc.next.next.txt in (",")
    else:
        return False 

def hasChildQue(acc):
    return acc.child and acc.child[0].txt and acc.child[0].txt.lower() == "que"

def isValidSubj(subj):
    # TODO ver o txt do SUBJ
    return subj and subj.txt.lower() != "se"

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