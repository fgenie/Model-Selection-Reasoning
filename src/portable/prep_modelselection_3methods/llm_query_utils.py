'''
- NEED: rims prompt post processing (for gsm)
'''
from tenacity import retry, wait_chain, wait_fixed
import openai
import func_timeout
import yaml

from itertools import combinations 
import re


import sys
from pathlib import Path

# Get the absolute path of the current script
THIS_PARENT = Path(__file__).parent.resolve()


sys.path.append(str(THIS_PARENT))
import math_prompt
sys.path.remove(str(THIS_PARENT))

# Construct the path to the openai_key.txt file
key_file_path = THIS_PARENT/'openai_key.txt'

# Read the API key from the file
openai.api_key = open(key_file_path).read().strip()




### almost same to string.Template, but with custom delimiter ( [QUESTION] == ${QUESTION}, to avoid `$` used frequently in price-related questions )
class PromptStr(str): 
    def __init__(self, template_str):
        super().__init__()
        self += template_str  

    def sub(self, 
            placeholder_name:str, 
            tobe:str):
        return PromptStr(self.replace(f"[{placeholder_name}]", str(tobe)))

    def get_placeholder_names(self) -> list:
        return re.findall(r"\[(.*?)\]", self)



### llm query functions ###
def query_cot(question:str, 
              cot_temperature: float, 
              backbone: str, 
              n=1, 
              seed=777):
    '''
    This function is used to query OpenAI for CoT solutions.

    Args:
        data: a dict containing the question and answer
        key: the OpenAI API key
        cot_temperature: the temperature used in CoT
        backbone: ChatGPT or GPT-4

    Returns:
        completions: a list containing the CoT solution
    '''
    query_message = get_cot_prompt(question, backbone=backbone)
    if backbone == 'gpt4':
        model_name = 'gpt-4'
    elif backbone == 'gpt4turbo':
        model_name  = 'gpt-4-1106-preview'
    elif backbone == 'chatgpt':
        model_name = 'gpt-3.5-turbo'

    completions = []
    cot_solution = openai.ChatCompletion.create(
            # api_key=key,
            model=model_name,
            max_tokens=500,
            stop='\n\n\n',
            messages=query_message,
            temperature=cot_temperature,
            top_p=1.0,
            seed=seed,
            n=n)
    if n ==1 :
        completions = [cot_solution['choices'][0]['message']['content']]
    else:
        completions = [cot_solution['choices'][i]['message']['content'] for i in range(n)]
    return completions, query_message


# actual llm query function for p2c method
def _query(#key, 
           model_name:str='gpt-3.5-turbo', max_tokens:int=2048, stop:str=None, messages=None, temperature=0., top_p=1.0, n=1, mode='plan', seed=777): # mode = plan or code
    resp = openai.ChatCompletion.create(# api_key=key,
                                model=model_name,
                                max_tokens=max_tokens,
                                stop=stop,
                                messages=messages,
                                temperature=temperature,
                                top_p=top_p,
                                n=n, seed=seed)
    if n ==1:
        content = resp['choices'][0]['message']['content'] # str
        if mode == 'plan':
            plan = postprocess_plan(content) # it will complain when failing
            return plan
        elif mode == 'code':
            code = postprocess_code(content)
            return code 
    else: # n>1
        contents = [ch['message']['content'] for ch in resp['choices']]
        postprocess = postprocess_plan if mode=='plan' else postprocess_code
        res_strs = [postprocess(c) for c in contents]
        return res_strs


