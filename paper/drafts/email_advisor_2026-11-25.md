# Email: đổi method, xin ý kiến Thầy

**Tiêu đề:** Xin ý kiến Thầy về method mới và tên bài

Chào Thầy,

Em xin báo cáo việc đổi method và xin Thầy vài ý kiến.

**Method mới.** Em bỏ bước KD từ LLM teacher. Method còn lại: 2 round
FedAvg SFT, sau đó là các round DPO. Mỗi round, client sample SQL từ model
global, chạy trên database của mình để gán nhãn đúng hay sai, rồi train
DPO + NLL trên các cặp đúng và sai đó.

**Lý do bỏ KD.** Gain nhỏ so với compute phải chạy. Ở setup cũ em đo
riêng từng bước trên Spider test (gộp 2 seed):

| Bước | Gain EX | Compute trên một card A5000 |
| --- | ---: | --- |
| Cả bước public (KD trên BIRD) | +1.40 | chạy teacher 7B trên 9,428 câu: khoảng 14 giờ (ước tính từ 5.5 giây mỗi câu); KD: 3.3 đến 3.6 giờ mỗi epoch |
| Riêng teacher, so với train gold SQL trên cùng data | +0.98 (p = 0.04) | như trên; train gold SQL không cần teacher: 2.7 giờ mỗi epoch |
| DPO ở client | **+3.19 đến +3.91** | khoảng 3 giờ mỗi round |

Em để KD làm hướng mở rộng sau.

**Kết quả.** Em so method với hai baseline, trên hai dataset và qua các
student model: FedAvg SFT là baseline federated ở cùng số round, centralized
SFT là mức tham chiếu khi gộp data của mọi client. EX, 5 client non-IID, 4
round.

BIRD dev (dataset chính):

| Model | Chưa train | Centralized SFT | FedAvg SFT | Method | Gain so với FedAvg SFT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-Coder-1.5B | 29.47 | chờ chạy | 42.57 | **48.76** | +6.19 |

Spider test:

| Model | Chưa train | Centralized SFT | FedAvg SFT | Method | Gain so với FedAvg SFT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-Coder-1.5B | 68.05 | 75.73 | 74.71 | **78.20** | +3.49 |
| Qwen2.5-Coder-0.5B | 54.40 | chưa chạy | 64.09 | **66.19** | +2.10 |
| DeepSeek-Coder-1.3B | 55.85 | chưa chạy | 69.82 (2 round) | **75.08** (3 round) | chờ FedAvg SFT round 3 |

- Method hơn FedAvg SFT trên cả hai dataset và trên hai model đã chạy đủ
  4 round; với model 1.5B trên Spider test, method hơn cả centralized SFT.
- Trên BIRD, round tốt nhất của FedAvg SFT là 43.68. Method hơn ở cả ba
  mức độ khó, rõ nhất ở moderate (39.66 so với 29.96), và số SQL lỗi khi
  chạy giảm từ 268 xuống 128.
- Hai model còn lại chưa chạy trên BIRD.

**Baseline.** FedAvg SFT, FedDPO của OpenFedLLM (cặp và reference cố
định), centralized SFT; em cân nhắc thêm FedProx và local SFT.

**Ablation.** Bỏ lần lượt: sample lại mỗi round, NLL term, thành phần
preference, 2 round SFT đầu.

**Khoảng trống.** Federated Text-to-SQL mới có một bài (Zhang et al., ACL
2023: T5-base, chỉ SFT). CodeLutra (TMLR 2025) có vòng sample, execution
và DPO tương tự nhưng train tập trung; em tìm thấy bài này sau khi thiết
kế. Phần mới của em: nhãn execution do từng client tạo trên database
riêng, sample lại theo từng round FL, với model 1.5B.

Em xin Thầy ba việc:

1. Đặt giúp em tên bài (tên tạm: FedLS-SQL).
2. Xem baseline và ablation như trên đã đủ chưa ạ.
3. Khoảng trống như trên có đủ cho một bài không ạ.

Em cảm ơn Thầy.
