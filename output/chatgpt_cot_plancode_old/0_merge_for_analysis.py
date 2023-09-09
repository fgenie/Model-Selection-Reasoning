from pathlib import Path 
import jsonlines as jsl
from functools import partial 


base = '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/chatgpt/gsm8k_sc1_s0_e1319_08_31_00_19.jsonl'

k5 = [
    'gsm8k_k5_sc1_s0_e1319_09_03_03_25.jsonl',
'gsm8k_k5_sc1_s143_e1319_09_03_09_45.jsonl',
'gsm8k_k5_sc1_s71_e1319_09_03_04_02.jsonl',
'gsm8k_k5_sc1_s72_e1319_09_03_04_05.jsonl',
]
    
k2 = [
    'gsm8k_k2_sc1_s0_e1319_09_03_03_55.jsonl',
'gsm8k_k2_sc1_s15_e1319_09_03_04_02.jsonl',
'gsm8k_k2_sc1_s19_e1319_09_03_04_05.jsonl',
]

exproot = Path()/'sep3'
if not exproot.exists():
    exproot.mkdir()

k2_merged = []
k5_merged = []
for f in k5:
    k5_merged.extend(list(jsl.open(f)))
for f in k2:
    k2_merged.extend(list(jsl.open(f)))
k2_merged = sorted(k2_merged, key=lambda rec: rec['index'])
k5_merged = sorted(k5_merged, key=lambda rec: rec['index'])
baserec = list(jsl.open(base))

def get_idxs(records):
    return [r['index'] for r in records]
bidx, k2idx, k5idx = map(get_idxs, [baserec, k2_merged, k5_merged])
bidx, k2idx, k5idx = map(set, [bidx, k2idx, k5idx ])
common = k2idx&k5idx
common = bidx & common 
common = list(common)
print()

def filter(records:list, idx:list=None):
    return [record for record in records if record['index'] in idx]

filter_common =  partial(filter, idx=common)
bs, k2, k5 = map(filter_common, [baserec, k2_merged, k5_merged])

with jsl.open(exproot/'baseline.jsonl', 'w') as wb, jsl.open(exproot/'k2.jsonl', 'w') as w2, \
    jsl.open(exproot/'k5.jsonl', 'w') as w5:
    wb.write_all(bs)
    w2.write_all(k2)
    w5.write_all(k5)

for f in [    'baseline.jsonl', 'k2.jsonl', 'k5.jsonl']:
    path = exproot/f
    print(str(path))