# p2c: querying plan and code separately inside
def query_plancode(question:str,#data: dict, 
                   plan_temperature: float=.0, 
                   code_temperature: float=.0, 
                   backbone: str='gpt-3.5-turbo', 
                   n=1, 
                   seed:int=777):
    '''
    PAL variant: 1. generate planning for the given question 2. based on 1, generate code like PAL does.

    args:
        mostly same arguments with `query_pal()` below
    returns: 
        [list of codes], [list of plans (1)], {codequery: str, planquery: str}
    '''
    # specify model
    if backbone == 'gpt4':
        model_name = 'gpt-4'
    elif backbone == 'gpt4turbo':
        model_name = 'gpt-4-1106-preview'
    elif backbone == 'chatgpt':
        model_name = 'gpt-3.5-turbo'
        
    if model_name.startswith('gpt-4'):
        # print(f'gpt-4 uses k_fewshot=5 as default (p2c fs_prompting)')
        k_fewshot = 5
    elif model_name.startswith('gpt-3.5-turbo'):
        # print(f'gpt-3.5 uses k_fewshot=8 as default (p2c fs-prompting)')
        k_fewshot = 8 

    # generate plan (retry included)
    plan_query_msg = get_plan_prompt(question, k_fewshot=k_fewshot)
    plan = _query(model_name=model_name, max_tokens=1024, stop='Question: ', messages=plan_query_msg, temperature=plan_temperature, top_p=1.0, n=1, mode='plan', seed=seed)

    if plan:
        code_query_msg = get_plan2code_prompt(question, plan=plan, k_fewshot=k_fewshot)
        code = _query(model_name=model_name, max_tokens=1024, stop='Question: ', messages=code_query_msg, temperature=code_temperature, top_p=1.0, n=n, mode='code', seed=seed)#, 
        if not code:
            return [None], [plan], {'codequery': code_query_msg, 'planquery': plan_query_msg}
        else: 
            return [code] if n==1 else code, [plan], {'codequery': code_query_msg, 'planquery': plan_query_msg}
    else:
        return None, None, {'codequery': code_query_msg, 'planquery': plan_query_msg}


def query_pal(question:str,
              pal_temperature: float, backbone: str, n=1, seed=777):
    '''
    This function is used to query OpenAI for PAL solutions.

    Args:
        data: a dict containing the question and answer
        key: the OpenAI API key
        pal_temperature: the temperature used in PAL
        backbone: ChatGPT or GPT-4

    Returns:
        completions: a list containing the PAL solution
    '''
    query_message = get_pal_prompt(question, backbone=backbone)
    if backbone == 'gpt4':
        model_name = 'gpt-4'
    elif backbone == 'gpt4turbo':
        model_name = 'gpt-4-1106-preview'
    elif backbone == 'chatgpt':
        model_name = 'gpt-3.5-turbo'
    completions = []
    pal_solution = openai.ChatCompletion.create(
                                model=model_name,
                                max_tokens=500,
                                stop='\n\n\n',
                                messages=query_message,
                                temperature=pal_temperature,
                                top_p=1.0,
                                seed=777,
                                n=n)

    if n ==1:
        completions.extend([choice['message']['content']
                        for choice in pal_solution['choices']]) # wtf this code...
        completions = completions[:1]
    else: # this line might not be compatible with self-consistency setting in the original code
        completions = [pal_solution['choices'][i]['message']['content'] for i in range(n)]
    return completions, query_message


def query_selection(question:str, 
                    backbone: str, 
                    cot_solution: str='', 
                    pal_solution: str='', 
                    p2c_plan_code_solution:str='', 
                    ):
    if backbone == 'gpt4':
        model_name = 'gpt-4'
    elif backbone == 'gpt4turbo':
        model_name = 'gpt-4-1106-preview'
    elif backbone == 'chatgpt':
        model_name = 'gpt-3.5-turbo'

    cot_pal_p2c_solution_list = [cot_solution, pal_solution, p2c_solution]
    cot_pal_p2c_solution_list = [s for s in cot_pal_p2c_solution_list if s] # remove p2c if empty
    selection_message = get_select_prompt(question, 
                                              cot_solution, 
                                              pal_solution, 
                                              p2c_plan_code_solution, backbone=backbone)
    selection_solution = openai.ChatCompletion.create(
        api_key=key,
        model=model_name,
        max_tokens=200,
        seed=777, # added on dec 21
        stop='\n\n',
        messages=selection_message,
        temperature=0.,
        top_p=1.0,
        n=1)['choices'][0]['message']['content'] 
    
    final_answer = postprocess_selection(selection_solution)
    return final_answer # 'pal'|'p2c'|'cot' 


