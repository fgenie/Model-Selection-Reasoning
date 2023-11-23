import pandas as pd 
from fire import Fire
from tenacity import retry, wait_chain, wait_fixed



from functools import partial
from pprint import pprint
from collections import defaultdict
from typing import Union 

from selection_math import *
# query_cot, query_pal, query_p2c
# jsl, pd, math, re... etc will already been loaded 


@retry(wait=wait_chain(*[wait_fixed(3) for i in range(5)])) #defining backoff for retrying.
def do_with_tenacity(func, *args, **kwargs):
    # print(f'running with {args=}, {kwargs=}')
    return func(*args, **kwargs)

def sln_eval(sln:str='', ans:Union[float, int]=-9999., method:str='')->bool:
    assert sln
    assert method in ['cot', 'pal', 'p2c']
    assert isinstance(sln, str)
    assert ans!=-9999., 'ans kwarg required'
    
    if method == 'cot':
        pred = extract_num_turbo(sln)
    else: #pal, p2c
        pred = safe_execute_turbo(sln)
    
    if pred is None:
        return False
    else: # pred worked!
        return abs(pred-ans) < 1e-3 # eval logic same as model-selection paper original code



def main(
    config_f:str = 'rims_train_config.yaml',
):
    print(f'loaded config from:\n\t{config_f}')
    kwargs = yaml.full_load(open(config_f))
    pprint(kwargs)
    # unpack kwargs
    for k,v in kwargs.items():
        globals()[k] = v
        # now kwargs[k] is accessible as a global variable `k` in this script    
    
    # check are they loaded properly 
    if not Path(dataset_f).is_file():
        gsm8k_train_download_and_parse()
        assert Path(dataset_f).is_file(), 'why is it not downloaded?'

    # sort and sample trainset (no length bias)
    train_samples = get_k_train_shots(k=num_train_sample, train_f=dataset_f, heuristics=heuristics)
    
    
    # if dbg:
    #     train_samples = train_samples[:1]
    #     verbal_T = 1.5
    #     code_T = 1.5
    #     backbone = 'chatgpt'

    # for cot, pal, and p2c, find the examples that successes reflection and resolution.
    method2query_f = {
        'cot': query_cot,
        'pal': query_pal,
        'p2c': query_plancode, 
    }
    method2failed_questions = defaultdict(list)

    for method in ['cot', 'pal', 'p2c']:
        f = method2query_f[method]
        if method == 'cot':
            query_f = partial(f, key = openai.api_key, cot_temperature=verbal_T, backbone=backbone, n=n_llmquery, seed=seed)
        elif method == 'pal':
            query_f = partial(f, key = openai.api_key, pal_temperature=verbal_T, backbone=backbone, n=n_llmquery, seed=seed)
        elif method == 'p2c':
            query_f = partial(f, key = openai.api_key, plan_temperature=verbal_T, code_temperature=code_T, backbone=backbone, n=n_llmquery, seed=seed)
        else:
            raise ValueError(f'unknown method {method}')    

        # find the ones that fails at first.
        for row in tqdm(train_samples, desc=f'gathering failure cases ({method=}, {n_llmquery=})'):
            ans = float(row['ans'])
            if dbg:
                row = ''
            out = do_with_tenacity(query_f, row)
            if method == 'p2c':
                predlst, planlst, querymsg_d = out
                row['query_msgs'] = querymsg_d
            else: # pal, cot
                predlst, querymsg_lst = out
            print()
            eval_lst = [sln_eval(sln=sln, ans=ans, method=method) for sln in predlst]
            if eval_lst.count(True) < eval_lst.count(False):
                row['howmany_failed'] = f"{backbone}: {eval_lst.count(False)}/{n_llmquery}"
                method2failed_questions[method].append(row)
                print(f"gotcha! {len(method2failed_questions[method])}/{n_candids}")
            if len(method2failed_questions[method]) == n_candids:
                print(f"at {row['idx']=}, gathering candids are done ({n_candids=}, {num_train_sample=})")
                break
        
        for method, candidlist in method2failed_questions.items():
            outdir_ = Path(outdir)
            if not outdir_.exists():
                outdir_.mkdir(parents=True, exist_ok=True)
            fname = f"failed_{method}_n{n_llmquery}_numtrain{num_train_sample}_{backbone}_vT{verbal_T}_cT{code_T}_seed{seed}.jsonl"
            outpath = outdir_/fname
            with jsl.open(outpath, 'w') as writer:
                writer.write_all(candidlist)
                print(f"{method} failure cases written to:\n\t{str(outpath)}")
        
        
            

            



def get_k_train_shots(
                k:int=100,
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

if __name__ == "__main__":
    Fire(main)
    '''
    usage:
    python rims_train.py [--KWARG VALUE] [--KWARG1 VALUE1] [--KWARG2 VALUE2] ...
    '''