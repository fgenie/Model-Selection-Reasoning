import pandas as pd
import yaml
from itertools import product
from typing import Sequence, Mapping
from fire import Fire
import re
import jsonlines as jsl
from functools import partial
from pathlib import Path
'''
read: 
- 2_good_examples_from_*xlsx
- 3_model_select_fs_prompt.yaml
- 3_reflect_fs_prompt.yaml
out:
several
- model select prompts (manual fill-in still left)
- reflection prompts (manual fill-in left)

--> need to manually fill Hints: and Reflection: parts 
--> See those work properly on several questions

'''

FS_D = pd.read_excel('2_good_examples_from_gsm_test.xlsx', sheet_name=None)
SELECT_YML = yaml.full_load(open('3_actor_model_select_prompts_plain.yaml'))
SEL_TMP = SELECT_YML['prompt_template']
SEL_REF_EXS = SELECT_YML['reflection_exs']
SEL_ACT_EXS = SELECT_YML['action_exs']

REFLECT_YML = yaml.full_load(open('3_actor_reflect_prompt_plain.yaml'))
REF_TMP = REFLECT_YML['prompt_template']
REF_EXS = REFLECT_YML['reflection_exs']
        




class PromptStr(str): # str class with some utility methods
    def __init__(self, template_str):
        super().__init__()
        self += template_str  

    def sub(self, 
            placeholder_name:str, 
            tobe:str):
        return PromptStr(self.replace(f"[{placeholder_name}]", str(tobe)))

    def get_placeholder_names(self) -> list:
        return re.findall(r"\[(.*?)\]", self)


def a_fewshot_prep(datarow, 
                   mode:str='select/reflect')->PromptStr:
    '''
    this function works same for SELECTION / REFLECTION (they share the format)
    (SEL_R_EXS, REF_EXS)

    datarow: 
    index	question	ans	correct_pred	wrong_pred	correct_sol	correct_model	wrong_sol	wrong_model

    '''
    assert mode in ['select_reflect', 'select_act', 'reflect']
    if mode == 'select_reflect':
        shot = PromptStr(SEL_REF_EXS)
    elif mode == 'select_act':
        shot = PromptStr(SEL_ACT_EXS)
    else: # mode == reflect
        shot = PromptStr(REF_EXS)
    
    for tagname in shot.get_placeholder_names():
        key = tagname.lower()
        if key in datarow.keys():
            shot = shot.sub(tagname, datarow[key])

    return shot

def get_fewshots_string(datarows:Sequence[Mapping], 
                        mode:str='')->PromptStr:
    assert mode in ['select_reflect', 'select_act', 'reflect']
    return PromptStr(
        '\n\n'.join([a_fewshot_prep(datarow, mode) for datarow in datarows])
        )


def fill_selection(reflection_exs:str='', 
                   action_exs:str='', 
                   question:str='')->PromptStr:
    '''
    reflection_fs and action_fs
    + question of interest
    '''
    # if actions_fs: # process SEL_TMP
    prompt = PromptStr(SEL_TMP)
    prompt = prompt.sub('REFLECTION_EXS', reflection_exs)
    prompt = prompt.sub('ACTION_EXS', action_exs)
    prompt = prompt.sub('QUESTION', question)

    # print(prompt.get_placeholder_names())
    return prompt

def fill_reflection(reflection_exs:str='',
                    datarow:str='')->PromptStr:
    '''
    reflection_fs and
    + data to reflect (datarow)
    '''
    prompt = PromptStr(REF_TMP)
    prompt = prompt.sub('REFLECTION_EXS', reflection_exs)
    for ph in prompt.get_placeholder_names():
        key = ph.lower()
        if key in datarow.keys():
            prompt = prompt.sub(ph, datarow[key])
    return prompt
        

