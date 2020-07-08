import sys
import pickle
import pprint

plan_pickle_path = sys.argv[1]
lat_pickle_path = sys.argv[2]

plans = pickle.load(open(plan_pickle_path, 'rb'))
lats = pickle.load(open(lat_pickle_path, 'rb'))



d = dict()
for k, plan in plans.items():
       if k == '10-q3_3-0':
           scale, template, seed = k.split('-')
           d[template + seed] = d.get(template + seed, []) + [(scale, lats[k])]
           pprint.pprint(plan)
           quit()

for k,v in d.items():
    print(k)
    pprint.pprint(v)
