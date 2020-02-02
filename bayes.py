# -*- coding: utf-8 -*-
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
import locale
from pymystem3 import Mystem

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

df = pd.read_excel(open('the_table.xls', 'rb'))
classes = df.columns
mystem = Mystem()
p = [dict() for x in range(len(classes))]
dlength = 0

def isunique(w):
	for t in range(0, len(classes)):
		if w in p[t]:
			return False
	return True

def word_process(cell):
	cell = cell.decode('utf-8')
	words = mystem.lemmatize(cell.lower())
	stemmer = RussianStemmer()
	words = [stemmer.stem(word) for word in words]
	return words

def count_freq(words, cnt):
	global dlength
	for w in words:
		if w in p[cnt]:
			p[cnt][w]+=1
		else:
			if isunique(w):
				dlength += 1
			p[cnt][w]=1

############ MAIN ############
def main():
	for cnt in range(0, len(classes)):
		for row in df.index:
			cell = df.at[row, classes[cnt]]
			if not isinstance(cell, int):
				cell = cell.encode('utf-8')
				words = word_process(cell)
				count_freq(words, cnt)	
			else:
				if 'number' in p[cnt]:
					p[cnt]['number'] += 1
				else:
					p[cnt]['number'] = 1
		for w in p[cnt]:
			#p[cnt][w] /= len(p[cnt])
			print(p[cnt][w], len(p[cnt]))
	#print(p[0])

if __name__== "__main__":
	main()
