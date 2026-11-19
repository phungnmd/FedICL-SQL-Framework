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

**3. Các bài gần nhất**

- CodeLutra (Tao et al., TMLR 2025, arXiv 2411.05199): gần nhất về cơ chế.
  Mỗi vòng sample 10 SQL cho mỗi câu hỏi, gán nhãn bằng execution, train
  DPO + SFT. Train tập trung với Llama-3-8B: Spider EX 59.3 lên 76.6 (SFT
  trên gold: 67.9), BIRD 22.3 lên 43.1 (SFT: 35.6).
- OpenFedLLM (Ye et al., 2024, arXiv 2402.06954): có FedDPO, tức DPO trong
  FedAvg với Llama2-7B. Cặp preference có sẵn và tạo một lần, reference cố
  định qua các round, không phải SQL.
- Zhang et al. (ACL 2023, arXiv 2305.17221): bài federated Text-to-SQL duy
  nhất em tìm thấy. T5-base, 8 client, chỉ SFT với FedAvg, FedProx, FedOPT,
  đo exact match; không có DPO và không dùng execution.

Em xin nói rõ một điểm: lúc thiết kế phần DPO này em chưa tìm bài kỹ nên
chưa biết CodeLutra, em tự đi đến cách sample, chạy SQL rồi train DPO + NLL.
Sau khi tìm thấy bài này, em thấy cơ chế đó đã có người làm ở dạng train tập
trung, nên đóng góp của bài em hẹp hơn em nghĩ lúc đầu: phần mới là đưa cơ
chế này vào federated (nhãn execution do từng client tạo trên database
riêng, mỗi round FL là một lần sample lại) với model 1.5B. Em sẽ trích
CodeLutra là bài gần nhất và nói rõ phần khác.

Em chưa thấy bài nào làm DPO với nhãn execution tại client cho federated
Text-to-SQL.

Em đang chạy tiếp trên BIRD để xem gain có giữ được trên bộ khó hơn không.

Em xin ý kiến Thầy hai điểm:

1. Có nên bỏ bước LLM public để bài gọn hơn không ạ, hay giữ lại như
   ablation?
2. Nếu bỏ, và khi đã có CodeLutra, phần federated DPO như trên có đủ đóng
   góp cho bài không ạ?

Em cảm ơn Thầy.
