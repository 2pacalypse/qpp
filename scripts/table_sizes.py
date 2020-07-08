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






d = dict()
table_names = ['ssbm_lineorder', 'ssbm_date', 'ssbm_part', 'ssbm_supplier', 'ssbm_customer']
for t_name in table_names:
    sf10_tname = t_name.replace('ssbm', 'ssbm10')
    query = 'select count(*) from '
    pg_curs100.execute(query + t_name)
    res = pg_curs100.fetchone()
    pg_curs10.execute(query + sf10_tname)
    res_sf10 = pg_curs10.fetchone()
    d[t_name] = res[0]
    d[sf10_tname] = res_sf10[0]

pprint.pprint(d)

