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

    input_path = args.input_path
    dataset_type = args.dataset_type

    output_data = jsonlines_load(input_path)

    total = 0
    correct = 0
    error = 0
    for i in range(len(output_data)):
        if dataset_type == 'math':
            if output_data[i]['majority_ans'] is not None:
                if abs(output_data[i]['majority_ans'] - output_data[i]['answer']) < 1e-3:
                    correct += 1
            else:
                error += 1

        else:
            if output_data[i]['final_ans'] == output_data[i]['answer']:
                correct += 1
            else:
                error += 1

        total += 1

    df = pd.DataFrame(output_data)
    m_cor = (df.answer == df.majority_ans)
    m_wro = ~m_cor
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
        f'Accuracy: {correct/total}, Total: {total}, Correct: {correct}, Error: {error}')
