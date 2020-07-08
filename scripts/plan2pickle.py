import sys
sys.path.append("../")

from utils import get_plan, get_db_conn, start_server, close_server
import pickle
import pprint
import os
import subprocess
import time

query_out_dir = sys.argv[1]
plan_pickle_path = sys.argv[2]


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
    p = get_plan(conn, q_text)
    conn.close()
    d[name] = p
    pprint.pprint(p)

    if i % 100 == 0:
        print(i)
    i += 1

close_server()
pickle.dump(d, open(plan_pickle_path, 'wb'))
