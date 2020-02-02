from __future__ import division
import re 
import pandas as pd 
import numpy as np
from random import random, seed
from sklearn import metrics
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from collections import defaultdict
from math import log

def train(samples, classes):
	freq = defaultdict(lambda:0)
	for feats, label in samples:
		for feat in feats:
			freq[label, feat] += 1          # count features frequencies

	for label, feat in freq:                # normalize features frequencies
		freq[label, feat] /= classes[label]
	for c in classes:                       # normalize classes frequencies
		classes[c] /= len(samples)

	return classes, freq			# return P(C) and P(O|C)



###################

df = pd.read_excel(open('the_table.xls', 'rb'))
classes = df.loc[0,:]

#df.dropna(inplace = True)
#df = df.iloc[1:,]
#df = df.drop(0, axis=0)
df = df.T

print(df)

#train(df, classes)
#print(df.describe())

#message=pd.read_csv('the_table.csv',sep='\t',names=["label","a","b","c","d"])
#print(message.describe())
