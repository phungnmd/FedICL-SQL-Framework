# Email: đổi method, xin ý kiến Thầy

**Tiêu đề:** Xin ý kiến Thầy về method mới và tên bài

Chào Thầy,

Em xin báo cáo việc đổi method và xin Thầy vài ý kiến.

**Method mới.** Em bỏ bước KD từ LLM teacher. Method còn lại: 2 round
FedAvg SFT, sau đó là các round DPO. Mỗi round, client sample SQL từ model
global, chạy trên database của mình để gán nhãn đúng hay sai, rồi train
DPO + NLL trên các cặp đúng và sai đó.

**Lý do bỏ KD.** Khi đo riêng từng bước (setup cũ), teacher chỉ thêm
khoảng 1 điểm EX so với train gold SQL trên cùng public data, còn DPO ở
client thêm 3 đến 4 điểm. Em để KD làm hướng mở rộng sau.

**Kết quả** (EX, Qwen2.5-Coder-1.5B, 5 client non-IID, 4 round)

| | FedAvg SFT | Method | Gain |
| --- | ---: | ---: | ---: |
| BIRD dev | 42.57 | **48.76** | +6.19 |
| Spider test | 74.71 | **78.20** | +3.49 |

Round tốt nhất của FedAvg SFT trên BIRD là 43.68.

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
