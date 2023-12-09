#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
# EXEHOME=/home/sison/Model-Selection-Reasoning/src # otherserver
cd ${EXEHOME}

python selection_math1.py \
    --tgt_conflict \
    --recent_gsm8k_fullrun \
    --rimsprompt RIMS/99_7_rims_cotpal_inference_prompt_k2_short_DEC4.txt # for verifying prompt's example robustness.
    # --rimsprompt /Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src/RIMS/99_7_rims_cotpal_inference_prompt_k2_long_DEC4.txt   # recorded 1264/1319

