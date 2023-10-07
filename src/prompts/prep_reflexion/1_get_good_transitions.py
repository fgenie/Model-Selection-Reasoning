COT_WRONG="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/cot_wrong.csv"
COT_RIGHT="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/cot_wrong.csv"

PAL_WRONG="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/pal_wrong.csv"
PAL_CORRECT="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/pal_correct.csv"

P2C_WRONG="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0924_plancode_v2_abl/gsm8k_k8_sc1_s0_e1319_09_24_01_16_wrong.csv"
P2C_CORRECT="/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0924_plancode_v2_abl/gsm8k_k8_sc1_s0_e1319_09_24_01_16_correct.csv"

import jsonlines as jsl
import pandas as pd

pal_wrong_df = pd.read_csv(PAL_WRONG, index_col='index')
p2c_wrong_df = pd.read_csv(P2C_WRONG, index_col='index')
cot_wrong_df = pd.read_csv(COT_WRONG, index_col='index')

pal_wrongs = set(pal_wrong_df.index.tolist())
p2c_wrongs = set(p2c_wrong_df.index.tolist())  
cot_wrongs = set(cot_wrong_df.index.tolist())

data = dict(
    pal = [pal_wrongs],
    p2c = [p2c_wrongs],
    cot = [cot_wrongs],
)

df = pd.DataFrame(
    data
)


df = df.apply(lambda x:x[0])
array = df.to_numpy()[None, :] # (1, 3)
x_wrong_y_correct = array - array.transpose() # (3, 3)

df_trans = pd.DataFrame(data = x_wrong_y_correct, index=['pal', 'p2c', 'cot'], columns=['pal', 'p2c', 'cot'])

models = ['pal', 'p2c', 'cot']

with jsl.open('switching_for_wrongtocorrect.jsonl', 'w') as writer:
    for m in models:
        for n in models:
            idxs = df_trans.loc[m, n]
            obj = {'wrong': n, 'correct': m, 'count': len(idxs), 'idxs_test': list(idxs)}
            if m==n:
                print(obj)
            else:
                writer.write(obj)
print(df_trans.apply(lambda x: x.apply(len)))
'''
     pal  p2c  cot  <- wrong
pal    0  189  132
p2c   76    0   98
cot  121  200    0

↑
correct

i.e.
df.loc[row, col] := col is wrong, row is correct
                := switching model from [col] to [row] is desirable
'''
print('wrote to switching_indices.jsonl')
        


