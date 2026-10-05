#!/usr/bin/env python3
"""Prepare blinded human/model judging packets from independently generated answers."""
import argparse
import json
import random
from pathlib import Path
from validate import ROOT

parser=argparse.ArgumentParser()
parser.add_argument('baseline',type=Path)
parser.add_argument('skilled',type=Path)
parser.add_argument('output',type=Path)
parser.add_argument('--seed',type=int,default=20261005)
parser.add_argument('--cases',type=Path,default=ROOT/'evals'/'cases.json')
args=parser.parse_args()
answers=[]
for path in [args.baseline,args.skilled]:
    records=json.loads(path.read_text())
    mapping={r['id']:r['answer'] for r in records}
    if len(mapping)!=len(records):
        raise SystemExit(f'Duplicate cases in {path}')
    answers.append(mapping)
cases=json.loads(args.cases.read_text())
ids={c['id'] for c in cases}
if any(set(a)!=ids for a in answers):
    raise SystemExit('Answer IDs must match evaluation cases exactly')
rng=random.Random(args.seed)
packet=[];key={}
for case in cases:
    flip=rng.choice([False,True])
    conditions=['skilled','baseline'] if flip else ['baseline','skilled']
    indices=[1,0] if flip else [0,1]
    packet.append({**case,'answers':dict(zip(['A','B'],[answers[i][case['id']] for i in indices]))})
    key[case['id']]=dict(zip(['A','B'],conditions))
args.output.mkdir(parents=True,exist_ok=True)
(args.output/'packet.json').write_text(json.dumps(packet,indent=2)+'\n')
(args.output/'key.json').write_text(json.dumps(key,indent=2)+'\n')
print(f'Prepared {len(packet)} pairs. Give judges packet.json only; keep key.json separate.')
