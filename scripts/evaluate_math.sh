#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
cd ${EXEHOME}

# Specify the input path
INPUTPATH1='/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/chatgpt_plancode/dbg_sc2_s0_e2_09_03_01_05.jsonl'


python evaluate.py --input_path ${INPUTPATH1}\
                --dataset_type 'math'
wc -l $INPUTPATH1

# python evaluate.py --input_path ${INPUTPATH2}\
                # --dataset_type 'math'
# wc -l $INPUTPATH2

# python evaluate.py --input_path ${INPUTPATH3}\
                # --dataset_type 'math'
# wc -l $INPUTPATH3