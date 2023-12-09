FNAME='3_blurb_-1.json'
OUTNAME = f"{FNAME}_print.txt"

import json
d = json.load(open(FNAME))



with open(OUTNAME, 'w') as wf:
    for k,txtlst in d.items():
        if k.endswith('_genonly'):
            if 'p2c' in k:
                continue
            print(k, file=wf)
            for l in txtlst:
                print("-"*20, file=wf)
                print(l, file=wf)
    print("="*20, file= wf)
    print("="*20, file=wf)
    for k,txtlst in d.items():
        if 'p2c' in k:
            continue
        if not k.endswith('_genonly'):
            print(k, file=wf)
            for l in txtlst:
                print("-"*20, file=wf)
                print(l, file=wf)
    
