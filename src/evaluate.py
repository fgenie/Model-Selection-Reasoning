import argparse
from tool import *
from pathlib import Path 
import pandas as pd 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True)
    parser.add_argument('--dataset_type', type=str,
                        choices=['math', 'date'], required=True)
    args = parser.parse_args()

    if '*' in args.input_path:
        candids = [p for p in Path().glob(args.input_path)]
        if len(candids)>1:
            raise ValueError(f"More than path found: {candids}")
        elif len(candids)==0:
            raise ValueError(f"No path found: {args.input_path}")
        else:
            print(f"interpret\n\t--input_path {args.input_path}\n\t->{candids[0]}")
            args.input_path = candids[0]
            print(args.input_path)


    input_path = args.input_path
    dataset_type = args.dataset_type

    output_data = jsonlines_load(input_path)


    datadf = pd.DataFrame(output_data)
    if dataset_type == 'math': # gsm8k here
        corrects = datadf.majority_ans.sub(datadf.answer) < 1e-3
    else:
        corrects = (datadf.final_ans == datadf.answer)

    acc = corrects.mean()
    ncorr = corrects.sum()
    nwro = (~corrects).sum()

    df = pd.DataFrame(output_data)
    m_cor = corrects
    m_wro = ~corrects
    assert (m_cor.sum() + m_wro.sum()) == len(df)
    ip = Path(input_path)
    fname = f"{ip.parent/ip.stem}_$$.csv"
    fcor = fname.replace("$$", 'correct')
    fwro = fname.replace("$$", 'wrong')
    df_cor = df[m_cor].loc[:, ['index', 'majority_ans', 'answer', 'question']]
    df_wro = df[m_wro].loc[:, ['index', 'majority_ans', 'answer', 'question']]

    df_cor.to_csv(fcor, index=False)
    df_wro.to_csv(fwro, index=False)

    print(
        f'Accuracy: {acc:.3f}, Total: {len(datadf)}, Correct: {ncorr}, Error: {nwro}')
