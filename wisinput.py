# module wisinput.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
wisinput module - Functions to create the input for WIS problem,
    given the quotations' attributes.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re
import globoquotes

def interval(qb, index = 0):
    """Creates an array with the quotations' interval.

    Args:
        qs: Array having a column with the quotation bounds annotation.
            A 'q' represents that the i-th token belongs to a quotation.
        index (optional): The index of the column in qs array with the
            quotation bounds annotation.

    Returns:
        An 1D array with tuples (s, e), where each tuple represents
        a quotation, being s the start index and e the end index.
    """
    intervals = []
    if type(qb[0]) is list:
        qb = [ e[index] for e in qb ]

    length = len(qb)
    inQuote = False
    s, e = 0, 0
    for i in range(length):
        #print(i, qb[i])
        if qb[i] == 'q':
            if not inQuote:
                s = i
                inQuote = True
            elif ((i + 1 >= length) 
                    or (qb[i + 1] == 'O')):
                e = i
                inQuote = False
                intervals.append( (s, e) )
                s, e = 0, 0

    return intervals

def coref(s, quotes, corefIndex):
    """
        two after the quotation and six before it

        Args:
            quotes:
            s: sentence in GloboQuotes format
            corefIndex: index of the column of s with coref information
        Returns:
            An array with the indexes of the coreferences
    """
    coref = []
    corefLabels = []

    for q in quotes:
        qstart = q[0]
        qend = q[1]

        index = []
        labels = ["dummy"]

        i = qend + 1
        n = 0
        while i < len(s) and n < 2:
            if s[i][corefIndex] != "O":
                if s[i-1][corefIndex] != s[i][corefIndex]:
                    index.append(i)
                    n += 1
            i += 1

        i = qstart - 1
        n = 0
        while i >= 0 and n < 6:
            if s[i][corefIndex] != "O":
                if s[i+1][corefIndex] != s[i][corefIndex]:
                    index.append(i)
                    n += 1
            i -= 1

        index.sort()
        for x in index:
            labels.append(s[x][corefIndex])
        coref.append(index)
        corefLabels.append(labels)

    return coref, corefLabels

def corefAnnotated(s, quotes, corefIndex, gpqIndex):
    """Searches for the correct coreferences of the quotes given.

    GPQ is in the format: r(dist)(inc), where:
        dist: is an integer that is the distance from the quotation to
            its coreference.
        inc: + or - signal, indicating if the coref is to the right
            or to the left from the quotation.
    Args:
        quotes: 2D array, which line having the quotation start and end indexes
        s: sentence in the GlbooQuotes format
        qpqIndex: index of GPQ column in the s array
    Returns:
        An array with the indexes of the coreferences
    """
    pattern = re.compile(r"r(\d+)([-+])")

    index = []
    labels = []

    for q in quotes:
        qstart = q[0]
        qend = q[1]

        gpq = s[qstart][gpqIndex]
        m = re.match(pattern, gpq)

        dist = int(m.group(1))
        inc = int(m.group(2) + '1')
        
        i = qend + 1
        if inc < 0: i = qstart - 1

        count = 1
        while count <= dist:
            if s[i][corefIndex] != 'O':
                if count == dist:
                    index.append([i])
                    labels.append([s[i][corefIndex]])
                count += 1

            i += inc

    return index, labels