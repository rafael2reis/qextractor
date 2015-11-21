# module quotation.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
quotation module - Main module, that trains and solve the task.

"""
__version__="1.0"

import wis
import numpy as np

def argmax(w, e):

    tasks = []
    i = 0
    for r in e.x:
        coref = w * np.array(r.coref.feat)
        t = wis.Task(r.quote.start, r.quote.end, np.sum(coref), i)

        tasks.append(t)
        i += 1

    wmax, set_tasks = wis.schedule(tasks)

    result = convertTasks(set_tasks, e.x)

    return result

def phi(e, y=None):
    if not y:
        y = e.y

    if y:
        phi = np.zeros( (len(y[0].coref.feat)), dtype=int )
    else:
        phi = np.zeros( (len(e.x[0].coref.feat)), dtype=int )
        
    for r in y:
        if r.coref.label != "dummy":
            phi = phi + r.coref.feat

    return phi

def convertTasks(resultTasks, x):
    conv = [ x[t.index] for t in resultTasks ]

    return conv


class Example:
    def __init__(self, x, y):
        self.x = x # List of Rows
        self.y = y # List of Rows

class Row:
    def __init__(self, quote, coref):
        self.quote = quote # A Quote
        self.coref = coref # A Coref

class Quote:
    def __init__(self, start, end):
        self.start = start # Start index of Quote
        self.end = end # End index of Quote

class Coref:
    def __init__(self, label, feat):
        self.label = label # Coref label
        self.feat = np.array([ int(e) for e in feat]) # Array of binary features
