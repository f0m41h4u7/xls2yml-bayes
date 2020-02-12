import aerospike
import pandas as pd
import redis
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import RussianStemmer
from pymystem3 import Mystem
import numpy as np

df = pd.read_excel(open('ks.xlsx', 'rb'))
classes = df.columns
mystem = Mystem()

config = {
    'hosts': [
        ( '127.0.0.1', 4000 )
    ],
    'policies': {
        'timeout': 1000 # milliseconds
    }
}
client = aerospike.client(config)

def isunique(w):
	for cls in classes:
		(key, meta) = client.exists(('vocabulary', cls, w))
		if meta!='None':
			return False
	return True

def word_process(cell):
	cell = cell.decode('utf-8')
	words = mystem.lemmatize(cell.lower())
	stemmer = RussianStemmer()
	words = [stemmer.stem(word) for word in words]
	return words

def count_freq(words, cls):
	for w in words:
		(key, meta) = client.exists(('vocabulary', cls, w))
		if meta!='None':
			client.increment(('vocabulary', cls, w), 1)
		else:
			client.put(('vocabulary', cls, w), 1)

def learn():
	for cls in classes:
		for row in df.index:
			cell = df.at[row, cls]
			if not isinstance(cell, int) and not isinstance(cell, np.int64) and not isinstance(cell, float) and not isinstance(cell, TimeStamp):
				cell = cell.encode('utf-8')
				words = word_process(cell)
				count_freq(words, cls)
			else:
				(key, meta) = client.exists(('vocabulary', cls, 'number'))
				if meta!='None':
					client.increment(('vocabulary', cls, 'number'), 1)
				else:
					client.put(('vocabulary', cls, 'number'), 1)
#		for w in p[cnt]:
			# p[cnt][w] /= len(p[cnt])
#			print(vocabulary[cnt][w], len(vocabulary[cnt]))

#if __name__ == "__main__":
#	learn()