def query_rims_inference(question: str, 
                          prompt_f: str, 
                          backbone: str,
                          n_fewshot:int=8,
                          turn_based:bool=False,
                          modif_prompt:bool=False) -> dict:
    if backbone == 'chatgpt':
        model_name = 'gpt-3.5-turbo-16k'
    elif backbone == 'gpt4':
        model_name = 'gpt-4'
    elif backbone == 'gpt4turbo':
        model_name = 'gpt-4-1106-preview'

    def get_turn_based_prompt(
                                prompt_f,
                                q:str='',
                                n_fewshot:int=8)->list:
        raise NotImplementedError('see 99_*yaml to implement here + query_enhanced_coh:get_turn_based_prompt()')

        
    
    def parse_raw_modif(rawqueryout:str)->dict:
        '''
        helper for Attempt 1,2,3... variants
        
        1/ read prompt to detect what to parse (`Some string here` <-- to be parsed)
        2/ and then parse those into a dict
        '''
        # read the output and get what to parse 
        pattern = r"`(.*?)`:"
        to_parse = re.findall(pattern, rawqueryout)
        to_parse = list(set(to_parse))

        # read the output again to parse the designated fields
        parse_dd = dict() 
        for fld in to_parse:
            # pattern = rf"`{fld}`:\s*(.*?)(?=`|$)"
            pattern = rf"`{fld}`:\s*(?:```)?(.*?)(?:```)?(?=`|$)"
            matches = re.findall(pattern, rawqueryout, re.DOTALL)
            if fld in {'Mistakes', "Hint for a better Method choice", "Workaround Method"}:
                parse_dd[fld] = matches
            else:    
                parse_dd[fld] = matches[0].strip()
        return parse_dd 
    

    def parse_raw(rawqueryout:str)->dict:
        '''
        helper function for output (universal for both turn_based=True|False)
        '''
        eval_starts = rawqueryout.find("`Evaluation`")

        cannotfind = []
        parse_idx_d = OrderedDict() 
        if eval_starts ==-1: # solved at once
            toparse = "`Method`: `Attempt`: `Answer`:".split()      
            for k in toparse:
                idx = rawqueryout.rfind(k)
                if idx == -1:
                    cannotfind.append(k)
                else:
                    parse_idx_d[k] = idx
      
        else: # parse last part
            toparse = ["`Method`:", "`Attempt`:", "`Mistakes`:", "`Hint for a better Method`:", "`Workaround Method`:", "`Corrected Attempt`:", "`Answer`:"]
            for k in toparse:
                idx = rawqueryout.rfind(k)
                if idx == -1:
                    cannotfind.append(k)
                else:
                    parse_idx_d[k] = idx

        # remove not-found keys
        for c in cannotfind:
            toparse.remove(c)
        
        # indices to strings
        parse_dd = dict() # actual parsed dict
        for i, k in enumerate(toparse):
            if i == len(toparse)-1:
                content = rawqueryout[parse_idx_d[k]:]
            else:
                content = rawqueryout[parse_idx_d[k]:parse_idx_d[toparse[i+1]]]
            parse_dd[k] = content
        # strip the keys
        parse_dd_ = {k:v.replace(k, "").strip() for k,v in parse_dd.items()}

        return pa
    # prep prompt
        rse_dd_

    if turn_based: # *.yaml
        messages = get_turn_based_prompt(
                                        prompt_f, 
                                        q=question,
                                        n_fewshot=n_fewshot
                                        )
    else: #*.txt  # DEC4 exps
        rawprompt = open(prompt_f).read().strip()
        prompt_tmp = PromptStr(rawprompt)
        prompt = prompt_tmp.sub('QUESTION', question) #data['question'])
        assert isinstance(prompt, str)
        messages = [
            {'role':'user', 'content': prompt}
        ]
    
    stop_tok = ["\n`Evaluation`: Correct", "Evaluation: Correct"] # could be a list or a single string object. Defaults: None
    raw_query_out = openai.ChatCompletion.create(
            # api_key=key,
            seed=777,
            model=model_name,
            max_tokens=1024, 
            stop=stop_tok, 
            messages=messages,
            temperature=0.,
            top_p=1.0,
            n=1)['choices'][0]['message']['content'] # str
    # toparse = ['`Attempt', '`Answer', '`Evaluation', '`Mistakes', '`Hint', '`Corrected Attempt', '`Answer',]
    if modif_prompt:
        parsed_dict = parse_raw_modif(raw_query_out)
    else:
        parsed_dict = parse_raw(raw_query_out)
        

    return parsed_dict, raw_query_out, messages





