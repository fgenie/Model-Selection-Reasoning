### (DEC9) added no-reflection examples at the top of the blurbs, lowers the performance

|    | name                                                    | total               | conflict_only   | reflect         | nonreflect      |   justfailed |
|---:|:--------------------------------------------------------|:--------------------|:----------------|:----------------|:----------------|-------------:|
|  2 | 99_7_no_refl_rims_cotpal_inference_prompt_k2_DEC9_gpt4  | 1264/1319 (95.83\%) | 46/73 (63.01\%) | 8/19 (42.11\%)  | 38/54 (70.37\%) |            0 |
|  4 | 99_7_no_refl_rims_cotpal_inference_prompt_k4_DEC9_gpt4  | 1265/1319 (95.91\%) | 47/73 (64.38\%) | 8/17 (47.06\%)  | 39/56 (69.64\%) |            0 |
|  9 | 99_7_no_refl_rims_cotpal_inference_prompt_k6_DEC9_gpt4  | 1260/1319 (95.53\%) | 42/73 (57.53\%) | 11/25 (44.00\%) | 31/48 (64.58\%) |            0 |


----

### (DEC9) more than k=2. format guide removed. llm generation successful now.
 so far, this is the SOTA performance 

|    | name                                                    | total               | conflict_only   | reflect         | nonreflect      |   justfailed |
|---:|:--------------------------------------------------------|:--------------------|:----------------|:----------------|:----------------|-------------:|
|  6 | 99_7_rims_cotpal_inference_prompt_k2_DEC9_noformat_gpt4 | 1270/1319 (96.29\%) | 52/73 (71.23\%) | 19/30 (63.33\%) | 33/43 (76.74\%) |            0 |
|  0 | 99_7_rims_cotpal_inference_prompt_k4_DEC9_noformat_gpt4 | 1263/1319 (95.75\%) | 45/73 (61.64\%) | 6/15 (40.00\%)  | 39/58 (67.24\%) |            0 |
| 10 | 99_7_rims_cotpal_inference_prompt_k6_DEC9_noformat_gpt4 | 1265/1319 (95.91\%) | 47/73 (64.38\%) | 18/29 (62.07\%) | 29/44 (65.91\%) |            0 |


----

### (DEC9) more than k=2. format guide deteriorates the llm-generation

|    | name                                                    | total               | conflict_only   | reflect         | nonreflect      |   justfailed |
|---:|:--------------------------------------------------------|:--------------------|:----------------|:----------------|:----------------|-------------:|
|  1 | 99_7_rims_cotpal_inference_prompt_k2_DEC9_gpt4          | 1266/1318 (96.05\%) | 48/72 (66.67\%) | 11/23 (47.83\%) | 37/49 (75.51\%) |            1 |
|  3 | ~~99_7_rims_cotpal_inference_prompt_k4_DEC9_gpt4~~          | ~~1237/1276 (96.94\%)~~ | ~~19/30 (63.33\%)~~ | ~~6/10 (60.00\%)~~  | ~~13/20 (65.00\%)~~ |           43 |
|  7 | ~~99_7_rims_cotpal_inference_prompt_k6_DEC9_gpt4~~          | ~~1227/1263 (97.15\%)~~ | ~~9/17 (52.94\%)~~  | ~~4/7 (57.14\%)~~   | ~~5/10 (50.00\%)~~  |           56 |


----

### (DEC4) k=2 reflection once only. 

|    |                                                         | total               | conflict_only   | reflect         | nonreflect      |   justfailed |
|---:|:--------------------------------------------------------|:--------------------|:----------------|:----------------|:----------------|-------------:|
|  5 | 99_7_rims_cotpal_inference_prompt_k2_short_DEC4_gpt4    | 1261/1319 (95.60\%) | 43/73 (58.90\%) | 11/23 (47.83\%) | 32/50 (64.00\%) |            0 |
|  8 | 99_7_rims_cotpal_inference_prompt_k2_long_DEC4_gpt4     | 1264/1319 (95.83\%) | 46/73 (63.01\%) | 17/33 (51.52\%) | 29/40 (72.50\%) |            0 |



--- 
### baseline performance 
|nov 4 | acc. (\%) | conflict_only (success rate) | 
|-|-|-|
| model-selection (cot;pal) - no seed  | 1260/1319 (95.5\%) | 47/75 (62.7\%) | 
|    | name                 | total               | conflict_only   |
|---:|:---------------------|:--------------------|:----------------|
|  seed=777 | baseline_cotpal_gpt4 | 1260/1319 (95.53\%) | 42/73 (57.53\%) |
|  noseed, nov 4   | baseline_cotpal_gpt4 | 1260/1319 (95.5\%) | 47/75 (62.7\%) | 

*we are doing this experiment with gpt-4-0613, paper refers to api version gpt-4-0314
*paper reports 10\%p higher success rate (this code is author's)
*paper reports 95.6\% which is less than 0.1\%p higher than our result. (ok.)