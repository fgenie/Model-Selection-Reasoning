import yaml
from typing import Dict, List, Tuple, Any, Sequence, Mapping, Callable
from fire import Fire

# heuristic for unbiased sampling from trainingset
import pandas as pd
import jsonlines as jsl 
from pathlib import Path
import datasets

ACTOR_PROMPTS = yaml.full_load('actor_prompt.yaml')

def kshot_harvesting(
    data:Dict[str, Any],
    n_reflect:int = 1, # args.n_reflect --> per method, how many times to reflect?
    first_reasoning_how:str='random', #'llm' args.first_reasoning_how
):
    '''
    Few-shot learning of the master LLM choosing a good method to tackle "a" problem. (constructs fewshot examples for master LLM model-choice)
    n_reflect * len(models_to_sample) times of querying the LLM.
    '''

    # system message
    models_to_sample = ['cot', 'pal', 'plan2code'] * (n_reflect+1)
    choice_traj = []
    iscorrect = False
    # first attempt
    sys_0 = ACTOR_PROMPTS['system_0']
    attempt_question = ACTOR_PROMPTS['attempt_question'].replace('{QUESTION}', question).replace('{CANDIDS}', f"{list(set(models_to_sample))}")
    user_msgs = [attempt_question]
    assist_msgs = []
    last_choice = ''
    prom = prep_gpt_input(sys=sys_0, user_msgs=user_msgs, assist_msgs=assist_msgs)
    while True:
        # 1. choice
        choice_reasoning = completion_with_backoff(
                api_key=key,
                model= model_name,
                max_tokens=500,
                stop='\n\n\n',
                messages=prom,
                temperature=cot_temperature,
                top_p=1.0,
                n=1)['choices'][0]['message']['content']
        
        choice = parse_choice(choice_reasoning)
        choice_traj.append(choice)
        models_to_sample.remove(choice)
        # if the method chosen before, try with hint prepended to the prompt. 

        # 2. solve
        retrying_same = last_choice == choice
        if retrying_same: 
            if choice == 'cot':
                sol = re_query_cot() # query cot with hint prepended: 
                # e.g. last time we tried `cot`, we got wrong answer `ans` {same `cot` prompt as usual}
            elif choice == 'pal':
                sol = re_query_pal()
            elif choice == 'plan2code':
                sol = re_query_plan2code()
        else:
            if choice == 'cot':
                sol = query_cot()
            elif choice == 'pal':
                sol = query_pal()
            elif choice == 'plan2code':
                sol = query_plan2code()
        pred = parse_sol(sol)
        
        # 3. check correctness
        iscorrect = (pred == ans)
        last_choice = choice
        
        # 4. ending condition
        if iscorrect:
            break
        elif not models_to_sample:
            break
        
        # 5. prepare next round
        sys = ACTOR_PROMPTS['system_reflect']
        attempt = ACTOR_PROMPTS['attempt_reflect'].replace("{CANDIDS}", f"{list(set(models_to_sample))}").replace("{QUESTION}", question)

        assist_msgs.append(choice_reasoning)
        user_msgs.append(attempt)
        prom = prep_gpt_input(sys=sys, user_msgs=user_msgs, assist_msgs=assist_msgs)
                
        
def prep_reflection_prompt(sol, choice, pred):
    return ACTOR_PROMPTS['invoke_reflection'].replace('{SOL}', sol).replace('{CHOICE}', choice).replace('{PRED}', pred)


def prep_gpt_input(
        sys:str='', 
        user_msgs:List[str]=None, 
        assist_msgs:List[str]=None,
        )->List[Dict[str, str]]:
    '''
    Prepare input for openai API call
        from system message, user messages, and assistant messages.
    '''
    assert user_msgs, 'At least one `user_msg` is needed.'
    msgs = [
        {'role': 'sys', 'content': sys},
    ]
    for i, msg in enumerate(user_msgs):
        msgs.append({'role': 'user', 'content': msg})
        if i<len(assist_msgs):
            msgs.append({'role': 'assist', 'content': assist_msgs[i]})
    return msgs

def get_k_train_shots(
                k:int=10,
                train_f:str='gsm8k_train.jsonl', 
                heuristics:str='wordcount'
                ): 
    if heuristics == 'wordcount':
        df = pd.DataFrame(jsl.open(train_f))
        df['wordcount'] = df.question.apply(lambda q:len(q.split()))
        df_ = df.sort_values(by='wordcount')
        idxs = [i for i in range(0, len(df), len(df)//k)][:k]
        resdf = df_.iloc[idxs]
        kshots = resdf.to_dict(orient='records')
    else:
        raise NotImplementedError(f'heuristics {heuristics} not implemented.')
    
    return kshots # List[Dict[str,str]]

# util for gsm8k train split download and parsing
def gsm8k_train_download_and_parse(root:str='./'):
    # check if exists
    root = Path(root)
    target_path = root/"gsm8k_train.jsonl"
    if target_path.exists():
        records = list(jsl.open(target_path))
        print(f"found train set @:\n\t{str(target_path)}")
        print(f"\t{records[0]=}")
        print(f"\t{len(records)=}")
    else: 
        # download 
        gsm_train = datasets.load_dataset('gsm8k', 'main')['train']

        # parse
        def parse_raw_target(answer_raw:str)-> str:
            return answer_raw.split("### ")[-1].strip()
        df = pd.DataFrame(gsm_train)
        df['ans'] = df.answer.apply(parse_raw_target)
        df['idx'] = df.index
        records = df.to_dict(orient='records')
        with jsl.open(target_path, 'w') as writer:
            writer.write_all(records)
            print(f'gsm8k train download and write: done.\n\t{str(target_path)}')
    return str(target_path)


def test_utils():
    gsm8k_train_download_and_parse()
    kshots=get_k_train_shots()
    print(kshots)

if __name__ == "__main__":
    Fire(test_utils) 
    