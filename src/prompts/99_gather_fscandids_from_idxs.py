
import jsonlines as jsl
import pandas as pd

def main(
        idxf = '98_switching_for_wrongtocorrect.jsonl',
        testset = '../../dataset/gsm8K_test.jsonl'
        ):
    testdf = pd.DataFrame(jsl.open(testset))
    idxdf = pd.DataFrame(jsl.open(idxf))
    models = ['cot', 'pal', 'p2c']
    for m in models:
        for n in models:
            if m==n: continue