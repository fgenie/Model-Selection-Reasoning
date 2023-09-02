import json
import os
import openai
import time
from datetime import datetime
import argparse
from tqdm import tqdm
# from typing import Union
from prompts import math_prompt
from prompts.plancode_util import *
from collections import OrderedDict, Counter
from tool import *
from tenacity import (
    retry,
    wait_chain,
    wait_fixed
) 
import yaml
from pprint import pprint

# after 6 times of retry, it raises exception. waits between retries are specified inside the `wait_chain`
@retry(wait=wait_chain(*[wait_fixed(3) for i in range(3)])) #defining backoff for retrying.
def completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)




def get_user_assistant_messages(system_message: str, user_message: str, assistant_message: str):
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


def get_cot_prompt(data: dict, backbone: str):
    '''
    This function is used to generate the CoT prompt.
    '''
    if backbone == 'gpt4':
        system_message = math_prompt.GPT4_COT_SYSTEM
        user_message = math_prompt.GPT4_COT_USER
        assistant_message = math_prompt.GPT4_COT_ASSISTANT
    elif backbone == 'chatgpt':
        system_message = math_prompt.TURBO_COT_SYSTEM
        user_message = math_prompt.TURBO_COT_USER
        assistant_message = math_prompt.TURBO_COT_ASSISTANT

    messages = get_user_assistant_messages(
        system_message, user_message, assistant_message)
    question_message = data['question']
    messages += [{"role": "user", "content": f"Question: {question_message}"}]

    return messages



def get_pal_prompt(data: dict, backbone: str):
    '''
    This function is used to generate the PAL prompt.
    '''
    if backbone == 'gpt4':
        system_message = math_prompt.GPT4_PAL_SYSTEM
        user_message = math_prompt.GPT4_PAL_USER
        assistant_message = math_prompt.GPT4_PAL_ASSISTANT

        messages = get_user_assistant_messages(
            system_message, user_message, assistant_message)

        question_message = data['question']
        messages += [{"role": "user",
                      "content": f"Question: {question_message}\n\n# solution in Python"}]

    elif backbone == 'chatgpt':
        system_message = math_prompt.TURBO_PAL_SYSTEM
        user_message = math_prompt.TURBO_PAL_USER
        assistant_message = math_prompt.TURBO_PAL_ASSISTANT

        messages = get_user_assistant_messages(
            system_message, user_message, assistant_message)

        question_message = data['question']
        messages += [{"role": "user",
                      "content": f"Answer the following question in Python: {question_message}"}]

    return messages


def get_select_prompt(data: dict, cot_solution: list, pal_solution: list, backbone: str):
    '''
    This function is used to generate the selection prompt.
    '''
    if backbone == 'gpt4':
        system_message = math_prompt.GPT4_SELECT_SYSTEM
        user_message = math_prompt.GPT4_SELECT_USER
        assistant_message = math_prompt.GPT4_SELECT_ASSISTANT
    elif backbone == 'chatgpt':
        system_message = math_prompt.TURBO_SELECT_SYSTEM
        user_message = math_prompt.TURBO_SELECT_USER
        assistant_message = math_prompt.TURBO_SELECT_ASSISTANT
    messages = get_user_assistant_messages(
        system_message, user_message, assistant_message)

    try:
        pal_generated_list = pal_solution[0].split('"""')
        pal_generated = pal_generated_list[0].strip(
        ) + pal_generated_list[2]
    except Exception as e:
        pal_generated = pal_solution[0]

    if cot_solution[0].startswith('Answer:'):
        cot_generated = cot_solution[0]
    else:
        cot_generated = 'Answer:\n' + cot_solution[0]

    user_message = f'''Math problem: {data['question'].strip()}

(A)
{cot_generated.strip()}

(B)
{pal_generated.strip()}

Which of the above two choices can correctly answer the math problem?'''

    messages += [{"role": "user", "content": user_message}]

    return messages


def query_cot(data: dict, key: str, cot_temperature: float, backbone: str):
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
    query_message = get_cot_prompt(data, backbone=backbone)
    if backbone == 'gpt4':
        model_name = 'gpt-4'
    elif backbone == 'chatgpt':
        model_name = 'gpt-3.5-turbo'

    # start_time = time.time()
    completions = []
    cot_solution = completion_with_backoff(
            api_key=key,
            model=model_name,
            max_tokens=500,
            stop='\n\n\n',
            messages=query_message,
            temperature=cot_temperature,
            top_p=1.0,
            n=1)

    # completions.extend([choice['message']['content']
    #                     for choice in cot_solution['choices']])
    completions = [cot_solution['choices'][0]['message']['content']]
    return completions


