import yaml
from fire import Fire
import pandas as pd
import jsonlines as jsl
from pathlib import Path
from itertools import combinations 
from collections import defaultdict

def main():
    # read yaml --> Dict[str, Dict[str, pd.DataFrame]]
    '''
        m2p2d:
        model
            path
                datafrmae
    '''
    with open('nov11_0_files.yaml') as f:
        paths = yaml.full_load(f)
        m2p2d = dict()
        m2p2d['chatgpt'] = {p:pd.DataFrame(jsl.open(p)) for p in paths['chatgpt']['2models']}
        m2p2d['gpt4'] = {p:pd.DataFrame(jsl.open(p)) for p in paths['gpt4']['2models']}
    
    results = []
    for model, p2d in m2p2d.items(): 
        for (p1, p2) in combinations(p2d.keys(), 2):
            df1, df2 = p2d[p1], p2d[p2]      
            df1.index = df1['index'] # index column to dataframe index
            df2.index = df2['index'] # index column to dataframe index
            common_idx = set(df1.index).intersection(set(df2.index)) # check if index is the same
            common_idx_ = sorted(list(common_idx))
            df1 = df1.loc[common_idx_ ]
            df2 = df2.loc[common_idx_]
            dropped_idx = set(range(1319)) - common_idx
            
            pal_gen_consistent = (df1.pal_generated.apply(lambda lst: lst[0].strip()) == df2.pal_generated.apply(lambda lst: lst[0].strip())).sum()
            cot_gen_consistent = (df1.cot_generated.apply(lambda lst: lst[0].strip()) == df2.cot_generated.apply(lambda lst: lst[0].strip())).sum()
            pal_ans_consistent = (df1.pal_executed.apply(lambda lst: lst[0]) - df2.pal_executed.apply(lambda lst: lst[0])).abs() < 1e-3
            cot_ans_consistent = (df1.cot_executed.apply(lambda lst: lst[0]) - df2.cot_executed.apply(lambda lst: lst[0])).abs() < 1e-3 
            pal_ans_consistent = pal_ans_consistent.sum()
            cot_ans_consistent = cot_ans_consistent.sum()
            
            resd = dict()
            resd['model'] = model 
            resd['pair'] = (p1, p2)
            resd['drop_idx'] = list(dropped_idx)
            resd['record_size'] = len(common_idx)
            resd['pal_gen_consistent'] = pal_gen_consistent
            resd['cot_gen_consistent'] = cot_gen_consistent
            resd['pal_ans_consistent'] = pal_ans_consistent
            resd['cot_ans_consistent'] = cot_ans_consistent
            results.append(resd)
    df_fin = pd.DataFrame(results)
    xl = pd.ExcelWriter('nov11_0_conflicts_check.xlsx')
    df_fin.to_excel(xl)
    xl.close()
    print(df_fin)
    print("wrote to nov11_0_conflicts_check.xlsx")
        
            
        

if __name__ == '__main__':
    Fire(main)