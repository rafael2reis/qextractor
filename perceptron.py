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

def structured(w, train, test, epochs, argmax, phi, phiAnswer):
    i = 0
    while i < epochs:
        for e in train:
            yp =  argmax(w, e)
            w = w + phi(e) - phi(e, yp)
    return w
