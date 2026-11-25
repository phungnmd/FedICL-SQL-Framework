# Email: đổi method, xin ý kiến Thầy

**Tiêu đề:** Xin ý kiến Thầy về method mới và tên bài

Chào Thầy,

Em xin báo cáo việc đổi method và xin Thầy vài ý kiến.

**Method mới.** Em bỏ stage knowledge distillation (KD) từ LLM teacher.
Method gồm hai stage: SFT warm-up bằng FedAvg (2 communication round),
sau đó là các on-policy DPO round. Ở mỗi DPO round, client sample N = 10
SQL candidate cho mỗi question từ global model, execute trên private
database để lấy execution label (execution result khớp gold SQL hay
không), rồi local training bằng DPO + NLL loss trên các preference pair
(chosen: SQL đúng, rejected: SQL sai). Server aggregate các LoRA adapter
bằng FedAvg.

![Method overview](../figures/fig_method_overview.png)

Hình 1. Method overview: SFT warm-up, sau đó là các on-policy DPO round
tại client; chỉ LoRA adapter được truyền giữa server và client.

**Lý do bỏ KD.** Gain nhỏ so với compute cost. Ở setup cũ em đo từng
stage trên Spider test (pooled 2 seed):

| Stage | EX gain | Compute cost trên một RTX A5000 |
| --- | ---: | --- |
| Public-data KD stage (trên BIRD) | +1.40 | teacher inference (7B) trên 9,428 sample: khoảng 14 GPU-hour (ước tính từ 5.5 s/sample); KD training: 3.3 đến 3.6 GPU-hour/epoch |
| Teacher supervision so với gold-SQL SFT trên cùng data | +0.98 (p = 0.04) | như trên; gold-SQL SFT không cần teacher: 2.7 GPU-hour/epoch |
| Client-side DPO | **+3.19 đến +3.91** | khoảng 3 GPU-hour/round |

Em để KD làm future work.

**Kết quả.** Em so sánh method với hai baseline, trên hai benchmark và
ba backbone: FedAvg SFT là federated baseline ở cùng số communication
round; centralized SFT là non-federated reference (train trên pooled data
của mọi client). Metric: execution accuracy (EX). Setup: 5 client,
non-IID partition, 4 communication round.

BIRD dev (primary benchmark):

| Backbone | Zero-shot | Centralized SFT | FedAvg SFT | Method | Gain vs. FedAvg SFT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-Coder-1.5B | 29.47 | pending | 42.57 | **48.76** | +6.19 |

Spider test:

| Backbone | Zero-shot | Centralized SFT | FedAvg SFT | Method | Gain vs. FedAvg SFT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-Coder-1.5B | 68.05 | 75.73 | 74.71 | **78.20** | +3.49 |
| Qwen2.5-Coder-0.5B | 54.40 | n/a | 64.09 | **66.19** | +2.10 |
| DeepSeek-Coder-1.3B | 55.85 | n/a | 69.82 (round 2) | **75.08** (round 3) | +5.26 |

- Method outperform FedAvg SFT trên cả hai benchmark và cả ba backbone;
  với 1.5B trên Spider test, method vượt cả centralized SFT.
- DeepSeek chưa có FedAvg SFT round 3, nên gain tính so với round 2, là
  initial checkpoint của DPO round.
- Trên BIRD, best round của FedAvg SFT đạt 43.68 EX. Method cao hơn ở cả
  ba difficulty level, rõ nhất ở moderate (39.66 so với 29.96), và số
  execution error giảm từ 268 xuống 128.

**Experimental plan của bài.** Main setup: 5 client, non-IID partition
(Dirichlet α = 0.1), full participation, LoRA fine-tuning, EX trên BIRD
dev và Spider test, single seed, significance bằng McNemar test. BIRD là
primary benchmark: mọi baseline và ablation đều chạy trên BIRD. Spider
dùng cho các extended experiment.

Baseline, trên BIRD và Spider:

- Zero-shot
- Local SFT: không aggregation; report mean, min, max qua các client
- Centralized SFT
- FedAvg SFT
- FedProx SFT
- FedDPO của OpenFedLLM: fixed preference pairs, fixed reference model,
  không NLL term

Ablation study, trên BIRD và Spider:

- w/o on-policy sampling: giữ preference pair và reference model của DPO
  round đầu
- w/o NLL term: DPO loss only
- w/o preference term: chỉ NLL loss trên correct sample
- Số SFT warm-up round k, cùng total budget 4 round: k = 0, 2, 3
- Aggregation weight: theo số preference pair, theo số question, uniform

Extended experiment:

- Backbone khác, trên Spider: Qwen2.5-Coder-0.5B, DeepSeek-Coder-1.3B
- Backbone thứ hai trên BIRD: DeepSeek-Coder-1.3B
- Federated setup, trên Spider, mỗi setup gồm FedAvg SFT và method. Data
  heterogeneity với K = 5: Dirichlet α = 0.1, α = 0.5, IID. Số client:
  K = 10 với α = 0.5
- Thêm một DPO round trên BIRD, total 5 round
- Pooled DPO, trên Spider: DPO round trên pooled data, không aggregation,
  so với federated
- FedAvg SFT với nhiều communication round hơn, trên Spider
- Robustness: Spider-Syn, Spider-Realistic, Spider-DK
- Test-suite accuracy, trên Spider

Analysis:

- Error analysis theo round: execution error, wrong-result error
- EX theo difficulty level
- Client update: số preference pair và cosine similarity giữa các client
  update theo round
- Cost analysis: client compute time mỗi round, communication cost theo
  adapter size
- Multiple-comparison correction (Holm) cho các McNemar test

**Research gap.** Prior work về federated Text-to-SQL mới có một bài
(Zhang et al., ACL 2023: T5-base, SFT only). CodeLutra (TMLR 2025) có
loop sampling, execution feedback và DPO tương tự nhưng ở centralized
setting; em tìm thấy bài này sau khi thiết kế. Contribution của em:
execution label được tạo tại từng client trên private database,
on-policy sampling theo từng communication round, với small language
model 1.5B.

Em xin Thầy ba việc:

1. Đặt giúp em tên bài (working title: FedLS-SQL).
2. Review giúp em experimental plan (baseline, ablation, extended
   experiment) như trên đã đủ chưa ạ.
3. Research gap và contribution như trên có đủ cho một bài không ạ.

Em cảm ơn Thầy.
