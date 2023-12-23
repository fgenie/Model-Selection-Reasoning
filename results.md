### last week training blurb prep.
```
# current learning loop: only-1-reflection blurbs prep

1. collect hard questions 
    - (`wrong solutions` are collected at the same time)
2. (with naive retries with T=1.0), sample correct solution
3. sample reflection and hint that bridges `q`, `wrong solution`, and `correct solution`
4. finalize 
    - `blurb` = q + wrong solution + reflection + hint + correct solution
    - `prompt-0` = sysmsg + blurb + instruction (end)
```
### try this week
```python
# expand blurbs on hard questions (blurb: only 1 reflection --> more than 1 reflection) 

response = llm(prompt_0, q)
if not eval( parse_final_ans(response), ans_GT) and did_reflect(response):
    blurb_1_refl = strip_last_eval_str(response)
    solved = False
    while not solved:
        response_new = llm(prompt_0, q)
        solved = eval( parse_final_ans(response_new), ans_GT)
    blurb_2_refl = (blurb_1_refl + response_new)
elif:
    ...
else: 
    ...

newprompt = promptify(blurb_2_refl) # newprompt contains the blurb that has more than 1 reflection.         
```       


## Dec 9-10:
- prompt structure: Evaluation and reflection at once.
    ```
    ${SYSTEM PROMPT}

    ${BLURBS}
        - no-reflection (cot, pal each 1, total 2):
            1st attempt -> eval (success)
        - reflection (if k=2 --> cot2pal + pal2cot):
            1st attempt -> eval -> mistake (diagnosis) -> hint (for a new method) -> 2nd attempt -> eval

    ${INSTRUCTION}
    ${QUESTION}
        - format guide removed
    ```
    
- blurb preparation
    1. gather questions (length evenly, 30 questions)
    2. find failing questions (try 3 times with pal or cot T=1.0 -- standard k=5 fewshot prompting, pick it when >= 0.5 times wrong)
    3. try gather correct solution with alternative method. try 5 times with standard fewshot prompting until it gets correct solution
    4. with the correct and wrong solution, generate `mistakes` (what was wrong) and `hint` (in what aspect altering the method will help) 
    ```
        # 0. how blurbs look like 
        Attempt: <generated solution from standard-fewshot cot/pal -- tried three times, when wrong >= 0.5 frequency>
        Answer: <parsing / execution >
        Evaluation: Wrong (answer --)
        Mistakes: <generated from wrong2correct solutions>
        Corrected Attempt: <generated solution from standard-fewshot cot/pal -- reattempting with T=1.0>
        Answer: <continued from above>
        Evaluation: Correct
    ```
- llm response: generated at once 
    ```
    # 1. reflection
    Attempt: 
    Answer: 
    Evaluation: Wrong (answer --)
    Mistakes: 
    Corrected Attempt: 
    Answer: 
    # Evaluation: Correct  # this is the `stop token`

    # 2. no-reflection 
    Attempt: 
    Answer: 
    # Evaluation: Correct 
    ```

