import pandas as pd
import jsonlines as jsl
from pathlib import Path
from fire import Fire
import yaml

def main(outf:str='nov11_1_onemethod_acc.txt'):
    
    # read data from yaml
    with open('nov11_0_files.yaml') as f:
        paths = yaml.full_load(f)
        m2p2d = dict()
        m2p2d['chatgpt'] = {p:pd.DataFrame(jsl.open(p)) for p in paths['chatgpt']['3models']}
        m2p2d['gpt4'] = {p:pd.DataFrame(jsl.open(p)) for p in paths['gpt4']['3models']}
    
    # m2p2d --> one big db
    dfbins = []
    for model in m2p2d.keys():
        for p in m2p2d[model].keys():
            df = m2p2d[model][p] 
            df['model'] = model
            df['filepath'] = p
            df = df.loc[:, ['model', 'filepath', 'index', 'answer', 'pal_executed', 'cot_executed', 'p2c_executed', 'pal_generated', 'cot_generated', 'p2c_generated']]
            dfbins.append(df)
    df = pd.concat(dfbins, axis = 'index')
    
    # measure ablation success rate
    res_d = dict()
    for method in 'cot pal p2c'.split():
        key = f'{method}_executed'
        method_d = dict()
        for model in 'chatgpt gpt4'.split():
            df_ = df[df.model == model]
            pred = df_[key].apply(lambda lst: lst[0])
            ans = df_.answer
            corrects = (pred - ans).abs() < 1e-3
            acc = corrects.sum()/1319
            acc_literal = f"{int(corrects.sum())}/1319 ({acc:.3f})"
            method_d[model] = acc_literal
        res_d[method] = method_d
    df_fin = pd.DataFrame(res_d)
    table_str = df_fin.to_markdown()
    with open(outf, 'w') as fw:
        fw.write(table_str)
    print(f'wrote to {outf}')


    return 


if __name__ == '__main__':
    Fire(main)  
