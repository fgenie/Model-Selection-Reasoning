from pathlib import Path
import subprocess as sb



for dataset in ['svamp', 'multiarith']:
    for backbone in ['chatgpt', 'gpt4']:
        if backbone =='chatgpt' and dataset == 'svamp':
            continue # done
        cmd = f"""python 99_run_inference.py baseline_inference \\
                    --backbone {backbone} \\
                    --gsm_jslf ../../dataset/{dataset}.jsonl
                    """
        print(cmd)
        sb.call(cmd, shell=True)

