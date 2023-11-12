import subprocess as sb
from pathlib import Path

outroot = "/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/nov11_tgt_conflict"
paths = list(Path(outroot).glob("**/tgt_conflict*_gsm*.jsonl"))

for jslf in paths:
    if 'unfinished' in str(jslf):
        pass
    else:
        cmd = f'bash eval_an_outjsl.sh {jslf}'
        print(cmd)
        sb.call(cmd, shell=True)