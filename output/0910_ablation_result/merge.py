import jsonlines as jsl
import pandas as pd 
from collections import defaultdict

def get_idxs(records):
    return [r['index'] for r in records]

pieces = {
    'cot':['ablation_cot/gsm8k_k0_sc1_s0_e1319_09_09_22_26.jsonl',
'ablation_cot/gsm8k_k6_sc1_s475_e1319_09_09_23_34.jsonl',],
    'pal': ['ablation_pal/gsm8k_k0_sc1_s0_e1319_09_09_22_27.jsonl',
'ablation_pal/gsm8k_k0_sc1_s51_e1319_09_09_23_06.jsonl',
'ablation_pal/gsm8k_k6_sc1_s102_e1319_09_09_23_28.jsonl',],
'plancode':['ablation_plancode/gsm8k_k6_sc1_s0_e1319_09_09_23_40.jsonl',
'ablation_plancode/gsm8k_k6_sc1_s86_e1319_09_10_00_25.jsonl',],
}

newdict= defaultdict(list)
for k,jsls in pieces.items():
    [newdict[k].extend(list(jsl.open(f))) for f in jsls]

newdict_ = {k:pd.DataFrame(records).drop_duplicates(subset='index').to_dict(orient='records') for k, records in newdict.items()}

for k in newdict_.keys():
    fname = f"{k}.jsonl"
    with jsl.open(fname, 'w') as writer:
        writer.write_all(newdict_[k])

    print(fname)
    