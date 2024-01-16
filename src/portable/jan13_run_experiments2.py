from pathlib import Path
import subprocess as sb

# # run rims and baseline on conflict only (gpt-4)
backbone2confl_jsl = {
    'chatgpt': {
        'svamp': '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/dataset/svamp_model_selection_baseline/conflictonly__chatgpt_merged_model_selection3.jsonl',
        # 'multiarith': confl jslf
    },
    'gpt4': {
        'svamp': "/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/dataset/svamp_model_selection_baseline/conflictonly__gpt4_merged_model_selection3.jsonl",
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
    if i<14:
        print('already done')
        continue
    sb.call(c, shell=True)


