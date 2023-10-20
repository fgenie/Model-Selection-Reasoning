# at Model-Selectio-Reasoning/
find . -name '*_correct.csv'

wc -l ./output/chatgpt_cot_pal/gsm8k_sc1_s0_e1319_08_31_00_19.jsonl
wc -l ./output/0903_result/k5.jsonl
wc -l ./output/0903_result/baseline.jsonl
wc -l ./output/0903_result/k2.jsonl
wc -l ./output/0910_ablation_result/cot.jsonl
wc -l ./output/0910_ablation_result/plancode.jsonl
wc -l ./output/0910_ablation_result/pal.jsonl
wc -l ./output/ablation_plancode/gsm8k_k8_sc1_s0_e1319_09_24_01_16.jsonl
wc -l ./expresults/0924_plancode_v2_abl/gsm8k_k8_sc1_s0_e1319_09_24_01_16.jsonl
wc -l ./output/oct14_actorselect_chatgpt/gsm8k_k8_sc1_s0_e1319_10_14_23_48.jsonl
wc -l ./output/oct14_actorselect_palcot_chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_09_13.jsonl
wc -l ./output/oct14_actorselect_hinted_chatgpt/gsm8k_k8_sc1_s0_e1319_10_14_23_49.jsonl
wc -l ./output/oct14_actorselect_hinted_palcot_chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_09_12.jsonl
wc -l ./output/oct15_actorselect_verbose/chatgpt/gsm8k_k8_sc1_s0_e1319_10_16_11_22.jsonl
wc -l ./output/oct15_actorselect_cotpal_verbose/chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_23_46.jsonl
wc -l ./output/oct19_enhanced_coh/chatgpt/gsm8k_k3.jsonl
wc -l ./output/oct19_enhanced_coh/chatgpt/gsm8k_k6.jsonl

# 1319 ./output/chatgpt_cot_pal/gsm8k_sc1_s0_e1319_08_31_00_19.jsonl
#  805 ./output/0903_result/k5.jsonl
#  805 ./output/0903_result/baseline.jsonl
#  805 ./output/0903_result/k2.jsonl
# 1318 ./output/0910_ablation_result/cot.jsonl
# 1316 ./output/0910_ablation_result/plancode.jsonl <- old
# 1319 ./output/0910_ablation_result/pal.jsonl
# 1319 ./expresults/0924_plancode_v2_abl/gsm8k_k8_sc1_s0_e1319_09_24_01_16.jsonl <- new
# 1319 ./output/oct14_actorselect_chatgpt/gsm8k_k8_sc1_s0_e1319_10_14_23_48.jsonl
# 1319 ./output/oct14_actorselect_palcot_chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_09_13.jsonl
# 1319 ./output/oct14_actorselect_hinted_chatgpt/gsm8k_k8_sc1_s0_e1319_10_14_23_49.jsonl
# 1319 ./output/oct14_actorselect_hinted_palcot_chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_09_12.jsonl
# 1319 ./output/oct15_actorselect_verbose/chatgpt/gsm8k_k8_sc1_s0_e1319_10_16_11_22.jsonl
# 1319 ./output/oct15_actorselect_cotpal_verbose/chatgpt/gsm8k_k8_sc1_s0_e1319_10_15_23_46.jsonl
# 1319 ./output/oct19_enhanced_coh/chatgpt/gsm8k_k3.jsonl
# 1318 ./output/oct19_enhanced_coh/chatgpt/gsm8k_k6.jsonl