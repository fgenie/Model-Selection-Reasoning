import subprocess as sb

pfiles = [
    # '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src/RIMS/99_9_rims_cotpal_inference_prompt_k2_long_DEC4.txt',
    '/home/sison/Model-Selection-Reasoning/src/RIMS/99_9_rims_cotpal_inference_prompt_k2_long_DEC4.txt',
    # '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src/RIMS/99_7_rims_cotpal_inference_prompt_k2_long_DEC4.txt',
    '/home/sison/Model-Selection-Reasoning/src/RIMS/99_7_rims_cotpal_inference_prompt_k2_long_DEC4.txt',
]

for f in pfiles:
    cmd = f'bash run_a_prompt.sh {f} > {f}.out'
    print(cmd)
    sb.call(cmd, shell=True)




