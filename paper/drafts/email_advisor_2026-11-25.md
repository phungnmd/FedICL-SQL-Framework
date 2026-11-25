# Email: đổi method, xin ý kiến Thầy

**Tiêu đề:** Xin ý kiến Thầy về method mới và tên bài

Chào Thầy,

Em xin báo cáo việc đổi method và xin Thầy vài ý kiến.

**Method mới.** Em bỏ bước knowledge distillation (KD) từ LLM teacher.
Method còn lại: 2 round FedAvg SFT (warm-up), sau đó là các round DPO. Mỗi
round, client sample SQL từ global model, execute trên database của mình
để lấy execution label (đúng hay sai so với gold SQL), rồi train DPO + NLL
trên các preference pair (SQL đúng, SQL sai).

**Lý do bỏ KD.** Gain nhỏ so với compute. Ở setup cũ em đo riêng từng
stage trên Spider test (pooled 2 seed):

| Stage | Gain EX | Compute trên một card A5000 |
| --- | ---: | --- |
| Public-data stage (KD trên BIRD) | +1.40 | teacher inference (7B) trên 9,428 câu: khoảng 14 giờ (ước tính từ 5.5 giây mỗi câu); KD: 3.3 đến 3.6 giờ mỗi epoch |
| Riêng teacher, so với SFT trên gold SQL của cùng data | +0.98 (p = 0.04) | như trên; SFT trên gold SQL không cần teacher: 2.7 giờ mỗi epoch |
| DPO ở client | **+3.19 đến +3.91** | khoảng 3 giờ mỗi round |

Em để KD làm future work.

**Kết quả.** Em so method với hai baseline, trên hai dataset và qua các
student model: FedAvg SFT là federated baseline ở cùng số round,
centralized SFT là reference không federated (train trên data của mọi
client). Metric: execution accuracy (EX); 5 client non-IID; 4 round.

BIRD dev (dataset chính):

| Model | Zero-shot | Centralized SFT | FedAvg SFT | Method | Gain so với FedAvg SFT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-Coder-1.5B | 29.47 | chờ chạy | 42.57 | **48.76** | +6.19 |

Spider test:

| Model | Zero-shot | Centralized SFT | FedAvg SFT | Method | Gain so với FedAvg SFT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-Coder-1.5B | 68.05 | 75.73 | 74.71 | **78.20** | +3.49 |
| Qwen2.5-Coder-0.5B | 54.40 | chưa chạy | 64.09 | **66.19** | +2.10 |
| DeepSeek-Coder-1.3B | 55.85 | chưa chạy | 69.82 (round 2) | **75.08** (round 3) | +5.26 |

- Method hơn FedAvg SFT trên cả hai dataset và cả ba model; với model
  1.5B trên Spider test, method hơn cả centralized SFT.
- DeepSeek chưa có FedAvg SFT round 3, nên gain tính so với round 2, là
  checkpoint khởi đầu của round DPO.
- Trên BIRD, round tốt nhất của FedAvg SFT là 43.68. Method hơn ở cả ba
  difficulty level, rõ nhất ở moderate (39.66 so với 29.96), và số
  execution error giảm từ 268 xuống 128.

**Kế hoạch thực nghiệm của bài.** Setup chung: 5 client non-IID
(Dirichlet alpha 0.1), student fine-tune bằng LoRA, EX trên BIRD dev và
Spider test, một seed, McNemar test. BIRD là dataset chính, Spider cho
phần mở rộng.

Baseline:

- Zero-shot (xong)
- Local SFT: mỗi client fine-tune riêng (Spider, dự kiến)
- Centralized SFT (Spider xong, BIRD chờ chạy)
- FedAvg SFT (xong)
- FedProx SFT (Spider, dự kiến)
- FedDPO của OpenFedLLM: fixed pairs, fixed reference model, không NLL
  (chờ chạy)

Ablation:

- Không on-policy sampling: dùng lại pair và reference của round DPO đầu
  (xong)
- Không NLL term: DPO loss thuần (Spider xong, BIRD chờ chạy)
- Không preference term: chỉ NLL trên sample đúng (round đầu xong, 4 round
  chờ chạy)
- Số round SFT warm-up: k = 0, 2, 3 trên Spider, k = 0, 1, 2 trên BIRD
  (xong)
- Aggregation weight: theo số pair, theo số câu hỏi, uniform (xong)

Thực nghiệm mở rộng, trên Spider:

- Student model khác: Qwen2.5-Coder-0.5B (xong), DeepSeek-Coder-1.3B (chờ
  round 3 và 4)
- Data heterogeneity: Dirichlet alpha 0.1 (xong), IID (chờ chạy)
- Pooled DPO: các round DPO trên data gộp, không aggregation, so với
  federated (chờ chạy)
- FedAvg SFT thêm round (xong)
- Robustness: Spider-Syn, Spider-Realistic, Spider-DK (1.5B xong)
- Test-suite accuracy (xong)

Phân tích:

- Error analysis theo round: execution error, wrong result (xong)
- EX theo difficulty level (xong)
- Client update: số pair và cosine similarity theo round (xong)
- Cost: client compute time mỗi round, communication cost theo kích thước
  adapter (dự kiến)

**Research gap.** Federated Text-to-SQL mới có một bài (Zhang et al., ACL
2023: T5-base, chỉ SFT). CodeLutra (TMLR 2025) có vòng sample, execution
và DPO tương tự nhưng là centralized training; em tìm thấy bài này sau khi
thiết kế. Phần mới của em: execution label do từng client tạo trên
database riêng, on-policy sampling theo từng round FL, với model 1.5B.

Em xin Thầy ba việc:

1. Đặt giúp em tên bài (tên tạm: FedLS-SQL).
2. Xem kế hoạch baseline, ablation và thực nghiệm như trên đã đủ chưa ạ.
3. Research gap như trên có đủ cho một bài không ạ.

Em cảm ơn Thầy.
