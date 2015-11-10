# module feature.py
#
# Copyright (c) 2015 Rafael Reis
#
"""
feature module - Functions to create the features representing the coreferences.

"""
__version__="1.0"
__author__ = "Rafael Reis <rafael2reis@gmail.com>"

def dummyCoref():
	return ["distanceNone", "directionNone", "verbsOfSpeechInBetweenNone", /
		"numVerbsOfSpeechInBetweenNone", "coreferenceInBetweenNone", "quoteInBetweenNone", /
		"boundedChunkNone", "verbOfSpeechNeighborhoodNone", "firstLetterUpperCaseNone"]

def create(s, quotes, coref, posIndex, corefIndex, quoteBounds, bc, vsn, fluc):
	features = []

	for i in range(len(quotes)):
		qs = quotes[i][0]
		qe = quotes[i][1]

		features.append([])
		features[i].append(dummyCoref())
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
					if quoteBounds[k] == 'q':
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

			#11
			if bc[c] == 1:
				feat.append("boundedChunk")

			#12
			if vsn[c] == 1:
				feat.append("verbOfSpeechNeighborhood")

			#13
			if fluc[c] == 1:
				feat.append("firstLetterUpperCase")

			features[i].append(feat)

	return features

def pos(s, posIndex):
	pos = set()
	for r in s:
		pos.add(r[posIndex])

	return pos

def binary(dic, feat):
	

def columns(pos):
	feat = {}
	index = 0

	# 1 - Distance
	feat["distanceNone"] = index
	index += 1
	for i in range(8):
		key = "distance" + str(i)
		feat[key] = index
		index += 1

	# 2 - Direction
	feat["directionNone"] = index
	index += 1
	feat["directionLeft"] = index
	index += 1
	feat["directionRight"] = index
	index += 1

	# 3 - Verb of Speech
	feat["verbsOfSpeechInBetweenNone"] = index
	index += 1
	feat["verbOfSpeechInBetween"] = index
	index += 1

	# 4 - Number of Verbs of Speech in Between
	feat["numVerbsOfSpeechInBetweenNone"] = index
	index += 1
	for i in range(8):
		key = "numVerbsOfSpeechInBetween" + str(i)
		feat[key] = index
		index += 1

	# 5 - Coreference in Between
	feat["coreferenceInBetweenNone"] = index
	index += 1
	feat["coreferenceInBetween"] = index
	index += 1

	# 6 - Quote in Between
	feat["quoteInBetweenNone"] = index
	index += 1
	feat["quoteInBetween"] = index
	index += 1

	# 8 - Coreference POS Window
	k = -5
	while k <= 5:
		pre = "corefPOSWin" + str(k) + "="
		key = pre + "None"
		
		feat[key] = index
		index += 1
		
		for p in pos:
			key = pre + p
			feat[key] = index
			index += 1
		k += 1

	# 9 - Quotation POS
	pre = "QuotationPOS="
	for p in pos:
		key = pre + p
		feat[key] = index
		index += 1

	# 10 - POS In Between
	pre = "POSInBetween="
	for p in pos:
		key = pre + p
		feat[key] = index
		index += 1

	# 11 - Bounded Chunk
	feat["boundedChunkNone"] = index
	index += 1
	feat["boundedChunk"] = index
	index += 1

	# 12 - Verb of Speech Neighborhood
	feat["verbOfSpeechNeighborhoodNone"] = index
	index += 1
	feat["verbOfSpeechNeighborhood"] = index
	index += 1

	# 13 - First Letter Upper Case
	feat["firstLetterUpperCaseNone"] = index
	index += 1
	feat["firstLetterUpperCase"] = index
	index += 1