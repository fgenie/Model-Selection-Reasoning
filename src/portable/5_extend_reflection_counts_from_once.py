'''
using the reflectonce prompt, prep the followings


blurbs per each method:
- reflection*0
- reflection*1
- reflection*2

prompts:
- reflection0 + 1 + 2 (+ordering)
    - 012
    - 021
    - 210
    - ...
- 

if possible, I want every method at least once to be presented as a correct approach (no bias for any method)
but not sure this is really a thing...?

- balanced vs biased
'''

from pathlib import Path
import random
random.seed(777)
import json

import jsonlines as jsl
from tqdm import tqdm 

from llm_query_utils import * # query_rims_prompt, PromptStr(class), etc.


CONTINUE_WRITING_INVOKE_PROMPT = "Continue reaching to the correct answer, carefully following the format presented above."
N_EXTEND_TRIALS = 5 #
TEMP = 1.
BLURB_F = '5_extend_reflection_blurbs.json'



# reflect once prompts
reflect_once = list(Path().glob("4_ablate_3_reflectonce_*.txt"))    

# each prompt will be used for extending blurb it contains 
train_samples = list(jsl.open('gsm8k_train.jsonl'))


# helpers  
def did_reflect(response:str)->bool:
    return '`Attempt 2`:' in response

def is_correct(pred:float, gt:float)->bool:
    return abs(pred-ans)<1e-3


# gather extended blurbs from training set (using the reflectonce prompt)
collected_blurbs = dict()
for pf in tqdm(reflect_once, desc=pf.stem):
    random.shuffle(train_samples)
    
    collected = {
        'cot': [],
        'pal': [],
        'p2c': [],
        'extend': []
    }
    for row in tqdm(train_samples, desc= "  ".join([f"{k}:{len(v)}/1" for k,v in collected.items()]) ):
        # if finish gathering all, break
        if set( [len(v) for v in collected.values()] ) == {1}:
            break

        # left things to gather
        question = row['question']
        gt = float(row['ans'])
        # check if the question already in the prompt
        if question in pf.open().read().strip():
            print(pf.open().read().strip())
            continue
        # query rims inference
        eval_friendly_d, __, raw_query_out, _ = query_rims_inference(question, pf, backbone='gpt4turbo', temperature=TEMP)
        if not raw_query_out.strip().split("\n")[-1].startswith('`Answer '):
            continue # rims inference failed to stop at Evaluation: Correct 
        pred = eval_friendly_d['good_ans']
        
        # chance to extend the blurb
        if not is_correct(pred, gt) and did_reflect(raw_query_out):
            if collected['extend']:
                continue # already done
            # extending blurb
            blurb_1_refl = f"`Question`: {question}\n{raw_query_out.strip()}"
            gpt_messages = [
                {'role': 'assistant', 'content': raw_query_out.strip()},
                {'role': 'user', 'content': CONTINUE_WRITING_INVOKE_PROMPT}
            ]

            eval_friendly_ds, parse_dds, raw_query_outs, _ = query_rims_inference(question, pf, backbone='gpt4turbo', temperature=TEMP, n=N_EXTEND_TRIALS, continue_writing_gpt_messages=gpt_messages)
            
            for i, d in enumerate(eval_friendly_ds):
                newpred = d['good_ans']
                if newpred == pred: # this will filter "only generating `Evaluation`: Correct" case
                    continue
                else:
                    if is_correct(new_pred, gt):
                        toappend = raw_query_outs[i]
                        extended = f"{blurb_1_refl.strip()}\n{toappend.strip()}\n`Evaluation`: Correct"
                        collected['extend'].append(extended)
                        break # only one extended blurb per prompt. added. finished for this prompt.
            
        # chance to gather one-shot correct question     
        elif is_correct(pred, gt) and not did_reflect(raw_query_out):
            # gather one-shot blurb
            if collected['cot'] and collected['pal'] and collected['p2c']:
                continue
            blurb_1 = f"`Question`: {question}\n{raw_query_out.strip()}\n`Evaluation`: Correct"
            method = eval_friendly_d['good_method']
            collected[method].append(blurb_1)
        else: # other cases, pass
            # did not reflect, wrong 
            # did reflect, correct
            continue 
    collected_blurbs[pf.name] = collected        
# save the blurb collected with promptfile watermark 
with open(BLURB_F, 'w') as jf:
    json.dump(collected_blurbs, jf, indent=4, ensure_ascii=False)
    print(f'{BLURB_F}')

# augment the prompt with collected blurbs 
# 1 extended only 

# 2 oneshot + extended 
    
# 3 oneshot + extended + original