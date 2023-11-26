import yaml
from string import Template 
from pathlib import Path 
import jsonlines as jsl
import pandas as pd

yamld = yaml.full_load(open('prompt_generate_reflection_forceformat.yaml'))
jslf= 'dbg_test_prompt.jsonl' # resolved output contained 
records = list(jsl.open(jslf)) # pd.json_normalize() does not work
tmp = Template(yamld['user'])


ABB2FULL = {'pal': 'Program-aided Language Modeling', 'cot': "Chain-of-Thought", "p2c": "Plan-and-then-Code"}

# df = pd.DataFrame(records)
def flatten_retries(row):
    for retry_d in row['retries']:
        retrymethod = retry_d['method']
        retry_d = {f"retry_{k}_{retrymethod}":v for k,v in retry_d.items()}
        row.update(retry_d)
    return row
records = [flatten_retries(row) for row in records]
# df = pd.DataFrame(records)
# df_ = pd.json_normalize(df) # does not work


for row in records:
    for k in row.keys():
        if k.startswith('retry_correct_solution_') and row[k]: 
            wrong_method = row['fail_method']
            wrong_method = ABB2FULL[wrong_method] + f" ({wrong_method})"
            wrong_solution = row['fail_solutions'][0]
            wrong_pred = row['fail_preds'][0]
            ans = row['ans']
            correct_method = k.replace('retry_correct_solution_', '')
            correct_pred = row[f'retry_correct_prediction_{correct_method}'] # float or str
            correct_method = ABB2FULL[correct_method] + f" ({correct_method})"
            correct_solutions = row[k]
            question = row['question']
            print(f"{wrong_method=}")
            print(f"{correct_method=}\n\n")

            '''
                Question: $QUESTION
                Approach: $WRONG_METHOD
                Attempt: $WRONG_SOLUTION
                Answer: $WRONG_PRED
                Evaluation: Wrong (correct answer: $ANS)
                Mistakes: <one_liner_explanation_for_whats_gone_wrong_in_the_attempt>
                Hint to Workaround: <one_liner_hint_to_workaround_with_different_approach>
                Workarund Approach: $CORRECT_METHOD
                Correct Attempt: $CORRECT_SOLUTION
                Answer: $CORRECT_PRED
                Evaluation: Correct
            '''
            for cs in correct_solutions:
                cp = correct_pred 
                wp = wrong_pred
                ws = wrong_solution
                userprompt = tmp.substitute(QUESTION = question, WRONG_SOLUTION = ws, WRONG_PRED = wp, ANS = ans, CORRECT_SOLUTION = cs, CORRECT_PRED = cp, WRONG_METHOD = wrong_method, CORRECT_METHOD = correct_method)
                print(userprompt)
                print('='*20)
                print("\n\n")
        else:
            continue