- What next?
    - 2 models experiments: 
        - [x] no-reflection blurb included setting (similar to standard fewshot)
            - [x] w/o format guide
            - [x] more than 1 pair of examples (k=2 --> k=2,4,6)
        - [ ] turn-based
        - [ ] re-use conflicting solutions for inference (randomly pick one amongst the conflicting solutions...since our prompt will generate over till it's correct)
        - [ ] reflect but with the same method (contrastive cot)
        - [ ] contemporary result for the baseline
    - [ ] 3 models experiments:
        - 의의: 
            - Reason to do 3 model exps: ensemble to cover more edge cases (= last mile 성능을 위함) 
            - Fair comparison 이라는 명목하에 baseline을 3 model로 할 필요가 있을 수 있는가? 그럴 순 있다.
        - 종합: 3 모델 실험은 성능이 2 모델보다 올라가야만 좋다는 것을 주장할 수 있다. 
        - [ ] model selection over 3 models implementation
        - [ ] p2c blurb re-prep (bug before: plan not recorded)
    - [ ] experiment with chatgpt's   
    - [ ] script for reparsing `Hint for a better Method choice` (parsing function is not working properly)

## Dec 6:
- result of dec4 experiments ( from `3_blrub-1__.json` (hint, mistakes are generated with temp=1.0) )
    - 7_prompt_short: worse than long examples, but still beats the baseline
        - ~~[ ] on nov cotpal_1 conflict runt ()~~
        - [x] on recent run (**43/73 + 1218/1246 = 1261/1319 (95.6\%) **)
            - reflected  11/23 (47.82\%)
            - did not reflect  32/50 (64.00\%)
    - 7_prompt_long
        - [x] ~~on nov cotpal_1 conflict only gpt-4 (45/75 + 1215/1244 = 1260/1319) (95.53\% = model selection baseline)~~
        - [x] on recent run (46/73 + 1218/1246) -> 1264/1319 (95.83\%)
            - on 73 conflicts
                - 33 reflected. amongst those, 17 are correct (17/33 = 51.5\%)
                - 40 did not. amongst those, 29 are correct (29/40 = 72.5\%)
    - ~~9_prompt results~~
        - [x] on nov cotpal_1 conflict only gpt-4 (44/75): (nonconflict=1215/1244 correct)
            - model selection baseline of 2 model selection (47/75, on different conflict set tho...)
        - [x] full_run with 777 seed with gpt4  --> 1259 / 1319 (**-1 question to baseline**)
            - 970 + 276 nonconflict (949 + 269 corrects)
            - 60 + 13 conflict (31 + 10 corrects)
                - did_reflect: true = 28 + 3
                    - correct = 9 + 2 (35.48%)
                - did_reflect: false = 32 + 10
                    - correct = 22 + 8 (72.43%)

    - Interpretations: 
        - LLM cannot self-reflect yet...이 생각나는 결과. reflection 정답률이 random 에 근접.
            - 9_prompt_long: 35.48\% (11/31)
            - 7_prompt_long: 51.5\% (17/33) 
            - 7_prompt_short: 11/23 (47.82\%)
        - nonreflection but contrastive solving: constantly higher result
            - 9_prompt_long: 72.43\% (30/42)
                - pal: 20/28
                - cot: 10/14
            - 7_prompt_long: 72.50\% (29/40)
            - 7_prompt_short: 32/50 (64.00\%)
        - (discussion point) 
            - **contrastive cot를 하는데 있어 pal/cot를 선택가능하게 해준 부분이 + alpha를 만든 부분이 있을까?**
        - (to defense?)
            - cot 구현에서 Answer 이후 부분을 파싱하도록 한 것이 도움이 된 것은 아닌가?... 


## Dec 4: 
- [x] run cot pal (2 models) experiment first: only blurbs with swtiching.
    - conflict only runs: **prompt need to contain `cotpal` when 2 model running required** (`--tgt_conflict` implies this. internally controlls other flags)
- [ ] do others
    - ~~[ ] blurb classifier to automate useful/useless blurb distinction (useless example: `src/RIMS/3_blurb_1.json:L47`: caused by limitation of automated result parsing of cot output)~~
        - [x] prepare the blurb that the first attempt is actually correct [openaiplayground](https://platform.openai.com/playground/p/6YujhXQUB1pfCuGHHK6k7hWY?model=gpt-4-1106-preview&mode=chat)
        - [ ] prepare the blurb that the workaround method is still the same method as the first choice (but answer corrects.) [openaiplayground](https://platform.openai.com/playground/p/2abad5yzZQquHD7XLtMzMPAE?model=gpt-4-1106-preview&mode=chat)
    - [ ] (debug) p2c -> * blurbs re-prep


## Dec 3:
- prompt for hint and mistake generation: mostly successful
    - [mistake/hint prompt](https://github.com/fgenie/Model-Selection-Reasoning/blob/main/src/RIMS/3_prompt_generate_reflection_forceformat.yaml)
    - [blurbs generated](https://github.com/fgenie/Model-Selection-Reasoning/blob/main/src/RIMS/3_blurb_1.json)
        - [txtfile](https://github.com/fgenie/Model-Selection-Reasoning/blob/main/src/RIMS/3_blurb_1.json_print.txt)
- errors in blurbs
    - ~~pal done with fewshot prompting with gpt-4-turbo sometimes tell something long in front of the code~~
        - [x] need to parse the code only to prompt right
    - p2c and pal are not clearly distinguished sometimes, but not much of a concern
    - (bug) p2c "plan" part mistakenly dropped when gathering failure cases --> need re-inference.
- before running experiment
    - [ ] adapt the inference prompt to hint/mistake prompt

    

## Nov 28:
- preparing blurb (1)
    - if some method does more wrongs within 3 trials, find a alternative
    - not reflection / just retries with alternative method

## Nov 21:
- [x] Success rate 보기 
    - 세상에 내가 이미 해놨잖아?
    - [x] 논문과 값 비교하기, 내 프롬의 success rate 이랑 얼마나 차이나는지 보기
- [x] RHMS 프롬만들기 프롬 돌리기

## Nov 13~20: 
* Slacked off or just needed excessive dose of fun to wrestle against my life again (I really enjoyed).

## Nov 12: results of RIMS prompt variants (from ideal training blurbs)

### nonconflicts 
<details>
<summary>majority vote between 3|2 models </summary>

* chatgpt

| | n_nonconflict | correct | 
|-|-|-|
| 3models | 1158 | 1049 (pal-0.45\%p, cot+1.10\%p, p2c+5.61\%p) | 
| 2models | 982 | 932 |

*2models from `output/oct27_only_conflict/coh_cotpal_1/chatgpt/gsm8k_k8_sc1_s306_e1319_10_28_12_23.jsonl`

* gpt4

| total\=1319 | n_nonconflict | nonconfl_correct | 
|-|-|-|
| 3models | 1304 | 1255 (palonly+0.83\%p) |
| 2models | 1244 | 1215 (palonly-2.20\%p) |

</details>

### on conflicts
* TLDR; RIMS prompts variants results
    * chatgpt / 3 models --> slightly worse but still outperform model-selection baseline significantly
    * gpt4 / 3 models --> almost the same
    * gpt4 / 2 models --> almost the same

* prompt notation
    * 8 = turn-based prompting
        * `src/prompts/prep_reflexion/8_cohlike_solvetwice_prompt_cotpal_1.yaml`
    * 7 = let LLM write failure attempt with failed method before writing the correct solution with successful method
        * `src/prompts/prep_reflexion/7_cohlike_solvetwice_prompt_cotpal_1.txt`
    * 6 = choose --> solve... (why it records the worst?)
        * `src/prompts/prep_reflexion/6_cohlike_solve_prompt_cotpal_1.txt`
    * (note) previous prompt = `src/prompts/prep_reflexion/5_cohlike_prompt_cotpal_1.txt`
    
* chatgpt / 3 models  
    * prev. 84.2\% == **1110 corrects** 
    * baseline 80.2\% == 1058 corrects

(total 1308, 11 examples --> failed to genereate)

| prompt | in total | correct / conflict | correct / otherwise |
|-|-|-|-|
|7| **1092**/1319 | 43/150 | 1049/1158 |
|6| **1104**/1319 | 55/150 | - |
*k=6 for all

* gpt4 / 3 models (prev. 95.7\% == 1262 corrects)

| prompt | in total | correct / conflict | correct / otherwise |
|-|-|-|-|
|8| 1259/1319 | 4/15 | 1255/1304 |
|7| 1260/1319 | 5/15 | - |
|6| 1258/1319 | 3/15 | - |

*k=6 for all

* gpt4 / 2 models

| prompt | in total | correct / conflict | correct / otherwise |
|-|-|-|-|
|8(k=2)| /1319 | /75 | 1215/1244 |
|8(k=4)| 1260/1319 | 45/75 (60\%) | - |
|8(k=6)| **1263/1319** | 48/75 (64\%) | - |
|7(k=2)| 1258/1319 | 45/75 | - |
|7(k=4)| 1254/1319 | 39/75 | - |
|7(k=6)| 1254/1319 | 39/75 | - |
|6(k=2)| /1319 | /75 | - |
|6(k=4)| 1232/1319 | 17/75 | - |
|6(k=6)| 1230/1319 | 15/75 | - |


## Nov 6~11
* one-method-only performance (drops from 95.5\%)
    - [x] gpt4
    - `scripts/nov11_1_onemethod_acc.py`

    | model | cot | pal | p2c |
    |-|-|-|-|
    | gpt-3.5-turbo | 1037/1319 (0.786) | 1055/1319 (0.800) | 975/1319 (0.739) |
    | gpt4 | 1244/1319 (0.943 (-1.2\%p)) | 1235/1319 (0.936 (-1.9\%p)) | 1209/1319 (0.917 (-3.8\%p)) |

* how inconsistent output does `T=0` model generate? **QUITE**
    - [x] chatgpt
    - [x] gpt4   

    It is QUITE INCONSISTENT. See `scripts/nov11_0_conflicts_check.xlsx` for more. (Note that by anwser-wise, consistency improves).

    | | gpt-3.5-turbo | gpt-4 | 
    |-|-|-|
    | PAL  | 1193/1308 | 873.0/1319 |
    | CoT | 907/1308 | 607.3/1319 |

* Is it acceptable to run things on conflict cases only? Is this consistent enough w/o setting a proper `seed`? **"Probably"**
    * chatgpt: we do not care much about this since it already recorded quite a gap compared to the baseline (for both 2-model or 3-model'ed cases)
    * gpt4: already we counted how much the overlap of conflict cases (indices) between two separate runs and over 75 conflict cases, 61 of those were common idxs that had conflict (see `output/nov4_gpt4greedy/baseline/gpt4/compare_idxs.py`)
    
    | | num conflict idxs |
    |-|-|
    |baseline run| 75 |
    |coh run| 75 |
    |intersection| 61 (81.3\%) | 

* it is possible that we only run prompts on **conflict cases only** that is... we don't need to run over 1319 examples.
    * `=` success rate.
    - [x] implement conflict only runs
    - [x] combining results code
* possible prompt change
    * change coh system prompt (from: choose -> to: solve) so that see if it changes performance
    * more fewshots for cotpal case?
        - [x] `6_cohlike_solve_prompt_1|2|3.txt` (added 2*1|2|3 pairs of examples for this)
        - run
            - [x] chatgpt
            - [x] gpt-4
    * transform into a turn-based few-shot prompt (p2c v1 `<` v2 for this reason)
        - [x] `8_cohlike_solvetwice_prompt.yaml`
        - [x] `8_cohlike_solvetwice_prompt_cotpal_1.yaml`
        - [x] `8_cohlike_solvetwice_prompt_cotpal_2.yaml`
        - [x] `8_cohlike_solvetwice_prompt_cotpal_3.yaml`
        - [x] prompt utils for querying
        - run
            - [x] chatgpt
* after things are all done, do constructing `training blurb`

### re-do things (after completing above)
* p2c prompt debugged
    [x] coh conflict only

| *debugged* | accuracy (\%) | 
|-|-|
| model-selection (cot;pal)* **(k=8)**  | 80.2 \% | 
| coh_conflictonly (cot;pal;p2c) | **84.2 \%** (+1.8%p from oct27)|
| coh_conflictonly (cot;pal) |  |
| coh_conflictonly (cot;pal_1) |  |
*increased performance -- caused by k=6 -> 8 applied to `query_cot|pal|p2c` + debugged `p2c` prompt.

## Nov 4: GPT-4 greedy (T=exact 0.)
* Corresponds to gsm8K result on Table 1 (greedy decoded results)

| | accuracy (\%) / GPT-4 greedy | 
|-|-|
| model-selection (cot;pal)*  | 95.5 \% |
| coh_conflictonly (cot;pal;p2c) | <u> 95.7 \% (+2 problems) </u> |
| coh_conflictonly (cot;pal_1) | <u> 95.5 \% (+0 problems) </u>  |

*exactly the same performance (1260 correct for 1st and 3rd row.)
*2 more questions correct on 2nd row.

### GPT-4 greedy decoding does not seem deterministic
https://community.openai.com/t/a-question-on-determinism/8185 
`compare_idxs.py`
n_conflict: 75
intersection_indices: 61


## Oct 27: coh when conflict only (select amongst 3, select btw 2) --> bug: k_fewshot = 6 for all
* Re-run model-selection baseline (to check whether it became inferior than before...)
* Apply [coh](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/CoH.md) when conflict
    - [coh_reflect_cotpalp2c](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/5_cohlike_prompt.txt)
    - [coh_reflect_cotpal](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/5_cohlike_prompt_cotpal.txt)
    - [coh_reflect_palcot](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/5_cohlike_prompt_cotpal_1.txt): Would showing 2 fewshots in different order affect hugely?
* running scripts: `scripts/OUREXP/oct27_onlyconflict`

| bug: k=6 | accuracy (\%) | 
|-|-|
| model-selection (cot;pal)* **(k=8)**  | 80.2 \% |
| coh_conflictonly (cot;pal;p2c) | **82.4 \%** |
| coh_conflictonly (cot;pal) | **81.8 \%** |
| coh_conflictonly (cot;pal_1) | **81.9 \%** |
*remeasured baseline acc is the same as before. no k_fewshot=6 bug on baseline

## Oct 26: actor-select when conflict only (select btw 2)
* select amongst 3 needs some modification (real-time construction of actor selection prompt with correct fewshot when choosing btw two not three.)
* current version uses hand-made `training-blurb`
* current version do not use printed-out solution for selection. Only static `training-blurb` is used. This could be improved by **newly inventing actor selection prompt w/ generated solutions with the `blurb`**
* ~~model-selection with 3 models prompt as a baseline~~

| | actorselect when conflict (cot + pal) | 
|-|-|
| acc.  | 79.2 \% |


## Aug 31: Unchanged fact = no method so far beats the original model selection (pal + cot)
| | standard prompts (k=8) | 
|-|-|
| acc.  | 80.1 \% |

*not sure is this greedy decoded. my commit is started from sep2 which performs 0903 exps, not 0831.
*but the commit where fork started implies it's greedy decoding (temperatures = 0.)

## Oct 20: enhanced_coh (with manual reflections k <= 6)  --> just bad 
> Don't stop after choosing, but continue to solve!  
see [`5_cohlike_prompt.txt`](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/5_cohlike_prompt.txt), [`CoH.md`](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/CoH.md) for details

| | k=6 | k=4* | k=3*
|-|-|-|-|
| acc.  | **74.0 \%** | 69.7 \% | 69.9 \% |

*for k=3, randomly pick 3 transition examples amongst possible 6 (3C2) variants


## Oct 14: actor prompt test (manual reflections k=6)
| acc. | amongst 3 models (6shots) | only 2 models (2shots) |
|-|-|-|
| select only | 77.3 \% | 78.2 \% |
| prepend hint | 75.1 \% | 78.2 \% |

* prepend hint does not help.
* exclusion of p2c improves acc.


### + verbose (Chain-of-Thought rather than `cot`)
| acc. | amongst 3 models (6shots) | only 2 models (2shots) |
|-|-|-|
| select only | 76.5\% | 78.5\% |

* exclusion of p2c improves acc.
* 3 model acc. degraded a bit, 2 model acc. improved. no consistent improvement.


<details>
    <summary> Click to expand: about actor selection </summary>
## actor selection prompt
```
Choose the most likely reasoning method for answering math-word questions. Followings are the three methods available: (1) Chain-of-Thought (`cot`) invokes step-by-step verbal reasoning to break the question to reach the correct answer. (2) Plan-to-Code (`p2c`) invokes to write the plan and write the code of it to reach the answer. (3) Program-aided Language modeling (`pal`) invokes writing a code that returns the answer of the question. Referring to the followings, learn to guess which method would be promising given the question. 

Previous attempts and reflections:

[reflection examples here]


Now, given the question, start guessing the most `Promising Method` after writing an appropriate `Hint` to correctly choose the reasoning method for  the `Question` based on your learnings. 

Question: [QUESTION]

<format>
Hint: <write a concise sentence that help the method choice for answering correctly>
Promising Method: <pick one between two reasoning methods> 
</format>
```

## querying w/ hint prompt

```
[system prompt for cot/pal/p2c]

[examples]

Question: question of interest ([HINT goes here (a sentence.)])

```




```bash
# raw results output

# bash evaluate_math.sh 
# amongst 3 methods
+ python evaluate.py --input_path ../output/oct14_actorselect/gsm8k_k8_sc1_s0_e1319_10_14_23_48.jsonl --dataset_type math
Accuracy: 0.7725549658832449, Total: 1319, Correct: 1019, Error: 49
+ wc -l ../output/oct14_actorselect/gsm8k_k8_sc1_s0_e1319_10_14_23_48.jsonl
    1319 ../output/oct14_actorselect/gsm8k_k8_sc1_s0_e1319_10_14_23_48.jsonl


+ python evaluate.py --input_path ../output/oct14_actorselect_hinted/gsm8k_k8_sc1_s0_e1319_10_14_23_49.jsonl --dataset_type math
Accuracy: 0.7513267626990144, Total: 1319, Correct: 991, Error: 63
+ wc -l ../output/oct14_actorselect_hinted/gsm8k_k8_sc1_s0_e1319_10_14_23_49.jsonl
    1319 ../output/oct14_actorselect_hinted/gsm8k_k8_sc1_s0_e1319_10_14_23_49.jsonl


# bewtween pal / cot (binary choice)
# no hint only select
Accuracy: 0.7824109173616376, Total: 1319, Correct: 1032, Error: 21

# hinted solution
Accuracy: 0.7816527672479151, Total: 1319, Correct: 1031, Error: 18

```
</details>

## Sep 24, Sep 10: Ablation cot, pal, p2c_v1/v2 (v1 prompt k=5 --> v2 prompt k=8 with dialogued fewshot)
| acc. | cot | pal | p2c |
|-|-|-|-|
| sep 10 | 78.8 \% | 80.2 \% | 67.6 \% |
| sep 24 v2 | n/a | n/a | 71.5 \% |

* p2c_v2 > p2c_v1

## Sep 3 Model Selection (cot + p2c_v1)
this experiment is **done on subset of gsm8k: 805 / 1319 instances** (all indices are common for three)
| | cot+pal | cot+p2c_v1 k=2 | cot+p2c_v1 k=5 |
|-|-|-|-|
| acc. | 81.9\% | 80.0 \% | 79.5\% |

* cot + p2c_v1 k=2: the closest to model selection so far. 



# 회의 전 생각
* ~~model selection 방법의 개선폭 (우리 실험상으로는 `sep10:palonly=90.8\%` &rarr; `sep3subset:pal+cot=92.8 \%` or `aug31nongreedy:pal+cot=91.4\%`로 `+0.6~2.0%`) 이 미미해보이지만 생각보다 그런 개선을 이뤄내기가 쉬운 것도 아니다. solution만 보고 selection하는건 llm이 어느정도 효과를 발휘 (`gpt-3.5-turbo, temperature=0.`) 하고 있다고 봐야한다.~~
    * ~~논문상에서 greedy decoding 결과는 82.6으로 뭔가 이상하다. PAL, CoT 성능으로 봐서는 잘못된 채점기를 그대로 사용중인 것 같다.~~
    * ~~지금 저자 깃헙 스크립트도 변함이 없다.~~
* p2c_v1이 좋았던 건 포맷 때문일까 fewshot example (코딩 등 수기 예제) 때문이었을까? --> v2에 차용 가능
    * k=2가 특히 좋았다
    * coh p2c의 승률은 어땠는가?
* p2c_v1 + cot 의 gsm8k full set에서의 성능은 어떨까? p2c_v2 + cot는?
    * 이 경우 model selection에서 나온 실험과 동일하다 (CCoT + CoT, CoT'+CoT 를 수행한 바 있음)
    * 물론... p2c를 무언가 잘 포장할 여지도 있긴 함
* coh에서 failed method solution 을 쓰도록 하고 answer, evaluation까지 쓰게 해서 correct가 나오면 그걸로 답을 제출하도록 해볼까? 그게 나으려나? (이 경우 스탠다드한 fewshot 이 됨)
    * solution까지 보고 selection 하도록 하는 프롬은 어떻게 만들어야 모델 셀렉션과 좀 달라보일까. reflection과 chimera 되어있고 p2c가 포함되어 있다는 점이 다른가?
    * 사실은 위의 coh 변형도 solution보고 셀렉션을 하는 케이스 아닐까?
    * 이렇게 하면 사실 evaluation까지 시키는 것이기도 하다. 
* 모델 세 개로 selection을 하는 경우 성능은?
* ablation solution과 oct14 solution, 그리고 oct20 solution을 비교해보자. 
