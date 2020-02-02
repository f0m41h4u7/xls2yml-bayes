# -*- coding: utf-8 -*-
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from pymystem3 import Mystem
import numpy
import xml.etree.ElementTree as et
import datetime
import json

df = pd.read_excel(open('the_table.xls', 'rb'))
classes = df.columns
mystem = Mystem()
p = [dict() for x in range(len(classes))]

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
	for w in words:
		if w in p[cnt]:
			p[cnt][w]+=1
		else:
			p[cnt][w]=1

########### CONVERT ###########
def convert(indexes):
	df_work = pd.read_excel(open('the_table.xls', 'rb'))
	with open('user_info.json', 'r') as f:
		user_info = json.load(f)

	# create file structure of yml
	yml_catalog = et.Element('yml_catalog')
	yml_catalog.set('date', datetime.datetime.now().strftime())
	shop = et.SubElement(yml_catalog, 'shop')

	name = et.SubElement(shop, 'name')
	name.text = user_info["name"]
	company = et.SubElement(shop, 'company')
	company.text = user_info["company"]
	url = et.SubElement(shop, 'url')
	url.text = user_info["url"]
	currency = et.SubElement(shop, 'currency')
	currency.set('id', 'RUB')
	currency.set('rate', '1')

	offers = et.SubElement(shop, 'offers')
	offer = []
	subitems = [[0 for x in range(len(df.index))] for y in range(len(classes))] 
	for i in range(0, len(df.index)):
		offer[i] = et.SubElement(offers, 'offer')
		offer[i].set('id', i)
		for cnt in range(0, len(classes)):
			subitems[i][cnt] = et.SubElement(offer[i], classes[cnt])
			subitems[i][cnt].text = df.at[i, classes[indexes[i]]]
	data = et.tostring(yml_catalog)
	resultfile = open("table!!.yml", "w")	
	resultfile.write(data)

############ WORK #############
def work():
        df_work = pd.read_excel(open('ks.xls', 'rb'))
	classes = df.columns
	for cnt in range(0, len(classes)):
                for row in df.index:
                        cell = df.at[row, classes[cnt]]
			if not isinstance(cell, int) and not isinstance(cell, numpy.int64) and not isinstance(cell, float):
				cell = cell.encode('utf-8')
                                words = word_process(cell)
				freq = [[0 for x in range(len(words))] for y in range(len(classes))]
				for w in range(len(words)):
					freq[w][cnt] = p[cnt]
	

############ LEARN ############
def learn():
	for cnt in range(0, len(classes)):
		for row in df.index:
			cell = df.at[row, classes[cnt]]
			if not isinstance(cell, int) and not isinstance(cell, numpy.int64) and not isinstance(cell, float):
				cell = cell.encode('utf-8')
				words = word_process(cell)
				count_freq(words, cnt)	
			else:
				if 'number' in p[cnt]:
					p[cnt]['number'] += 1
				else:
					p[cnt]['number'] = 1
		for w in p[cnt]:
			# p[cnt][w] /= len(p[cnt])
			print(p[cnt][w], len(p[cnt]))		

############ MAIN #############
def main():
	learn()
#	work()

if __name__== "__main__":
	main()
