import pandas as pd
import redis
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import RussianStemmer
from pymystem3 import Mystem
import numpy as np
import aerospike

config = {
  'hosts': [ ('127.0.0.1', 3000) ]
}

try:
  client = aerospike.client(config).connect()
except:
  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)


df = pd.read_excel(open('ks.xlsx', 'rb'))
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

def learn():
	for cnt in range(0, len(classes)):
		for row in df.index:
			cell = df.at[row, classes[cnt]]
			if not isinstance(cell, int) and not isinstance(cell, np.int64) and not isinstance(cell, float) and not isinstance(cell, TimeStamp):
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

#if __name__ == "__main__":
#	learn()
