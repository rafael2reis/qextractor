# module dataset.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
dataset module - Module that loads the raw dataset in memory

The core function is load, which reads the GloboQuotes dataset
from file and load its datas in memory.
"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re

def load(file):
    data = [(, )]
    reNewsStart = re.compile('^#d+') # Reg Exp for identifying a news start

    with open(file, 'r') as f:
        f.readLine() # Reads the header line

        for line in f:
            if line == '':
                continue
            else if re.search(line)

def loadTrain():
    load("GloboQuotes/corpus-globocom-cv.txt")
