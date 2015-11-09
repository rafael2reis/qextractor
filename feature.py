# module feature.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
feature module - Functions to create the features representing the coreferences.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

def create(s, quotes, coref, posIndex, corefIndex, qIndex):

	for i in range(len(quotes)):
		qs = quotes[i][0]
		qe = quotes[i][1]

		for j in range(len(coref[i])):
			feat = []
			c = coref[i][j]
			dist = set()
			direction = ""
			quoteBt = False
			vsay = 0

			start = 0
			end = 0

			if c < qs:
				direction = "directionLeft"
				start = c + 1
				end = qs - 1
			else:
				direction = "directionRight"
				start = qe + 1
				end = c - 1

			k = start
			while k <= end:
					# 1-Distance:
					if s[k][corefIndex] != "O" and s[k-1][corefIndex] != s[k][corefIndex]:
						dist.add(s[k][corefIndex])
					# 4-Number of Verb of Speech:
					if s[k][posIndex] == 'VSAY':
						vsay += 1
					# 6-Quote in Between:
					if s[k][qIndex] == 'q':
						quoteBt = True

					k += 1

			feat.append("distance" + len(dist)) #1
			feat.append(direction) #2
			
			if vsay > 0:
				feat.append("verbOfSpeechInBetween") #3
			feat.append("numVerbsOfSpeechInBetween" + str(vsay)) #4

			if len(dist) > 0:
				feat.append("coreferenceInBetween") #5
			if quoteBt:
				feat.append("quoteInBetween") #6

			#8
			k = 0
			cont = c
			while k >= -5:
				if cont >= 0:
					if k+1 == 0 and s[cont][corefIndex] == s[c][corefIndex]:
						k += 1

					feat.append("corefPOSWin" + str(k) + "=" + s[cont][posIndex])
				else:
					feat.append("corefPOSWin" + str(k) + "=None")

				cont -= 1
				k -= 1

			k = 0
			cont = c
			while k <= 5:
				if cont < len(s):
					if k-1 == 0 and s[cont][corefIndex] == s[c][corefIndex]:
						k -= 1

					feat.append("corefPOSWin" + str(k) + "=" + s[cont][posIndex])
				else:
					feat.append("corefPOSWin" + str(k) + "=None")

				cont += 1
				k += 1

			#9
			k = qs
			while k <= qe:
				feat.append("QuotationPOS=" + s[k][posIndex])

			#10
			k = start
			while k <= end:
				feat.append("POSInBetween=" + s[k][posIndex])
				k += 1




