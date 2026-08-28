# P1.1b-v2 Qwen deployment-resource benchmark — complete

## Scope

This benchmark compares the deployed FedLS-SQL Qwen2.5-1.5B student at T3
against the local Qwen2.5-Coder-7B teacher loaded in 4-bit mode. It measures
steady-state inference only: prompt formatting/tokenization plus greedy
generation. Model load and SQL scoring are outside the timed region.

Both roles use the same deterministic 32-row Spider subset, full schema,
batch size 4, `max_new_tokens=256`, two warm-up rows, seed 0, and five fresh
independent repetitions on GPU 0 (NVIDIA RTX A5000). All 5/5 repetitions are
eligible for both roles; the comparison requires at least 3.

## Results

| Deployment role | Median s/query (IQR) | Median query/s (IQR) | Peak allocated VRAM | Peak reserved VRAM | Process RSS |
|---|---:|---:|---:|---:|---:|
| FedLS-SQL student, Qwen2.5-1.5B BF16 + T3 adapter | 0.7873 (0.0671) | 1.2701 (0.1090) | 3,474.6 MB | 3,684.7 MB | 1,815.2 MB |
| Teacher reference, Qwen2.5-Coder-7B 4-bit | 1.6460 (0.0100) | 0.6075 (0.0037) | 6,776.8 MB | 7,044.3 MB | 2,021.0 MB |

Under this controlled deployment protocol, the teacher is `2.0906x` slower
per query. Equivalently, the deployed student provides `2.0906x` median
throughput, uses `48.73%` less peak allocated GPU memory, `47.69%` less peak
reserved GPU memory, and `10.18%` less process RSS.

## Claim boundary

This supports a measured SLM-deployment efficiency claim on one shared-server
inference protocol. It is not a federated-7B baseline, training-time benchmark,
energy measurement, concurrency benchmark, full-test latency distribution, or
accuracy comparison on the 32 timing rows. The teacher is already quantized to
4-bit while the student is BF16, so the observed student memory advantage is
relative to that practical teacher deployment configuration.

## Canonical artifacts

- comparison:
  `experiments/resource_benchmark/results/p11b_v2_qwen15b_vs_7b_spider32_s0_independent_gpu0.json`;
- student collection:
  `experiments/resource_benchmark/results/p11b_v2_qwen15b_fedls_t3_spider32_s0_independent_gpu0/`;
- teacher collection:
  `experiments/resource_benchmark/results/p11b_v2_qwen7b_teacher4bit_spider32_s0_independent_gpu0/`;
- nested result commit: `1c82be5`;
- protocol implementation: `487b3b2`;
- comparison fingerprint:
  `60665e60a63ae93c1871401d01a9094caa0e82454f79bf1be473085d794c13c9`.

The exact PowerShell launch line remains recoverable from outer commit
`543f9b6`; the committed per-role configs are the canonical scientific recipe.
