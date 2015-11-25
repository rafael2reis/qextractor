# module metrics.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
metrics module - Functions to evaluate the quality and performance of a model

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

def validate(w, dataset, argmax):
    corr = 0.0
    incorr = 0.0
    corrD = 0.0 # Correct Dummy
    incorrD = 0.0 # Incorrect Dummy
    quot = 0.0 # Num of real quotations

    for e in dataset:
        predict = argmax(w, e)

        y = e.y
        quot += len(y)
        for r in predict:
            a = search(r, y)

            if not a:
                if r.coref.label == "dummy":
                    corrD += 1
                else:
                    incorrD += 1
            else:
                if r.coref.label == a.coref.label:
                    corr += 1
                else:
                    incorr += 1

    precision = (corr + corrD)/(corr + corrD + incorr + incorrD)
    recall = corr/quot

    return precision, recall

def show(w, train, test, argmax, epoch):
    ptra, rectra = validate(w, train, argmax)
    ptes, rectes = validate(w, test, argmax)

    print(epoch.ljust(3), str(ptra).ljust(20), str(rectra).ljust(20), str(ptes).ljust(20), str(rectes).ljust(20))

def search(r, y):
    start = r.quote.start
    end = r.quote.end

    for x in y:
        if x.quote.start == start and x.quote.end == end:
            return x

    return None