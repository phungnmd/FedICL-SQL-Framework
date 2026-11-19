# Email: đề xuất bỏ bước LLM public

**Tiêu đề:** Đề xuất bỏ bước LLM public, tập trung vào federated DPO cho Text-to-SQL

Chào Thầy,

Em xin cập nhật và đề xuất một thay đổi cho bài. Hướng Thầy gợi ý gồm ba
bước: LLM teacher dạy student trên public data ở server, FedAvg trên private
data, rồi DPO ở client. Em đề xuất bỏ bước LLM public và chỉ giữ phần
federated DPO.

Setup: student Qwen2.5-Coder-1.5B, teacher Qwen2.5-Coder-7B, 5 client Spider
non-IID, public data là BIRD train, số đo là EX trên Spider test (2.147 câu).

## 1. Đóng góp của teacher nhỏ

Gain EX của từng phần, gộp 2 seed:

| Phần | Gain EX |
| --- | ---: |
| DPO ở client, không có bước public | **+3.91** |
| DPO ở client, sau bước public | +3.19 |
| Bước public (teacher KD trên BIRD), đo sau DPO | +1.40 |
| Riêng teacher so với train gold SQL trên cùng BIRD, đo sau DPO | +0.98 (p = 0.04) |

- Phần lớn gain của cả pipeline đến từ DPO ở client, có hay không có bước
  public đều khoảng 3 đến 4 điểm.
- Teacher chỉ hơn việc train thẳng gold SQL của BIRD khoảng 1 điểm. Phần này
  khó thành đóng góp chính của bài.

Bảng này đo trên setup cũ, trước khi em sửa prompt và chạy lại toàn bộ từ
ngày 17/11, nên mức EX không so trực tiếp được với bảng ở mục 2.

## 2. Federated DPO đủ làm bài riêng

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
  p = 3e-05), và FedAvg SFT đã dừng tăng sau round 3.
- Cả hai phần của loss đều cần: bỏ NLL còn 73.59, chỉ NLL trên sample đúng
  được 75.87, đủ cả hai được 77.46 (cùng điểm xuất phát, 1 round).
- Khoảng trống: em chỉ tìm thấy một bài federated Text-to-SQL (Zhang et al.,
  ACL 2023, T5-base, FedAvg và các biến thể). FedDPO trong OpenFedLLM dùng cặp
  preference có sẵn, không phải SQL. CodeLutra (arXiv 2411.05199) làm vòng
  sample, chạy SQL, DPO nhưng train tập trung với model 8B. Em chưa thấy bài
  nào làm DPO với nhãn execution tại client cho federated Text-to-SQL.

## 3. Đề xuất

- Bỏ bước LLM public khỏi method. Bài còn một ý: client có database để chạy
  SQL, FedAvg SFT chỉ dùng label, method dùng cả hai.
- BIRD chuyển từ public data thành bộ client thứ hai.

## 4. Đang làm

- Chạy FedAvg SFT và federated DPO trên BIRD (student chưa train: 29.47 trên
  BIRD dev) để xem gain còn giữ trên bộ khó hơn.
- Sau đó: baseline FedProx, FedNTD, FedDPO như OpenFedLLM; centralized SFT;
  seed thứ hai; các mức non-IID khác.

Em xin ý kiến Thầy về việc bỏ bước LLM public, và nếu bỏ thì phần federated
DPO như trên có đủ cho bài không ạ.

Em cảm ơn Thầy.
