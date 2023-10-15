# Result
| acc. | amongst 3 models (6shots) | only 2 models (2shots) |
|-|-|-|
| select only | 77.3\% | 78.2\% |
| prepend hint | 75.1\% | 78.2\% * |

*slightly worse.

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

# Choosing model with unabbreviated names (i.e. current:cot -> newattempt: chain of thought (cot))
- on going... not really expecting but trying 






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