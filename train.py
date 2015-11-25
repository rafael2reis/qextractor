# module train.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
train module - Train the model, using the Structured Perceptron

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import perceptron
import train_example
import quotation
import numpy as np
from sklearn.cross_validation import KFold

def calibration():
	examples = train_example.load()

	# Split examples in train and validation using 5-fold
	print("examples size:", len(examples))
	kf = KFold(len(examples), n_folds=5)

	wLength = len(examples[0].x[0].coref.feat)

	for trainIndex, testIndex in kf:
		train = [ examples[e] for e in trainIndex ]
		print("\n\ntrain size:", len(train))
		validation = [ examples[e] for e in testIndex ]
		print("validation size:", len(validation))

		w = np.array([0]*wLength)

		w = perceptron.structured(w, train, test=validation, epochs=65, argmax=quotation.argmax, phi=quotation.phi)

def train():
	examples = train_example.load()

	# Split examples in train and validation using 5-fold
	print("examples size:", len(examples))

	wLength = len(examples[0].x[0].coref.feat)
	w = np.array([0]*wLength)

	w = perceptron.structured(w, examples, test=None, epochs=38, argmax=quotation.argmax, phi=quotation.phi)

	return w