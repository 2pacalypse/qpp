import os
import re
import sys
sys.path.append('../')
from config import ssb_qgen_dir


query_out_dir = sys.argv[1]
if not os.path.exists(query_out_dir):
    os.makedirs(query_out_dir)

os.chdir(ssb_qgen_dir)
files = os.listdir("./queries-templates")
q_templates = [x.replace('.sql', '') for x in files]

for template in q_templates: 
    if template in ('q4_3', 'q4_2', 'q4_1'):
        continue
    for seed in range(30):
        cmdStr = './qgen.sh' + ' ' + template + ' '  +  str(seed)
        q = os.popen(cmdStr).read()
        q = re.sub(r'\blineorder\b', 'ssbm_lineorder', q, flags = re.IGNORECASE)
        q = re.sub(r'\bdates\b', 'ssbm_date', q, flags = re.IGNORECASE)

        q = re.sub(r'\bpart\b', 'ssbm_part', q, flags = re.IGNORECASE)
        q = re.sub(r'\bsupplier\b', 'ssbm_supplier', q, flags = re.IGNORECASE)
        q = re.sub(r'\bp_brand\b', 'p_brand1', q, flags = re.IGNORECASE)

        q = re.sub(r'\bcustomer\b', 'ssbm_customer', q, flags = re.IGNORECASE)

        q = q.replace(';', '')
        q2 = q.replace('ssbm', 'ssbm10')
        with open(query_out_dir + '/100-' + template + '-' + str(seed) + '.sql', 'w') as f:
            print(q, file = f)
        with open(query_out_dir + '/10-' + template + '-' + str(seed) + '.sql', 'w') as f:
            print(q2, file=f)


