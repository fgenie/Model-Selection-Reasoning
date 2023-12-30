from itertools import product, permutations
from collections import Counter 
import json


FNAME='2_blurb_-1.json'
d = json.load(open(FNAME))


# each method in a prompt need to be once wrong and once correct --> this constraint makes possible directions (6 -> 3) 
methods = 'cot pal p2c'.split()
correct_candids = methods
wrong_candids = methods


def flatten(lst_pairs)->list:
    flat = []
    for pair in lst_pairs:
        flat.extend(list(pair))
    return flat

def tuplst2strlst(lst_pairs)->list:
    return [f"{tup[0]}2{tup[1]}" for tup in lst_pairs] 

# the function below will make 3-pairs-sequence possibly drawn each from correct_candids and wrong_candids, each pair cannot be a pair of two identical string. The resultant 3-pairs-sequence need to contain all the elements in correct_candids exactly twice (i.e. [(p2c, pal), (pal, cot), (cot, p2c)] is valid, where [(p2c, pal), (p2c, cot), (pal, cot)] is not valid))])
def possible_sequences(correct_candids:list, wrong_candids:list)->list:
    # make all possible pairs
    all_directions = list(product(correct_candids, wrong_candids))
    # remove same2same
    directions = [d for d in all_directions if d[0]!=d[1]]
    # make possible 3-pairs-sequences
    sequences = list(permutations(directions, 3))
    # remove sequences that depicts one method better than the others (i.e. cot is 3 times correct while pal corrects only once)
    sequences = [s for s in sequences if set(Counter(flatten(s)).values())=={2} ]
    # (method1, method2) --> {method1}2{method2}
    directions_fin = [tuplst2strlst(s) for s in sequences]
    return directions_fin

possible_comps = possible_sequences(correct_candids, wrong_candids) # 48 distinct prompt compositions possible... we just pick 9 of those...
# pick 9 of above list with even intervals within same start
starts2possibles = {
    method: [s for s in possible_comps if s[0].startswith(method)] for method in methods
}
picked_9 = {k: v[::len(v)//3] for k,v in starts2possibles.items()}

# make 9 prompts


