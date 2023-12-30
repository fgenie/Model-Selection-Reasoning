from pathlib import Path
import re 

modifprompts = list(Path().glob('modif_*rims*.txt'))
print(modifprompts)

newfs = [str(f).replace('modif_', 'rm_ans_') for f in modifprompts]

def erase_answer_hinting(prompt:str)->str:
    ptn = r'\(correct answer: [0-9]+[\.]*[0-9]*\)'
    matches = re.findall(ptn, prompt)
    [print(m) for m in matches]
    # print()
    for txt in matches:
        prompt = prompt.replace(txt, "")
    return prompt

for f, nf in zip(modifprompts, newfs):
    prompt = open(f).read().strip()
    newp = erase_answer_hinting(prompt)
    with open(nf, 'w') as wf:
        wf.write(newp)
        print(nf)
    
    