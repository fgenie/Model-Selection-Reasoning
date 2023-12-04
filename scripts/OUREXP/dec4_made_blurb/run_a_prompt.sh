#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
# EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
EXEHOME=/home/sison/Model-Selection-Reasoning/src # otherserver
cd ${EXEHOME}

promptf=$1

python selection_math.py \
    --dataset 'gsm8k' \
    --sc_num 1 \
    --tgt_conflict \
    --rimsprompt $promptf