@retry(wait=wait_chain(*[wait_fixed(3) for i in range(2)])) 
def _query(key, model_name='gpt-3.5-turbo', max_tokens=2048, messages=None, temperature=0., top_p=1.0, n=1, mode='plan', docstring_def:str=''): # mode = plan or code
    # print("_query")
    resp = openai.ChatCompletion.create(api_key=key,
                                model=model_name,
                                max_tokens=max_tokens,
                                messages=messages,
                                temperature=temperature,
                                top_p=top_p,
                                n=n)
                                # stop=stop,
    # print('apicall reached')
    content = resp['choices'][0]['message']['content'] # str
    if mode == 'plan':
        plan = postprocess_plan(content) # it will complain when failing
        if not plan: 
            print('retrying plangen')
            raise ValueError
        return plan
    elif mode == 'code':
        assert docstring_def
        code = postprocess_code_answer(content, docdef=docstring_def)
        if not code: 
            print('retrying codegen')
            raise ValueError
        return code


def query_plancode(data: dict, key: str='', plan_temperature: float=.0, code_temperature: float=.0, backbone: str='gpt-3.5-turbo', k_fewshot:int=0):
    '''
    PAL variant: 1. generate planning for the given question 2. based on 1, generate code like PAL does.

    args:
        mostly same arguments with `query_pal()` below
    returns: 
        completions: Sequence[
                code_solution:str
                ]
    '''
    # specify model
    if backbone == 'gpt4':
        model_name = 'gpt-4'
    elif backbone == 'chatgpt':
        model_name = 'gpt-3.5-turbo'

    # generate plan (retry included)
    plan_query_msg = get_plan_prompt(data, k_fewshot=k_fewshot)
    # kvprint(plan_query_msg)
    # print(f"{k_fewshot=}")
    plan = _query(key, model_name=model_name, max_tokens=1024, messages=plan_query_msg, temperature=plan_temperature, top_p=1.0, n=1, mode='plan')
    # print(f"{plan=}")

    # generate code
    code_query_msg = get_plan2code_prompt(data, plan=plan, k_fewshot=k_fewshot)
    # kvprint(code_query_msg)
    # print(f"{k_fewshot=}")
    indent = " "*4
    docdef = f'def solution():\n{indent}"""{add_indents2plan(plan)}"""'
    code = _query(key, model_name=model_name, max_tokens=1024, messages=code_query_msg, temperature=code_temperature, top_p=1.0, n=1, mode='code', docstring_def=docdef)
    # print(f"{code=}")
    # wrapup
    completions = [code]

    return completions

def query_pal(data: dict, key: str, pal_temperature: float, backbone: str):
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
    query_message = get_pal_prompt(data, backbone=backbone)
    # for m in query_message: print(len(m['content']));
    # pprint(query_message)
    if backbone == 'gpt4':
        model_name = 'gpt-4'
    elif backbone == 'chatgpt':
        model_name = 'gpt-3.5-turbo'
    completions = []
    pal_solution = completion_with_backoff(
                                api_key=key,
                                model=model_name,
                                max_tokens=500,
                                stop='\n\n\n',
                                messages=query_message,
                                temperature=pal_temperature,
                                top_p=1.0,
                                n=1)


    completions.extend([choice['message']['content']
                        for choice in pal_solution['choices']]) # wtf this code...
    completions = completions[:1]
    return completions

def query_selection(data: dict, key: str, cot_solution: list, pal_solution: list, backbone: str):
    '''
    This function is used to query OpenAI for selection solutions.

    Args:
        data: a dict containing the question and answer
        key: the OpenAI API key
        cot_solution: a list containing the CoT solution
        pal_solution: a list containing the PAL solution
        backbone: ChatGPT or GPT-4

    Returns:
        completions: a list containing the selection solution
    '''
    selection_message = get_select_prompt(
        data, cot_solution, pal_solution, backbone=backbone)
    if backbone == 'gpt4':
        model_name = 'gpt-4'
    elif backbone == 'chatgpt':
        model_name = 'gpt-3.5-turbo'
    completions = []
    selection_solution = completion_with_backoff(
        api_key=key,
        model=model_name,
        max_tokens=200,
        stop='\n\n',
        messages=selection_message,
        temperature=0.,
        top_p=1.0,
        n=1)
    
    completions.extend([choice['message']['content']
                            for choice in selection_solution['choices']])
    completions = completions[:1]
    return completions


