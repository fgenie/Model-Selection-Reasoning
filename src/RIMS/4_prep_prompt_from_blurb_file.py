import json
from fire import Fire 

def main(blurb_f:str = '3_blurb_-1.json',
         include_noreflection:bool=False,
         include_noswitching:bool=False,
         n_repeat:int=1,
         from_back:bool=True, # from longest to shortest (blurb_f sorted in this way, using the solution length)
         ):
    d = json.load(open(blurb_f))
    if from_back:
        d = {k:sorted(v, reverse=True) for k,v in d.items()}
    
    picked_blurbs = dict()
    for k,v in d.items():
        idxs = range(0, len(v), len(v)//n_repeat)[:n_repeat]
        picked_blurbs[k] = [v[i] for i in idxs]
        picked_blurbs[k+"idxs"] = idxs
    

    # mind the idices already used above!
    if include_noreflection:
        # just pick the correct solution and make it into a no-reflection blurbs
        
    if include_noswitching:
        raise NotImplementedError(f'need to prepare the no_switching case into {blurb_f=} first')