### getting prompts for each method ###
def get_select_prompt(question: str, cot_pal_p2c_sln_d:dict, backbone: str):
    '''
    This function is used to generate the selection prompt.
    '''
    if len(cot_pal_p2c_sln_d)==3:
        if backbone == 'gpt4' or backbone == 'gpt4turbo':
            system_message = math_prompt.GPT4_SELECT_SYSTEM3
            user_message = math_prompt.GPT4_SELECT_USER3
            assistant_message = math_prompt.GPT4_SELECT_ASSISTANT3
        elif backbone == 'chatgpt':
            system_message = math_prompt.TURBO_SELECT_SYSTEM3
            user_message = math_prompt.TURBO_SELECT_USER3
            assistant_message = math_prompt.TURBO_SELECT_ASSISTANT3      
    elif len(cot_pal_p2c_sln_d)==2:
        if backbone == 'gpt4' or backbone == 'gpt4turbo':
            system_message = math_prompt.GPT4_SELECT_SYSTEM
            user_message = math_prompt.GPT4_SELECT_USER
            assistant_message = math_prompt.GPT4_SELECT_ASSISTANT
        elif backbone == 'chatgpt':
            system_message = math_prompt.TURBO_SELECT_SYSTEM
            user_message = math_prompt.TURBO_SELECT_USER
            assistant_message = math_prompt.TURBO_SELECT_ASSISTANT
    else:
        assert False, f"len(cot_pal_p2c_sln_d) needs to be 2 or 3 (current = {len(cot_pal_p2c_sln_d)})"
    
    messages = get_user_assistant_messages(
        system_message, user_message, assistant_message)

    try: # try to remove docstring from pal solution generated... looks unhappy but kind of needed..
        pal_solution_lines_strip = [l.strip for l in pal_solution.split('\n')]
        docstring_idxs = [i for i, x in enumerate(pal_solution_lines_strip) if x == '"""' or x == "'''"]
        dsstart, dsend = min(docstring_idxs), max(docstring_idxs)

        pallines = [l for l in pal_solution.split('\n')]
        pal_generated = "\n".join(pallines[:dsstart] + pallines[dsend+1:])
    except Exception as e:
        pal_generated = pal_solution[0]

    if cot_solution[0].startswith('Answer:'): # put 'Answer:' at the start of CoT answer generation. Original code does this but not sure what they really wanted to do with this... biasing toward CoT?
        cot_generated = cot_solution[0]
    else:
        cot_generated = 'Answer:\n' + cot_solution[0]

    if len(cot_pal_p2c_sln_d) == 2:
        user_message = f'''Math problem: {question.strip()}

(A)
{cot_generated.strip()}

(B)
{pal_generated.strip()}

Which of the above two choices can correctly answer the math problem?'''
        
    else: # len(cot_pal_p2c_sln_d)==3:
        p2c_choice_str = f"(C)\n{p2c_solution[0].strip()}\n\nWhich of the above three choices can correctly answer the math problem?"
        user_message = user_message.replace('Which of the above two choices can correctly answer the math problem?', p2c_choice_str)

    messages += [{"role": "user", "content": user_message}]

    return messages


def get_user_assistant_messages(system_message: str, 
                                user_message: str, 
                                assistant_message: str):
    '''
    This function is used to convert the prompt into the message format used by OpenAI Chat API.
    '''
    messages = []
    messages.append({"role": "system", "content": system_message})
    split_user_messages = user_message.split('\n'*4)
    split_assistant_messages = assistant_message.split('\n'*4) # delim==4*\n... 
    for i in range(len(split_user_messages)): # user messages and assistant messages are paired... actually. This should have been `zip()`.
        question = split_user_messages[i]
        answer = split_assistant_messages[i]
        messages += [
            {"role": "user", "content": f"{question}"},
            {"role": "assistant", "content": f"{answer}"},
        ]
    return messages

