# FedLS-SQL: literature và giới hạn claim

Cập nhật: 2026-11-04. Gộp từ ba file đã archive (bản đầy đủ, kèm các lớp
đính chính): [COT_RL_RESEARCH](../archive/directions_2026-11/COT_RL_RESEARCH_2026-11-03.md),
[RELATED_WORK_NOVELTY_MATRIX](../archive/directions_2026-11/RELATED_WORK_NOVELTY_MATRIX_2026-10-28.md),
[related_papers](../archive/directions_2026-11/related_papers_2026-10.md). File này giới hạn
cách diễn đạt claim, không giới hạn việc chọn hướng (AGENTS.md, novelty bar).

## 1. Giới hạn claim

- Không claim "first" và không giấu closest work.
- FL + LoRA, LLM-to-SLM KD, KD server lặp theo round (FedCoLLM), KD qua
  rationale (FedCoT), và lọc target của teacher bằng execution (Struct-SQL)
  đều đã có. Federated RL với verifiable reward đã có ở toán và code (FedMOA,
  PubSwap). Phần claim được là adaptation cho federated cross-schema
  Text-to-SQL và bằng chứng có comparator tương ứng.
- Privacy là cô lập dữ liệu theo cấu trúc, không phải differential privacy.

## 2. Closest work theo trục

