#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
cd ${EXEHOME}


python selection_math.py --start 0 \
        --end -1 \
        --dataset 'dbg' \
        --backbone 'chatgpt' \
        --cot_temperature 0. \
        --pal_temperature 0. \
        --sc_num 1 \
        --output_dir '../output/' 

