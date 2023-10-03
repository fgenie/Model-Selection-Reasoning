TODO for the exp.
- [x] code utils for trainset prep
- [ ] complete `kshot_harvesting` -- constructing a chain of prompts.
    - [x] explore the details of Reflexion prompting: `scribbles on actor_prompt.yaml`
    - [x] how to discipline actor reflection with fewshot-reflection example prompt? my fewshot prompt for reflection will guide the reflection of the actor explicitly. --> look at gsm8k wrong.csv to get some hints. What is the weakpoint of CoT, PAL? When they wrongdo sth and when they doa'right? --> could they be complimentary to each other? `99_aretheycomplimentary.py` --> yes switching models can help!
    - [x] get some good model switching cases 
        - [ ] (also check their patterns if it's apparent)
    - [ ] two modes of kshot_harvesting return (1) concise / (2) verbose history
- [ ] Glue the codes on `scratch.py` to `src/selection_math.py`.
    - [ ] `re_query_*()` functions
- [ ] debug
- [ ] improve prompts


