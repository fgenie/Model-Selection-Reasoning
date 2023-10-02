TODO for the exp.
- [x] code utils for trainset prep
- [ ] complete `kshot_harvesting` -- constructing a reflexion-variant for model-selection or retrying with the same prompt.
    - [x] explore the details of Reflexion prompting: `scribbles on actor_prompt.yaml`
    - [ ] how to discipline actor reflection with fewshot-reflection example prompt? my fewshot prompt for reflection will guide the reflection of the actor explicitly. --> look at gsm8k wrong.csv to get some hints. What is the weakpoint of CoT, PAL? When they get wrongdo sth and when they do not? --> could they be complimentary to each other?
        - [ ] changing to another model example (e.g. cot -> pal)
        - [ ] retrying the model example (e.g. cot -> cot again)
    - [ ] two modes of kshot_harvesting return (1) simple / (2) whole
- [ ] Glue the codes on `scratch.py` to `src/selection_math.py`.
    - [ ] `re_query_*()` functions
- [ ] debug
- [ ] improve prompts


