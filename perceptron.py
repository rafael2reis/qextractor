# module perceptron.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
perceptron module - Perceptron algorithm that creates the model.

Convergir: é quando o erro de validação parou de diminuir (mas ele fixa o número de épocas, então não deve ter feito teste de convergência!!!)



"""
__version__="1.0"

import numpy as np
import metrics

def structured(w, train, test, epochs, argmax, phi):
    i = 0
    while i < epochs:
        for e in train:
            yp =  argmax(w, e)
            w = w + phi(e) - phi(e, yp)
        i += 1

        metrics.show(w=w, train=train, test=test, argmax=argmax, epoch=str(i))
    return w
