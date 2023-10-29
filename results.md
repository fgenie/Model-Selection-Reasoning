
## Oct 27: coh when conflict only (select amongst 3, select btw 2)
* Re-run model-selection baseline (to check whether it became inferior than before...)
* Apply [coh](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/CoH.md) when conflict
    - [coh_reflect_cotpalp2c](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/5_my_greatgreat_prompt.txt)
    - [coh_reflect_cotpal](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/5_my_greatgreat_prompt_cotpal.txt)
    - [coh_reflect_palcot](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/5_my_greatgreat_prompt_cotpal_1.txt): Would showing 2 fewshots in different order affect hugely?
* running scripts: `scripts/OUREXP/oct27_onlyconflict`

| | accuracy (\%) | 
|-|-|
| model-selection (cot;pal)*  | 80.2 \% |
| coh_conflictonly (cot;pal;p2c) | **82.4 \%** |
| coh_conflictonly (cot;pal) | **81.8 \%** |
| coh_conflictonly (cot;pal_1) | **81.9 \%** |

*remeasured baseline acc is the same as before. 

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
see [`5_my_greatgreat_prompt.txt`](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/5_my_greatgreat_prompt.txt), [`CoH.md`](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/CoH.md) for details

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
