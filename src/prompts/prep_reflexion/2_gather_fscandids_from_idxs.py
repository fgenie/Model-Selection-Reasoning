
import jsonlines as jsl
import pandas as pd
from itertools import product
from fire import Fire

def df_entry_cleaner(df):
    '''
    if an entry: 
    list of length 1 --> pop()
    or
    empty list --> drop the column
    '''
    for col in df.columns:
        if isinstance(df[col][0],list):
            if len(df[col][0])==1:
                df[col] = df[col].apply(lambda x: x[0])
            elif len(df[col][0])==0:
                df[col] = ''
    return df 

def alternate_flatten(records:list):
    newrecords = []
    records = list(records)
    for row in records:
        wrong_models = row['wrong']
        idx1, idx2 = [], []
        idxs = row['idxs_test']
        for i, idx in enumerate(idxs):
            if i%2==1:
                idx1.append(idx)
            else:
                idx2.append(idx)
        row1 = row.copy()
        row2 = row.copy()
        row1['wrong'] = wrong_models[0]
        row2['wrong'] = wrong_models[1] 
        row1['idxs_test'] = idx1
        row2['idxs_test'] = idx2  
        newrecords.append(row1)
        newrecords.append(row2)
    assert len(newrecords) == 2*len(records)
    return newrecords


def main(
        idxf = '1_onlyone_correct.jsonl',
        cotjsl='/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/cot.jsonl',
        paljsl='/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0910_ablation_result/pal.jsonl',
        p2cjsl='/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/expresults/0924_plancode_v2_abl/gsm8k_k8_sc1_s0_e1319_09_24_01_16.jsonl',
        outxl= '2_good_examples_from_gsm_test.xlsx',
        ):
    models = ['cot', 'pal', 'p2c']
    modelouts = [cotjsl, paljsl, p2cjsl ]
    modelsdf = { # open cotjsl, paljsl, p2cjsl
        m: pd.DataFrame.from_records(list(jsl.open(jslf)), index='index') for m, jslf in zip(models,modelouts)
    }
    modelsdf = { # clean up the entries
        m: df_entry_cleaner(df) for m, df in modelsdf.items()
    }

    # some processings for p2c output
    modelsdf['p2c'] = modelsdf['p2c'].rename(columns=lambda x: x.replace('pal_', 'p2c_')) # rename column
    modelsdf['p2c'].p2c_generated = modelsdf['p2c'].plan + '\n' + modelsdf['p2c'].p2c_generated
    print(modelsdf['p2c'].p2c_generated)

    # for every entry in modelsdf, unlist list of length 1
    idxdf = pd.DataFrame(jsl.open(idxf))
    if isinstance(idxdf['wrong'].iloc[0], list):
        idxdf = pd.DataFrame(alternate_flatten(jsl.open(idxf)))



    wrong_correct_modelpairs = product(models, models)
    xl = pd.ExcelWriter(outxl)
    for wmodel, cmodel in wrong_correct_modelpairs:
        if wmodel == cmodel:
            continue
        # get the idxs of interest
        mask = (idxdf['wrong']==wmodel) & (idxdf['correct']==cmodel)
        # check if cdf and wdf have all the idxs (some cases they drop one or two)
        filtered_idxs = sorted(idxdf[mask].idxs_test.item())
        wdf = modelsdf[wmodel].copy()
        cdf = modelsdf[cmodel].copy()
        filtered_idxs = [i for i in filtered_idxs if i in wdf.index and i in cdf.index]

        
        wdf['wrong_sol'] = wdf[f"{wmodel}_generated"]
        wdf['wrong_pred'] = wdf['majority_ans'] 
        cdf['correct_sol'] = cdf[f"{cmodel}_generated"] 
        cdf['correct_pred'] = cdf[f"majority_ans"] 

        df = pd.DataFrame({
            'question': cdf.question,
            'ans': cdf.answer,
            'correct_pred': cdf.correct_pred,
            'wrong_pred': wdf.wrong_pred,
            'correct_sol': cdf.correct_sol,
            'correct_model': cmodel,
            'wrong_sol': wdf.wrong_sol,
            'wrong_model': wmodel,
        }, index = cdf.index).loc[filtered_idxs, :]
        
        sheet = f"{wmodel}_wrong_{cmodel}_correct"
        df.to_excel(xl, sheet_name=sheet)
    print(f"saved to {outxl}")
    xl.close()


if __name__ == '__main__':
    Fire(main)