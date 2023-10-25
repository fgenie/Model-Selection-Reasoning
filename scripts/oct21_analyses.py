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
'0831': ['/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/chatgpt_cot_pal/gsm8k_sc1_s0_e1319_08_31_00_19.jsonl' ], # 
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
}


def method_dist(df):
    if 'reasoning_method' in df.columns: # for actor selection
        if df.iloc[0].reasoning_method in ['cot', 'pal', 'p2c']:
            return df.reasoning_method.value_counts()
    elif 'actual_method' in df.columns: # for coh
        return df.actual_method.value_counts()
    else: # manual check -- model selections
        mask = df.choice_solution.apply(lambda x: len(x)>0)
        mask = abs(df.cot_executed.sub(df.majority_ans)) < 1e-3
        
        
    
def method_success_rate(df):
    return 
# get success rate / distribution
# 0831: model selection full, <-- greedy too. according to the commit history
# 0903: model selection subset, greedy
# oct14* actor selection 
interests = [
    '0831',
    '0903',
    'oct 14 actor selection',
]

# xl = pd.ExcelWriter('oct21_selection_analyses.xlsx')

for k, jslf in exp_of_interests.items():
    if k in interests:
        # name experiment
        if k == '0831':
            name = 'nongreedy_model_selection'
        elif k == '0903':
            name = 'greedy_model_selection'
        elif k == 'oct 14 actor selection':
            name = Path(jslf).parent.name.replace('oct14_', '').replace('oct15_', '')
        
        df = pd.DataFrame(jsl.open(jslf))
        dist = method_dist(df)
        success_rate = method_success_rate(df)
        


# solution이 어떻게 다른지 비교
# coh - standard prompting (ablation)
# coh-gpt3.5-16k v coh-gpt3.5
# p2c_v1, p2c_v2, p2c_coh


# numbers from ablation
# numbers from model selection