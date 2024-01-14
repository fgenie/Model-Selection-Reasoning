from fire import Fire
import jsonlines as jsl
from tqdm import tqdm
import pandas as pd

from datetime import datetime
from typing import Any


from llm_query_utils import *

CONTINUE_WRITING_INVOKE_PROMPT = "Continue reaching to the correct answer, carefully following the format presented above."  # same as in 5_extend_*.py

"""
unify the field of the inference records.

row:
    (from gsm)
    - idx
    - question
    - ans
    (from what's inferred)
    - prompt_path
    - ansmap:
        {cot: pal: p2c:}
    - solmap:
        {cot: pal: p2c:}
    - majority_ans: None or majority answer (final answer to be evaluated)
    - selection_or_rims: 
        각자에 합당한 아웃풋
        rims: eval_friendly_d
        model_selection (baseline): 
            {
                good_method, 
                good_ans,
                selection_choice,
                bad_method, 
                bad_ans,
            }
        majority_vote: True (if inference ends with majority vote)
    


"""


def evaluate_result_to_md_table(
    records: list,
    original_dataset_length: int,
    outdir: str = "",
):
    result_df = pd.DataFrame(records)
    failed = original_dataset_length - len(result_df)

    corrects = result_df.answer.diff(result_df.majority_ans).abs() < 1e-3
    n_correct = corrects.sum()
    raise NotImplementedError("need to implement the rest of the metrics...")
    return


def indiv_inference(
    row: dict = None,
    num_methods: int = 3,
    temperature: float = 0.0,
    n: int = 1,
    backbone: str = "chatgpt",  # [chatgpt, gpt4] # later mixtral / llama
    seed: int = 777,
):
    """
    inference each method and return indiv results


    return:
        solmap : {cot: pal: p2c:}
        ansmap : {cot: pal: p2c:} (solution executed)
    """

    if n > 1:
        raise NotImplementedError(
            "n>1 will serve as a self-consistency parameter, not implemented yet"
        )

    question = row["question"]

    # check for already-done indiv methods
    if "ansmap" in row.keys() and "solmap" in row.keys():
        if row["ansmap"] and row["solmap"]:
            ansmap = row["ansmap"]
            solmap = row["solmap"]
            missing_methods = []
            for method in ["cot", "pal", "p2c"]:
                if method not in ansmap.keys():
                    if not ansmap[method]:
                        missing_methods.append(method)
    else:
        missing_methods = "cot pal p2c".split()
        ansmap = dict()
        solmap = dict()

    if "cot" in missing_methods:
        # try:
        cot_lst, _msgs = query_cot(
            question, temperature=temperature, n=n, backbone=backbone, seed=seed
        )
        # except Exception as e:
        #     print(e)
        #     cot_lst, _msgs = [None], ['cot query failed']
        cot_sol = cot_lst.pop()  # solution: str
        # try:
        cot_ans = extract_num_turbo(cot_sol)
        # except Exception as e:
        #     print(e)
        #     cot_ans = None
        solmap["cot"] = cot_sol
        ansmap["cot"] = cot_ans

    if "pal" in missing_methods:
        # try:
        pal_lst, __msgs = query_pal(
            question, temperature=temperature, n=n, backbone=backbone, seed=seed
        )
        # except Exception as e:
        #     print(e)
        #     pal_lst, __msgs = [None], ['pal query failed']
        pal_sol = pal_lst.pop()
        # try:
        pal_ans = safe_execute_turbo(pal_sol)
        # except Exception as e:
        #     print(e)
        #     pal_ans = None
        solmap["pal"] = pal_sol
        ansmap["pal"] = pal_ans

    if num_methods == 3:
        if "p2c" in missing_methods:
            # try:
            code_lst, plan_lst, ___msgs = query_plancode(
                question,
                plan_temperature=temperature,
                code_temperature=temperature,
                backbone=backbone,
                n=n,
                seed=seed,
            )
            # except Exception as e:
            #     print(e)
            #     code_lst, plan_lst, ___msgs = [None], [None], ['p2c query failed']

            plan = plan_lst.pop()
            p2c_solution = [plan + "\n" + code for code in code_lst]
            code = code_lst.pop()
            # try:
            p2c_ans = safe_execute_turbo(code)
            # except Exception as e:
            #     print(e)
            #     p2c_ans = None
            ansmap["p2c"] = p2c_ans
            solmap["p2c"] = p2c_solution

    return ansmap, solmap  # updated ones


