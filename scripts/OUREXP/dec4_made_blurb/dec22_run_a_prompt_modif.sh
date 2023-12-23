#!/bin/bash
promptf=$1
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
# EXEHOME=/home/sison/Model-Selection-Reasoning/src # otherserver
cd ${EXEHOME}

python selection_math1.py \
    --tgt_conflict \
    --recent_gsm8k_fullrun \
    --rimsprompt $promptf \
    --modif_prompt  # attempt numbering applied to the prompt