def get_cot_prompt(question:str, backbone: str):
    '''
    This function is used to generate the CoT prompt.
    append "Question: " to the `question` 
    '''
    if backbone == 'gpt4' or backbone == 'gpt4turbo':
        system_message = math_prompt.GPT4_COT_SYSTEM
        user_message = math_prompt.GPT4_COT_USER
        assistant_message = math_prompt.GPT4_COT_ASSISTANT
    elif backbone == 'chatgpt':
        system_message = math_prompt.TURBO_COT_SYSTEM
        user_message = math_prompt.TURBO_COT_USER
        assistant_message = math_prompt.TURBO_COT_ASSISTANT

    messages = get_user_assistant_messages(
        system_message, user_message, assistant_message)
    messages += [{"role": "user", "content": f"Question: {question}"}]

    return messages

def get_pal_prompt(question:str,
                   backbone: str):
    '''
    This function is used to generate the PAL prompt.
    '''
    if backbone == 'gpt4' or backbone == 'gpt4turbo':
        system_message = math_prompt.GPT4_PAL_SYSTEM
        user_message = math_prompt.GPT4_PAL_USER
        assistant_message = math_prompt.GPT4_PAL_ASSISTANT
        messages = get_user_assistant_messages(
            system_message, user_message, assistant_message)

        messages += [{"role": "user",
                      "content": f"Question: {question}\n\n# solution in Python"}]

    elif backbone == 'chatgpt':
        system_message = math_prompt.TURBO_PAL_SYSTEM
        user_message = math_prompt.TURBO_PAL_USER
        assistant_message = math_prompt.TURBO_PAL_ASSISTANT
        messages = get_user_assistant_messages(
            system_message, user_message, assistant_message)

        messages += [{"role": "user",
                      "content": f"Answer the following question in Python: {question}"}]
    return messages

def get_plan_prompt(question:str, k_fewshot:int=0)->str:
    '''
    prep prompt for plan generation
    put "Question: " in front of the `question`

    '''
    PLAN_F = THIS_PARENT/'prompts_plan_v2.yaml'
    PLAN_PROMPTS_D= yaml.full_load(open(PLAN_F))
    prompt_d = PLAN_PROMPTS_D
    
    # q = data['question']
    q = question  
    system = prompt_d['system_msg']
    user_tmp = prompt_d['user_template'] 
    user_attempt = user_tmp.replace('{QUESTION}', f"Question: {q}")

    fewshots_user = prompt_d['fewshots_user'][:k_fewshot] # list of fewshot strings include Question: as a stop sequence.
    fewshots_assistant = prompt_d['fewshots_assistant'][:k_fewshot]
    
        
    msgs =  [{'role': 'system', 'content': system},]
    for fu, fa in zip(fewshots_user, fewshots_assistant):
        usr = {'role': 'user', 'content': fu}
        astnt = {'role': 'assistant', 'content': fa}
        msgs.append(usr)
        msgs.append(astnt)
    msgs.append({'role':'user', 
    'content': user_attempt})
    

    return msgs
    
def get_plan2code_prompt(question:str,#data:dict, 
                         plan:str='', k_fewshot:int=0, custom_idxs:list=None):
    # little bit revision from PAL prompt.
    # `solution()` is returned (can execute with solution() call w/o argument
    '''
    prep prompt for plan generation
    put "Qu
    estion: " in front of the `question`
    '''
    CODE_F = THIS_PARENT/'prompts_code_v2.yaml'
    prompt_d = yaml.full_load(open(CODE_F))
    
    q = question #data['question'] 
    system = prompt_d['system_msg']
    user_tmp = prompt_d['user_template'] 
    user_attempt = user_tmp.replace('{PLAN}', plan).replace('{QUESTION}', f"Question: {q}")

    if not custom_idxs:
        fewshots_user = prompt_d['fewshots_user'][:k_fewshot] # list of fewshot strings include Question: as a stop sequence.
        fewshots_assistant = prompt_d['fewshots_assistant'][:k_fewshot]
    else:
        fewshots_user = [prompt_d['fewshots_user'][i] for i in custom_idxs]
        fewshots_assistant = [prompt_d['fewshots_assistant'][i] for i in custom_idxs]
        
    msgs =  [{'role': 'system', 'content': system},]
    for fu, fa in zip(fewshots_user, fewshots_assistant):
        usr = {'role': 'user', 'content': fu}
        astnt = {'role': 'assistant', 'content': fa}
        msgs.append(usr)
        msgs.append(astnt)
    msgs.append({'role':'user', 'content': user_attempt})
    
    return msgs



