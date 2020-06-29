from config import host, catalog_path, tables, columns, ops, table_sizes
import torch
import jaydebeapi
import xmltodict, json
from treeutils import create_node, add_child
from collections import OrderedDict
import pprint
import json
import re
import numpy as np
import os, subprocess, time
import psycopg2
from jaydebeapi import _DEFAULT_CONVERTERS, _java_to_py
_DEFAULT_CONVERTERS.update({'BIGINT': _java_to_py('longValue')})

def transform_dict(d):
    r = dict()
    r[d['@name']] = d['#text']
    return r

def transform_dicts(ds):
     r = dict()
     for d in ds:
         r[d['@name']] = d['#text']
     return r

def process_node(n):
    props = n['Property']
    if isinstance(props, OrderedDict):
        if props['@name'] in ('trait', 'traits', 'intrait'):
            return (n['@type'], None)
        else:
            return (n['@type'], transform_dict(props))
    elif isinstance(props, list):
        props = [x for x in props if x['@name'] not in ('trait', 'traits', 'intrait')]
        return  (n['@type'], transform_dicts(props))



def traverse(o, t):
    if o is None:
        return

    o = o['RelNode']

    if isinstance(o, list):
        for elem in o:
            d = process_node(elem)
            add_child(t, create_node(d))
            traverse(elem['Inputs'], t[1][-1])
    elif isinstance(o, OrderedDict):
        d = process_node(o)
        add_child(t, create_node(d))

        traverse(o['Inputs'], t[1][-1])



def get_db_conn():
    conn = jaydebeapi.connect("org.apache.calcite.avatica.remote.Driver",
                          "jdbc:avatica:remote:url=" + host + ";serialization=PROTOBUF",
                          {}, '/scratch/mtopak/pelago2/opt/lib/avatica-1.13.0.jar')

    return conn


def get_plan(conn, q_txt):
    curs = conn.cursor()
    curs.execute("ALTER SESSION SET hwmode = cpuonly");
    curs.execute("ALTER SESSION SET cpudop = 1");
    q = 'EXPLAIN PLAN AS XML FOR ' + q_txt
    curs.execute(q)
    res = curs.fetchall()[0][0]
    res = res.replace('\t\n', '')
    res = xmltodict.parse(res)
    tree = create_node(-1)
    traverse(res, tree)
    tree = tree[1][0]
    curs.close()
    return tree
    

def get_latency(conn, q_txt):
    curs = conn.cursor()
    curs.execute("ALTER SESSION SET hwmode = cpuonly");
    curs.execute("ALTER SESSION SET cpudop = 1");
    try:
        res = curs.execute(q_txt)
    except Exception as e:
        #print("excepted", e)
        curs.execute("select * from SessionTimings")
        res = curs.fetchall()[-1]
        res = [x.value for x in res[:-1]] + [res[-1]]
        ret = dict(zip([x[0] for x in curs.description], res))
    finally:
        curs.close()
        return ret


def get_plan_ops(plan):
    acc = set([plan[0][0]])
    for child in plan[1]:
        ret = get_plan_ops(child)
        acc.update(ret)
    return acc


def get_op_names(plans):
    acc = set()
    for k,plan in plans.items():
        op_names = get_plan_ops(plan)
        acc.update(op_names)

    return list(acc)


def get_op_counts(plan, op_names):
    freqs = dict(zip(op_names, [0] * len(op_names)))
    queue = [plan]
    while queue:
        front = queue.pop(0)
        freqs[front[0][0]] += 1
        if front[1] is not None:
            for child in front[1]:
                queue.append(child)
    return freqs

def get_cumulative_hash(plan):
    hash_props = []

    queue = []
    queue.append(plan)
    while queue:
        popped = queue.pop(0)
        if popped[0][0] == 'PelagoJoin':
            hash_props.append(popped[0][1])
        for ch in popped[1]:
            queue.append(ch)

    ret = {}
    for d in hash_props:
        for k,v in d.items():
            if k not in ('joinType', 'condition', 'build'):
                ret[k] = ret.get(k,0) + float(v)

    return ret



def get_pack(plan):
    props = []
    queue = []
    queue.append(plan)
    while queue:
        popped = queue.pop(0)
        if popped[0][0] == 'PelagoPack':
            props.append(popped[0][1])
        for ch in popped[1]:
            queue.append(ch)
    ret = {}
    for d in props:
        for k,v in d.items():
            if k == 'inputRows':
                ret[k] = ret.get(k,0) + float(v)
            if k == 'cost':
                v = v.strip('{}').split(',')
                v = [tuple(x.split()[::-1]) for x in v]
                for k2,v2 in v:
                    ret[k2] = ret.get(k,0) + float(v2)
    return ret


def get_tables():
    with open(catalog_path) as f:
        data = json.load(f)
        return list(data.keys())        

def get_columns():
    ret = dict()
    with open(catalog_path) as f:
        data = json.load(f)
        for t in data.keys():
            attrs = [x['attrName'] for x in data[t]['type']['inner']['attributes']]
            ret[t] = attrs
    return ret

def get_col_idx(t_name, col_id):
    idx = 0
    for t in tables:
        if(t == t_name):
            idx += col_id
            return idx
        else:
            idx += len(columns[t])
    
    
def get_empty_base():
    vec_size = sum([len(x) for x in columns.values()])
    return [0] * vec_size



def parse_scan_props(scan_props):
    t_name = scan_props['table'].strip('[]').split(', ')[1]
    fields = list(map(int, scan_props['fields'].strip('[]').split(', ')))
    return t_name, fields




