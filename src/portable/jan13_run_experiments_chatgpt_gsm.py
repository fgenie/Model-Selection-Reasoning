from pathlib import Path
import subprocess as sb
import jsonlines as jsl



# run baseline gsm
cmd = 'python 99_run_inference.py baseline_inference --backbone chatgpt --gsm_jslf /Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/dataset/gsm8K_test.jsonl --start_idx 474'
print(cmd)
sb.call(cmd, shell=True)


# separate chatgpt gsm result: conflict only
chatgpt_gsm_conflicts_only_f = '../../dataset/conflict_only_gsm_chatgpt_jan14.jsonl'

INFERRED_F = '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/dataset/gsm8K_test_model_selection_baseline/chatgpt_*_model_selection3.jsonl'
conflict_only_records = []
inferred_f_wildcard = Path(INFERRED_F)
fs = list(inferred_f_wildcard.parent.glob(inferred_f_wildcard.name))
records_lst = [list(jsl.open(f)) for f in fs]
records = []
for r in records_lst:
    records.extend(r)   
    

for row in records:
    # just in case majority_vote==False
    if 'majority_vote' in row['selection_or_rims'] and not row['selection_or_rims']['majority_vote']:
        conflict_only_records.append(row)
    elif 'error' in row['selection_or_rims'] or 'majority_vote' not in row['selection_or_rims']:
        conflict_only_records.append(row)
    elif row['majority_ans'] is None:
        conflict_only_records.append(row)
with jsl.open(chatgpt_gsm_conflicts_only_f, 'w') as writer:
    writer.write_all(conflict_only_records)
    print(f'wrote to {conflict_only_records}')



# run rims on conflicts only
backbone2confl_jsl = {
    'chatgpt': {
        'gsm8k': chatgpt_gsm_conflicts_only_f,
        # 'multiarith': confl jslf
    },
}


prompt_files = list(Path().glob('*.txt_rm_ans'))
cmds = []
for bb, dd_jslf in backbone2confl_jsl.items():
    for dd, jslf in dd_jslf.items():
        for f in prompt_files:
            cmd = f"""python 99_run_inference.py rims_inference \\
                        --prompt_f {str(f)} \\
                        --backbone {bb} \\
                        --gsm_jslf {jslf}
                        """
            cmds.append(cmd)
for i, c in enumerate(cmds):
    print(c)
    sb.call(c, shell=True)


# run evaluation
cmd_eval = 'python evaluate_all_chatgpt_gsm.py'
print(cmd_eval)
sb.call(cmd_eval, shell=True)