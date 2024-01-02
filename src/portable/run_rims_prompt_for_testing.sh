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