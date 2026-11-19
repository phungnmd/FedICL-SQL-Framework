# Email: xin ý kiến về bước LLM public

**Tiêu đề:** Xin ý kiến Thầy về việc bỏ bước LLM public, tập trung vào federated DPO cho Text-to-SQL

Chào Thầy,

Em xin báo cáo kết quả gần đây và xin ý kiến Thầy về hướng của bài.

Theo hướng Thầy gợi ý, pipeline gồm ba bước: LLM teacher dạy student trên
public data ở server, FedAvg trên private data, rồi DPO ở client. Sau khi đo
riêng từng bước, em thấy phần teacher đóng góp ít, còn phần DPO ở client cho
gain rõ. Em trình bày số liệu bên dưới, mong Thầy xem giúp em có nên bỏ bước
LLM public để bài gọn hơn không ạ.

Setup: student Qwen2.5-Coder-1.5B, teacher Qwen2.5-Coder-7B, 5 client Spider
non-IID, public data là BIRD train, số đo là EX trên Spider test (2.147 câu).

## 1. Đóng góp của từng bước trong pipeline ba bước

Gain EX của từng phần, gộp 2 seed:

| Phần | Gain EX |
| --- | ---: |
| DPO ở client, không có bước public | **+3.91** |
| DPO ở client, sau bước public | +3.19 |
| Bước public (teacher KD trên BIRD), đo sau DPO | +1.40 |
| Riêng teacher so với train gold SQL trên cùng BIRD, đo sau DPO | +0.98 (p = 0.04) |

- Gain chủ yếu đến từ DPO ở client, có hay không có bước public đều khoảng 3
  đến 4 điểm.
- Teacher chỉ hơn việc train thẳng gold SQL của BIRD khoảng 1 điểm, nên em
  thấy khó trình bày teacher như một đóng góp chính của bài.

Bảng này em đo trên setup cũ, trước khi em sửa prompt và chạy lại toàn bộ từ
ngày 17/11, nên mức EX không so trực tiếp được với bảng ở mục 2.

## 2. Kết quả khi chỉ có federated DPO

Mỗi round, client sample SQL từ model global, chạy trên database của mình để
biết câu nào đúng, câu nào sai, ghép cặp đúng và sai rồi train DPO + NLL;
server FedAvg như thường. Không thêm data, không gửi gì ngoài LoRA adapter.

Kết quả trên setup mới (seed 0, student chưa train: 68.05):

| Số round | FedAvg SFT | Federated DPO |
| ---: | ---: | ---: |
| 1 | 72.43 | **75.87** |
| 2 | 74.10 | **77.18** |
| 3 | 74.71 | **77.69** |
| 4 | 74.71 | **78.02** |

- Federated DPO hơn FedAvg SFT 3.1 đến 3.4 điểm ở mọi round (round 4:
  p = 3e-05), trong khi FedAvg SFT dừng tăng sau round 3.
- Cả hai phần của loss đều cần: bỏ NLL còn 73.59, chỉ NLL trên sample đúng
  được 75.87, đủ cả hai được 77.46 (cùng điểm xuất phát, 1 round).
- Về bài liên quan, em chỉ tìm thấy một bài federated Text-to-SQL (Zhang et
  al., ACL 2023, T5-base, FedAvg và các biến thể). FedDPO trong OpenFedLLM
  dùng cặp preference có sẵn, không phải SQL. CodeLutra (arXiv 2411.05199)
  làm vòng sample, chạy SQL, DPO nhưng train tập trung với model 8B. Em chưa
  thấy bài nào làm DPO với nhãn execution tại client cho federated
  Text-to-SQL.

## 3. Hướng em đang nghĩ

Em nghĩ bài có thể gọn lại còn một ý: client có database để chạy SQL; FedAvg
SFT chỉ dùng label, còn method dùng cả hai. Bước LLM public khi đó không nằm
trong method.

Hiện em đang chạy FedAvg SFT và federated DPO trên BIRD (student chưa train:
29.47 trên BIRD dev) để xem gain có giữ được trên bộ khó hơn không. Sau đó em
dự định chạy các baseline FedProx, FedNTD, FedDPO như OpenFedLLM, centralized
SFT, seed thứ hai và các mức non-IID khác.

## 4. Em xin ý kiến Thầy

1. Thầy thấy có nên bỏ bước LLM public khỏi method không ạ, hay nên giữ lại
   như một phần phụ hoặc ablation?
2. Nếu bỏ, phần federated DPO như trên đã đủ đóng góp cho bài chưa, hay cần
   thêm phần nào ạ?
3. Về thí nghiệm, Thầy thấy em cần bổ sung baseline hay dataset nào không ạ?

Em cảm ơn Thầy.
