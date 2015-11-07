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
    	if qb[i] == 'q':
    		if not inQuote:
    			s = i
    			inQuote = True
    		elif ((i + 1 >= length) 
    				or (qb[i + 1] == '-')):
    			e = i
    			inQuote = False
    			intervals.append( (s, e) )
    			s, e = 0, 0

    return intervals
