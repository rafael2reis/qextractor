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

def boundedChunk(s):
    """Indetifies the Bounded Chunk.

    Assigns a 1 to the three quotation marks ' " - and also to all 
    the tokens between them, whenever there are more than three 
    tokens between the quotation marks. Otherwise, assigns a 0 to the token.

    Args:
        s: 2D array that represents a sentence in the GloboQuotes format
    Returns:
        An 1D array that indicates if the i-th position is
        a bounded chunk.
    """
    bc = [ 0 for i in range(len(s))]

    a = [ e[0] for e in s ]

    text, dicIndex = detoken(a)

    #print(text)

    p1 = re.compile(r"\"( \w+?){3}.*? \"", re.U)
    p2 = re.compile(r"\'( \w+?){3}.*? \'", re.U)
    p3 = re.compile(r"\-( \w+?){3}.*? \-", re.U)

    for m in re.finditer(p1, text):
        #print(m.start(0), m.end(0))
        #print(m.group(0))
        i = dicIndex[m.start(0)]
        end = dicIndex[m.end(0)-1]
        while i < end:
            bc[i] = 1
            i += 1

    for m in re.finditer(p2, text):
        #print(m.start(0), m.end(0))
        #print(m.group(0))
        i = dicIndex[m.start(0)]
        end = dicIndex[m.end(0)-1]
        while i < end:
            bc[i] = 1
            i += 1

    for m in re.finditer(p3, text):
        #print(m.start(0), m.end(0))
        #print(m.group(0))
        i = dicIndex[m.start(0)]
        end = dicIndex[m.end(0)-1]
        while i < end:
            bc[i] = 1
            i += 1

    return bc

def firstLetterUpperCase(s):
    """Indetifies the tokens with First Letter Upper Case.

    Args:
        s: 2D array that represents a sentence in the GloboQuotes format
    Returns:
        An 1D array that indicates if the i-th position is
        a token that starts with upper letter case.
    """
    uc = [ 0 for e in s ]
    tokenIndex = 0
    pattern = re.compile(r"\w+")

    for i in range(len(s)):
        text = s[i][tokenIndex][0]
        if re.match(pattern, text) and text == text.upper():
            uc[i] = 1

    return uc

def verbSpeechNeighb(s):
    """Indetifies the Verb of Speech Neighbourhood.

    Assigns a 1 to each verb of speech and also to its four closest tokens. 
    Otherwise, assigns a 0 to the token.

    Args:
        s: 2D array that represents a sentence in the GloboQuotes format
    Returns:
        An 1D array that indicates if the i-th position is
        a verb of speech neighborhood.
    """
    posIndex = 1
    vsn = [ 0 for e in s ]

    n = len(s)

    for i in range(n):
        if s[i][posIndex] == 'VSAY':
            vsn[i] = 1
            if i-1 >= 0:
                vsn[i-1] = 1
            if i-2 >= 0:
                vsn[i-2] = 1
            if i+1 < n:
                vsn[i+1] = 1
            if i+2 < n:
                vsn[i+2] = 1

    return vsn


def quotationStart(s):
    """Indetifies the quotatins' start by regexp patterns.

    Args:
        s: 2D array that represents a sentence in the GloboQuotes format
    Returns:
        An 1D array that indicates if the i-th position is
        a quotation start.
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

    print("baseline.quotationEnd:", text)
    print("len(dic):", len(dicIndex))

    applyLabel(qe, pattern=r"(\' #QS#.*?)[\'\n]", text=text, dic=dicIndex, group=1, offset=-1, offDic=-1, label="E")
    applyLabel(qe, pattern=r"(\" #QS#.*?)[\"\n]", text=text, dic=dicIndex, group=1, offset=-1, offDic=-1, label="E")

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
        print(m.end(group) + offDic)
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

def quoteBounds(qs, qe):
    """Creates a 1D array with Quotation Bounds indicators.

    Args:
        qs: 1D array with the quotation start annotation. An
            'S' represents a start and '-' otherwise.
        qe: 1D array with the quotation end annotation. An
            'E' represents an end and '-' otherwise.

    Returns:
        An 1D array that indicates if the i-th position 
        belongs to a quotation, marked with 'q'. If not,
        the position contains '-'.
    """
    quote = ["O" for i in range(len(qs))]
    inQuote = False

    for i in range(len(qs)-1, 0, -1):
        if qe[i] == 'E' and not inQuote:
            quote[i] = 'q'
            inQuote = True
        elif qs[i] == 'S' and inQuote:
            quote[i] = 'q'
            inQuote = False
        elif inQuote:
            quote[i] = 'q'

    return quote

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
    #index = [2]
    index = [0]

    for i in range(len(a)):
        text = text + " " + a[i]
        index.append(i)
        for j in range(len(a[i])):
            index.append(i)
        #if i > 0:
            #index.append(index[i - 1] + 1 + len(a[i-1]))

    text = text + "\n"

    #dic = { index[i] : i for i in range(len(index)) }
    
    return text, index