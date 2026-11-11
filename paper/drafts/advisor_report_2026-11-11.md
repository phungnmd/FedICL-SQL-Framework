# FedLS-SQL: báo cáo tiến độ 11/11/2026

Thưa thầy,

Em gửi thầy kết quả mới và ba điểm em muốn xin ý kiến thầy.

**Method** gồm 3 bước:

1. Server distill teacher 7B sang student 1.5B trên BIRD (data public).
2. FedAvg 3 round trên data Spider của các client.
3. Federated DPO 3 round: mỗi client sample 8 câu SQL cho mỗi câu hỏi, chạy
   trên database của mình để ghép cặp đúng / sai, train DPO, rồi server gộp
   bằng FedAvg. Client không gửi data ra ngoài.

**Kết quả** (EX):

| Cấu hình | Spider test | Spider dev | Realistic | SYN | DK |
| --- | ---: | ---: | ---: | ---: | ---: |
| Base 1.5B | 57.89 | - | - | - | - |
| FedProx | 70.42 | - | - | - | - |
| FedAvg | 71.26 | 67.89 | 58.86 | 53.77 | 52.15 |
| Centralized Spider + BIRD | 73.96 | - | - | - | - |
| Bước 1 + 2 (chưa DPO) | 73.31 | 72.82 | 62.01 | 56.67 | 58.13 |
| Bước 2 + 3 (bỏ bước 1) | 75.13 | 73.11 | 63.58 | 58.32 | 58.88 |
| Bước 1 dùng gold SQL thay teacher + 2 + 3 | 75.22 | 73.79 | **65.35** | 59.86 | 57.94 |
| **Cả 3 bước** | **76.71** | **76.50** | 64.17 | **61.03** | **64.11** |

- DPO là phần tạo ra mức tăng chính: 3.4 điểm trên Spider test khi có bước 1
  và 3.9 điểm khi không có. Không có bước 1, DPO vẫn tăng 4.6-6.7 điểm trên
  bốn set còn lại. Control (chỉ train trên câu đúng, hoặc SFT thêm round)
  không tạo ra mức tăng này. 3 round là đủ.
- Cả 3 bước hơn FedAvg 5.45 điểm trên Spider test, hơn bản centralized 2.75
  điểm, và gần bằng teacher 7B zero-shot (77.22).
- Còn khoảng 20% câu Spider test là SQL chạy được nhưng sai kết quả; DPO chủ
  yếu sửa các câu SQL không chạy được, chưa sửa được nhóm này. CoT ở 1.5B
  kém SQL-only ở mọi bước nên em chỉ giữ làm một phân tích ngắn.

**So với các paper liên quan:**

| Mảng | Paper gần nhất | Đã có | Chưa có |
| --- | --- | --- | --- |
| Federated Text-to-SQL | [FL4SP](https://arxiv.org/abs/2305.17221) | T5-base, exact match | SLM decoder, EX |
| Federated DPO | [OpenFedLLM](https://arxiv.org/abs/2402.06954), [FedBiscuit](https://arxiv.org/abs/2407.03038) | DPO ở client rồi gộp LoRA, nhãn preference của người | nhãn từ execution |
| Federated RL có verifier | [PubSwap](https://arxiv.org/abs/2604.12160), [Fed-GRPO](https://arxiv.org/abs/2610.11502), [FedMOA](https://arxiv.org/abs/2602.00453) | GRPO ở 1.5-4B, trên toán và code | Text-to-SQL |
| DPO cho Text-to-SQL | [CoT for DPO](https://aclanthology.org/2025.acl-long.1031/), [ExCoT](https://arxiv.org/abs/2503.19988), [SQLoom](https://arxiv.org/abs/2611.03298) | centralized; 7B-70B, phải có CoT mới tăng; SQLoom ở 1.7B dùng GPT-4 trong lúc train | federated, không dùng model ngoài |

- Em chưa tìm thấy paper nào làm federated DPO với cặp do client tự gán nhãn
  bằng execution trên database của mình. Text-to-SQL hợp với hướng này vì
  verifier có sẵn ở client: không cần nhãn của người, không cần gửi data.
- Kết quả của em ngược với CoT for DPO và ExCoT. Hai paper này báo SQL-only
  DPO không tăng ở 7B trở lên (Qwen2.5-Coder-7B trên BIRD dev: 61.6 xuống
  61.3), và tỉ lệ SQL không chạy được tăng sau DPO. Ở 1.5B, SQL-only DPO của
  em tăng 3.4-3.9 điểm và số câu SQL không chạy được giảm (129 xuống 58 trên
  Spider test). Cách làm của em khác ở ba chỗ: train DPO kèm loss SFT, sample
  lại sau mỗi round, và dùng gold SQL khi không có sample đúng (theo
  [Iterative RPO](https://arxiv.org/abs/2404.19733)). Em chưa tách được chỗ
  nào tạo ra khác biệt.

**Em xin ý kiến thầy:**

1. Trọng tâm của bài. Tên FedLS-SQL và outline hiện tại xoay quanh việc
   distill từ LLM sang SLM, trong khi phần tạo ra kết quả là DPO. Em đề xuất
   đổi trọng tâm sang federated DPO với cặp gán nhãn bằng execution ở client,
   và đưa bước 1 xuống thành một phần phụ. Tên gợi ý: "Federated
   Execution-Guided Preference Optimization for Text-to-SQL with Small
   Language Models". Outline gợi ý: bài toán; method (FedAvg rồi federated
   DPO); kết quả và control; phân tích (loại lỗi được sửa, số round, bước
   server với teacher, CoT); hạn chế.
2. Phần teacher và BIRD. Data BIRD với gold SQL không còn tác dụng sau DPO
   (75.22 so với 75.13). Teacher giúp thêm 1.5 điểm trên Spider test, chưa rõ
   rệt, nhưng rõ trên Spider dev (+2.7) và DK (+6.2); hai set này dùng chung
   database. Sau DPO student đã gần bằng teacher (76.71 so với 77.22), nên em
   nghĩ phần teacher đóng góp là robustness hơn là EX. Thầy đánh giá mức này
   có đủ để giữ bước 1 trong method không, hay chỉ nên để ở phần ablation?
3. Phần bổ sung. Em định chạy thêm DPO centralized và DPO ở từng client không
   gộp, để thấy setting federated mất và được gì, rồi thêm một cách chia data
   client khác. Thầy thấy thứ tự này có hợp lý không?

**Tiếp theo:** seed thứ hai đang chạy, dự kiến xong sáng 13/11.

Em cảm ơn thầy ạ.
