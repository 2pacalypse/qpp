import sys
sys.path.append("../")

from utils import get_plan, get_db_conn, get_latency, start_server, close_server
import pickle
import pprint
import os
import subprocess
import time
import signal
import psutil


query_out_dir = sys.argv[1]
latency_pickle_path = sys.argv[2]


d = dict()
files = os.listdir(query_out_dir)

i = 0
for file_name in files:
    name = file_name.replace('.sql', '')
    with open(query_out_dir + '/' + file_name, 'r') as f:
        q_text = f.read()

    close_server()
    start_server()
    conn = get_db_conn()
    l = get_latency(conn, q_text)
    conn.close()
    d[name] = l
    pprint.pprint(l)

    if i % 100 == 0:
        print(i)
    i += 1

close_server()
pickle.dump(d, open(latency_pickle_path, 'wb'))
