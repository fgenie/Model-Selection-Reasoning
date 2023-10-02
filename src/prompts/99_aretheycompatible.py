COT_F="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/cot_wrong.csv"

PAL_F="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/pal_wrong.csv"

P2C_F="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0924_plancode_v2_abl/gsm8k_k8_sc1_s0_e1319_09_24_01_16_wrong.csv"

import pandas as pd

pal_wrong_df = pd.read_csv(PAL_F, index_col='index')
p2c_wrong_df = pd.read_csv(P2C_F, index_col='index')
cot_wrong_df = pd.read_csv(COT_F, index_col='index')

pal_wrongs = set(pal_wrong_df.index.tolist())
p2c_wrongs = set(p2c_wrong_df.index.tolist())  
cot_wrongs = set(cot_wrong_df.index.tolist())

print(f"pal: {len(pal_wrongs)}")
print(f"p2c: {len(p2c_wrongs)}")
print(f"cot: {len(cot_wrongs)}")

print(f"{len(pal_wrongs.intersection(p2c_wrongs))=}")
print(f"{len(pal_wrongs.intersection(cot_wrongs))=}")
print(f"{len(p2c_wrongs.intersection(cot_wrongs))=}")

print(f"{len(pal_wrongs.intersection(p2c_wrongs).intersection(cot_wrongs))=}")


'''
While preparing the reflexion-kshot-harvesting prompt, I report some numbers we can expect from the previous ablations.

Our kshot-harvesting agent needs a prompt that invokes a decision from the followings.

For better solution the agent should...
- switch the model (e.g. cot -> pal)
- retry the model (e.g. cot -> cot)

To prepare the prompt, I've explored ablation (single-modeled results) on gsm8k (to see realistic cases for model switching)


(condition chatgpt, greedy sampling, standard few-shot prompts for gsm8k)

> When greedily decoded, how many each models get wrong over 1319 questions?

pal: 268
p2c: 381
cot: 279

> Do they fail on the same questions? no
len(pal_wrongs.intersection(p2c_wrongs))=192
len(pal_wrongs.intersection(cot_wrongs))=147
len(p2c_wrongs.intersection(cot_wrongs))=181

> What is the lowerbound of the error rate using three models above optimally? 9.02% (=119/1319)
len(pal_wrongs.intersection(p2c_wrongs).intersection(cot_wrongs))=119


'''

