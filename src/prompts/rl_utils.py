from typing import Sequence, Tuple, Dict, Union
import openai
import yaml

yaml.full_load()

KEY = open('/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/openai_key.txt').read().strip()
openai.api_key = KEY # set key

def completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def sample_a_model(
            models_to_sample:Sequence[str], 
            howtosample:str='random',
            **kwargs):
    if howtosample == 'random':
        sampled = random.choice(models_to_sample)
    elif howtosample == 'llm':
        if backbone == 'chatgpt':
            model_name = 'gpt-3.5-turbo'
        elif backbone == 'gpt-4':
            model_name = backbone
        
        sampled, resp_raw = query_modelsample(data, key=key, models_to_sample)
    models_to_sample.remove(sampled)
    return model_name, models_to_sample


def query_modelsample()->Tuple[str, str]:

    msgs = get_modelsample_prompt(data, models_to_sample)
    advice = completion_with_backoff(
            api_key=key,
            model= model_name,
            max_tokens=500,
            stop='\n\n\n',
            messages=query_message,
            temperature=cot_temperature,
            top_p=1.0,
            n=1)
    
    model_name = parse_model_name(advice['choices'][0]['message']['content'])
    return model_name, advice

def get_model_sample_prompt(data:Dict, models_to_sample:Sequence[str])->str:
    raise NotImplementedError('rl_utils.py::get_model_sample_prompt'')
    return 

def parse_model_name(advice:str)->str:
    lines = advice.split('\n')
    for l in lines:
        if l.startswith('Method: '):
            gist = l
            break
    return l.split('Model: ')[-1]

def query_verification(data:dict, 
                       key:str, 
                       sol:str='', 
                       majority_ans:Union[str, int]=None, 
                       howtoverify:str='') -> Tuple[bool, str]:
    if howtoverify == 'llm'
        '''args=
        https://arxiv.org/abs/2309.11495
        '''
        raise NotImplementedError()
    elif howtoverify == 'oracle':
        iscorrect = majority_ans == data['ans']
        judgement_raw = f'ORACLE VERIF: {majority_ans}({type(majority_ans)})=={data["ans"]}({type(data["ans"])})'
    return iscorrect, judgement_raw

def augment_user_msg_with_hint(msgs:Sequence[Dict[str,str]], wrong_answer:Sequence[Union[int,str]])->Dict:
    '''
    This function augments the user_msg with a hint to avoid the same wrong answer to be queried again. (progressive hint prompting improves reasoning (https://arxiv.org/abs/2304.09797))

    msgs: actual msgs for apicall
    wrong_answer: list of `parsed(!)` wrong answers 
    '''
    user_msg = msgs[-1]
    user_msg['content'] = f"{user_msg['content']} (Avoid wrong answers: [{', '.join(wrong_answer)}])"
    msgs[-1] = user_msg
    return msgs