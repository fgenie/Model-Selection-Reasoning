#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
cd ${EXEHOME}

# Specify your API key
APIKEY=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/openai_key.txt

python selection_math.py --start 0 \
        --end -1 \
        --dataset 'gsm8k' \
        --backbone 'gpt4' \
        --cot_temperature 0.5 \
        --pal_temperature 0.8 \
        --sc_num 15 \
        --output_dir '../output/' \
        --key ${APIKEY}



# python selection_math.py --start 0 --end -1 --dataset gsm8k --backbone gpt4 --cot_temperature 0.5 --pal_temperature 0.8 --sc_num 15 --output_dir ../output/ --key /Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/openai_key.txt