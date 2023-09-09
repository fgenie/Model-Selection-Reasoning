import yaml
CODE_F = 'prompts_code_old.yaml'
PLAN_F = 'prompts_plan_old.yaml'

# write to txt
def main():
    process_fewshots_code(CODE_F)



def process_fewshots_code(codef:str):
    d = yaml.full_load(open(codef))
    fewshots = d['fewshots']
    def split2query_completion(txt:str)->tuple:
        lines = txt.replace("# </end>", "").strip().split("\n")
        justafter_docstring = lines.index("    '''")+1
        lines_ = lines[justafter_docstring:]
        codestarts = lines_.index("    '''") + justafter_docstring + 1
        query = "\n".join(lines[:codestarts]) 
        codecompletion = "\n".join(lines[codestarts:])
        return query, codecompletion
    
    qs, codes = [], []
    for shot in fewshots:
        query, code_completion = split2query_completion(shot)
        qs.append(query);codes.append(code_completion)
    
    with open('fs_code_query.txt', 'w') as qf, open('fs_code_completion.txt', 'w') as cf:
        sep = "\n=====================================\n"
        for q, c in zip(qs, codes):
            qf.write(q)
            qf.write(sep)
            cf.write(c)
            cf.write(sep)
if __name__ == '__main__':
    main()