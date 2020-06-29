import sys
sys.path.append("../")

import torch
import torch.nn as nn
import torch.optim as optim
from models import Scan_NN, Join_NN, Estimator, Model
#import gensim.models
import pickle
from utils import get_base_feature, get_filter_feature, get_join_feature
import pprint
import numpy as np
import random
import itertools

plan_pickle_path = sys.argv[1]
lat_pickle_path = sys.argv[2]

plans = pickle.load(open(plan_pickle_path, 'rb'))
lats = pickle.load(open(lat_pickle_path, 'rb'))
#w2vmodel =gensim.models.Word2Vec.load(word2vec_model_path)

model = Model()

opt = optim.SGD(model.parameters(), lr= 0.0001, weight_decay =0.01)
criterion = nn.L1Loss()



def featurize_tree(plan_tree):
    scan_fs = []
    join_fs = []
    stack = [plan_tree]
    while stack:
        popped = stack.pop()
        node_name = popped[0][0]
        if node_name == 'PelagoTableScan':
            f = get_base_feature(popped)
            scan_fs.append(f)
        elif node_name == 'PelagoJoin':
            f = get_join_feature(popped)
            join_fs.append(f)
        for ch in popped[1]:
            stack.append(ch)
    scan_fs = torch.mean(torch.stack(scan_fs), axis = 0)
    join_fs = torch.mean(torch.stack(join_fs), axis = 0)
    return torch.cat([scan_fs, join_fs])



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

experiment_no = 2
train, val = split_dataset(experiment_no)
train_data, val_data = [], []
train_labels, val_labels = [], []
for k,v in train.items():
    train_data.append(featurize_tree(v))
    train_labels.append(lats[k]['execution_time']/1000)
for k,v in val.items():
    val_data.append(featurize_tree(v))
    val_labels.append(lats[k]['execution_time'] / 1000)

train_data = torch.stack(train_data)
val_data = torch.stack(val_data)
train_labels = torch.Tensor(train_labels)
val_labels =  torch.Tensor(val_labels)

train_mean, train_var = torch.mean(train_data, axis = 0), torch.std(train_data, axis = 0)
train_data.sub_(train_mean).div_(train_var)
val_data.sub_(train_mean).div_(train_var)

for e in itertools.count():
    #print('\n\n', 'experiment=', experiment_no, ' epoch=', e, '\n\n')
    opt.zero_grad()
    preds = model(train_data)
    loss = criterion(preds, train_labels.view(-1,1))
    loss.backward()
    opt.step()

    #print("----------val-----------\n--------\n-----")
    with torch.no_grad():   
        val_loss = 0
        val_preds = model(val_data)
        val_loss = criterion(val_preds, val_labels.view(-1,1))
        if e % 50 == 0:
            overall_accs = (torch.max(preds / train_labels.view(-1,1), train_labels.view(-1,1) / preds))
            val_overall_accs = (torch.max(val_preds / val_labels.view(-1,1), val_labels.view(-1,1) / val_preds))
            print("epoch=", e, " train loss/r", loss.item(), torch.mean(overall_accs).item(), "test loss/r", val_loss.item(), torch.mean(val_overall_accs).item())

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
