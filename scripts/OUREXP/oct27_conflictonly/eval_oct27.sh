#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
cd ${EXEHOME}

# run evaluation at once
python evaluate.py --input_path '../output/oct27_rerun_baseline/chatgpt/gsm8k*.jsonl' --dataset_type 'math'

python evaluate.py --input_path '../output/oct27_only_conflict/coh/chatgpt/gsm8k*.jsonl' --dataset_type 'math'
python evaluate.py --input_path '../output/oct27_only_conflict/coh_cotpal/chatgpt/gsm8k*.jsonl' --dataset_type 'math'
python evaluate.py --input_path '../output/oct27_only_conflict/coh_cotpal_1/chatgpt/gsm8k*.jsonl' --dataset_type 'math'

# python evaluate.py --input_path ../output/oct27_only_conflict/coh/chatgpt/gsm8k_k8_sc1_s0_e1319_11_06_12_35.jsonl --dataset_type 'math'