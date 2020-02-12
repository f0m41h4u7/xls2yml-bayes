import aerospike
import pandas as pd
import datetime
from pandas import Timestamp
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import RussianStemmer
from pymystem3 import Mystem
import numpy as np

def isunique(w):
	for cls in classes:
		(key, meta) = client.exists(('test', cls, w))
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
		(key, meta) = client.exists(('test', cls, w))
		if meta!='None':
			client.increment(('test', cls, w), 'qty', 1)
		else:
			client.put(('test', cls, w), {'qty': 1})

# Open dataset table
df = pd.read_excel(open('ks.xlsx', 'rb'))
classes = df.columns
mystem = Mystem()

# Connect to aerospike db
config = {
    'hosts': [
        ( '127.0.0.1', 3000 )
    ],
    'policies': {
        'timeout': 1000
    }
}
client = aerospike.client(config)
client.connect()

# Start learning
for cls in classes:
	for row in df.index:
		cell = df.at[row, cls]
		if not isinstance(cell, int) and not isinstance(cell, np.int64) and not isinstance(cell, float) and not isinstance(cell, Timestamp) and not isinstance(cell, datetime.time) and not isinstance(cell, long):
			cell = cell.encode('utf-8')
			words = word_process(cell)
			count_freq(words, cls)
		elif isinstance(cell, Timestamp) or isinstance(cell, datetime.time):
			(key, meta) = client.exists(('test', cls, 'datetime'))
                        if meta!='None':
                                client.increment(('test', cls, 'datetime'), 'qty', 1)
                        else:
                                client.put(('test', cls, 'datetime'), {'qty': 1})
		else:
			(key, meta) = client.exists(('test', cls, 'number'))
			if meta!='None':
				client.increment(('test', cls, 'number'), 'qty', 1)
			else:
				client.put(('test', cls, 'number'), {'qty': 1})
#	for w in p[cnt]:
		# p[cnt][w] /= len(p[cnt])
#		print(test[cnt][w], len(test[cnt]))

