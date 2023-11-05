#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
cd ${EXEHOME}

# run evaluation at once
python evaluate.py --input_path '../output/nov4_gpt4greedy/coh_cotpal_1/gpt4/gsm8k*.jsonl' --dataset_type 'math'
python evaluate.py --input_path '../output/nov4_gpt4greedy/baseline/gpt4/gsm8k*.jsonl' --dataset_type 'math'
python evaluate.py --input_path '../output/nov4_gpt4greedy/coh/gpt4/gsm8k*.jsonl' --dataset_type 'math'