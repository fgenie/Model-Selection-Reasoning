#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
cd ${EXEHOME}

# python selection_math.py --start 0 \
#         --end -1 \
#         --dataset 'gsm8k' \
#         --backbone 'gpt4' \
#         --cot_temperature 0. \
#         --pal_temperature 0. \
#         --sc_num 1 \
#         --output_dir '../output/nov4_only_conflict/coh_cotpal' \
#         --when_only_conflict 2 \
#         --cohprompt /Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src/prompts/prep_reflexion/5_cohlike_prompt_cotpal.txt
        # --actor_selection_prompt "/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src/prompts/prep_reflexion/4_selection_prompt_0_1_nobiassys_modif_cotpalonly_verbose_nomenclature.txt" 

python selection_math.py --start 0 \
        --end -1 \
        --dataset 'gsm8k' \
        --backbone 'gpt4' \
        --cot_temperature 0. \
        --pal_temperature 0. \
        --sc_num 1 \
        --output_dir '../output/nov4_gpt4greedy/coh_cotpal_1' \
        --when_only_conflict 2 \
        --cohprompt /Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src/prompts/prep_reflexion/5_cohlike_prompt_cotpal_1.txt


        
