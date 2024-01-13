import jsonlines as jsl
import pandas as pd

from pathlib import Path

PREF = 'conflictonly_'
FILES = [
    "/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/dataset/svamp_model_selection_baseline/chatgpt_merged_model_selection3.jsonl",
    "/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/dataset/svamp_model_selection_baseline/gpt4_merged_model_selection3.jsonl"
]


for record_f in FILES:
    conflict_only_records = [] 
    records = list(jsl.open(record_f))

    for row in records:
        # just in case majority_vote==False
        if 'majority_vote' in row['selection_or_rims'] and not row['selection_or_rims']['majority_vote']:
            conflict_only_records.append(row)
        elif 'error' in row['selection_or_rims'] or 'majority_vote' not in row['selection_or_rims']:
            conflict_only_records.append(row)
            
        
    
    newf = Path(record_f).parent/f"{PREF}_{Path(record_f).name}"
    with jsl.open(newf, 'w') as wf:
        wf.write_all(conflict_only_records)
        print(newf)        
            