def rims_inference(
    prompt_f: str = "",
    gsm_jslf: str = "",
    eval_indiv_method: bool = False,
    # llm options
    temperature: float = 0.0,
    n: int = 1,  # later for self-consistency
    backbone: str = "chatgpt",  # [chatgpt, gpt4] # later mixtral / llama
    seed: int = 777,
    start_idx: int = 0,
    # dev option
    dbg: bool = False,
):
    assert prompt_f, f"need to specify {prompt_f=}"
    assert gsm_jslf, f"need to specify {gsm_jslf=}"

    if n > 1:
        raise NotImplementedError(
            "n>1 will serve as a self-consistency parameter, not implemented yet"
        )

    # output directory for the inference results:
    outdir = Path(gsm_jslf).resolve().parent / (
        Path(gsm_jslf).stem + "_" + Path(prompt_f).stem
    )  # same dirname as prompt file stem
    if not outdir.exists():
        outdir.mkdir(parents=True)
    dt_string = datetime.now().strftime("%m_%d_%H_%M")
    outpath = (
        outdir
        / f"{'dbg_' if dbg else ''}{backbone}_rims{'_eval_indiv' if eval_indiv_method else ''}_{dt_string}.jsonl"
    )

    # load_gsm_dataset to infer on
    records = list(jsl.open(gsm_jslf))[start_idx:]

    print(f"writing to {outpath}")
    with jsl.open(outpath, "w") as writer:
        for row in tqdm(records):
            try:
                question = row["question"]

                # individual method inference: this will check if row already has individual method inferred, and if done, keep those to use.
                ansmap, solmap = indiv_inference(
                    row,
                    num_methods=3,
                    temperature=temperature,
                    n=n,
                    backbone=backbone,
                    seed=seed,
                )
                row["ansmap"] = ansmap
                row["solmap"] = solmap

                # is there majority answer? in ansmap?
                majority_ans = get_concordant_answer(
                    list(ansmap.values()), ensure_unanimity=False
                )

                # do rims
                if majority_ans is None:
                    if (
                        eval_indiv_method
                    ):  # (optional) are we going to check the individual method's correctness?
                        checked_answers = set()
                        for method, sol in solmap.items():
                            if isinstance(sol, list):
                                sol = sol.pop()
                                if solmap[method]:
                                    raise NotImplementedError(
                                        f"not implemented for n>1, solmap contains more than 1 solution per method {solmap[method]}"
                                    )
                            if ansmap[method] in checked_answers:
                                continue  # do not check twice if some ans judged as wrong
                            to_eval_blurb = solution2blurb(
                                method=method, solution=sol, ans=ansmap[method]
                            )
                            gpt_msg = [
                                {"role": "assistant", "content": to_eval_blurb},
                                {
                                    "role": "user",
                                    "content": CONTINUE_WRITING_INVOKE_PROMPT,
                                },
                            ]
                            (
                                eval_friendly_d,
                                parse_dd,
                                raw_query_out,
                                query_msg,
                            ) = query_rims_inference(
                                question,
                                prompt_f,
                                backbone=backbone,
                                temperature=temperature,
                                continue_writing_gpt_messages=gpt_msg,
                                stop_tok=["`Mistakes`: "],
                            )

                            checked_answers.add(ansmap[method])
                            # check if the solution is considered correct
                            if "`Evaluation`: Correct" in raw_query_out:
                                eval_friendly_d.update(
                                    {
                                        "--eval_indiv_method": (True, method),
                                        "raw_query_out": raw_query_out,
                                        "query_msg": query_msg,
                                    }
                                )
                                row["selection_or_rims"] = eval_friendly_d
                                row["majority_ans"] = ansmap[method]
                                majority_ans = row["majority_ans"]

                    if majority_ans is None:  # problems are not done properly.
                        # if dbg:
                        (
                            eval_friendly_d,
                            __,
                            raw_query_out,
                            query_msg,
                        ) = query_rims_inference(
                            question,
                            prompt_f,
                            backbone=backbone,
                            temperature=temperature,
                        )
                        # else:
                        #     eval_friendly_d, __, raw_query_out, query_msg = do_with_tenacity(query_rims_inference(question, prompt_f, backbone=backbone, temperature=temperature))

                        eval_friendly_d.update(
                            {"raw_query_out": raw_query_out, "query_msg": query_msg}
                        )
                        row[
                            "selection_or_rims"
                        ] = eval_friendly_d  # this contains all we need depicted above
                        row["majority_ans"] = eval_friendly_d["good_ans"]
                else:
                    row["selection_or_rims"] = {"majority_vote": True}
                    row["majority_ans"] = majority_ans
                row["prompt_file"] = str(prompt_f)
                row["inference_mode"] = "rims"
            except Exception as e:
                print(e)
                print(f"error occured at {row['index']}")
                row["selection_or_rims"] = {"error": True}
                row["majority_ans"] = None
                row["prompt_file"] = str(prompt_f)
                row["inference_mode"] = "rims"
                continue
            writer.write(row)

    return


