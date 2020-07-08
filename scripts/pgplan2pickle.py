import sys
sys.path.append("../")

from utils import get_plan, get_db_conn, get_latency, start_server, close_server, pg_connect, pghint_from_proteus
import pickle
import pprint
import os
import subprocess
import time
import signal
import psutil



query_out_path = sys.argv[1]
plan_out_path = sys.argv[2]
postgres_plan_out_path = sys.argv[3]

plans = pickle.load(open(plan_out_path, 'rb'))
queries = pickle.load(open(query_out_path, 'rb'))

pg_conn100 = pg_connect('ssbm100')
pg_curs100 = pg_conn100.cursor()

pg_conn10 = pg_connect('ssbm10')
pg_curs10 = pg_conn10.cursor()

for curs in (pg_curs100, pg_curs10):
    curs.execute("load 'pg_hint_plan'")
    curs.execute("SET max_parallel_workers_per_gather = 0")
    curs.execute("SET enable_seqscan = on")
    curs.execute("SET enable_hashjoin = on")
    curs.execute("SET enable_bitmapscan = off")
    curs.execute("SET enable_indexscan = off")
    curs.execute("SET enable_mergejoin = off")
    curs.execute("SET enable_nestloop = off")
    curs.execute("SET enable_indexonlyscan = off")





plans = pickle.load(open(plan_out_path, 'rb'))
queries = pickle.load(open(query_out_path, 'rb'))

d = dict()
for k,v in plans.items():
    print(k)
    scale_factor = k.split('-')[0]
    q = queries[k]
    hint = pghint_from_proteus(v)
    hint = '/*+ leading(' + hint + ') */'
    statement = hint + '\n'+ 'explain (analyze false, costs true, format JSON)' + '\n'+ q
    curs = pg_curs100 if scale_factor == '100' else pg_curs10
    curs.execute(statement)
    json_plan = curs.fetchone()
    d[k] = json_plan


pickle.dump(d, open(postgres_plan_out_path, 'wb'))


