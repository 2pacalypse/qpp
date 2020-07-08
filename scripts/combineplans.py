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



def extract_postgres_stats(node):
    if node['Node Type'] in ['Seq Scan', 'Index Scan', 'Bitmap Heap Scan', 'Index Only Scan']: #leaf
        return [{'pg_plan_rows': node['Plan Rows'], 'pg_total_cost': node['Total Cost']}]

    elif node['Node Type'] in ['Nested Loop', 'Hash Join', 'Merge Join']:
        left_stats = extract_postgres_stats(node['Plans'][0])
        right_stats = extract_postgres_stats(node['Plans'][1])
        return [{'pg_plan_rows': node['Plan Rows'], 'pg_total_cost': node['Total Cost']}] + left_stats + right_stats
    else:
        return extract_postgres_stats(node['Plans'][0])


def place_postgres_stats(node, pg_stats, index):
    if 'Join' in node[0][0]:
        updated_dict = {**node[0][1], **pg_stats[index]}
        left_ch =  place_postgres_stats(node[1][0], pg_stats, index + 1)
        right_ch = place_postgres_stats(node[1][1], pg_stats, index + 2)
        return (node[0][0], updated_dict), [left_ch, right_ch]
    elif 'Scan' in node[0][0]:
        updated_dict = {**node[0][1], **pg_stats[index]} 
        return (node[0][0], updated_dict), []
    else:
        ch = place_postgres_stats(node[1][0], pg_stats, index)
        return node[0], [ch]

proteus_plan_out_path = sys.argv[1]
postgres_plan_out_path = sys.argv[2]
combined_plan_path = sys.argv[3]


proteus_plans = pickle.load(open(proteus_plan_out_path, 'rb'))
pg_plans = pickle.load(open(postgres_plan_out_path, 'rb'))

d = dict()
for k,proteus_plan in proteus_plans.items():
    pg_plan = pg_plans[k][0][0]['Plan']
    pg_stats = extract_postgres_stats(pg_plan)
    new_proteus_plan = place_postgres_stats(proteus_plan, pg_stats, 0)
    d[k] = new_proteus_plan

pickle.dump(d, open(combined_plan_path, 'wb'))


