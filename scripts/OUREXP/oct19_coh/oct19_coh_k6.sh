#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
cd ${EXEHOME}

python selection_math.py --start 1308 \
        --end -1 \
        --dataset 'gsm8k' \
        --backbone 'chatgpt' \
        --cot_temperature 0. \
        --pal_temperature 0. \
        --sc_num 1 \
        --output_dir '../output/oct19_enhanced_coh' \
        --cohprompt "/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src/prompts/prep_reflexion/5_cohlike_prompt.txt" 

# v2 plancode run command
# bash gsm8k_onlyone_method.sh plancode 0