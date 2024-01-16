from pathlib import Path
import subprocess as sb

# run rims and baseline on conflict only (gpt-4)
prompt_files = Path().glob('*.txt_rm_ans')
cmds = []
for f in prompt_files:
    cmd = f"""python 99_run_inference.py rims_inference \\
                --prompt_f {str(f)} \\
                --backbone gpt4 \\
                --eval_indiv_method \\
                --gsm_jslf ../../dataset/conflict_only/3methods_exp/gpt4_3method_conflicts.jsonl
                """
    cmds.append(cmd)
cmds_ = [c.replace('--eval_indiv_method', '') for c in cmds]
cmds += cmds_

for c in cmds:
    print(c)
    sb.call(c, shell=True)


# run baseline (3model) on full dataset
# 1. gsm (chatgpt)
# 2. svamp (chatgpt, gpt4)

datasets = ["../../dataset/gsm8K_test.jsonl", "../../dataset/svamp.jsonl"]

for full_dataset in datasets:
    for backbone in ['chatgpt', 'gpt4']:
        if backbone == 'chatgpt' and ('gsm8K' in full_dataset):
            continue
        cmd = f"""python 99_run_inference.py baseline_inference \\
                    --backbone {backbone} \\
                    --gsm_jslf {full_dataset}
                    """
        print(cmd)
        sb.call(cmd, shell=True)

'''
# model-selection-resoning baseline
python 99_run_inference.py  baseline_inference \ 
                --dbg \
                --backbone chatgpt \
                --gsm_jslf ../../dataset/dbg.jsonl 


# rims algorithm run
python 99_run_inference.py  rims_inference  \ 
                --prompt_f  3_reflectonce_cot2p2c.pal2cot.pal2p2c.txt_rm_ans  \
                --dbg  \
                --eval_indiv_method  \
                --backbone  gpt4turbo  \ 
                --gsm_jslf ../../dataset/dbg.jsonl '''