def main(outdir='3_prompts_for_manual_fill'):
    models = ['cot', 'pal', 'p2c']
    
    outdir = Path(outdir)
    if not outdir.exists():
        outdir.mkdir(parents=True, exist_ok=True)
    for idx in range(3): # try three compositions from the examples
        datarows = []
        # get datarows: all 6 model switching cases 
        for (wm, cm) in product(models, models):
            if wm == cm:
                continue
            sheetname = f"{wm}_wrong_{cm}_correct"
            df = FS_D[sheetname]
            row = df.iloc[idx]
            # print(wm, cm, idx, row)
            datarows.append(row)
        sel_ref_exs = get_fewshots_string(datarows, mode='select_reflect')
        sel_act_exs = get_fewshots_string(datarows, mode='select_act')
        ref_exs = get_fewshots_string(datarows, mode='reflect') 
        # save almost-done prompt
        s_prompt_temp = fill_selection(reflection_exs=sel_ref_exs, action_exs=sel_act_exs, question='[QUESTION]')
        r_prompt_temp = fill_reflection(reflection_exs=ref_exs, datarow={})
        
        with open(outdir/f"reflection_prompt_{idx}.txt", 'w') as rf, open(outdir/f'selection_prompt.txt_{idx}', 'w') as sf:
            sf.write(s_prompt_temp)
            rf.write(r_prompt_temp)
        print(f'saved to {str(outdir)}')


          
            
def preptest(outdir='3_prompts_for_manual_fill/test'):
    '''
    check whether the prompts works as expected
    expected:
        1. selection prompt generates:
            - hint that hints about correct model
            - selects correct model
        2. reflection prompt generates:
            - reflection that pincets what's gone wrong
            - hints that hints the model selection
    '''
    outdir = Path(outdir)
    if not outdir.exists():
        outdir.mkdir(parents=True, exist_ok=True)
    models = ['cot', 'pal', 'p2c']
    r_tmp = PromptStr(open(outdir.parent / 'reflection_prompt_0_1.txt').read())
    s_a0shot = PromptStr(open(outdir.parent / 'selection_prompt_0_1.txt').read())
    s_a6shot = PromptStr(open(outdir.parent / 'selection_prompt_0_1_action_fewshots.txt').read())
    for w, c in product(models, models):
        if w==c:
            continue
        sheet_name = f"{w}_wrong_{c}_correct"
        df = FS_D[sheet_name]
        df = df[3:]
        # complete prompts 
        prompt_records = [] 
        for i, row in df.iterrows():
            s_prompt_0 = s_a0shot # highy suspected...
            s_prompt_fs = s_a6shot
            r_prompt = r_tmp
            fill = partial(fill_placeholders, datarow=row)
            s_prompt_0, s_prompt_fs, r_prompt = map(fill,[s_prompt_0, s_prompt_fs, r_prompt])
            obj = {'selectprompt_0': s_prompt_0, 'selectprompt_fs': s_prompt_fs, 'reflectprompt': r_prompt}
            prompt_records.append(obj)
            # check whether the prompt contains the question
            assert row.question in s_prompt_0
            assert row.question in s_prompt_fs
            assert row.question in r_prompt         
        test_data = df.to_dict(orient='records')
        with jsl.open(outdir/f'{sheet_name}_prompt.jsonl', 'w') as writer, jsl.open(outdir/f'{sheet_name}_data.jsonl', 'w') as writer2:
            writer.write_all(prompt_records)
            writer2.write_all(test_data)
        print(f'saved to {str(outdir)}')

        
def fill_placeholders(prompt:PromptStr, datarow:dict)->PromptStr:
    for ph in prompt.get_placeholder_names():
        key = ph.lower()
        if key in datarow.keys():
            prompt = prompt.sub(ph, datarow[key])
    return prompt  
    
def test(outdir='3_prompts_for_manual_fill/test'):
    outdir = Path(outdir)
    preptest()


if __name__ == '__main__':
    # Fire(main)
    Fire(test)

        
        
    
    