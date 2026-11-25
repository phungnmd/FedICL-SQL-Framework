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

**Kết quả** (EX, 5 client non-IID, 4 round, Qwen2.5-Coder-1.5B nếu không
ghi khác)

| | Chưa train | FedAvg SFT | Method | Gain |
| --- | ---: | ---: | ---: | ---: |
| BIRD dev | 29.47 | 42.57 | **48.76** | +6.19 |
| Spider test | 68.05 | 74.71 | **78.20** | +3.49 |
| Spider-Syn / Realistic / DK | 56.77 / 65.16 / 60.19 | 59.09 / 67.72 / 59.63 | **62.96 / 70.47 / 63.55** | +3.87 / +2.75 / +3.92 |
| Spider test, model 0.5B | 54.40 | 64.09 | **66.19** | +2.10 |

- Trên BIRD, method hơn ở cả ba mức độ khó, rõ nhất ở moderate (39.66 so
  với 29.96); số SQL lỗi khi chạy giảm từ 268 xuống 128.
- Trên Spider test, method hơn cả centralized SFT (75.73).
- Round tốt nhất của FedAvg SFT trên BIRD là 43.68.

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
