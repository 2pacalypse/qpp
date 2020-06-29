import sys
sys.path.append("../")

import torch
import torch.nn as nn
import torch.optim as optim
from models import Scan_NN, Join_NN, Estimator
#import gensim.models
import pickle
from utils import get_base_feature, get_filter_feature, get_join_feature
import pprint
import numpy as np
import random


plan_pickle_path = sys.argv[1]
lat_pickle_path = sys.argv[2]

plans = pickle.load(open(plan_pickle_path, 'rb'))
lats = pickle.load(open(lat_pickle_path, 'rb'))
#w2vmodel =gensim.models.Word2Vec.load(word2vec_model_path)

model_scan =  Scan_NN()
model_join = Join_NN()
model_estimator = Estimator()


opt_scan = optim.Adam(model_scan.parameters(), lr= 0.00001)
opt_join = optim.Adam(model_join.parameters(), lr= 0.00001)
opt_estimator = optim.Adam(model_estimator.parameters(), lr= 0.001)

criterion = nn.L1Loss()

def model_step(loss):
       opt_scan.zero_grad()
       #opt_predicate.zero_grad()
       #opt_filter.zero_grad()   
       opt_join.zero_grad()  
       opt_estimator.zero_grad()    
       loss.backward()
       opt_scan.step()
       #opt_predicate.step()
       #opt_filter.step() 
       opt_join.step()
       opt_estimator.step() 

def init_loss_dict():
    d = dict()
    d['scan_loss'] = []
    #d['predicate_loss'] = []
    #d['filter_loss'] = []
    d['join_loss'] = []
    d['est_loss'] = []
    return d

def train_tree(plan_tree, latency, d):
    node_name = plan_tree[0][0]

    if node_name == 'PelagoTableScan':
        inp = get_base_feature(plan_tree)
        #print(inp, "hahhahaha")
        reconstructed, encoded = model_scan(inp)
        loss = criterion(inp, reconstructed)
        d['scan_loss'].append(loss.item())
        return encoded, loss
        """
    elif node_name == 'PelagoFilter':
        child_encoded, child_loss = train_tree(plan_tree[1][0], latency, d)
        top_level_op, vectors = get_filter_feature(plan_tree, w2vmodel)
        predicate_reconstructed, predicate_encoded = model_predicate(vectors)
        predicate_loss = criterion(vectors, predicate_reconstructed)
        d['predicate_loss'].append(predicate_loss.item())

        if top_level_op == 'AND':
            predicate_encoded, _ = torch.min(predicate_encoded, dim=0)
        elif top_level_op == 'OR':
            predicate_encoded, _ = torch.max(predicate_encoded, dim=0)
        else:
            predicate_encoded = torch.squeeze(predicate_encoded)

        filter_vector = torch.cat([child_encoded, predicate_encoded])
        filter_reconstructed, filter_encoded = model_filter(filter_vector)
        filter_loss = criterion(filter_vector, filter_reconstructed)
        d['filter_loss'].append(filter_loss.item())

        return filter_encoded, child_loss + predicate_loss + filter_loss
        """
    elif node_name == 'PelagoJoin':
        ch1_encoded, ch1_loss = train_tree(plan_tree[1][0], latency,d)
        ch2_encoded, ch2_loss = train_tree(plan_tree[1][1], latency,d)

        vector = get_join_feature(plan_tree)
        vector = torch.cat([vector, ch1_encoded, ch2_encoded])
        reconstructed, encoded = model_join(vector)
        join_loss = criterion(vector, reconstructed)
        d['join_loss'].append(join_loss.item())
        return encoded, ch1_loss + ch2_loss + join_loss

    elif node_name == 'PelagoToEnumerableConverter':
        ch_encoded, ch_loss = train_tree(plan_tree[1][0], latency, d)
        #print(ch_encoded)
        predicted_latency = model_estimator(ch_encoded)
        est_loss = criterion(predicted_latency, latency)
        d['est_loss'].append(est_loss.item())
        return predicted_latency, ch_loss + est_loss
    else:
        return train_tree(plan_tree[1][0], latency, d)

