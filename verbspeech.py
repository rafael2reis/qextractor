# module labeldb.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
verbspeech module - Functions and a class to proccess Verbs of Speech.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

import re

def remove_accents(s):
    return s.replace("á", "a").replace("í", "i").replace("é", "e").replace("ó", "o").replace("ú", "u")

def load(file="Label/Label-Delaf_pt_v4_1.dic",fvspeech="verbos_dizer_ACDC.txt"):
    """Creates a ordered list of verbs of speech in all inflected forms. 
    
    Args:
        file: The dictionary (in UTF-8 encoding) in Label format.
        fvspeech: A file with a list of verbs of speech.

    Returns:
        A list with verbs of speech in all inflected forms, ordered alphabetically.
    """
    lb = []
    vs = []

    with open(fvspeech, 'r') as f:
        f.readline()

        for i in range(210):
            verb = f.readline().replace("\\+se", "").replace("\\+ele", "").replace("\\+eu", "").replace("\n", "").replace("\\+nós", "")
            vs.append(verb)

    with open(file, 'r') as f:
        for line in f:
            if line[0] == '%':
                continue
            
            match = re.search(r"(V\:|V\+)", line)
            if match:
                s = line.split(',')
                s[1] = s[1][:s[1].find(".")]

                if s[1] in vs:
                    lb.append( remove_accents(s[0]) )

    return lb

class DataBase:
    def __init__(self):
        self.db = load()

    def search(self, word):
        first = 0
        last = len(self.db)-1
        found = False

        while first<=last and not found:
            midpoint = int((first + last)/2)

            if self.db[midpoint] == word:
                found = True
            else:
                if word < self.db[midpoint]:
                    last = midpoint-1
                else:
                    first = midpoint+1

        return found

class Converter:
    def __init__(self, dataBase=None):
        if dataBase:
            self.vs = dataBase
        else:
            self.vs = DataBase()

    def vsay(self, s, tokenIndex, posIndex):
        for e in s:
            if e[posIndex] == 'V' and self.vs.search( remove_accents(e[tokenIndex]) ):
                e[posIndex] = "VSAY"