| Trục | Bài gần nhất | Khác với ta |
|---|---|---|
| Federated Text-to-SQL | Zhang et al., [Federated Learning for Semantic Parsing](https://aclanthology.org/2023.acl-long.678/), ACL 2023 | Mỗi client một dataset, không teacher, không RL |
| FL + server LLM / client SLM | [FedCoLLM](https://arxiv.org/abs/2411.11707) (mutual KD trên dữ liệu phụ mỗi round), [FedMKT](https://aclanthology.org/2025.coling-main.17/) (COLING 2025) | Task chung, không execution check, không RL |
| FL + CoT từ server | [FedCoT](https://aclanthology.org/2025.findings-emnlp.454/) (Findings EMNLP 2025) | Một client, không gộp model, không execution check |
| FL + RL verifiable reward | [FedMOA](https://arxiv.org/abs/2602.00453) (federated GRPO, toán/code), [PubSwap](https://arxiv.org/abs/2604.12160) (federated RLVR, public set nhỏ) | Không teacher, không Text-to-SQL, không cross-schema |
| FL + DPO | [OpenFedLLM](https://arxiv.org/pdf/2402.06954) (FedDPO), [FedPDPO](https://arxiv.org/html/2603.19741) | Pair cố định hoặc task khác; FedPDPO giảm khi tăng số client |
| Replay chống forgetting | [DER](https://arxiv.org/abs/2004.07211) (NeurIPS 2020), Zhao et al. 2018 (public data chống non-IID) | Ta replay logit của teacher ngoài, trong FL |
| CoT distillation Text-to-SQL | [Struct-SQL](https://arxiv.org/abs/2512.17053), [OmniSQL](https://arxiv.org/html/2503.02240v2), [RetrySQL](https://arxiv.org/html/2507.02529v2) | Centralized |
| RL Text-to-SQL | [ExCoT](https://arxiv.org/html/2503.19988v1) (DPO theo execution), [SLM-SQL](https://aclanthology.org/2025.findings-ijcnlp.92.pdf), [FINER-SQL](https://arxiv.org/html/2605.03465v1), [Think2SQL](https://arxiv.org/html/2504.15077), [Arctic-Text2SQL-R1](https://arxiv.org/html/2505.20315) | Centralized |
| RL quên ít hơn SFT | Shenfeld et al. 2025, RL's Razor; Chu et al. 2025, SFT Memorizes, RL Generalizes (ICML 2025) | Không federated; cơ sở cho giả thuyết của hướng A. Chưa đọc PDF trong dự án, cần kiểm khi viết |
| On-policy distillation | Agarwal et al., [GKD](https://arxiv.org/html/2306.13649v3), ICLR 2024 | Centralized; cơ sở cho hướng C |

## 3. CoT có hơn SQL-only không

Chỉ các bài có cả hai dòng trên cùng model:

| Bài | Model | Điều kiện | SQL-only | CoT |
|---|---|---|---:|---:|
| RetrySQL | OpenCoder 1.5B | BIRD, gold schema links, beam | 37.48 | 54.71 |
| Think2SQL | Qwen-Coder 3B, SFT | BIRD, schema thu gọn | 42.7 | 46.0 |
| OmniSQL | Coder 7B | Spider dev / test, greedy | 76.9 / 80.7 | 80.3 / 86.6 |
| ExCoT | LLaMA 70B, SFT | Spider test | 83.00 | 81.42 |
| ExCoT | LLaMA 70B, SFT | BIRD dev | 62.03 | 58.14 |
| Struct-SQL | Qwen3 4B, LoRA | BIRD mini-dev | 34.30 | 36.90 tự do, 45.00 có cấu trúc |
| Ta, P2.58 | Coder 1.5B, LoRA | Spider dev, greedy, full schema | 72.53 | 62.48 |
| Ta, P2.62 sau RL | Coder 1.5B, LoRA | Spider dev, greedy | 74.18 | 70.89 |

Gain dương lớn nằm ở BIRD và thường dùng gold schema links hoặc sampling
nhiều lần. Trên Spider với greedy, kết quả lẫn lộn.

## 4. RL trong Text-to-SQL

| Bài | Cấu hình | Kết quả |
|---|---|---|
| SLM-SQL | GRPO, 6 rollouts, RL trên BIRD | Spider 1.5B (16 samples) dev 74.53 lên 75.15 |
| FINER-SQL | GRPO, 32 rollouts, reward phụ | BIRD 1.5B 59.4 lên 63.1 |
| Think2SQL | GRPO | 1.5B RL từ zero-shot 27.5 lên 44.2 (BIRD) |
| ExCoT | DPO, 1 round off-policy (GPT-4o) rồi 2 on-policy | Spider 70B: SFT 81.42, on-policy 86.59 |
| Xiong et al. 2025 | So thuật toán trên toán, 7B | Iterative DPO thấp nhất (48.8), GRPO 56.3 |
| Ta, P2.62 | DPO + NLL, K=8, retry câu toàn sai | 1.5B Spider dev 58.80 lên 74.18 |

Training gốc của SLM-SQL, FINER-SQL và ExCoT cần GPU lớn hơn A5000; DPO của ta
đã đo vừa 24 GB (P2.58: peak 14.43 GiB với CoT).

## 5. Teacher có đóng góp riêng không

- ExCoT: một round GPT-4o rồi hai round tự sinh hơn ba round tự sinh rõ ở BIRD
  (68.51 so với 67.08), rất ít ở Spider (86.59 so với 86.21).
- Li et al. 2025 ([Small Models Struggle to Learn from Strong Reasoners](https://arxiv.org/html/2502.12143v3)):
  với student 1.5B, teacher lớn không hơn teacher nhỏ.
- SERT (Zhang et al. 2025): reasoning tự sinh cộng reasoning của teacher cao
  nhất; riêng teacher có thể thua fine-tune.
- Dự án: soft label của teacher hơn gold, không do smoothing hay anchoring,
  nhưng nhỏ trên Spider test (RESEARCH_STATE K2, K3).

## 6. Nguồn khác đã dùng

[STaR](https://arxiv.org/abs/2203.14465), [Iterative RPO](https://arxiv.org/html/2404.19733v3),
[Schema-R1](https://arxiv.org/html/2506.11986), [VCoT-SQL](https://aclanthology.org/2026.emnlp-main.2686.pdf),
[KID](https://aclanthology.org/2024.findings-emnlp.403/), [FedNTD](https://arxiv.org/abs/2106.03097),
FedProx (Li et al., MLSys 2020), TAID (Shing et al., ICLR 2025), virtual teacher
(Yuan et al., CVPR 2020), FFA-LoRA (Sun et al., ICLR 2024), Hinton et al. 2015.