def split_dataset(experiment_no):
    if experiment_no == 0:
       all_plans = list(plans.items())
       random.shuffle(all_plans)
       l = len(all_plans)
       train_plans = dict(all_plans[:int(l * 0.8)])
       val_plans = dict(all_plans[int(l*0.8): ])
       return train_plans, val_plans

    if experiment_no == 1:
        all_plans = list(plans.items())
        random.shuffle(all_plans)
        sf100_plans = dict([(k,v) for (k,v) in all_plans if k.startswith('100')])
        sf10_plans = dict([(k,v) for (k,v) in all_plans if k.startswith('10') and '100' not in k]) 
        return sf100_plans, sf10_plans


    if experiment_no == 2:
        all_plans = list(plans.items())
        random.shuffle(all_plans)
        sf100_plans = [(k,v) for (k,v) in all_plans if k.startswith('100')]
        train_plans = [(k,v) for k,v in sf100_plans if 'q3_' in k or 'q2_' in k]
        test_plans = [(k,v) for k,v in sf100_plans if 'q1_' in k]
        return dict(train_plans), dict(test_plans)

    if experiment_no == 3:
         all_plans = list(plans.items())
         random.shuffle(all_plans) 
         sf100_plans = [(k,v) for (k,v) in all_plans if k.startswith('100')]
         l = len(sf100_plans)
         train_plans = dict(sf100_plans[:int(l * 0.8)])
         val_plans = dict(sf100_plans[int(l*0.8): ])
         return train_plans, val_plans

    if experiment_no == 4:
         all_plans = list(plans.items())
         random.shuffle(all_plans)
         sf10_plans = [(k,v) for (k,v) in all_plans if k.startswith('100')]
         l = len(sf10_plans)
         train_plans = dict(sf10_plans[:int(l * 0.8)])
         val_plans = dict(sf10_plans[int(l*0.8): ])
         return train_plans, val_plans

experiment_no = 0
train, val = split_dataset(experiment_no)

for e in range(10000):
    print('\n\n', 'experiment=', experiment_no, ' epoch=', e, '\n\n')
    overall_accs = []
    loss_dict = init_loss_dict()
    loss_per_template = dict()
    acc_per_template = dict()
    loss = 0
    for k,v in train.items():
        lat = torch.Tensor([lats[k]['execution_time'] / 1000]) 
        predicted_lat, tree_loss = train_tree(v, lat, loss_dict) 
        q_template = k.split('-')[0]
        loss_per_template[q_template] = loss_per_template.get(q_template, 0) +  tree_loss.item()
        acc_per_template[q_template] = acc_per_template.get(q_template, []) + [np.max([predicted_lat/lat, lat/predicted_lat])]
        loss += tree_loss
        overall_accs.append(np.max([predicted_lat / lat, lat / predicted_lat]))

    model_step(loss )
    for k,v in loss_dict.items():
        print(k, np.mean(v))

    print('total_loss=', loss.item())
    print('mean_overall_acc=', torch.mean(torch.Tensor(overall_accs)), ' median_overall_acc=', torch.median(torch.Tensor(overall_accs)) ,'min=', torch.min(torch.Tensor(overall_accs))) 
    print('loss per template')
    pprint.pprint(loss_per_template)
    for k in acc_per_template.keys():
        print(k, torch.mean(torch.Tensor(acc_per_template[k])),  torch.median(torch.Tensor(acc_per_template[k])))



    print("----------val-----------\n--------\n-----")
    overall_accs = [] 
    loss_dict = init_loss_dict()
    loss_per_template = dict()
    acc_per_template = dict()
    loss = 0 
    with torch.no_grad():   
    
        for k,v in val.items():
            lat = torch.Tensor([lats[k]['execution_time'] / 1000]) 
            predicted_lat, tree_loss = train_tree(v, lat, loss_dict) 
            q_template = k.split('-')[0]
            loss_per_template[q_template] = loss_per_template.get(q_template, 0) +  tree_loss.item()
            acc_per_template[q_template] = acc_per_template.get(q_template, []) + [np.max([predicted_lat/lat, lat/predicted_lat])]
            loss += tree_loss
            overall_accs.append(np.max([predicted_lat / lat, lat / predicted_lat]))
    for k,v in loss_dict.items():
        print("val", k, np.mean(v))

    print('total_loss=', loss.item())
    print('mean_overall_acc=', torch.mean(torch.Tensor(overall_accs)), ' median_overall_acc=', torch.median(torch.Tensor(overall_accs)) ,'min=', torch.min(torch.Tensor(overall_accs)))
    print('loss per template')
    pprint.pprint(loss_per_template)
    for k in acc_per_template.keys():
        print(k, torch.mean(torch.Tensor(acc_per_template[k])),  torch.median(torch.Tensor(acc_per_template[k])))

quit()

for t in range(60000):
    encoded_inp = model_scan.encoder(inp)
    encoded_inp2 = model_filter.encoder(inp2)

    pred_m1 = model_scan(inp)
    pred_m2 = model_filter(inp2)



    opt1.zero_grad()
    opt2.zero_grad()

    loss1 = criterion(pred_m1, inp) 
    loss2 = criterion(pred_m2, inp2)
    loss3 = loss1 + loss2

    if t % 300 == 0:
        print(loss1.item(), loss2.item(), loss3.item(), 'loss')
        print('enc1 enc2 pred1 pred2')   
        print(encoded_inp.data.tolist())
        print(encoded_inp2.data.tolist())
        print(pred_m1.data.tolist())
        print(pred_m2.data.tolist())
    loss3.backward()
    opt1.step()
    opt2.step()

#optimizer = optim.Adam(model.parameters(), lr=1e-3)
#criterion = nn.MSELoss()
