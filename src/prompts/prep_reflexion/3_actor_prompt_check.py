import pandas as pd
import yaml
from itertools import product
import jsonlines as jsl
from typing import Sequence, Mapping

'''
read: 
- 2_good_examples_from_*xlsx
- 3_model_select_fs_prompt.yaml
- 3_reflect_fs_prompt.yaml
out:
several
- model select prompts (manual fill-in still left)
- reflection prompts (manual fill-in left)

--> need to manually fill Hints: and Reflections parts 
--> See those work properly on several questions

'''

FS_D = pd.read_excel('2_good_examples_from_gsm_test.xlsx', sheet_name=None)
SELECT_YML = yaml.full_load('3_model_select_fs_prompt.yaml')
SEL_TMP = SELECT_YML['prompt_template']
SEL_REF_EXS = SELECT_YML['reflection_exs']
SEL_ACT_EXS = SELECT_YML['action_exs']

REFLECT_YML = yaml.full_load('3_reflect_fs_prompt.yaml')
REF_TMP = REFLECT_YML['prompt_template']
REF_EXS = REFLECT_YML['reflection_1']
        

class PromptStr:
    '''
    class for prompt string (with some utility method)
    '''
    def __init__(self, template_str:str):
        self._template = template_str
    def __str__(self):
        return self._template
    def sub(self, 
            placeholder_name:str, 
            tobe:str):
        self._template = self._template.replace(f"[{placeholder_name}]", tobe)
    def get_placeholder_names(self) -> list:
        return re.findall(r"\[(.*?)\]", self._template)


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
    
    for tagname in prompt.get_placeholder_names():
        key = tagname.lower()
        shot.sub(tagname, datarow[key])

    return shot

def get_fewshots_string(datarows:Sequence[Mapping], 
                        mode:str='')->PromptStr:
    assert mode in ['select_reflect', 'select_act', 'reflect']
    return PromptStr(
        '\n\n'.join([a_fewshot_prep(datarow, mode) for datarow in datarows])
        )


def fill_selection(reflection_exs:str='', 
                   action_exs:str='', 
                   question:str = '')->PromptStr:
    '''
    SEL_TMP needs reflection_fs and action_fs
    REF_TMP needs only reflection_fs
    '''
    if actions_fs: # process SEL_TMP
        prompt = PromptStr(SEL_TMP)
        prompt.sub('REFLECTION_EXS', reflection_exs)
        prompt.sub('ACTION_EXS', action_exs)
        prompt.sub('QUESTION', question)
    else: # process REF_TMP 
        prompt = PromptStr(REF_TMP)
        prompt.sub('REFLECTION_EXS', reflection_exs)
        prompt.sub('QUESTION', question)

    print(prompt.get_placeholder_names())
    return prompt
        



def main():
    
    models = ['cot', 'pal', 'p2c']

    for idx in range(3): # try three compositions from the examples
        for (wm, cm) in product(models, models):
            if wm == cm:
                continue
            sheetname = f"{wm}_wrong_{cm}_correct"
            df = fs_pool_dict[sheetname]
            row = df.iloc[idx]
            
            fs = {}
        
        
    
    