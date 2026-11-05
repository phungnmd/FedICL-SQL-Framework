# FedLS-SQL: literature và giới hạn claim

Cập nhật: 2026-11-05 (thêm closest work của hướng D, từ web search, mới đọc abstract). Gộp từ ba file đã archive (bản đầy đủ, kèm các lớp
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
| RL cho câu toàn sai, có teacher | [AAPO](https://aclanthology.org/2026.findings-acl.169/) (hint của teacher khi mọi rollout sai), [ADHint](https://arxiv.org/pdf/2512.13095) (prefix của teacher theo độ khó), [LUFFY](https://arxiv.org/abs/2504.14945) (trộn trace off-policy) | Teacher thấy chính câu đang train; ta không được (teacher chỉ ở server, public) |
| Text-to-SQL RL có teacher | [ReToolSQL](https://arxiv.org/html/2608.27796v1) (teacher có gold viết reasoning cho câu toàn sai), [SERL-SQL](https://arxiv.org/abs/2608.00485) (teacher chấm lại action của student) | Centralized, teacher thấy câu train |
| Federated RLVR | [PubSwap](https://arxiv.org/pdf/2604.12160) (ICML 2026), Fed-GRPO (arXiv 2610.11502), FedGRPO (arXiv 2602.12014) | Không teacher, không Text-to-SQL |
| CoT rollout chuyển sang policy không CoT | Masked Distillation (2026, chưa đọc), Yu et al. 2024 Distilling System 2 into System 1 (SFT, self-consistency) | Cần đọc kỹ: gần nhất với hướng D |
| DPO Text-to-SQL và CoT | Liu et al., [Uncovering the Impact of CoT for DPO: Lessons from Text-to-SQL](https://aclanthology.org/2025.acl-long.1031) (ACL 2025): DPO không CoT thường không giúp trên BIRD (6.7B-15B), CoT tổng hợp giúp; [AutoThinkSQL](https://arxiv.org/pdf/2607.22622): học khi nào cần reasoning | Centralized; ta thấy SQL-only DPO + NLL hiệu quả ở 1.5B Spider (`g3d` - `g3n` +2.22) |
| FL + KD từ server, task chung | [KnowledgeSG](https://arxiv.org/pdf/2410.05725) (EMNLP 2024), [Communication-aware KD](https://arxiv.org/html/2509.01750v2), [POPri](https://openreview.net/forum?id=ZuaU2bYzlc) (DPO cho synthetic data riêng tư) | Không Text-to-SQL, không execution |
| DPO cho code theo execution | [Aligning CodeLLMs with DPO](https://www.arxiv.org/pdf/2410.18585) (unit test xếp hạng output) | Centralized, code |
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

### 3.1. RL có CoT so với RL chỉ SQL (kiểm 2026-11-05 trên full text)

| Bài | Model, RL | Điều kiện | RL chỉ SQL | RL có CoT |
|---|---|---|---:|---:|
| ExCoT, Table 1 | LLaMA-3.1 70B, on-policy iterative DPO sau SFT trên data GPT-4o | BIRD dev / Spider test | 59.97 / 81.00 | 68.51 / 86.59 |
| Liu et al. 2025, Table 1 | Qwen2.5-Coder-7B, DPO chuẩn (không NLL), CoT GPT-4o-mini thấy gold | BIRD dev, greedy | 61.3 | 63.4 |
| Liu et al. 2025, Table 14 | DeepSeek-Coder-6.7B / Qwen2.5-7B / CodeS-7B | Spider dev, greedy | 81.0 / 79.7 / 79.4 | 82.1 / 80.5 / 80.0 |
| Reasoning-SQL, Table 1 | Qwen2.5-Coder-7B, GRPO, reward tổng hợp (execution, schema, n-gram, LLM judge) | BIRD dev | 62.25 | 64.01 |
| Reward-SQL, Table 6 | Qwen3-8B; quy trình train của hai dòng đầu không nêu | BIRD dev, greedy | 63.6 | 64.2 NL-CoT, 66.0 Chain-of-CTEs |
| AutoThinkSQL, Table 1 | Qwen3-Coder-30B-A3B (3B active), LoRA r16, SFT + DPO trên rollout tự sinh, train BIRD | Spider dev / BIRD dev, greedy | 84.23 / 57.64 | 69.14 / 54.02 |
| AutoThinkSQL, Table 1 | như trên | Spider dev / BIRD dev, Maj@8 | 84.46 / 58.01 | 83.33 / 59.55 |
| Ta, P2.62 | Coder-1.5B, DPO + NLL, tự sinh, xuất phát khác dữ liệu | Spider dev, greedy | 74.18 | 70.89 |

Liu et al. phụ lục A, Table 7 (BIRD dev, Qwen2.5-7B, SFT 58.8): DPO chỉ SQL có
thêm SFT loss trên câu đúng (tức DPO + NLL) đạt 60.0 (+1.2); KTO 59.8; dữ liệu
pair kiểu SENSE 58.4. Arm CoT của họ là DPO không NLL, đạt 61.9. CoT của họ
có thêm phần giải thích sau SQL. Vậy với NLL, SQL-only DPO có gain nhỏ, cùng
cỡ `g3d` - `g2` +1.93 của ta; CoT vẫn hơn khoảng 2 điểm trên BIRD ở 7B.

VCoT-SQL (EMNLP 2026, Table 3) là bài có writer CoT 7B cho gain: student
Coder-7B, gold SFT 60.04 BIRD dev / 83.1 Spider test, CoT theo clause đã lọc
64.86 / 86.7. Student cùng cỡ writer, có schema filtering. Chi tiết (đọc
PDF và data công khai 2026-11-05): writer Qwen2.5-Coder-7B thấy gold SQL, 3
ví dụ few-shot, kiểm gold trước; CoT theo clause, thứ tự SELECT, WHERE,
GROUP/ORDER, FROM cuối, mỗi bước nối cụm từ trong câu hỏi với cột hoặc bảng;
lọc theo cấu trúc, độ dài, SQL của writer khớp gold khi execute, không nhắc
gold, và có nhắc đủ bảng/cột của gold. Giữ 5,477/8,659 câu Spider và
3,669/9,428 câu BIRD; full fine-tune 4 epoch, greedy. Bước lọc là phần lớn
gain (+2.23 đến +2.44 BIRD dev); thứ tự logic chỉ thêm +0.42 đến +0.63.
Baseline SQL dùng đủ 18K dòng, không có baseline SQL trên cùng tập đã lọc,
và không có RL. P2.59 `tc` của ta gần thiết kế này nhưng không kiểm SQL
của writer, thay SQL cuối bằng gold, và chạy trên SynSQL.

Think2SQL không có arm RL chỉ SQL. Liu et al. (phụ lục G) ghi rằng trên
Spider, pass@16 của tập train ≥ 99%, nên chỉ có 0.1k-0.3k pair (BIRD
1.5k-2.5k). Cũng trong bài đó (Table 9), writer yếu vẫn cho DPO gain lớn:
writer Qwen2.5-1.5B 40.9 lên 59.1, 7B 54.3 lên 60.6, GPT-4o-mini 57.4 lên 61.9
(BIRD dev, student Qwen2.5-7B).

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

### 5.1. Vai trò của teacher khi không dùng CoT (kiểm 2026-11-05)

| Vai trò | Bài, số liệu | Ghi chú |
|---|---|---|
| Tổng hợp dữ liệu mới (schema, câu hỏi, SQL, domain mới) | [SENSE](https://arxiv.org/abs/2408.03256) (ACL 2024): GPT-4 sinh 8,216 câu trên 503 DB; CodeLLaMA-13B Spider dev 79.4 (Spider + BIRD) lên 82.9 (thêm synthetic), BIRD 51.6 lên 52.9 (Figure 6) | Dòng "w/o Strong" trong Table 5 là base chưa SFT, không phải bỏ riêng synthetic |
| Tổng hợp dữ liệu | [SQuaD-SQL](https://arxiv.org/html/2607.08161v1): GPT-4o sinh 50K cặp WikiSQL, Qwen 1.5B LoRA từ 35.6 lên 86.9 | Chỉ WikiSQL, không có baseline dữ liệu người |
| Tổng hợp dữ liệu quy mô lớn | OmniSQL (SynSQL-2.5M, nhiều LLM 7B-72B) | Không tách riêng vai trò từng model |
| Pair âm cho DPO | SENSE: model yếu DeepSeek-Coder-1.3B sinh SQL sai; DPO thêm Spider dev +0.1 đến +0.9, BIRD +1.3 đến +2.6 | Liu et al. thử lại kiểu SENSE: 58.4 (-0.4) |
| Context distillation (teacher có prompt đặc quyền) | Zhu et al., NAACL Industry 2025: teacher thấy schema đã lọc, student thấy full; TS +1.9 Spider dev | Mới đọc abstract |
| Reward hoặc judge | Reasoning-SQL: Gemini làm LLM judge trong reward; Reward-SQL: PRM 7B | Ta: reward ở client là execution |
| Component lúc inference | Schema linker, Pre-SQL, validator (Reasoning-SQL, VCoT-SQL) | Không hợp setup (chỉ deploy SLM) |

Không thấy bài Text-to-SQL nào dùng KD ở mức logit (Hinton) như ta.

## 6. Nguồn khác đã dùng

[STaR](https://arxiv.org/abs/2203.14465), [Iterative RPO](https://arxiv.org/html/2404.19733v3),
[Schema-R1](https://arxiv.org/html/2506.11986), [VCoT-SQL](https://aclanthology.org/2026.emnlp-main.2686.pdf),
[KID](https://aclanthology.org/2024.findings-emnlp.403/), [FedNTD](https://arxiv.org/abs/2106.03097),
FedProx (Li et al., MLSys 2020), TAID (Shing et al., ICLR 2025), virtual teacher
(Yuan et al., CVPR 2020), FFA-LoRA (Sun et al., ICLR 2024), Hinton et al. 2015.
