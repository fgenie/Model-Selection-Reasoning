import json
from fire import Fire 
import random
import re

def parseout_correct_solution(blurb:str):
    q = re.search('`Question`: (.+)?\n', blurb)
    question = blurb[q.start(): q.end()]
    cs = re.search('`Workaround Method`: (.|\n)+', blurb)
    correct_solution = blurb[cs.start(): cs.end()]
    correct_solution_ = correct_solution.replace('`Workaround Method`: ', '`Method`: ').replace('`Corrected Attempt`: ', '`Attempt`: ')
    # print(question)
    # print(correct_solution_)
    transformed_blurb = f"{question}{correct_solution_}".strip()
    # print(transformed_blurb)
    return transformed_blurb

def main(blurb_f:str = '3_blurb_-1.json',
         include_noreflection:bool=False,
         include_noswitching:bool=False,
         n_repeat:int=1,
         from_back:bool=True, # from longest to shortest (blurb_f sorted in this way, using the solution length)
         outf:str='99_7_rims_cotpal_inference_prompt_k(N)_DEC9.txt',
         ):
    
    outf = outf.replace("(N)", str(n_repeat*2))

    d = json.load(open(blurb_f))
    if from_back:
        d = {k:sorted(v, reverse=True) for k,v in d.items()}
    
    picked_blurbs = dict()
    for k,v in d.items():
        idxs = range(0, len(v), len(v)//n_repeat)[:n_repeat]
        picked_blurbs[k] = [v[i] for i in idxs]
        picked_blurbs[k+"_idxs"] = idxs
    
    

    # mind the indices already used above!
    if include_noreflection:
        outf = outf.replace('99_7_', '99_7_no_refl_')
        # just pick the correct solution and make it into a no-reflection blurbs
        palidx = picked_blurbs['cot2pal_idxs'][len(picked_blurbs['cot2pal_idxs'])//2]-1
        cotidx = picked_blurbs['pal2cot_idxs'][len(picked_blurbs['pal2cot_idxs'])//2]-1
        
        palex = d['cot2pal'][palidx]
        cotex = d['pal2cot'][cotidx]

        pal_norefl = parseout_correct_solution(palex)
        cot_norefl = parseout_correct_solution(cotex)

        picked_blurbs['cot_norefl'] = [cot_norefl]
        picked_blurbs['pal_norefl'] = [pal_norefl]
        
        
    if include_noswitching:
        outf = outf.replace('99_7_', '99_7_no_switch_')
        raise NotImplementedError(f'need to prepare the no_switching case into {blurb_f=} first')
    
    
    # build the prompt with the above
    blurbs = []

    # blurb composition = (noswitch) + reflection + noreflection 
    if include_noreflection:
        blurbs.extend(picked_blurbs['cot_norefl'])
        blurbs.extend(picked_blurbs['pal_norefl'])
    if include_noswitching:
        raise NotImplementedError(f'need to prepare the no_switching case into {blurb_f=} first')
    
    reflection_blurbs = []
    for k,v in picked_blurbs.items():
        if '2' in k and len(k)==7:
            reflection_blurbs.extend(v)
    random.shuffle(reflection_blurbs)
    
    blurbs.extend(reflection_blurbs)

    # finalize by adding system prompt and the instruction
    # system prompt
    sys = '''You are now solving math word problems. You brilliantly detects the errors in the wrong solution and find `Workaround Method` to correct the solution. The methods you are taking are as follows. Each has its strength and weakness:

- Chain of Thought (cot): Solving problem with writing steps of reasoning in a natural language. Might help correct understanding of the problem but this could be weaker in precise computation.
- Program-aided Language Modeling (pal): Using python language to reason and obtain an accurate answer to the given question, but this could be weaker in understanding the problem. 

Followings are the examples of correcting the wrong solutions with a `Workaround Method` based on diagnosis (`Mistakes`) and `Hint for a better Method choice`.'''

    instruction_template = '''Now, try the `Question` below following the same procedure as above. Try the question with the choice of your `Method`, and evaluate the `Answer`. If your `Attempt` is considered wrong, identify the `Mistakes` and reason to take `Workaround Method` by writing `Hint for a better Method choice`. Based on it, reattempt correctly on `Corrected Attempt`.

`Question`: [QUESTION]
`Method`: <your first choice how to approach>
`Attempt`: <your first attempt to solve> 
`Answer`: <answer from the attempt>
`Evaluation`: <evaluate your answer. If your answer evaluates wrong, start re-attempting with identifying `Mistakes`. Otherwise, stop solving and finish>'''

    blurbs = [sys] + blurbs + [instruction_template]
    prompt = "\n\n\n".join(blurbs)
    
    with open(outf, 'w') as f:
        f.write(prompt)
        print('wrote the prompt to', outf)


if __name__ == "__main__":
    Fire(main)  