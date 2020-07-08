import os
import pickle
import sys

#sys.path.append("../")
#from config import query_out_dir, query_pickle_path


query_out_dir = sys.argv[1]
query_pickle_path = sys.argv[2]

d = dict()

files = os.listdir(query_out_dir)

i = 0
for file_name in files:
    name = file_name.replace('.sql', '')
    with open(query_out_dir + '/' + file_name, 'r') as f:
        q_text = f.read()

    d[name] = q_text

    if i % 100 == 0:
        print(i)
    i += 1

pickle.dump(d, open(query_pickle_path, 'wb'))