# def query_math(data: dict, key: str, cot_temperature: float, pal_temperature: float, sc_num: int, backbone: str, use_plancode:bool=False):
def query_math(
        data: dict, 
        key: str, 
        cot_temperature: float, 
        pal_temperature: float, 
        sc_num: int, 
        backbone: str, 
        
        plan_temperature: float=.0, # when use_plancode == True
        code_temperature: float=.0,
        k_fewshot:int=0,
        use_plancode:bool=False
        ):
    '''
    This function is used to query OpenAI for answers in arithmetic tasks. It contains three steps:
    1. Query CoT for solutions
    2. Query PAL for solutions
    3. Query model selection answers

    Note that we only query selection answers when CoT and PAL answers are different. Otherwise, we directly use CoT or PAL answers.

    We also use majority voting to select the final answer if we have multiple self-consistency samples.

    Args:
        data: a dict containing the question and answer
        key: the OpenAI API key
        cot_temperature: the temperature used in CoT. 0 for greedy decoding. We set it to 0.5 for self-consistency samples.
        pal_temperature: the temperature used in PAL. 0 for greedy decoding. We set it to 0.8 for self-consistency samples.
        sc_num: the number of self-consistency samples
        backbone: ChatGPT or GPT-4

    Returns:
        to_dump_data: a dict containing the question, answer, the final answer and other information
    
        
    added query_plancode routine inside
    '''

    cot_answers = []
    pal_answers = []
    cot_solutions = []
    pal_solutions = []
    selection_solutions = []
    final_answers = []

    for i in range(sc_num):
        cot_ans = None
        pal_ans = None
        selection_ans = None
        final_ans = None
        cot_solution = query_cot(
            data, key, cot_temperature, backbone=backbone)
        if cot_solution is None:
            print('Time out')
            return None
        else:
            cot_ans = extract_num_turbo(cot_solution[0])
            cot_answers.append(cot_ans)
            cot_solutions.append(cot_solution[0])
        if use_plancode:
            pal_solution = query_plancode(data, key=key, plan_temperature=plan_temperature, code_temperature=code_temperature, backbone=backbone, k_fewshot=k_fewshot)
        else:
            pal_solution = query_pal(
                data, key, pal_temperature, backbone=backbone)
        if pal_solution is None:
            print('Time out')
            return None
        else:
            pal_ans = safe_execute_turbo(pal_solution[0])
            pal_answers.append(pal_ans)
            pal_solutions.append(pal_solution[0])

        if cot_ans is not None and pal_ans is not None:

            # ==== Only select when CoT and PAL are different ====
            if abs(cot_ans - pal_ans) > 1e-3:
                selection_ans = query_selection(
                    data, key, cot_solution=cot_solution, pal_solution=pal_solution, backbone=backbone)
                if selection_ans is None:
                    print('Time out')
                    return None
                else:
                    selection_choice = extract_choice_turbo(selection_ans[0])
                    selection_solutions.append(selection_ans[0])
                    if selection_choice == '(A)':
                        final_ans = cot_ans
                    elif selection_choice == '(B)':
                        final_ans = pal_ans
            else:
                final_ans = cot_ans

        elif cot_ans is not None and pal_ans is None:
            final_ans = cot_ans
        elif cot_ans is None and pal_ans is not None:
            final_ans = pal_ans
        else:
            final_ans = None

        final_answers.append(final_ans)

    count = Counter(final_answers)
    majority_ans = count.most_common(1)[0][0]

    # === dump data ===
    to_dump_data = OrderedDict(
        {'index': data['index'], 'question': data['question'], 'answer': data['answer'],
         'majority_ans': majority_ans, 'final_answers': final_answers,
         'cot_executed': cot_answers, 'pal_executed': pal_answers,
         'cot_generated': cot_solutions, 'pal_generated': pal_solutions, 'choice_solution': selection_solutions}
    )

    return to_dump_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--end', type=int, default=-1)
    parser.add_argument('--dataset', type=str, choices=['dbg', 
                        'gsm8k', 'svamp', 'asdiv', 'singleeq', 'singleop',
                        'singleaddsub', 'multiarith'], default='gsm8k')
    parser.add_argument('--backbone', type=str,
                        choices=['chatgpt', 'gpt4'], default='gpt4')
    parser.add_argument('--cot_temperature', type=float, default=0.)
    parser.add_argument('--pal_temperature', type=float, default=0.)
    parser.add_argument('--sc_num', type=int, default=1,
                        help='Self-consistency samples. 1 indicates greedy decoding')
    parser.add_argument('--output_dir', type=str, default='../output/')
    parser.add_argument(
        '--key', type=str, default='sk-', required=True)

    # plancode options
    parser.add_argument('--use_plancode', action='store_true')
    parser.add_argument('--plan_temperature', type=float, default=0.)
    parser.add_argument('--code_temperature', type=float, default=0.)
    parser.add_argument('--k_fewshot', type=int, default=0) #  >= 0


    args = parser.parse_args()

    start_index = args.start
    end_index = args.end
    dataset_name = args.dataset
    cot_temperature = args.cot_temperature
    pal_temperature = args.pal_temperature
    backbone = args.backbone
    sc_num = args.sc_num
    output_dir = args.output_dir
    key = args.key

    start_time_0 = time.time()
    print('Current time: ', time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()))

    dt_string = datetime.now().strftime("%m_%d_%H_%M")

    if dataset_name == 'gsm8k':
        dataset = jsonlines_load('../dataset/gsm8K_test.jsonl')
    elif dataset_name == 'dbg':
        dataset = jsonlines_load('../dataset/dbg.jsonl') # 2 lines of gsm8k test
    elif dataset_name == 'svamp':
        dataset = jsonlines_load('../dataset/svamp.jsonl')
    elif dataset_name == 'asdiv':
        dataset = jsonlines_load('../dataset/asdiv.jsonl')
    elif dataset_name == 'singleeq':
        dataset = jsonlines_load('../dataset/single_eq.jsonl')
    elif dataset_name == 'singleop':
        dataset = jsonlines_load('../dataset/single_op.jsonl')
    elif dataset_name == 'singleaddsub':
        dataset = jsonlines_load('../dataset/single_addsub.jsonl')
    elif dataset_name == 'multiarith':
        dataset = jsonlines_load('../dataset/multiarith.jsonl')

    # === slice data based on start and end ===
    total_num = len(dataset)
    print('total data: ', total_num)
    if end_index == -1:
        end_index = total_num

    if end_index > total_num:
        end_index = total_num

    tasks = dataset[start_index:end_index]
    task_num = len(tasks)
    print('Current total tasks: ', task_num)

    unfinished_tasks = []

    output_path = os.path.join(output_dir, f'{backbone}/')
    if args.use_plancode:
        output_path = os.path.join(output_dir, f"{backbone}_plancode/")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    save_path = os.path.join(output_path,
                             f'{dataset_name}_k{args.k_fewshot}_sc{sc_num}_s{start_index}_e{end_index}_{dt_string}.jsonl')


    # === run experiments ===
    progress_bar = tqdm(range(task_num))
    for i in range(task_num):
        task = tasks[i]
        wait_time = min(sc_num * 300, 360)
        start_time = time.time()
        while True:
            try:
                if dataset_name=='dbg':
                    print(f"""{args.plan_temperature=}\n{args.code_temperature=}\n{args.use_plancode=}\n{args.k_fewshot=}""")
                ans = query_math(
                    task, key=key, cot_temperature=cot_temperature,
                    pal_temperature=pal_temperature, sc_num=sc_num,backbone=backbone,
                    plan_temperature=args.plan_temperature,
                    code_temperature=args.code_temperature,
                    k_fewshot=args.k_fewshot,
                    use_plancode=args.use_plancode,
                    )
                
            except Exception as e:
                print(e)
                ans = None

            if ans is not None:
                with open(save_path, "a+") as fout:
                    fout.write(json.dumps(ans)+'\n')
                progress_bar.update(1)
                break
            else:
                pass
                print("retrying (main)")
                # sleep_time = random.uniform(3, 5)
                # time.sleep(sleep_time)

            if time.time() - start_time > wait_time:
                print('Time out')
                print('Current Task: ', i)
                unfinished_tasks.append(task)
                break

        # sleep_time = random.uniform(3, 5)
        # time.sleep(sleep_time)

    end_time_0 = time.time()
    print('Finish at time: ', time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime()))
    print(f'Time used: {end_time_0 - start_time_0} seconds')
    if len(unfinished_tasks) > 0:
        print('Unfinished tasks: ')
        for task in unfinished_tasks:
            print(task)

    print('Done')
