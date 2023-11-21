import pandas as pd 
from pprint import pprint


from fire import Fire
# using Fire --> *args, **kwargs of the main will define the exp arguments alone

from selection_math import *
# query_cot, query_pal, query_p2c
# jsl, pd, math, re... etc will already been loaded 


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
    dataset = jsl.open(dataset_f)

    # sort and sample trainset (no length bias)
    kshots = get_k_train_shots(k=num_train_sample, train_f=dataset_f, heuristics=heuristics)

    # for cot, pal, and p2c, find the examples that successes reflection and resolution.
    method2query_f = {
        'cot': query_cot,
        'pal': query_pal,
        'p2c': query_plancode, 
    }
    for method in ['cot', 'pal', 'p2c']:
        query_f =     


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