# Email: xin ý kiến về bước LLM public

**Tiêu đề:** Xin ý kiến Thầy về việc bỏ bước LLM public

Chào Thầy,

Em xin báo cáo kết quả và xin ý kiến Thầy về hướng của bài. Với pipeline ba
bước Thầy gợi ý (LLM teacher trên public data, FedAvg trên private data, DPO
ở client), em đo riêng từng bước thì thấy teacher đóng góp ít, còn DPO ở
client cho gain rõ.

Setup: student Qwen2.5-Coder-1.5B, teacher Qwen2.5-Coder-7B, 5 client Spider
non-IID, public data là BIRD train, số đo là EX trên Spider test.

**1. Gain của từng bước, đo ở cuối pipeline** (setup cũ, trước khi em sửa
prompt ngày 17/11; gộp 2 seed)

| Phần | Gain EX |
| --- | ---: |
| DPO ở client (có / không có bước public) | **+3.19 / +3.91** |
| Bước public (teacher KD trên BIRD) | +1.40 |
| Riêng teacher so với train gold SQL trên cùng BIRD | +0.98 |

**2. Chỉ federated DPO, không có bước public** (setup mới, seed 0)

Mỗi round, client sample SQL từ model global, chạy trên database của mình để
gán nhãn đúng hay sai, rồi train DPO + NLL trên các cặp đúng và sai đó.

| Số round | FedAvg SFT | Federated DPO |
| ---: | ---: | ---: |
| 1 | 72.43 | **75.87** |
| 2 | 74.10 | **77.18** |
| 3 | 74.71 | **77.69** |
| 4 | 74.71 | **78.02** |

- Federated DPO hơn FedAvg SFT 3.0 đến 3.4 điểm ở mọi round (round 4:
  p = 3e-05).
- Em chưa thấy bài nào làm DPO với nhãn execution tại client cho federated
  Text-to-SQL. Gần nhất là CodeLutra (train tập trung, model 8B) và FedDPO
  của OpenFedLLM (cặp preference có sẵn, không phải SQL).

Em đang chạy tiếp trên BIRD để xem gain có giữ được trên bộ khó hơn không.

Em xin ý kiến Thầy hai điểm:

1. Có nên bỏ bước LLM public để bài gọn hơn không ạ, hay giữ lại như
   ablation?
2. Nếu bỏ, phần federated DPO như trên đã đủ đóng góp cho bài chưa ạ?

Em cảm ơn Thầy.
