import pandas as pd
import jsonlines as jsl
from pathlib import Path
import numpy as np


'''
Measure success rate of the previous experiments
- 0903: model selection with p2c_v1 + cot
- 0831: model selection with pal + cot

success rate = when queried for selection, ratio that the selected method correctly answers the question
'''


exp_of_interests = {
'0831': [
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/chatgpt_cot_pal/gsm8k_sc1_s0_e1319_08_31_00_19.jsonl' ], # 
'0903': [
    # '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/0903_result/k5.jsonl',
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/0903_result/baseline.jsonl',
    # '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/0903_result/k2.jsonl',
    ],

'0910 ablation': [
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/0910_ablation_result/cot.jsonl' ,
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/0910_ablation_result/plancode.jsonl' ,
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/0910_ablation_result/pal.jsonl' ,
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0924_plancode_v2_abl/gsm8k_k8_sc1_s0_e1319_09_24_01_16.jsonl' ,
    ],

'oct14 actor selection ': [
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct14_actorselect_chatgpt/gsm8k_k8_sc1_s0_e1319_10_14_23_48.jsonl' ,
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct14_actorselect_palcot_chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_09_13.jsonl' ,
    # '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct14_actorselect_hinted_chatgpt/gsm8k_k8_sc1_s0_e1319_10_14_23_49.jsonl' ,
    # '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct14_actorselect_hinted_palcot_chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_09_12.jsonl' ,
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct15_actorselect_verbose/chatgpt/gsm8k_k8_sc1_s0_e1319_10_16_11_22.jsonl' ,
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct15_actorselect_cotpal_verbose/chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_23_46.jsonl' ,
    ],
'oct19 enhanced coh':
    [
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct19_enhanced_coh/chatgpt/gsm8k_k3.jsonl' ,
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct19_enhanced_coh_another/chatgpt/gsm8k_k4_sc1_s0_e1319_10_20_21_16.jsonl',
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct19_enhanced_coh/chatgpt/gsm8k_k6.jsonl', 
    ],
'oct27_onlyconflict':[
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct27_onlyconflict/chatgpt/gsm8k_k8_sc1_s0_e1319_10_27_22_00.jsonl',
    '../output/oct27_only_conflict/coh_cotpal/chatgpt',
    '../output/oct27_only_conflict/coh_cotpal_1/chatgpt',
    ],
'oct27_rerun_baseline': [
        '../output/oct27_rerun_baseline/chatgpt/gsm8k*.jsonl',
    ],
}


def method_dist(df):
    '''
    `method choice distribution`
    - when queried for model selection
    - when queried for actor selection
        - only conflict
        - fully done
    - when queried for coh selection and solution 
        - only conflict
        - fully done
    '''
    if 'reasoning_method' in df.columns: # for actor selection
        if df.iloc[0].reasoning_method in ['cot', 'pal', 'p2c']:
            return df.reasoning_method.value_counts()
    elif 'actual_method' in df.columns: # for coh
        return df.actual_method.value_counts()
    else: # manual check -- model selections
        mask = df.choice_solution.apply(lambda x: len(x)>0)
        mask = abs(df.cot_executed.sub(df.majority_ans)) < 1e-3
        
        
    
def method_success_rate(df):
    '''
    `when some method chosen, how often it gets correct answer?`
    - ablations
    - when queried for model selection
    - when queried for actor selection
        - only conflict
        - fully done
    - when queried for coh selection and solution 
        - only conflict
        - fully done
    '''
    # rerun base has no is_correct --> (answer - majority_ans).abs()<1e-3
    #   compare with base old (0831)
    method_success_rate()


    # actor selection
    # oct26 actor onlyconflict: choice_selection[0] == actual method 
    method_dist()

    return 



def main():
    