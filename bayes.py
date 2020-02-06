# -*- coding: utf-8 -*-
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from pymystem3 import Mystem
import numpy as np
import xml.etree.ElementTree as et
import datetime
import json

df = pd.read_excel(open('/home/grimpoteuthis/app/xls2xml_bayes/the_table.xls', 'rb'))
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
    df_work = pd.read_excel(open('/home/grimpoteuthis/app/uploads/excel.xls', 'rb'))
    with open('/home/grimpoteuthis/app/user_info.json', 'r') as f:
        user_info = json.load(f)

    # create file structure of yml
    yml_catalog = et.Element('yml_catalog')
#    yml_catalog.set('date', datetime.datetime.now())
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
    offer = [0 for x in range(len(df_work.index))]
    subitems = [[0 for x in range(len(df_work.index))] for y in range(len(classes))] 
    for i in range(0, len(df_work.index)):
        offer[i] = et.SubElement(offers, 'offer')
        offer[i].set('id', str(i))
        subname = et.SubElement(offer[i], 'name') 
        subdes = et.SubElement(offer[i], 'description')
        subpr = et.SubElement(offer[i], 'price')
        subqty = et.SubElement(offer[i], 'qty')
        subname.text = str(df_work.at[i, df_work.columns[0]].encode('utf-8'))
        subdes.text = str(df_work.at[i, df_work.columns[1]].encode('utf-8'))
        subpr.text = str(df_work.at[i, df_work.columns[2]])
        subqty.text = str(df_work.at[i, df_work.columns[3]])
#        for cnt in range(0, len(classes)):
#            subitems[i][cnt] = et.SubElement(offer[i], classes[cnt])
#            subitems[i][cnt].text = df_work.at[i, df_work.columns[indexes[i]]]

#    data = et.tostring(yml_catalog)
    resultfile = open("/home/grimpoteuthis/app/xls2xml_bayes/res.yml", "w")   
    resultfile.write(et.tostring(yml_catalog, encoding="unicode"))

############ WORK #############
def work():
    df_work = pd.read_excel(open('/home/grimpoteuthis/app/uploads/excel.xls', 'rb'))
    classes = df.columns
    for cnt in range(0, len(classes)):
        freq = np.empty([65536, len(classes)])
        for row in df.index:
            cell = df.at[row, classes[cnt]]
            if not isinstance(cell, int) and not isinstance(cell, np.int64) and not isinstance(cell, float):
                cell = cell.encode('utf-8')
                words = word_process(cell)
        #        freq = [[0 for x in range(len(words))] for y in range(len(classes))]
            #    freq = np.empty((len(words), len(classes)))    
                for w in range(len(words)):
                    if words[w] != "\n":
                        if words[w] in p[cnt]:
                            freq[w][cnt] = p[cnt][words[w]]
                        else:
                            freq[w][cnt] = 1
            elif words[w] != "\n":
                if 'number' in p[cnt]:
                    freq[w][cnt] = p[cnt][words[w]]
                else:
                    freq[w][cnt] = 1
        sums = []
        for cnt in range(len(classes)):
            #sums.append(df.columns[cls].sum())
            temp=0
            idx=[]
            for x in range(len(df.index)):
                temp+=freq[x][cnt]    
            sums.append(temp)
#        print(sums.index(max(sums)))
        idx.append(sums.index(max(sums)))
    convert(idx)

############ MAIN #############
def parse():
    work()
