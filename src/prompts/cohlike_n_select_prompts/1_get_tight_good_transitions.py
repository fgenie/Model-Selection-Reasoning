COT_WRONG="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/cot_wrong.csv"
COT_CORRECT="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/cot_correct.csv"

PAL_WRONG="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/pal_wrong.csv"
PAL_CORRECT="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/pal_correct.csv"

P2C_WRONG="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0924_plancode_v2_abl/gsm8k_k8_sc1_s0_e1319_09_24_01_16_wrong.csv"
P2C_CORRECT="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0924_plancode_v2_abl/gsm8k_k8_sc1_s0_e1319_09_24_01_16_correct.csv"

import jsonlines as jsl
import pandas as pd
from itertools import product

pal_wrong_df = pd.read_csv(PAL_WRONG, index_col='index')
p2c_wrong_df = pd.read_csv(P2C_WRONG, index_col='index')
cot_wrong_df = pd.read_csv(COT_WRONG, index_col='index')

pal_wrongs = set(pal_wrong_df.index.tolist())
pal_corrects = set(pd.read_csv(PAL_CORRECT, index_col='index').index.tolist())
p2c_wrongs = set(p2c_wrong_df.index.tolist())  
p2c_corrects = set(pd.read_csv(P2C_CORRECT, index_col='index').index.tolist())
cot_wrongs = set(cot_wrong_df.index.tolist())
cot_corrects = set(pd.read_csv(COT_CORRECT, index_col='index').index.tolist())

correct_d = {
    'cot': cot_corrects,
    'pal': pal_corrects,
    'p2c': p2c_corrects,
}
wrong_d = {
    'cot': cot_wrongs,
    'pal': pal_wrongs,
    'p2c': p2c_wrongs,
}


models = ['pal', 'p2c', 'cot']
with jsl.open('1_onlyone_correct.jsonl', 'w') as writer:
    for m in models:
        idxs = correct_d[m]
        for w in models:
            if w == m: 
                continue
            else: 
                idxs = idxs.intersection(wrong_d[w])
        obj = {'correct': m, 'wrong': list(set(models)-{m}), 'count': len(idxs), 'idxs_test': sorted(list(idxs))}
        writer.write(obj)
    print('wrote to 1_onlyone_correct.jsonl')


