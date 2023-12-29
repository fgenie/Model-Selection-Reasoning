from fire import Fire
import jsonlines as jsl
from tqdm import tqdm 

from portable.llm_query_utils import *

DBG = True

verbT = 0.
codeT = 0.


jslf_2confl = '../dataset/conflict_only/conflictonly_cotpal_gpt4.jsonl'
outjslf = '../dataset/conflict_only/p2c_gpt4_on_conflictonly2.jsonl'
records = list(jsl.open(jslf_2confl))

# if DBG:
#     print(f'{("p2c_generated" in records[0])=}')
#     try:
#         print(f'{records[0]["p2c_generated"] =}')
#     except Exception as e:
#         print(e)

for row in tqdm(records):
    q = row['question']
    codes, plans, querymsg = do_with_tenacity(query_plancode, q, plan_temperature=verbT, 
                                        code_temperature=codeT, 
                                        backbone='gpt4', 
                                        n=1, 
                                        seed=777)
    code = codes[0] # post-processed code returned
    plan = plans[0]
    p2c_ans = safe_execute_turbo(code)
    
    row['p2c_executed'] = p2c_ans
    row['plan'] = [plan]
    row['p2c_generated'] = f'{plan.strip()}\n{code.strip()}'
    row['ansmap']['p2c'] = p2c_ans
    row['solmap']['p2c'] = code.strip()    
    print(plan[:50])
    print(code[:50])
    print(q)
    
    # if DBG:
    #     print(f"{'p2c_executed' in records[0]}, {records[0]['p2c_generated']}, {records[0]['ansmap']['p2c']}, {records[0]['solmap']['p2c']}")
        
    # print()
    
with jsl.open(outjslf, 'w') as writer:
    writer.write_all(records)
    print(outjslf)