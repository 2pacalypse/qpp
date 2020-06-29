import struct
import os
from config import data_path, word2vec_model_path
import pprint
import gensim.models
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 

dicts =  set()
data = dict()

files = os.listdir(data_path)
files.remove('catalog.json')

for f in files:
    tokens = f.split('.')
    if tokens[-1] == 'dict':
        dicts.update([(tokens[0], tokens[2])])
    else:
        d = data.get(tokens[0], [])
        d.append(tokens[2])
        data[tokens[0]] = d


def read_table(t_name, chunk_size):
    cols = data[t_name]
    print(cols)
    gens = [read_col(t_name, col, chunk_size) for col in cols]
    while True:
        lists = [next(g) for g in gens]
        lists = [l if isinstance(l[0], str) else list(map(str, l)) for l in lists]
        yield list(map(list, zip(*lists)))


def read_col(t_name, col, chunk_size):
    if (t_name, col) in dicts:
        with open(data_path +t_name + '.csv.' + col + '.dict' , 'r') as f:
           dict = f.read()
           dict = dict.split('\n')
           dict = [x.split(':')[0] for x in dict]
    with open(data_path + t_name + '.csv.' + col, 'rb') as f:
        total_bytes = os.path.getsize(data_path + t_name + '.csv.' + col)
        if total_bytes % (chunk_size * 4) != 0:
            raise Exception('Give a divisible of ', total_bytes / 4)
        read_bytes = 0
        while read_bytes < total_bytes :
            read_bytes += chunk_size * 4
            bytes = f.read(chunk_size * 4)
            elements = struct.unpack(str(chunk_size) + 'i', bytes)
            if (t_name, col) in dicts:
                elements = [dict[x] for x in elements]
            yield elements


class Sentences(object):
    def __init__(self, t_names, chunk_sizes):
        self.t_names = t_names
        self.chunk_sizes = chunk_sizes
 
    def __iter__(self):
        for t,c in zip(self.t_names, self.chunk_sizes):
            for l in read_table(t, c):
                for sentence in l:
                    yield sentence




#sentences = Sentences(['supplier'], [20000]) # a memory-friendly iterator
#sentences = Sentences(['date', 'customer', 'part', 'supplier'], [2556,40000, 70000, 20000])
#model = gensim.models.Word2Vec(sentences, workers = 4)
#model.save(word2vec_model_path)

model =gensim.models.Word2Vec.load(word2vec_model_path)
vector = model.wv["MFGR#2239"]

normal_neighbors = model.wv.most_similar([vector], topn=11)
for neighbor in normal_neighbors:
    print(neighbor)

#print("another haha")
#y = read_col('customer', 'c_address', 10)

