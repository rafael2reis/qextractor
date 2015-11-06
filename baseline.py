# module baseline.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
baseline module - Functions to produce the Baseline System's features.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re
import globoquotes

def quotationStart(s):
    """
    Given a sentence s, return a column c filled as follow:
    If the token in the i-th line is the beginning of a sentence,
    c[i] = 'S'. Otherwise, c[i] = '-'

    where:
    sentece s: 2D array in the GloboQuotes format
    """
    qs = ["-" for i in range(len(s))]

    a = [ e[0] for e in s ]
    convertNe(a, s)

    text, dicIndex = detoken(a)

    pattern = re.compile(r"[^\d] [\'\"-] .")

    for m in re.finditer(pattern, text):
        qs[ dicIndex[m.end(0)-1] ] = "S"

    pattern = re.compile(r"[\.\?]( #PO#)+ \: (?!#PO#)")

    for m in re.finditer(pattern, text):
        qs[ dicIndex[m.end(0)] ] = "S"

    return qs

def convertNe(a, s):
    """
    Call the function convert with the parameters to translate the tokens
    in the array a to "#PO#", whenever NE is in the valueList.
    """
    convert(a, s, transIndex=3, valueList=["I-PER", "I-ORG"], label="#PO#")

def convert(a, s, transIndex, valueList, label):
    """
    Given a 1D array a, a 2D sentence array s, sets
    a[i] to label, where s[transIndex] in labelList
    """
    for i in range(len(s)):
        if s[i][transIndex] in valueList:
            a[i] = label


def detoken(sconv):
    """
    Given an array sconv of tokens, returns a text string with the tokens
    separated by space.

    Also, returns a dicionary(k,v) where:
    v: original index of the token in the sentence
    k: index of the token in the string

    This dicionary is usefull to translate from the
    indexes found by regexp in the text string
    """
    text = " "
    index = [2]

    for i in range(len(sconv)):
        text = text + " " + sconv[i]
        if i > 0:
            index.append(1 + index[i - 1] + len(sconv[i-1]))

    dic = { index[i] : i for i in range(len(index)) }
    
    return text, dic