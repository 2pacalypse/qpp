import struct
import os
from config import data_path, word2vec_model_path
import pprint
import gensim.models
import logging
import numpy as np 
import sys

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




col_gen = read_col(sys.argv[1], sys.argv[2], int(sys.argv[3]))

dist = dict()
for elems in col_gen:
    for val in elems:
        dist[val] = dist.get(val, 0) + 1
        #print(val)
#pprint.pprint(dist)
print(list(sorted(dist.keys())))