def baseline_inference(
    prompt_f: str = "math_prompt.py",  # only for recording promptfilename to the result. Actual prompt is read at `llm_query_utils.py`
    gsm_jslf: str = "",
    num_methods: int = 3,  # number of methods (3-> cot pal p2c / 2-> cot pal )
    start_idx: int = 0,
    # llm options
    temperature: float = 0.0,
    n: int = 1,  # later for self-consistency
    backbone: str = "chatgpt",  # [chatgpt, gpt4] # later mixtral / llama
    seed: int = 777,
    # dev option
    dbg: bool = False,
):
    assert gsm_jslf, f"need to specify {gsm_jslf=}"

    if n > 1:
        raise NotImplementedError(
            "n>1 will serve as a self-consistency parameter, not implemented yet"
        )

    # load_gsm_dataset to infer on
    records = list(jsl.open(gsm_jslf))[start_idx:]
    if dbg:
        records = records[17:100]

    # output directory for the inference results:
    outdir = Path(gsm_jslf).resolve().parent / (
        Path(gsm_jslf).stem + "_model_selection_baseline"
    )  # same dirname as prompt file stem
    if not outdir.exists():
        outdir.mkdir(parents=True)
    dt_string = datetime.now().strftime("%m_%d_%H_%M")
    outpath = outdir / f"{backbone}_{dt_string}_model_selection{num_methods}.jsonl"

    print(f"writing to {outpath}")
    with jsl.open(outpath, "w") as writer:
        for row in tqdm(records):
            question = row["question"]

            # individual method inference: this will check if row already has individual method inferred, and if done, keep those to use.
            ansmap, solmap = indiv_inference(
                row,
                num_methods=3,
                temperature=temperature,
                n=n,
                backbone=backbone,
                seed=seed,
            )
            row["ansmap"] = ansmap
            row["solmap"] = solmap

            # is there majority answer? in ansmap? (2,2,1 --> 2 is majority, can assert hard condition such as requiring unanimous votes)
            majority_ans = get_concordant_answer(
                list(ansmap.values()), ensure_unanimity=False
            )

            if majority_ans is None:  # do selection
                chosen_method, selection_str = query_selection(
                    question,
                    backbone=backbone,
                    cot_solution=solmap["cot"],
                    pal_solution=solmap["pal"],
                    p2c_plan_code_solution=solmap["p2c"],
                )
                row["selection_or_rims"] = {
                    "good_method": chosen_method,
                    "good_answer": ansmap[chosen_method],
                    "good_solution": solmap[chosen_method],
                    "selection_str": selection_str,
                }
                row["majority_ans"] = ansmap[chosen_method]
            else:
                row["selection_or_rims"] = {"majority_vote": True}
                row["majority_ans"] = majority_ans
            row["prompt_file"] = prompt_f
            row["inference_mode"] = f"baseline {num_methods} methods"
            writer.write(row)

        return


if __name__ == "__main__":
    Fire()
    """
    usage:
    python 99_run_inference baseline_inference|rims_inference [--KWARGS VALUE]*
    """
