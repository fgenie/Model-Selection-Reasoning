import yaml 
from typing import Sequence, Mapping, Any, Union, Callable
PLAN_F = '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src/prompts/prompts_plan.yaml'
CODE_F = '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src/prompts/prompts_code.yaml'
import openai
KEY = open('/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/openai_key.txt').read().strip()
PLAN_PROMPTS_D= yaml.full_load(open(PLAN_F))
CODE_PROMPTS_D = yaml.full_load(open(CODE_F))


def get_plan_prompt(data: dict, k_fewshot:int=0)->str:
    '''
    prep prompt for plan generation
    '''
    prompt_d = PLAN_PROMPTS_D
    
    q = data['question']
    system = prompt_d['system_msg']
    user_tmp = prompt_d['user_template'] if k_fewshot==0 else prompt_d['user_template_fewshot']
    fewshots = prompt_d['fewshots'][:k_fewshot] # list of fewshot strings include </end> tag included.
    fewshots_concat = "\n\n".join(fewshots)
    assistant_start = prompt_d['assistant_start']


    user = user_tmp.replace('{NEWLINE2_FEWSHOTS}', fewshots_concat).replace('{QUESTION}', f"Question: {q}")
    assistant = assistant_start

    # print(system)
    # print(user)
    # print(assistant)
    # print(k_fewshot)
    # print()
    
    msgs = [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': user},
        {'role': 'assistant', 'content': assistant}
    ]
    return msgs
    
    
def get_plan2code_prompt(data:dict, plan:str='', k_fewshot:int=0, custom_idxs:list=None):
    # little bit revision from PAL prompt.
    # `solution()` is returned (can execute with solution() call w/o argument
    q = data['question']
    prompt_d = CODE_PROMPTS_D
    system = prompt_d['system_msg']
    user_tmp = prompt_d['user_template'] if k_fewshot==0 else prompt_d['user_template_fewshot']
    assistant = prompt_d['assistant_start']
    if custom_idxs is None:
        fewshots = prompt_d['fewshots'][:k_fewshot] # list of fewshot strings include </end> tag included.
    else:
        fewshots = [prompt_d['fewshots'][i] for i in custom_idxs]
    fewshots_concat = "\n\n".join(fewshots)

    user = user_tmp.replace('{QUESTION}', f"Question: {q}")
    user = user.replace('{NEWLINE2_FEWSHOTS}', fewshots_concat)
    assistant = assistant.replace('{PROCESSEDPLAN}', add_indents2plan(plan)) 
    # print(system)
    # print(user)
    # print(assistant)
    # print(k_fewshot)
    # print()

    msgs = [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': user},
        {'role': 'assistant', 'content': assistant}
    ]
    # if k_fewshot>0:
    #     msgs = msgs[:2] # do not force assistant head. it invokes repeated definition of solution() # dunno why...
    # this is ridiculous. I need to pass the plan explicitly to the code generator.


    return  msgs

def add_indents2plan(plan:str)->str:
    indent = " "*4
    plan_ = plan.split("\n")
    plan__ = [indent+p for p in plan_ if p!='</end>'] # remove </end> if exists
    processed = "\n".join(plan__)
    processed = f"\n{processed}\n" #+ indent #added at postprocess
    return processed

def postprocess_plan(rawanswer:str):
    lines = [l for l in rawanswer.split('\n') if '</end>' not in l]
    if len(lines)>=1:
        plan_ = "\n".join(lines)
    else:
        print('plan gen failed')
        print(f"{rawanswer=}")
        plan_ = ''
    return plan_

def postprocess_code_answer(rawanswer:str, docdef:str='', k_fewshot:int=0):
    try:
        # removing starting wrap ```
        if "```python" in rawanswer:
            code = rawanswer.split("```python")[-1]
        elif rawanswer.startswith('```'):
            rawanswer = rawanswer.split('```')[-1]
        # removing ``` at the end
        code = rawanswer.split("```")[0] #ending ``` removal
        # remove possible starting repetition # solution in Python:\n\n\n
        code = code.replace('# solution in Python:\n\n\n', '')
        if k_fewshot>0: # just use output do not modif
            if code.startswith('def solution():'):
                pass
            else:
                code = docdef + '\n' + (code if code.startswith('\t') else f"\t{code}")
        code = remove_prints(code)
        exec(code) # check if it is executable
    except: 
        print('code gen fails (unexecutable or funcname?)')
        print(f"code:\n{rawanswer}")
        code = ''
    return code

def remove_prints(code:str)->str:
    lines = code.split("\n")
    lines_ = [l if not l.startswith('print(') else l.replace('print(', '# print(') for l in lines]
    code_ = "\n".join(lines_)
    return code_


def make_code_examples()->Sequence[str]:
    def parse_fewshot2q_plan(txt):
        lines = txt.strip().split("\n")
        q = lines[0] 
        assert q.startswith('Question:')
        
        planlines = []
        start = lines.index('Suggestion:')+1
        for i in range(start, len(lines)):
            if lines[i].startswith('</end>'):
                break
            planlines.append(lines[i])
        plan = "\n".join(planlines)
        return q, plan

    

    prompt_d = yaml.full_load(open(PLAN_F))
    fewshots = prompt_d['fewshots']

    code_fewshots = []
    
    for shot in fewshots:
        q, plan = parse_fewshot2q_plan(shot)
        indent=" "*4
        docstring_def = f'def solution():\n{indent}"""{add_indents2plan(plan)}"""'
        qd = {'question': q}
        cprompt0 = get_plan2code_prompt(qd, plan=plan)
        if 'solution' in globals():
            del globals()['solution']
        while 'solution' not in globals():
            resp = openai.ChatCompletion.create(api_key=KEY,
                                model='gpt-3.5-turbo',
                                max_tokens=1024,
                                stop='</end>',
                                messages=cprompt0,
                                temperature=0,
                                top_p=1.0,
                                n=1)
            code = resp['choices'][0]['message']['content']
            # try: 
            codeonly = postprocess_code_answer(code, docdef=docstring_def)
            exec(codeonly, globals())
            # verify answer of the question
            # except:
            #     print(f'retrying (not a code)\n{code=}\n{codeonly=}')
        
        # print(code)
        # pack fewshots into list
        code_shot = f"{q}\n# solution in Python:\n\n\n{codeonly}"
        code_fewshots.append(code_shot)
        print('completed_fewshots')
        for fs in code_fewshots:
            print(fs)
    return code_fewshots
 
def kvprint(record):
    for r in record:
        print(r['role'])
        print(r['content'])


if __name__ == '__main__':
    prompt_dd = yaml.full_load(open('prompts_code.yaml'))
    print()

    data = {"question": "Question: What do you do for a living?"}
    pp2 = get_plan_prompt(data, k_fewshot=2)
#     pp3 = get_plan_prompt(data, k_fewshot=5)
    plan = '''1. Check how much money Olivia had at first, and store it into some variable.
2. She's consuming it to buy bagels. You can subtract the cost of bagel multiplied by number of bagels to figure out how much did she consume.
3. Subtract the cost from initial deposit.
4. Return the calculated number.
# </end>'''
    cp2 = get_plan2code_prompt(data, plan=plan, k_fewshot=2)
    print("===========")
    kvprint(pp2)
    print("===========")
    kvprint(cp2)
    print("===========")