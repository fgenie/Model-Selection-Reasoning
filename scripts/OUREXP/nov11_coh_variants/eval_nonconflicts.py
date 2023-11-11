import subprocess as sb
from pathlib import Path

outroot = "../output/nov11_tgt_conflicts/"
paths = list(Path(outroot).glob("**/noconflict_gsm8k*.jsonl"))

for jslf in paths:
    cmd = f'bash eval_an_outjsl.sh {jslf}'
    print(cmd)
    sb.call(cmd, shell=True)




