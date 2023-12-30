from fire import Fire
import jsonlines as jsl 

'''
unify the field of the inference records.

row:
    (from gsm)
    - idx
    - question
    - ans
    (from what's inferred)
    - prompt_path
    - ansmap:
        {cot: pal: p2c:}
    - solmap:
        {cot: pal: p2c:}
    - majority_ans: None or majority answer
    - selection_or_rims: 
        각자에 합당한 아웃풋
        rims: eval_friendly_d
        model_selection (baseline): 
            {
                good_method, 
                good_ans,
                selection_choice,
                bad_method, 
                bad_ans,
            }
    


'''


def rims_inference(
        prompt_f:str='', 
    ):
    assert prompt_f, f'need to specify {prompt_f=}'
    return

def baseline_inference(
        prompt_f:str='math_prompt.py' # only for recording promptfilename to the result. Actual prompt is read at `llm_query_utils.py`
    ):
    return 

if __name__ == '__main__':
    Fire()
    '''
    usage:
    python 99_run_inference baseline_inference|rims_inference [--KWARGS VALUE]*
    '''