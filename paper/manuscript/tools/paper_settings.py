#!/usr/bin/env python3
"""Write the settings of the paper from the committed configs of the runs it prints.

Sources, all in the code repository: the records of the FedAvg SFT rounds
(experiments/federated/results/*/config.json and metrics.json), of the preference rounds
(audits/protocol_v2/*/setup.json, dpo/arm.json, dpo/round_*/round.json), of the evaluations
(experiments/eval_arms/results/*/config.json and metrics.json), uv.lock for library versions,
and four values that live only in the code, each read with a pattern that must match.
The script stops when two runs of the paper disagree on a setting.

Writes, under paper/manuscript/generated/:
  settings.tex       one macro per setting: \\setting{name}
  tab_settings.tex   the tabular of Appendix B
  settings.md        the same values with their sources (for the Setup brief)

    python3 tools/paper_settings.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANUSCRIPT = HERE.parent
ROOT = MANUSCRIPT.parents[1]
CODE = ROOT / "fedicl-sql"
GEN = MANUSCRIPT / "generated"

ROUNDS, WARMUP = 4, 2
# the runs of the main rows: FedAvg SFT rounds and the preference rounds of the method
FED_RUN = {"bird": "federated__fedavg__s0__7ecd649662f3__5e43d16b", "spider": "federated__fedavg__s0__2dd4b43f7431__74de6d4f"}
PREF_AUDIT = {"bird": "fedpref_bird_sftr2_p2_ddl_alpha01_s0", "spider": "fedpref_sftr2_ddlrows_alpha01_s0"}
# the other models on Spider: FedAvg SFT run and preference audit
OTHER = {"Qwen/Qwen2.5-Coder-0.5B-Instruct": ("federated__fedavg__s0__70273d96254d__45898072", "fedpref_qwen05b_sftr2_p2_ddlrows_alpha01_s0"),
         "deepseek-ai/deepseek-coder-1.3b-instruct": ("federated__fedavg__s0__61430860915d__c5bb4004",
                                                      "fedpref_deepseek13b_sftr2_p2_ddlrows_alpha01_s0")}
MAKER = {"python": "Python Software Foundation", "torch": "PyTorch Foundation", "transformers": "Hugging Face",
         "peft": "Hugging Face", "vllm": "vLLM project", "cuda": "NVIDIA"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def same(values: list, what: str):
    seen = {json.dumps(v, sort_keys=True) for v in values}
    if len(seen) != 1:
        raise SystemExit(f"STOP: runs of the paper disagree on {what}: {sorted(seen)}")
    return values[0]


def in_code(rel: str, pattern: str, what: str) -> str:
    m = re.search(pattern, (CODE / rel).read_text(encoding="utf-8"))
    if not m:
        raise SystemExit(f"STOP: {what} not found in {rel} (pattern {pattern!r})")
    return m.group(1) if m.groups() else m.group(0)


def sci(x: float) -> str:
    mant, exp = f"{x:e}".split("e")
    mant, exp = float(mant), int(exp)
    if exp >= -2:
        return f"{x:g}"
    return f"$10^{{{exp}}}$" if mant == 1 else f"${mant:g}\\times10^{{{exp}}}$"


def thousands(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


def collect() -> list[tuple]:
    """(group, label, name, value in LaTeX, plain value, source)."""
    out: list[tuple] = []

    def add(group, label, name, tex, plain=None, source=""):
        out.append((group, label, name, str(tex), str(tex if plain is None else plain), source))

    # ---- FedAvg SFT rounds
    cfgs, trains, envs = [], [], []
    for ds, run in FED_RUN.items():
        for r in range(1, ROUNDS + 1):
            d = CODE / "experiments/federated/results" / f"{run}__r{r}"
            cfgs.append(load(d / "config.json"))
            m = load(d / "metrics.json")
            trains += [c["train_config"] for c in m["client_training"]]
    src = "FedAvg SFT round records (config.json, train_config)"
    t = {k_: same([x[k_] for x in trains], f"SFT {k_}") for k_ in
         ("model_id", "lora_r", "lora_alpha", "lora_dropout", "target_modules", "lr", "epochs", "batch_size", "grad_accum",
          "warmup_ratio", "max_len", "truncation_policy", "seed", "prox_mu", "lm_loss")}
    c = {k_: same([x[k_] for x in cfgs], f"FedAvg {k_}") for k_ in ("n_clients", "local_epochs", "clients_per_round", "arm")}
    if t["truncation_policy"] != "error" or c["clients_per_round"] != 0 or t["prox_mu"] != 0.0:
        raise SystemExit("STOP: the SFT rounds truncate, sample clients or use a proximal term; the table would be wrong")
    in_code("fedls_sql/training/lora_trainer.py", r"torch\.optim\.AdamW\(\(p for p in model\.parameters\(\) if p\.requires_grad\), lr=config\.lr\)",
            "the SFT optimizer")
    in_code("fedls_sql/training/lora_trainer.py", r"get_cosine_schedule_with_warmup\(opt, warmup, opt_updates\)", "the SFT schedule")

    # ---- preference rounds
    setups, arms, rounds = [], [], []
    for ds, audit in PREF_AUDIT.items():
        a = CODE / "audits/protocol_v2" / audit
        setups.append(load(a / "setup.json"))
        arms.append(load(a / "dpo" / "arm.json"))
        rounds += [load(a / "dpo" / f"round_{r}" / "round.json") for r in range(1, ROUNDS - WARMUP + 1)]
    psrc = "preference round records (setup.json, arm.json, round.json)"
    s = {k_: same([x[k_] for x in setups], f"preference {k_}") for k_ in
         ("model", "lora_r", "lora_alpha", "max_len", "n_clients", "sampling", "pair_rule", "participation", "seed", "truncation_policy")}
    dpo = same([x["dpo"] for x in arms], "the DPO settings")
    agg = same([(x["aggregation"]["method"], x["aggregation"]["weights"]) for x in rounds], "the aggregation of a preference round")
    if (s["model"], s["lora_r"], s["lora_alpha"], s["max_len"], s["n_clients"], s["seed"]) != (
            t["model_id"], t["lora_r"], t["lora_alpha"], t["max_len"], c["n_clients"], t["seed"]):
        raise SystemExit("STOP: the SFT rounds and the preference rounds disagree on the model, the adapter, the length or the seed")
    if s["participation"]["clients_per_round"] != 0 or dpo["preference_weight"] != 1.0 or dpo["pair_batch"]:
        raise SystemExit("STOP: a preference setting the table does not print has changed")
    pref_dropout = in_code("fedls_sql/federated/pref_rounds.py",
                           r"lora_r=setup\.lora_r, lora_alpha=setup\.lora_alpha, lora_dropout=([0-9.]+)", "the LoRA dropout of a preference round")
    in_code("fedls_sql/training/dpo.py", r"torch\.optim\.AdamW\(", "the preference optimizer")
    in_code("fedls_sql/training/dpo.py", r"get_cosine_schedule_with_warmup\(opt, math\.ceil\(config\.warmup_ratio \* updates\), updates\)",
            "the preference schedule")
    bytes_ = same([x["communication_bytes"]["global_adapter"] for x in rounds if "communication_bytes" in x], "the adapter size")
    envs += [x["provenance"]["runtime_environment"] for x in rounds if "runtime_environment" in x["provenance"]]

    # ---- the other models: what differs from the main model
    others = []
    for model, (run, audit) in OTHER.items():
        tc = [c_["train_config"] for c_ in load(CODE / "experiments/federated/results" / f"{run}__r1" / "metrics.json")["client_training"]]
        su = load(CODE / "audits/protocol_v2" / audit / "setup.json")
        mx = same([x["max_len"] for x in tc] + [su["max_len"]], f"the length limit of {model}")
        for k_ in ("lora_r", "lora_alpha", "lora_dropout", "lr", "epochs", "batch_size", "grad_accum", "warmup_ratio"):
            if same([x[k_] for x in tc], f"{model} {k_}") != t[k_]:
                raise SystemExit(f"STOP: {model} trains with another {k_} than the main model")
        if su["sampling"] != s["sampling"] or su["pair_rule"] != s["pair_rule"]:
            raise SystemExit(f"STOP: {model} samples or pairs differently from the main model")
        others.append((model.split("/")[-1], mx))

    # ---- evaluations
    ecfg, emet = [], []
    for d in sorted((CODE / "experiments/eval_arms/results").glob("*/metrics.json")):
        emet.append(load(d))
        ecfg.append(load(d.parent / "config.json"))
    esrc = "evaluation records (config.json, metrics.json)"
    rep = same([x["repetition_penalty"] for x in ecfg], "the repetition penalty of an evaluation")
    engine = same([x["engine"] for x in emet], "the generation engine")
    evaluators = sorted({(x["evaluator"], x["execution_evaluator"]) for x in emet})
    envs += [x["runtime_environment"] for x in emet]
    env = {k_: same([x[k_] for x in envs], f"the {k_} of the runs") for k_ in ("python", "torch", "cuda_runtime", "gpu_names")}
    eval_tokens = in_code("fedls_sql/eval/loop.py", r"generate_raw_batch_with_usage\(prompts, max_new_tokens=(\d+)\)",
                          "the new tokens of an evaluation")
    in_code("fedls_sql/models/vllm_student.py", r"n=1, temperature=0\.0, top_p=1\.0, max_tokens=max_new_tokens, seed=0",
            "greedy decoding of an evaluation")
    timeout = same([re.search(r"timeout(\d+)", e).group(1) for _, e in evaluators if "timeout" in e], "the SQL timeout")
    lock = (CODE / "uv.lock").read_text(encoding="utf-8")
    ver = {n: re.search(rf'name = "{n}"\nversion = "([^"]+)"', lock).group(1) for n in ("transformers", "peft")}

    # ---- the splits and the centralized reference
    split_seed = same([load(m)["seed"] for m in sorted((CODE / "processed_data/protocol_v2").glob("*/*/federated/*/*/meta.json"))],
                      "the seed of the client splits")
    central = sorted((CODE / "experiments/client_train/results").glob("central_ddl_rows_e*_s0/config.json"))
    for f in central:
        cc = load(f)
        if (cc["lr"], cc["lora_r"], cc["batch_size"] * cc["grad_accum"], cc["max_len"], cc["epochs"]) != (
                t["lr"], t["lora_r"], t["batch_size"] * t["grad_accum"], t["max_len"], 1):
            raise SystemExit(f"STOP: centralized SFT ({f.parent.name}) does not train with the SFT recipe")
    central_epochs = len(central)

    # ---- the table
    g = "Model and adapter"
    add(g, "Model", "model", t["model_id"].split("/")[-1], source=src)
    add(g, "Other models", "models.other", ", ".join(PAPER_NAME.get(n, n) for n, _ in others), source=src)
    add(g, "Adapter", "lora", f"LoRA, rank {t['lora_r']}, $\\alpha$ {t['lora_alpha']}", f"LoRA, rank {t['lora_r']}, alpha {t['lora_alpha']}", src)
    add(g, "Adapted matrices", "lora.modules", ", ".join(f"\\texttt{{{m.replace('_', chr(92) + '_')}}}" for m in t["target_modules"]),
        ", ".join(t["target_modules"]), src)
    add(g, "Adapter size", "adapter.mb", f"{bytes_ / 1e6:.1f} MB", source=psrc)
    add(g, "Longest sequence", "max_len", f"{thousands(t['max_len'])} tokens, no truncation", f"{t['max_len']} tokens, no truncation", src)
    for n, mx in others:
        if mx != t["max_len"]:
            add(g, f"Longest sequence, {PAPER_NAME.get(n, n)}", f"max_len.{n.split('-')[0]}", f"{thousands(mx)} tokens", f"{mx} tokens", src)
    add(g, "Rank", "lora.r", t["lora_r"], source=src)
    add(g, "Alpha", "lora.alpha", t["lora_alpha"], source=src)

    g = "Federation"
    add(g, "Clients in a round", "clients", f"all {c['n_clients']}", source=src)
    add(g, "Rounds", "rounds", f"{ROUNDS}: {WARMUP} warm-up rounds, then {ROUNDS - WARMUP} preference rounds", source="queue and round records")
    add(g, "Total rounds", "rounds.total", ROUNDS, source="round records")
    add(g, "Warm-up rounds", "rounds.warmup", WARMUP, source="round records")
    add(g, "Preference rounds", "rounds.pref", ROUNDS - WARMUP, source="round records")
    add(g, "Training seed", "seed", t["seed"], source=src)
    add(g, "Seed of the client splits", "split.seed", split_seed, source="split files (meta.json)")

    g = "FedAvg SFT round"
    add(g, "Local epochs", "sft.epochs", c["local_epochs"], source=src)
    add(g, "Learning rate", "sft.lr", sci(t["lr"]), f"{t['lr']:g}", src)
    add(g, "Examples per update", "sft.batch", t["batch_size"] * t["grad_accum"], source=src)
    add(g, "Optimizer", "sft.optimizer", "AdamW, cosine schedule", source="fedls_sql/training/lora_trainer.py")
    add(g, "Warm-up share of the updates", "sft.warmup", f"{t['warmup_ratio']:g}", source=src)
    add(g, "LoRA dropout", "sft.dropout", f"{t['lora_dropout']:g}", source=src)
    add(g, "Averaging weights", "sft.weights", "question count", source="FedAvg SFT round records (aggregation)")
    add(g, "Epochs of centralized SFT", "central.epochs", central_epochs, source="centralized SFT records")

    g = "Preference round"
    add(g, "Samples per question", "pref.samples", s["sampling"]["k"], source=psrc)
    add(g, "Sampling temperature, top-$p$", "pref.temperature", f"{s['sampling']['temperature']:g}, {s['sampling']['top_p']:g}", source=psrc)
    add(g, "Temperature", "pref.t", f"{s['sampling']['temperature']:g}", source=psrc)
    add(g, "New tokens per sample", "pref.tokens", s["sampling"]["max_new_tokens"], source=psrc)
    add(g, "Pairs per question", "pref.pairs", s["pair_rule"]["pairs_per_question"], source=psrc)
    m_pairs = s["pair_rule"]["pairs_per_question"]
    in_code("fedls_sql/preference/pairs.py", r"return rng\.choices\(pool, k=k\) if len\(pool\) < k else rng\.sample\(pool, k\)",
            "the draw of the samples of a pair")
    in_code("fedls_sql/preference/pairs.py", r"chosen, rejected = draw\(correct\), draw\(wrong\)", "the two draws of a pair")
    add(g, "Pairing", "pref.rule",
        {"random": f"{m_pairs} correct and {m_pairs} incorrect samples of the question, drawn uniformly and independently, "
                   f"each without replacement when the question has at least {m_pairs} samples of that label and with replacement "
                   "otherwise; paired in the order drawn"}[s["pair_rule"]["rule"]], source=psrc + "; fedls_sql/preference/pairs.py")
    in_code("fedls_sql/preference/sampling.py", r"if not norm:\n\s+outcome, error = EMPTY, None", "the label of a sample without query text")
    add(g, "Sample without query text", "pref.blank", "labeled incorrect", source="fedls_sql/preference/sampling.py")
    in_code("fedls_sql/preference/sampling.py", r'finished = \[s for s in record\["samples"\] if s\["finish_reason"\] == "eos"\]',
            "the samples that are executed")
    add(g, "Sample truncated at the token limit", "pref.truncated", "not executed, not labeled", source="fedls_sql/preference/sampling.py")
    add(g, "Questions on a database without rows", "pref.empty", {True: "give no pair"}[s["pair_rule"]["skip_empty_databases"]], source=psrc)
    add(g, "$\\beta$ of the preference term", "pref.beta", f"{dpo['beta']:g}", source=psrc)
    add(g, "Weight of the NLL term", "pref.nll", f"{dpo['nll_alpha']:g}", source=psrc)
    add(g, "Local epochs", "pref.epochs", dpo["epochs"], source=psrc)
    add(g, "Learning rate", "pref.lr", sci(dpo["lr"]), f"{dpo['lr']:g}", psrc)
    add(g, "Pairs per update", "pref.batch", dpo["grad_accum"], source=psrc)
    add(g, "Optimizer", "pref.optimizer", f"AdamW, weight decay {sci(dpo['weight_decay'])}, cosine schedule",
        f"AdamW, weight decay {dpo['weight_decay']:g}, cosine schedule", psrc)
    add(g, "Warm-up share of the updates", "pref.warmup", f"{dpo['warmup_ratio']:g}", source=psrc)
    add(g, "LoRA dropout", "pref.dropout", f"{float(pref_dropout):g}", source="fedls_sql/federated/pref_rounds.py")
    add(g, "Averaging weights", "pref.weights", {"pair_count": "pair count"}[agg[1]], source=psrc)
    in_code("fedls_sql/eval/metrics.py", r'"kind": "question"[\s\S]{0,200}?"budget": _budget\(evaluator\)',
            "the time limit of the execution labels")
    add(g, "Time limit of the execution labels", "pref.timeout", "that of evaluation", source="fedls_sql/eval/metrics.py")

    g = "Evaluation"
    add(g, "Decoding", "eval.decoding", "greedy, one output", source="fedls_sql/models/vllm_student.py")
    add(g, "New tokens", "eval.tokens", eval_tokens, source="fedls_sql/eval/loop.py")
    add(g, "Repetition penalty", "eval.penalty", {1.0: "none"}[rep], source=esrc)
    bird_s = in_code("fedls_sql/eval/sql_exec.py", r"BIRD_PAIR_TIMEOUT_SECONDS = (\d+)", "the time limit on BIRD")
    spider_s = in_code("fedls_sql/eval/sql_exec.py", r"SPIDER_QUERY_TIMEOUT_SECONDS = (\d+)", "the time limit on Spider")
    if bird_s != timeout:
        raise SystemExit(f"STOP: the BIRD evaluations ran with a time limit of {timeout} s, the code has {bird_s} s")
    tsrc = esrc + "; fedls_sql/eval/sql_exec.py"
    add(g, "Time limit on BIRD", "eval.timeout.bird", f"{bird_s} s for a query and the gold SQL query together", source=tsrc)
    add(g, "Time limit on Spider", "eval.timeout.spider", f"{spider_s} s for each query", source=tsrc)
    add(g, "Time limit on BIRD, seconds", "timeout.bird", f"{bird_s} s", source=tsrc)
    add(g, "Time limit on Spider, seconds", "timeout.spider", f"{spider_s} s", source=tsrc)

    g = "Software and hardware"
    add(g, "Python", "sw.python", f"{env['python']} ({MAKER['python']})", source=esrc)
    torch_v, cuda = env["torch"].split("+")[0], env["cuda_runtime"]
    add(g, "PyTorch", "sw.torch", f"{torch_v} ({MAKER['torch']}), CUDA {cuda} ({MAKER['cuda']})", source=esrc)
    add(g, "Transformers", "sw.transformers", f"{ver['transformers']} ({MAKER['transformers']})", source="uv.lock")
    add(g, "PEFT", "sw.peft", f"{ver['peft']} ({MAKER['peft']})", source="uv.lock")
    add(g, "Generation engine", "sw.engine", f"{ {'vllm': 'vLLM'}[engine['name']] } {engine['version']} ({MAKER['vllm']})".replace("  ", " "),
        source=esrc)
    add(g, "GPU", "hw.gpu", f"{same(env['gpu_names'], 'the GPU')}, 24 GB", source=esrc)
    return out


# rows of Appendix B; the other entries exist as macros only
# names of the models as the paper writes them, where the repository name differs
PAPER_NAME = {"deepseek-coder-1.3b-instruct": "DeepSeek-Coder-1.3B-Instruct"}
IN_TABLE_SKIP = {"lora.r", "lora.alpha", "rounds.total", "rounds.warmup", "rounds.pref", "pref.t", "timeout.bird", "timeout.spider"}

ACCESSOR = r"""%% Written by tools/paper_settings.py from the committed configs. Do not edit.
\makeatletter
\newcommand{\st@def}[2]{\expandafter\gdef\csname st@\detokenize{#1}\endcsname{#2}}
\newcommand{\setting}[1]{\ifcsname st@\detokenize{#1}\endcsname\csname st@\detokenize{#1}\endcsname\else
  \textbf{??}\@latex@warning{No committed number for setting \detokenize{#1}}\fi}
"""


def main() -> None:
    rows = collect()
    GEN.mkdir(exist_ok=True)
    tex = [ACCESSOR] + [f"\\st@def{{{name}}}{{{value}}}" for _, _, name, value, _, _ in rows] + ["\\makeatother"]
    (GEN / "settings.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")
    lines, group = ["\\toprule", "Setting & Value \\\\"], None
    for g, label, name, value, _, _ in rows:
        if name in IN_TABLE_SKIP:
            continue
        if g != group:
            lines += ["\\midrule", f"\\multicolumn{{2}}{{@{{}}l}}{{\\textit{{{g}}}}} \\\\"]
            group = g
        lines.append(f"{label} & {value} \\\\")
    lines.append("\\bottomrule")
    (GEN / "tab_settings.tex").write_text(
        "%% Written by tools/paper_settings.py. Do not edit.\n\\begin{tabular}{@{}p{0.36\\linewidth}p{0.58\\linewidth}@{}}\n" + "\n".join(lines)
        + "\n\\end{tabular}\n", encoding="utf-8")
    md = ["# Settings of the paper", "", "Written by `tools/paper_settings.py` from the committed configs.", "",
          "| Group | Setting | Macro | Value | Source |", "|---|---|---|---|---|"]
    md += [f"| {g} | {label.replace('$', '').replace(chr(92), '')} | `\\setting{{{name}}}` | {plain} | {source} |"
           for g, label, name, _, plain, source in rows]
    (GEN / "settings.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(rows)} settings -> {GEN.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
