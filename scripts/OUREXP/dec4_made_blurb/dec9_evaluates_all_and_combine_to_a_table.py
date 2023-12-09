import numpy as np
from pathlib import Path 
import jsonlines as jsl
import pandas as pd 

ROOT='../../../dataset/conflict_only'
NONCONF = np.array((1218, 1246)) # num corrects, num total 

# CONF = np.array( [n_correct, 73])

# directories to score the num_corrects over conflict only examples
dirs = list(Path(ROOT).glob("*/tgt_conflict_*.jsonl"))

def count_corrects(record):
    df = pd.DataFrame(record)
    # reflect / nonreflect
    df_reflect = df [ df.reattempt.apply(lambda x: x['did_reflect'] ) ] 
    df_nonreflect = df[ df.reattempt.apply(lambda x: not x['did_reflect'] ) ]
    
    # count_corrects
    correct_refl = df_reflect['ans==majority_ans'].sum(), len(df_reflect)
    correct_nonrefl = df_nonreflect['ans==majority_ans'].sum(), len(df_nonreflect)

    c_refl, c_nonrefl = map(np.array, [correct_refl, correct_nonrefl])
    
    return c_refl, c_nonrefl

def array2readable(array):
    correct, total = array 
    return f"{int(correct)}/{int(total)} ({100*(correct/total):.2f}\%)"



conf2records = {dir.parent.name: list(jsl.open(dir)) for dir in dirs}
to_table = []
for prompt, record in conf2records.items():
    reflect, nonreflect= count_corrects(record)
    # reflect, nonreflect = np.array([correct:int, total:int])
    # justfailure = int 
    to_table.append( {'name': prompt, 'total': NONCONF+reflect+nonreflect, 'conflict_only': reflect + nonreflect, 'reflect': reflect, 'nonreflect': nonreflect, 'justfailed': 73-nonreflect[1]-reflect[1]} )

table = pd.DataFrame(to_table)
for col in ['total', 'conflict_only', 'reflect', 'nonreflect']:
    table[col] = table[col].apply(array2readable)


with open('dec9_results_table.md', 'w') as f:
    print(table.to_markdown(), file=f)
print('wrote to \n\tdec9_results_table.md')