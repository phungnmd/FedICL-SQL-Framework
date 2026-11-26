# Settings of the paper

Written by `tools/paper_settings.py` from the committed configs.

| Group | Setting | Macro | Value | Source |
|---|---|---|---|---|
| Model and adapter | Model | `\setting{model}` | Qwen2.5-Coder-1.5B-Instruct | FedAvg SFT round records (config.json, train_config) |
| Model and adapter | Other models | `\setting{models.other}` | Qwen2.5-Coder-0.5B-Instruct, DeepSeek-Coder-1.3B-Instruct | FedAvg SFT round records (config.json, train_config) |
| Model and adapter | Adapter | `\setting{lora}` | LoRA, rank 16, alpha 32 | FedAvg SFT round records (config.json, train_config) |
| Model and adapter | Adapted matrices | `\setting{lora.modules}` | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj | FedAvg SFT round records (config.json, train_config) |
| Model and adapter | Adapter size | `\setting{adapter.mb}` | 73.9 MB | preference round records (setup.json, arm.json, round.json) |
| Model and adapter | Longest sequence | `\setting{max_len}` | 7168 tokens, no truncation | FedAvg SFT round records (config.json, train_config) |
| Model and adapter | Longest sequence, DeepSeek-Coder-1.3B-Instruct | `\setting{max_len.deepseek}` | 8704 tokens | FedAvg SFT round records (config.json, train_config) |
| Model and adapter | Rank | `\setting{lora.r}` | 16 | FedAvg SFT round records (config.json, train_config) |
| Model and adapter | Alpha | `\setting{lora.alpha}` | 32 | FedAvg SFT round records (config.json, train_config) |
| Federation | Clients in a round | `\setting{clients}` | all 5 | FedAvg SFT round records (config.json, train_config) |
| Federation | Rounds | `\setting{rounds}` | 4: 2 warm-up rounds, then 2 preference rounds | queue and round records |
| Federation | Total rounds | `\setting{rounds.total}` | 4 | round records |
| Federation | Warm-up rounds | `\setting{rounds.warmup}` | 2 | round records |
| Federation | Preference rounds | `\setting{rounds.pref}` | 2 | round records |
| Federation | Training seed | `\setting{seed}` | 0 | FedAvg SFT round records (config.json, train_config) |
| Federation | Seed of the client splits | `\setting{split.seed}` | 42 | split files (meta.json) |
| FedAvg SFT round | Local epochs | `\setting{sft.epochs}` | 1 | FedAvg SFT round records (config.json, train_config) |
| FedAvg SFT round | Learning rate | `\setting{sft.lr}` | 0.0002 | FedAvg SFT round records (config.json, train_config) |
| FedAvg SFT round | Examples per update | `\setting{sft.batch}` | 16 | FedAvg SFT round records (config.json, train_config) |
| FedAvg SFT round | Optimizer | `\setting{sft.optimizer}` | AdamW, cosine schedule | fedls_sql/training/lora_trainer.py |
| FedAvg SFT round | Warm-up share of the updates | `\setting{sft.warmup}` | 0.03 | FedAvg SFT round records (config.json, train_config) |
| FedAvg SFT round | LoRA dropout | `\setting{sft.dropout}` | 0.05 | FedAvg SFT round records (config.json, train_config) |
| FedAvg SFT round | Averaging weights | `\setting{sft.weights}` | question count | FedAvg SFT round records (aggregation) |
| FedAvg SFT round | Epochs of centralized SFT | `\setting{central.epochs}` | 3 | centralized SFT records |
| Preference round | Samples per question | `\setting{pref.samples}` | 10 | preference round records (setup.json, arm.json, round.json) |
| Preference round | Sampling temperature, top-p | `\setting{pref.temperature}` | 1, 1 | preference round records (setup.json, arm.json, round.json) |
| Preference round | Temperature | `\setting{pref.t}` | 1 | preference round records (setup.json, arm.json, round.json) |
| Preference round | New tokens per sample | `\setting{pref.tokens}` | 256 | preference round records (setup.json, arm.json, round.json) |
| Preference round | Pairs per question | `\setting{pref.pairs}` | 2 | preference round records (setup.json, arm.json, round.json) |
| Preference round | Pairing | `\setting{pref.rule}` | 2 correct and 2 incorrect samples of the question, drawn uniformly and independently, each without replacement when the question has at least 2 samples of that label and with replacement otherwise; paired in the order drawn | preference round records (setup.json, arm.json, round.json); fedls_sql/preference/pairs.py |
| Preference round | Sample without query text | `\setting{pref.blank}` | labeled incorrect | fedls_sql/preference/sampling.py |
| Preference round | Sample truncated at the token limit | `\setting{pref.truncated}` | not executed, not labeled | fedls_sql/preference/sampling.py |
| Preference round | Questions on a database without rows | `\setting{pref.empty}` | give no pair | preference round records (setup.json, arm.json, round.json) |
| Preference round | beta of the preference term | `\setting{pref.beta}` | 0.1 | preference round records (setup.json, arm.json, round.json) |
| Preference round | Weight of the NLL term | `\setting{pref.nll}` | 1 | preference round records (setup.json, arm.json, round.json) |
| Preference round | Local epochs | `\setting{pref.epochs}` | 1 | preference round records (setup.json, arm.json, round.json) |
| Preference round | Learning rate | `\setting{pref.lr}` | 5e-05 | preference round records (setup.json, arm.json, round.json) |
| Preference round | Pairs per update | `\setting{pref.batch}` | 16 | preference round records (setup.json, arm.json, round.json) |
| Preference round | Optimizer | `\setting{pref.optimizer}` | AdamW, weight decay 0.0001, cosine schedule | preference round records (setup.json, arm.json, round.json) |
| Preference round | Warm-up share of the updates | `\setting{pref.warmup}` | 0.1 | preference round records (setup.json, arm.json, round.json) |
| Preference round | LoRA dropout | `\setting{pref.dropout}` | 0 | fedls_sql/federated/pref_rounds.py |
| Preference round | Averaging weights | `\setting{pref.weights}` | pair count | preference round records (setup.json, arm.json, round.json) |
| Preference round | Time limit of the execution labels | `\setting{pref.timeout}` | that of evaluation | fedls_sql/eval/metrics.py |
| Evaluation | Decoding | `\setting{eval.decoding}` | greedy, one output | fedls_sql/models/vllm_student.py |
| Evaluation | New tokens | `\setting{eval.tokens}` | 256 | fedls_sql/eval/loop.py |
| Evaluation | Repetition penalty | `\setting{eval.penalty}` | none | evaluation records (config.json, metrics.json) |
| Evaluation | Time limit on BIRD | `\setting{eval.timeout.bird}` | 30 s for a query and the gold SQL query together | evaluation records (config.json, metrics.json); fedls_sql/eval/sql_exec.py |
| Evaluation | Time limit on Spider | `\setting{eval.timeout.spider}` | 60 s for each query | evaluation records (config.json, metrics.json); fedls_sql/eval/sql_exec.py |
| Evaluation | Time limit on BIRD, seconds | `\setting{timeout.bird}` | 30 s | evaluation records (config.json, metrics.json); fedls_sql/eval/sql_exec.py |
| Evaluation | Time limit on Spider, seconds | `\setting{timeout.spider}` | 60 s | evaluation records (config.json, metrics.json); fedls_sql/eval/sql_exec.py |
| Software and hardware | Python | `\setting{sw.python}` | 3.11.15 (Python Software Foundation) | evaluation records (config.json, metrics.json) |
| Software and hardware | PyTorch | `\setting{sw.torch}` | 2.11.0 (PyTorch Foundation), CUDA 12.8 (NVIDIA) | evaluation records (config.json, metrics.json) |
| Software and hardware | Transformers | `\setting{sw.transformers}` | 5.10.2 (Hugging Face) | uv.lock |
| Software and hardware | PEFT | `\setting{sw.peft}` | 0.19.1 (Hugging Face) | uv.lock |
| Software and hardware | Generation engine | `\setting{sw.engine}` | vLLM 0.33.0 (vLLM project) | evaluation records (config.json, metrics.json) |
| Software and hardware | GPU | `\setting{hw.gpu}` | NVIDIA RTX A5000, 24 GB | evaluation records (config.json, metrics.json) |
