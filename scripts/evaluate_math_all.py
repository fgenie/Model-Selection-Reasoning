import subprocess as sb
from pathlib import Path


EXEHOME='/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src'

EXP2PATH = {'0831': ['/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/chatgpt_cot_pal/gsm8k_sc1_s0_e1319_08_31_00_19.jsonl' ],
'0903': [
'/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/0903_result/k5.jsonl' ,
'/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/0903_result/baseline.jsonl' ,
'/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/0903_result/k2.jsonl' ,
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
'/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct14_actorselect_hinted_chatgpt/gsm8k_k8_sc1_s0_e1319_10_14_23_49.jsonl' ,
'/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct14_actorselect_hinted_palcot_chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_09_12.jsonl' ,
'/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct15_actorselect_verbose/chatgpt/gsm8k_k8_sc1_s0_e1319_10_16_11_22.jsonl' ,
'/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct15_actorselect_cotpal_verbose/chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_23_46.jsonl' ,
],
'oct19 enhanced coh':
[
'/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct19_enhanced_coh/chatgpt/gsm8k_k3.jsonl' ,
'/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct19_enhanced_coh_another/chatgpt/gsm8k_k4_sc1_s0_e1319_10_20_21_16.jsonl',
'/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/oct19_enhanced_coh/chatgpt/gsm8k_k6.jsonl', 
],}
with open('oct19_all_results_report.txt', 'w') as f:
    for expname, paths in EXP2PATH.items():
        print(expname, file=f)
        print("===================================", file=f)
        for p in paths:
            cmd = f"python evaluate.py --input_path {p} --dataset_type 'math'"
            print(f"{Path(p).parent}/{Path(p).stem}", file=f)
            res = sb.run(cmd, shell=True, cwd=EXEHOME, capture_output=True, text=True)
            print(res.stdout, file=f)
        print("===================================\n\n", file=f)
        
print('wrote to oct19_all_results_report.txt')