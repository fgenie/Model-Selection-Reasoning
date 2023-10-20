# Crooked `evaluate.py`!: Re-reporting all previous results 
* found bug in eval script (`evaluate.py`) and fixed
* **re-measured renewing all the results** as follows
    * trend does not really change but it blows my mind...
    * cot + p2c_v1 was close and p2c_v2 > p2c_v1 still holds.
    

## Aug 31: Unchanged fact = no method so far beats the original model selection (pal + cot)
| | standard prompts (k=8) | 
|-|-|
| acc.  | ~~80.2\%~~ &rarr; **91.4\%** | 

## Oct 20: enhanced_coh (with manual reflections k <= 6) 
> Don't stop after choosing, but continue to solve!  
see [`5_my_greatgreat_prompt.txt`](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/5_my_greatgreat_prompt.txt), [`CoH.md`](https://github.com/fgenie/Model-Selection-Reasoning/blob/PR_si/src/prompts/prep_reflexion/CoH.md) for details

| | k=6 | k=3* |
|-|-|-|
| acc.  | 87.6\% | 83.0\% |

*for k=3, randomly pick 3 transition examples amongst possible 6 (3C2) variants
* lower than pal only acc = **90.8 \%**.


## Oct 14: actor prompt test (manual reflections k=6)
| acc. | amongst 3 models (6shots) | only 2 models (2shots) |
|-|-|-|
| select only | ~~77.3\%~~ &rarr; 87.5\% | ~~78.2\%~~ &rarr; 89.5\% |
| prepend hint | ~~75.1\%~~ &rarr; 86.5\% | ~~78.2\%~~ &rarr; 89.5\% |
* lower than pal only acc = **90.8 \%**.


### + verbose (Chain-of-Thought rather than `cot`)

| acc. | amongst 3 models (6shots) | only 2 models (2shots) |
|-|-|-|
| select only | ~~76.5\%~~ &rarr; 86.9\% | ~~78.5\%~~ &rarr; 89.3\% |
* lower than pal only acc = **90.8 \%**.

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

1019 / (1319-9) = 0.7778625954198474


+ python evaluate.py --input_path ../output/oct14_actorselect_hinted/gsm8k_k8_sc1_s0_e1319_10_14_23_49.jsonl --dataset_type math
Accuracy: 0.7513267626990144, Total: 1319, Correct: 991, Error: 63
+ wc -l ../output/oct14_actorselect_hinted/gsm8k_k8_sc1_s0_e1319_10_14_23_49.jsonl
    1319 ../output/oct14_actorselect_hinted/gsm8k_k8_sc1_s0_e1319_10_14_23_49.jsonl

991/(1319 - 16) = 0.760552570990023


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
| sep 10 | ~~78.8\%~~ &rarr; 87.5\% | ~~80.2 \%~~ &rarr; 90.8 \% | ~~67.6\%~~ &rarr; 82.1\% |
| sep 24 v2 | n/a | n/a | ~~71.5\%~~ &rarr; 86.5\% |

## Sep 3 Model Selection (cot + p2c_v1)
this experiment is done on 805 / 1319 instances (all indices are common for three)
| | cot+pal | cot+p2c_v1 k=2 | cot+p2c_v1 k=5 |
|-|-|-|-|
| acc. | ~~81.9\%~~ &rarr; **92.8\%** | ~~80.0 \%~~ &rarr; 90.9 \% | ~~79.5\%~~ &rarr; 91.6\% |



# 회의 전 생각
* p2c_v1이 좋았던 건 포맷 때문일까 fewshot example (코딩 등 수기 예제) 때문이었을까? --> v2에 차용 가능
* p2c_v1 + cot 의 gsm8k full set에서의 성능은 어떨까?
* coh에서 failed method solution 을 쓰도록 하고 answer, evaluation까지 쓰게 해서 correct가 나오면 그걸로 답을 제출하도록 해볼까? 그게 나으려나? (이 경우 스탠다드한 fewshot 이 됨)
    * solution까지 보고 selection 하도록 하는 프롬은 어떻게 만들어야 모델 셀렉션과 좀 달라보일까. reflection과 chimera 되어있고 p2c가 포함되어 있다는 점이 다른가?
    * 사실은 위의 coh 변형도 solution보고 셀렉션을 하는 케이스 아닐까?
    * 이렇게 하면 사실 evaluation까지 시키는 것이기도 하다. 
* 모델 세 개로 selection을 하는 경우 성능은?
* model selection 방법의 개선폭이 미미해보이지만 생각보다 그런 개선을 이뤄내기가 쉬운 것도 아니다. solution만 보고 selection하는건 llm이 어느정도 효과를 발휘 (\<1.5\% for `gpt-3.5-turbo, temperature=0.`) 하고 있다고 봐야한다.
* ablation solution과 oct14 solution, 그리고 oct20 solution을 비교해보자. 