While preparing the reflexion-kshot-harvesting prompt, I report some numbers we can expect from the previous ablations.

Our kshot-harvesting agent needs a prompt that invokes a decision from the followings.
For better solution the agent should...
- switch the model (e.g. cot -> pal)
- retry the model (e.g. cot -> cot)

To prepare the prompt, I've explored ablation (single-modeled results) on gsm8k (to see realistic cases for model switching)

(condition chatgpt, greedy sampling, standard few-shot prompts for gsm8k)

> When greedily decoded, how many each models get wrong over 1319 questions?

pal: 268
p2c: 381
cot: 279


> Do they fail on the same questions? no

len(pal_wrongs.intersection(p2c_wrongs))=192
len(pal_wrongs.intersection(cot_wrongs))=147
len(p2c_wrongs.intersection(cot_wrongs))=181


> What is the lowerbound of the error rate using three models above optimally? 9.02% (=119/1319)

len(pal_wrongs.intersection(p2c_wrongs).intersection(cot_wrongs))=119