import subprocess as sb
from pathlib import Path

outroot = "/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/nov11_tgt_conflict"
paths = list(Path(outroot).glob("**/noconflict_gsm8k*.jsonl"))
print(paths)

for jslf in paths:
    cmd = f'bash eval_an_outjsl.sh {jslf}'
    print(cmd)
    sb.call(cmd, shell=True)




'''

## nonconflicts 

### chatgpt

| total\=1319 | n_nonconflict | correct | 
|-|-|-|-|
| 3models | 1158 | 1049 (pal-0.45\%p, cot+1.10\%p, p2c+5.61\%p) | 
| 2models |  |  |

### gpt4

| total\=1319 | n_nonconflict | nonconfl_correct | 
|-|-|-|
| 3models | 1304 | 1255 (palonly+0.83\%p) |
| 2models | 1244 | 1215 (palonly-2.20\%p) |

'''