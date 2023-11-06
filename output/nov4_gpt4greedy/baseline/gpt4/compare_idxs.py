f = ['baseline_conflict_idx.txt',
    '/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/output/nov4_gpt4greedy/coh_cotpal_1/gpt4/coh_coflict_idx.txt',
    ]

sets = [set(open(f_).readlines()) for f_ in f]

intr = sets[0].intersection(sets[1])
print(len(sets[1]))
print(len(intr))