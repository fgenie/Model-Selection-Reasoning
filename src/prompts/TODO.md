# readme
- My whole picture for prompting and the reasonings to implement the reflexion-agent of ours (`reflexion-kshot-harvesting`?) is depicted on `actor_model_select_prompt.yaml` and `actor_reflect_prompt.yaml`. 
- Note: `scratch.py` (code skeletone presented in the last meeting) and `actor__promt_IDEATION.yaml` is outdated for now.

## initial idea
- make a chimera of reflexion and [progressive hint prompting](https://arxiv.org/abs/2304.09797) for 
`reflexion-kshot-harvesting` somehow. Ours does not do reflection during inference but it would somehow improve its performance. Look at the [OPRO](https://arxiv.org/abs/2309.03409) case... **hopefully** it will learn sth.

## now
- Our method **does not reflect during the inference**. To make use of *k-shot harvested reflections trajectory* for our agent during inference, **[CoH](https://arxiv.org/abs/2302.02676)** style prompting (kind of conditional language modeling) will help. (see `actor_model_select_prompt.yaml`)
- This experiments is getting sophisticated... modularly add progressive hint prompting **after implementing model-switching reflexion agent**
- or we need evaluation guess prompt and loops on inference (*rejected but could be an alternative*) 

## algorithm sketch
1. `actor_reflect_prompt.yaml` will be used for k-shot reflection harvesting. harvest reflections and hint throughout the k questions in the train split of gsm8k. If available, reflect until the question gets correct or it gets fails on three method, give it up (or retry with progressive hint prompting: `re_query_*()` or it will distract the actor learning relation between question and the model to be sampled) (`actor_reflect_prompt.yaml`)
2. Use the output of `1.`, inference through the test split. No reflection, no loop. Sample a method for reasoning with CoH style-prompting and go on to solve the question with the sampled method. (`actor_model_select_prompt.yaml`)


----
# TODO for the exp.
- [x] code utils for trainset prep
- [ ] need `try-except` for other modes than `--custom_prompt` (removed `while True:try-except` from `__main__`)
- [ ] implement `reflexion_kshot_harvesting` (`scratch.py`)  -- constructing an agent with the prompts.
    - [x] prompt qualitative test (`src/prompts/prep_reflexion/*`)
    - `scratch.py`: (currently outdated, presented in the last meeting): pseudo code for `k-shot harvesting`, containing both concepts of `model-switching` and `retrying` at the same time.  
    - [x] explore the details of Reflexion prompting (code): `scribbles on actor_prompt.yaml`
    - [x] imitate the reflexion prompt to configure gsm-harvesting prompt (+CoH prompt)
        - [x] `verbose`
        - [ ] `concise` 
    - [x] switching models (reflexion)
        - [x] could they be complimentary to each other?  `99_aretheycomplimentary.py` --> yes switching models can help! (model-selection paper also proves this)
        - [x] inspect the exclusive questions for each reasoning method to figure out the weakness or strength of the reasoning method 
- [x] attest your oracle actor prompt against gsm8k
    - [x] 1. actor only selects
        - reflection_prompt_0_1
        - selection_prompt_0_1_nobiassys
    - [x] 2. actor selects and injects hint when querying chosen method
    - [ ] 3. refer to solution before actor selection
    - [x] 3. generating further to complete solution
    - additional analyses...
        - [ ] verbose selection: bias? (actor_prompt_selection test)
        - [ ] how actual results being biased?
    - tweaks and concerns
        - [x] ablate p2c and try the same
        - [ ] model selection with 3 models?
        - [ ] update previous ablations...(chatgpt get updates)
- [x] Glue functions in `scratch.py` to `src/selection_math.py`.
    - [x] debug