### postprocessing helpers ###
# for p2c response
def postprocess_plan(rawanswer:str):
    # lines = [l for l in rawanswer.split('\n') if '</end>' not in l]
    lines = rawanswer.split('\n')
    if len(lines)>=1:
        plan_ = "\n".join(lines)
    else:
        print('plan gen failed')
        print(f"{rawanswer=}")
        plan_ = ''
    return plan_

def postprocess_code(rawanswer:str, k_fewshot:int=0):
    def remove_prints(code:str)->str:
        lines = code.split("\n")
        lines_ = [l if not l.startswith('print(') else l.replace('print(', '# print(') for l in lines]
        code_ = "\n".join(lines_)
        return code_
    
    try:
        # 1 removing starting wrap ```
        if "```python" in rawanswer:
            code = rawanswer.split("```python")[-1]
        elif rawanswer.startswith('```'):
            rawanswer = rawanswer.split('```')[-1]
        
        # 2 removing ``` at the end
        code = rawanswer.split("```")[0] #ending ``` removal
        
        code = remove_prints(code)
        assert code
    except: 
        print('code gen fails (unexecutable or funcname?)')
        print(f"code:\n{rawanswer}")
        code = ''
    return code

# p2c response postprocessing utility
def separate_plan_code(rawstr:str)->tuple:
    # used for 5_cohlike_prompt
    # p2c results in plan\ncode so split it.
    rawstr = rawstr.strip()
    lines = rawstr.split("\n")
    found_code = False
    for i,l in enumerate(lines):
        if l.startswith('def ') and l.strip().endswith(':'):
            found_code = True
            break
    if found_code:
        plan = "\n".join(lines[:i])
        code = "\n".join(lines[i:])
    else:
        plan, code = None, None
    return plan, code

# method name normalization for rimsprompt
def parse_method2(methodstr:str)->str:
    # works for --rimsprompt option
    normalized = methodstr.replace("-", ' ').replace("_", " ").lower()
    norm2short = {
        'chain of thought': 'cot',
        'cot': 'cot',
        'program aided language modeling': 'pal',
        'program aided language model': 'pal',
        'pal': 'pal',
        'plan and then code': 'p2c',
        'p2c': 'p2c',
    } # this should be key as abb, and value as a set of component patterns for capturing
    for k in norm2short.keys():
        if k in normalized:
            return norm2short[k]
    else:
        return methodstr
    
# rims prompt: cot answer extracting postprocessing 
def parse_num_from_answer(rawstr)->float:
    '''
    used for parsing number out from Answer (dec 4 exp)
    '''
    ptn = r'(-?\d+\.\d+|\d+)'
    nums = re.findall(ptn, rawstr)
    if not nums:
        return None
    else: # more than one number 
        return float(nums[-1])


### executing a code
def safe_execute_turbo(code_string: str, keys=None):
    def get_func_name_from_string(codestring:str)->str:
        match = re.search(r'def (\w+)\(', codestring)
        if match:
            funcname = match.group(1)
            # print(funcname)
        else:
            funcname = ''
        return funcname
    def execute(x, code_return):
        try:
            exec(x)
            locals_ = locals()
            if keys is not None:
                return [locals_.get(k, None) for k in keys]

            solution = locals_.get('solution', None)
            funcname = get_func_name_from_string(x) # for nontrivial code naming
            if solution is not None:
                return solution()
            elif funcname: # if any function name appears
                exec(x)
                solution = locals_.get(funcname, None)
                return solution()
            else:
                executed_code = 'import math\n' + 'import datetime\n' + \
                    '\n'.join([xx[4:]
                                for xx in x.strip().split('\n')[1:-1]])
                exec(executed_code)
                locals_ = locals()
                return locals_.get(code_return, None)

        except Exception as exp:
            print('Executing code error', exp)
            return None

    # === find code snippets between def solution(): and return ===
    try:
        code_list = code_string.strip().split('\n')

        new_code_list = []
        all_codes = []
        code_return = 'ans'

        for i in range(len(code_list)):
            # if code_list[i].strip() == 'def solution():':
            if re.search(r'def (\w+)\(', code_list[i]) and code_list[i].startswith('def '): # avoid including inner function definition
                new_code_list.append(code_list[i])
                for j in range(i+1, len(code_list)):
                    if code_list[j].startswith('    '):
                        new_code_list.append(code_list[j])
                    if code_list[j].startswith('    return '): # affirms outtermost return
                        code_return = code_list[j].split('return ')[1].strip()
                all_codes.append('\n'.join(new_code_list))
                new_code_list = []
        new_code = all_codes[-1]
        # ans = execute(new_code, code_return) 
        ans = func_timeout.func_timeout(
            3, execute, args=(new_code, code_return,))
        ans = ans if ans is not None else ans
    except func_timeout.FunctionTimedOut:
        ans = None

    try:
        ans = float(ans) if ans is not None else ans
    except:
        ans = None

    return ans