def get_base_feature(scan_node):
    scan_props = scan_node[0][1] #props of scan
    t_name, fields = parse_scan_props(scan_props)
    table_size = table_sizes[t_name]
    t_name = re.sub(r'\d+', '', t_name)

    vec = get_empty_base()
    col_idxs = [get_col_idx(t_name, x) for x in fields]
    for idx in col_idxs:
        vec[idx] = 1

    pg_vec = [np.log((scan_props['pg_total_cost'])), np.log(scan_props['pg_plan_rows'])]
    vec += pg_vec
    #return torch.Tensor(pg_vec)
    return torch.Tensor(vec)
    #field_names = [columns[t_name][x] for x in fields]
    #print(t_name, fields)
    #print(vec)

def get_ops(op_name, plan):
    vals = []
    queue = [plan]
    while queue:
        popped = queue.pop(0)
        if popped[0][0] == op_name:
            vals.append(popped)
        for ch in popped[1]:
            queue.append(ch)
    return vals

def parse_filter_props(filter_props):
    condition_string = filter_props['condition']
    p_ops = re.compile("AND|OR|>=|<=|<|>|=|!=")
    p_tokens = re.compile("(?<=\$)\d+")
    p_literals = re.compile("(?<=')[^\$]+(?=')|(?<!\$)\d+")

    ops = p_ops.findall(condition_string)
    tokens = p_tokens.findall(condition_string)
    literals = p_literals.findall(condition_string)
    return ops, tokens, literals

def get_op_vector(op):
    #print(op, ops)
    vec = [0] * len(ops)
    vec[ops.index(op)] = 1
    return vec

def get_empty_op_vector():
    return [0] * len(ops)

def get_top_level_vector(top_level_op):
    if top_level_op == None:
        return [0,0]
    return [1,0] if top_level_op == 'AND' else [0,1]

def get_filter_feature(filter_node, w2vmodel):
    scan_node = get_ops('PelagoTableScan', filter_node)[0]
    t_name, t_fields = parse_scan_props(scan_node[0][1])
    f_ops, f_tokens, f_literals = parse_filter_props(filter_node[0][1])

    top_level_op = None
    vectors = []
    if f_ops[0] in ('AND', 'OR'):
        top_level_op = f_ops[0]
        f_ops = f_ops[1:]

        #single predicate

    for op, token, lit in zip(f_ops, f_tokens, f_literals):
        field = t_fields[int(token)]

        table_vec = get_empty_base()
        table_vec[get_col_idx(t_name, field)] = 1

        op_vec = get_op_vector(op)
        lit_vec = [(float(lit))] + [0] * 100 if str.isdigit(lit) else [0] + w2vmodel.wv[lit].tolist()
        vectors.append(table_vec + op_vec + lit_vec)
        #vectors.append(table_vec)

    #vector = list(map(sum, zip(*vectors)))
    #top_level_op_vector = get_top_level_vector(top_level_op)
    #print(vectors, np.sum(vectors, axis=0))
    #return top_level_op, torch.Tensor(np.sum(vectors, axis=0).tolist())
    return top_level_op, torch.Tensor(vectors)
    #return top_level_op, vectors

        #if str.isdigit(lit):
        #    print(op, token, lit)
        #    print(table_vec, op_vec, lit_vec)
    #for op, token, lit in zip(f_ops, f_tokens, f_literals):
    #    field = t_fields[int(token)]
    #    print(t_name,columns[t_name][field], op, lit)
        #table_vec = get_empty_base()
        #table_vec[get_col_idx(t_name, field)] = 1
        #op_vec = get_op_vector(op)
        #if not str.isdigit(lit):
        #    print(lit, w2vmodel.wv[lit])
    
        #print(op,field,lit)


def get_join_feature(join_node):
    feature_names = ('h_bits', 'pg_total_cost', 'pg_plan_rows')
    #feature_names = ('rowcnt',)
    feature = [np.log(float(join_node[0][1][x])) for x in feature_names]
    #print(feature)
    return torch.Tensor(feature)



def measure(q):
    os.system('ps aux | grep /scratch/mtopak/pelago2 | grep -v "grep" | awk \'{print $2}\' | xargs kill -9')
    p = subprocess.Popen(["make","run-server"], cwd="/scratch/mtopak/pelago2", stdout=subprocess.PIPE)
    while True:
        output = p.stdout.readline()
        if output == b'log4j: Finished configuring.\n':
            time.sleep(1)
            conn = get_db_conn()
            #print(conn, "asdasda")
            l = get_latency(conn, q)
            conn.close()
            return l

def start_server():
    p = subprocess.Popen(["make","run-server"], cwd="/scratch/mtopak/pelago2", stdout=subprocess.PIPE)
    while True:
        output = p.stdout.readline()
        if output == b'log4j: Finished configuring.\n':
            time.sleep(1)
            return

def close_server():
    os.system('ps aux | grep /scratch/mtopak/pelago2 | grep -v "grep" | awk \'{print $2}\' | xargs kill -9')


def pg_connect(PGDATABASE):
    try:
        conn_string = (
        "host="
        + "localhost"
        + " port="
        + "5432"
        + " dbname="
        + PGDATABASE
#        + " options='-c statement_timeout=60000'"
#                               + " user="
#                               + creds.PGUSER
#                               + " password="
#                               + creds.PGPASSWORD
        )
        conn = psycopg2.connect(conn_string)
        print ("DB connection succesfull")
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error connecting", error)


def pghint_from_proteus(tree):
    if ('TableScan' in tree[0][0]):
        tab_name = tree[0][1]['table'].split(',')[1].strip()[:-1]
        hint = tab_name
        return hint
    elif ('Join' in tree[0][0]):
        h1 = pghint_from_proteus(tree[1][0])
        h2 = pghint_from_proteus(tree[1][1])
        return '(' + h1 + ' '+ h2 + ')'
    else:
        return pghint_from_proteus(tree[1][0])
