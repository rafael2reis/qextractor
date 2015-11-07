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
    Returns an array qs(Quotation Start) filled as follow:
    If the token in the i-th line is the beginning of a quotation,
    qs[i] = 'S'. Otherwise, qs[i] = '-'

    Arguments:
    sentece s: 2D array in the GloboQuotes format
    """
    qs = ["-" for i in range(len(s))]

    a = [ e[0] for e in s ]
    convertNe(a, s)

    text, dicIndex = detoken(a)

    pattern = re.compile(r"(?=([^\d] [\'\"-] .))")

    for m in re.finditer(pattern, text):
        qs[ dicIndex[m.end(1)-1] ] = "S"

    pattern = re.compile(r"[\.\?]( #PO#)+ \: (?!#PO#)")

    for m in re.finditer(pattern, text):
        qs[ dicIndex[m.end(0)] ] = "S"

    return qs

def quotationEnd(s, qs):
    """Creates a 1D array with Quotation End indicators.

    Returns an array qe(Quotation End) filled as follow:
    If the token in the i-th line is the end of a quotation,
    qe[i] = 'E'. Otherwise, qe[i] = '-'

    Args:
        s: 2D array that represents a sentence in the GloboQuotes format
        qs: 1D array with the quotation start annotation. Must be
            seen as an additional column of s.

    Returns:
        An 1D array that indicates if the i-th position is
        a quotation end.
    """
    qe = ["-" for i in range(len(s))]

    a = [ e[0] for e in s ]
    convertNe(a, s)
    convertQuotationStart(a, qs)
    text, dicIndex = detoken(a)

    applyLabel(qe, pattern=r"(\' #QS#.*?)[\'\n]", text=text, dic=dicIndex, group=1, offset=-1, offDic=0, label="E")
    applyLabel(qe, pattern=r"(\" #QS#.*?)[\"\n]", text=text, dic=dicIndex, group=1, offset=-1, offDic=0, label="E")

    convertProPess(a, s)
    text, dicIndex = detoken(a)
    applyLabel(qe, pattern=r"(?=(\- #QS#.*?((?<!ex )\-(?!#PPE#)|$)))", text=text, dic=dicIndex, group=1, offset=-1, offDic=-1, label="E")

    convertQuotationStart(a, qs)
    text, dicIndex = detoken(a)
    applyLabel(qe, pattern=r"(?=(#PO# \: #QS#.*?[\.\?])((( #PO#)+ \:)|$))", text=text, dic=dicIndex, group=1, offset=0, offDic=-1, label="E")

    return qe

def applyLabel(q, pattern, text, dic, group, offset, offDic, label):
    p = re.compile(pattern)

    for m in re.finditer(p, text):
        q[ dic[m.end(group) + offDic] + offset ] = label

def convertNe(a, s):
    """
    Call the function convert with the parameters to translate the tokens
    in the array a to "#PO#", whenever NE is in the valueList.
    """
    convert(a, s, transIndex=3, valueList=["I-PER", "I-ORG"], label="#PO#")

def convertQuotationStart(a, qs):
    """
    Call the function convert with the parameters to translate the tokens
    in the array a to "#PO#", whenever NE is in the valueList.
    """
    convert(a, qs, transIndex=0, valueList=["S"], label="#QS#")

def convertProPess(a, s):
    """
    Translates the tokens in the array a to "#PO#", whenever NE is in the valueList.
    """
    convert(a, s, transIndex=1, valueList=["PROPESS"], label="#PPE#")

def convert(a, s, transIndex, valueList, label):
    """
    Given a 1D array a, a 2D sentence array s, sets
    a[i] to label, where s[transIndex] in labelList
    """
    for i in range(len(s)):
        if s[i][transIndex] in valueList:
            a[i] = label


def detoken(a):
    """Detokenizes an array of tokens.

    Given an array a of tokens, it creates a text string with the tokens
    separated by space and a dictionary.

    This dicionary is usefull to translate from the
    indexes found by regexp in the text string

    Args:
        a: array of tokens

    Returns:
        A dicionary(k,v) where:
            v: original index of the token in the sentence
            k: index of the token in the string
    """
    text = " "
    index = [2]

    for i in range(len(a)):
        text = text + " " + a[i]
        if i > 0:
            index.append(index[i - 1] + 1 + len(a[i-1]))

    text = text + "\n"

    dic = { index[i] : i for i in range(len(index)) }
    
    return text, dic