# parsing (executing) cot result into a float
def extract_num_turbo(solution: str):
    ans = solution.strip().split('\n')[-1].replace('So the answer is ', '')
    prd = [x[0] for x in regex.finditer(
        r'[\d\.,]+', ans) if regex.search(r'\d', x[0])]
    if len(prd) > 2:
        prd = prd[-1]
    elif len(prd):
        prd = prd[0]
    else:
        prd = None
    try:
        prd = float(prd.replace(',', '').rstrip('.')) if prd else prd
    except:
        prd = None
    return prd





### retry wrapper ###
@retry(wait=wait_chain(*[wait_fixed(3) for i in range(5)])) #defining backoff for retrying.
def do_with_tenacity(func, *args, **kwargs):
    return func(*args, **kwargs)



def get_concordant_answer(answers:list):
    '''
    check if there is a pair of concordant answers.
    input: cot_ans, pal_ans, p2c_ans, [, ...]
    output: ans if concordant else None

    *recommend to put answers in the order of cot going first (usually they are intgers)
    '''
    answers_no_none = [a for a in answers if a is not None]
    if not answers_no_none:
        return None
    elif len(answers_no_none) == 1:
        return answers_no_none.pop()
    elif len(answers_no_none) == 2:
        if abs(answers[0]-answers[1])<1e-3:
            return answers[0]
        else:
            return None
    else: # >=3
        for a1,a2 in combinations(answers_no_none,2):
            if abs(a1-a2)<1e-3:
                return a1
        return None # no concordant answers
   





if __name__ == "__main__":
    
    questions = []
    for line in math_prompt.TURBO_SELECT_USER.split("\n"):
        if line.lower().startswith('math problem: '):
            q = line.replace('Math problem: ', "").replace('Math Problem: ', "")
            questions.append(q)
            print(q)


    '''
    Question: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?
    Question: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?
    Question: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?
    Question: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?
    Question: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?
    '''

    # for q in questions:
    #     codes, plans, querymsgs = query_plancode(
    #                                                 q,
    #                                                 plan_temperature=1.0, 
    #                                                 code_temperature=1.0, 
    #                                                 backbone='chatgpt', 
    #                                                 n=1, 
    #                                                 seed=777
    #                                                 )
    #     solution = plans[0] + "\n" + codes[0] 
    #     print("====================================")
    #     print(f"Question: {q}")
    #     print(solution)
    p2c_chatgptout = open('p2c_chatgptout.txt').read().strip()
    q_sln_lst = p2c_chatgptout.split("====")
    
    ab_examples = math_prompt.TURBO_SELECT_USER.split("Which of the above two choices can correctly answer the math problem?") 
    attempt_choice3 = "Which of the above three choices can correctly answer the math problem?"
    
    select3_prompt = []
    for q_sln, ab in zip(q_sln_lst, ab_examples):
        q, sln = q_sln.split("Question: ")[1].split("\n", 1)
        print(f"Question: {q}")
        print('solution')
        print(sln)
        print('answer')
        print(f"{safe_execute_turbo(sln)=}")
        print('====')

        abc_user = f"{ab}(C)\n{sln}\n\n{attempt_choice3}\n\n\n\n"
        select3_prompt.append(abc_user)
        
    select3_prompt = "".join(select3_prompt).strip()
    print(select3_prompt, file=open('select3user.txt', 'w'))
        
