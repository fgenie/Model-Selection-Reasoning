abl=$1 # abl could be 'cot' / 'pal' / 'plancode'
st=$2
echo $abl

#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
cd ${EXEHOME}

python selection_math.py --start $st \
        --end -1 \
        --dataset 'gsm8k' \
        --backbone 'chatgpt' \
        --cot_temperature 0. \
        --pal_temperature 0. \
        --sc_num 1 \
        --output_dir '../output/' \
        --ablation $abl

# v2 plancode run command
# bash gsm8k_onlyone_method.sh plancode 0