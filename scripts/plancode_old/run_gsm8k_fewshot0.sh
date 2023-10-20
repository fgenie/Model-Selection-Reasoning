#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
cd ${EXEHOME}

# Specify your API key
APIKEY="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"

python selection_math.py --start 0 \
        --end -1 \
        --dataset 'gsm8k' \
        --backbone 'chatgpt' \
        --sc_num 1 \
        --output_dir '../output/' \
        --cot_temperature 0. \
        --use_plancode \
        --plan_temperature 0. \
        --code_temperature 0. \
        --k_fewshot 0 \
        --key ${APIKEY}