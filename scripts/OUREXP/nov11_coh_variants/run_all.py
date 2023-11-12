import subprocess as sb

pfiles = [
# # 150건짜리 chatgpt + 15건짜리 gpt4
# 'prompts/prep_reflexion/6_cohlike_solve_prompt.txt', 
# 'prompts/prep_reflexion/7_cohlike_solvetwice_prompt.txt', 
'prompts/prep_reflexion/8_cohlike_solvetwice_prompt.yaml'


# # 75 건짜리 coh gpt4에 진행 (baseline은 nov12 폴더로 빼놓음)
# 'prompts/prep_reflexion/6_cohlike_solve_prompt_cotpal_1.txt', 
# 'prompts/prep_reflexion/7_cohlike_solvetwice_prompt_cotpal_1.txt', 
# 'prompts/prep_reflexion/8_cohlike_solvetwice_prompt_cotpal_1.yaml', 

# 'prompts/prep_reflexion/6_cohlike_solve_prompt_cotpal_2.txt', 
# 'prompts/prep_reflexion/7_cohlike_solvetwice_prompt_cotpal_2.txt', 
# 'prompts/prep_reflexion/8_cohlike_solvetwice_prompt_cotpal_2.yaml', 

# 'prompts/prep_reflexion/6_cohlike_solve_prompt_cotpal_3.txt', 
# 'prompts/prep_reflexion/7_cohlike_solvetwice_prompt_cotpal_3.txt', 
# 'prompts/prep_reflexion/8_cohlike_solvetwice_prompt_cotpal_3.yaml', 
]

for f in pfiles:
    cmd = f'bash run_a_prompt.sh {f}'
    print(cmd)
    sb.call(cmd, shell=True)




