## this script is for understanding how things and codes work, but the actual experiment will run on the same python scripts.
# gsm_jslf is for dataset of the same format as gsm8K_test.jsonl. It could be other (svamp, single_op,... )



# model-selection-resoning baseline
python 99_run_inference.py  baseline_inference \ 
                --dbg \
                --backbone chatgpt \
                --gsm_jslf ../../dataset/dbg.jsonl 


# rims algorithm run
python 99_run_inference.py  rims_inference  \ 
                --prompt_f  3_reflectonce_cot2p2c.pal2cot.pal2p2c.txt_rm_ans  \
                --dbg  \
                --eval_indiv_method  \
                --backbone  gpt4turbo  \ 
                --gsm_jslf ../../dataset/dbg.jsonl 