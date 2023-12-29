from fire import Fire
import jsonlines as jsl
from tqdm import tqdm 
import pandas as pd 

from portable.llm_query_utils import *

DBG = True

jslf = '../dataset/conflict_only/p2c_gpt4_on_conflictonly2.jsonl'
confl_jslf = '../dataset/conflict_only/gpt4_3method_conflicts.jsonl'
nonconfl_jslf = '../dataset/gpt4_3method_nonconflicts.jsonl'
records = list(jsl.open(jslf))
df = pd.DataFrame(records)


df['concordant_ans'] = df.ansmap.apply(lambda d: get_concordant_answer(list(d.values())))
conflict_mask = df.concordant_ans.isna()
df_confl = df[conflict_mask]
df_nonconfl = df[~conflict_mask]

print(f"{df.shape=}")
print(f"{df_confl.shape=}")    
print(f"{df_nonconfl.shape=}")    
    
    
with jsl.open(confl_jslf, 'w') as confl_wr, jsl.open(nonconfl_jslf, 'w') as nonconfl_wr:
    confl_wr.write_all(df_confl.to_dict(orient='records'))
    nonconfl_wr.write_all(df_nonconfl.to_dict(orient='records'))
    
    