# TODO (였던 것)
* p2c_v1이 좋았던 건 포맷 때문일까 fewshot example (코딩 등 수기 예제) 때문이었을까? --> v2에 차용 가능
* p2c_v1 + cot 의 gsm8k full set에서의 성능은 어떨까?
* coh에서 failed method solution 을 쓰도록 하고 answer, evaluation까지 쓰게 해서 correct가 나오면 그걸로 답을 제출하도록 해볼까? 그게 나으려나? (이 경우 스탠다드한 fewshot 이 됨)
    * solution까지 보고 selection 하도록 하는 프롬은 어떻게 만들어야 모델 셀렉션과 좀 달라보일까. reflection과 chimera 되어있고 p2c가 포함되어 있다는 점이 다른가?
    * 사실은 위의 coh 변형도 solution보고 셀렉션을 하는 케이스 아닐까?
    * 이렇게 하면 사실 evaluation까지 시키는 것이기도 하다. 
* 모델 세 개로 selection을 하는 경우 성능은?
* model selection 방법의 개선폭이 미미해보이지만 생각보다 그런 개선을 이뤄내기가 쉬운 것도 아니다. solution만 보고 selection하는건 llm이 어느정도 효과를 발휘 (\<1.5\% for `gpt-3.5-turbo, temperature=0.`) 하고 있다고 봐야한다.


<details>
    <summary> click to expand </summary>

- My whole picture for prompting and the reasonings to implement the reflexion-agent of ours (`reflexion-kshot-harvesting`?) is depicted on `actor_model_select_prompt.yaml` and `actor_reflect_prompt.yaml`. 
- Note: `scratch.py` (code skeletone presented in the last meeting) and `actor__promt_IDEATION.yaml` is outdated for now.


   
## initial idea
- ~~make a chimera of reflexion and [progressive hint prompting](https://arxiv.org/abs/2304.09797) for ~~
`reflexion-kshot-harvesting` somehow. Ours does not do reflection during inference but it would somehow improve its performance. Look at the [OPRO](https://arxiv.org/abs/2309.03409) case... **hopefully** it will learn sth.


## now
- Our method **does not reflect during the inference**. To make use of *k-shot harvested reflections trajectory* for our agent during inference, **[CoH](https://arxiv.org/abs/2302.02676)** style prompting (kind of conditional language modeling) will help. (see `actor_model_select_prompt.yaml`)
- This experiments is getting sophisticated... modularly add progressive hint prompting **after implementing model-switching reflexion agent**
- or we need evaluation guess prompt and loops on inference (*rejected but could be an alternative*) 

</details>

## algorithm sketch (still valid)
1. `actor_reflect_prompt.yaml` will be used for k-shot reflection harvesting. harvest reflections and hint throughout the k questions in the train split of gsm8k. If available, reflect until the question gets correct or it gets fails on three method, give it up ~~(or retry with progressive hint prompting: `re_query_*()` or it will distract the actor learning relation between question and the model to be sampled) (`actor_reflect_prompt.yaml`)~~
2. Use the output of `1.`, inference through the test split. No reflection, no loop. Sample a method for reasoning with CoH style-prompting and go on to solve the question with the sampled method. (`actor_model_select_prompt.yaml`)


----
# TODO for the exp.
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
    - [ ] 3. refer to solution before actor selection (CHUL oct15)
    - [x] 4. generating further to complete solution (ME oct17: CoH)
        - [ ] do for k=2,4
        - [ ] generate failed solution too...?
    - additional analyses...
        - [x] verbose selection: bias? (actor_prompt_selection test)
        - [ ] how actual results being biased?
    - tweaks and concerns
        - [x] ablate p2c and try the same
        - [ ] model selection with 3 models?
        - [ ] update previous ablations...(chatgpt get updates)

