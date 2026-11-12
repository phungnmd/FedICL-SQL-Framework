# FedLS-SQL: báo cáo tiến độ 11/11/2026

Thưa thầy,

Em gửi thầy kết quả mới và ba điểm em muốn xin ý kiến thầy.

**Method** gồm 3 bước, student là Qwen2.5-Coder-1.5B train bằng LoRA, 5 client
chia từ Spider train:

1. Server: distill logit của teacher 7B (Hinton KD) sang student trên BIRD
   (data public), 2 epoch. Teacher chỉ chạy ở server.
2. FedAvg SFT 3 round: mỗi client train trên câu hỏi và gold SQL của mình,
   server gộp adapter.
3. Federated DPO 3 round, bắt đầu từ model của bước 2. Mỗi round:
   - Sample: mỗi client dùng model global hiện tại sample 8 câu SQL cho mỗi
     câu hỏi train của mình (temperature 0.7).
   - Gán nhãn: client chạy từng sample trên database của mình và so với kết
     quả của gold SQL: đúng, sai kết quả, hoặc không chạy được.
   - Ghép cặp: chosen là một sample đúng, rejected là một sample sai của
     cùng câu hỏi; ưu tiên hai câu SQL giống nhau nhất, mỗi sample dùng một
     lần, tối đa 2 cặp mỗi câu hỏi. Câu hỏi không có sample đúng thì gold
     SQL làm chosen. Câu hỏi có cả 8 sample đúng thì không tạo cặp.
   - Train: loss DPO (beta 0.1) cộng loss NLL trên chosen, 2 local epoch;
     reference model là model global đầu round.
   - Gộp: server FedAvg adapter của các client, weight theo số cặp.

   Round sau sample lại từ model global mới, nên các cặp luôn lấy từ lỗi
   hiện tại của model và số cặp giảm dần: trên 8,659 câu hỏi, 5,393 cặp ở
   round 1 (609 cặp dùng gold SQL) xuống 3,208 ở round 3. Client chỉ gửi
   adapter; data, sample và các cặp ở lại client.

**Kết quả** trên Spider test:

| Cấu hình                  |        EX |        EM |
| ------------------------- | --------: | --------: |
| Base 1.5B zero-shot       |     57.89 |     31.11 |
| FedProx                   |     70.42 |     58.69 |
| FedAvg                    |     71.26 |     60.32 |
| Centralized Spider + BIRD |     73.96 |     65.07 |
| Method w/o DPO            |     73.31 |     64.42 |
| Method w/o server stage   |     75.13 |     62.93 |
| Method w/o teacher        |     75.22 |     64.97 |
| **Method**                | **76.71** | **65.49** |
|                           |           |           |
| _Teacher 7B zero-shot_    |   _77.22_ |   _46.48_ |

Method w/o DPO là bước 1 + 2; w/o server stage là bước 2 + 3; w/o teacher là
cả 3 bước nhưng bước 1 train bằng gold SQL của BIRD thay cho distill teacher.

EX trên các set khác:

| Cấu hình                | Spider dev | Realistic |       SYN |        DK |
| ----------------------- | ---------: | --------: | --------: | --------: |
| FedAvg                  |      67.89 |     58.86 |     53.77 |     52.15 |
| Method w/o DPO          |      72.82 |     62.01 |     56.67 |     58.13 |
| Method w/o server stage |      73.11 |     63.58 |     58.32 |     58.88 |
| Method w/o teacher      |      73.79 | **65.35** |     59.86 |     57.94 |
| **Method**              |  **76.50** |     64.17 | **61.03** | **64.11** |

- DPO là đóng góp chính: 3.4% EX trên Spider test khi có bước 1
  và 3.9 điểm khi không có. Không có bước 1, DPO vẫn tăng 4.6-6.7 điểm trên
  bốn set còn lại. Control (chỉ train trên câu đúng, hoặc SFT thêm round)
  không tạo ra mức tăng này. 3 round là đủ.
- Method hơn FedAvg 5.45 điểm EX trên Spider test, hơn bản centralized 2.75
  điểm, và gần bằng teacher 7B zero-shot (77.22).
- EM tăng ít hơn EX sau DPO (1.1 điểm khi có bước 1, 2.6 khi không có).
  Teacher zero-shot có EX cao nhất nhưng EM chỉ 46.48, vì chưa train trên
  Spider nên viết SQL khác dạng của gold.
- Còn khoảng 20% câu Spider test là SQL chạy được nhưng sai kết quả; DPO chủ
  yếu sửa các câu SQL không chạy được, chưa sửa được nhóm này. CoT ở 1.5B
  kém SQL-only ở mọi bước nên em chỉ giữ làm một phân tích ngắn.

**So với các paper liên quan:**

- Khoảng trống: chưa có bài nào làm federated DPO cho Text-to-SQL với cặp do
  client tự gán nhãn bằng execution trên database của mình. Federated
  Text-to-SQL mới có [FL4SP](https://arxiv.org/abs/2305.17221) (T5-base,
  exact match). Federated DPO
  ([OpenFedLLM](https://arxiv.org/abs/2402.06954),
  [FedBiscuit](https://arxiv.org/abs/2407.03038)) dùng nhãn preference của
  người. Federated RL có verifier
  ([PubSwap](https://arxiv.org/abs/2604.12160),
  [Fed-GRPO](https://arxiv.org/abs/2610.11502),
  [FedMOA](https://arxiv.org/abs/2602.00453)) làm trên toán và code. DPO cho
  Text-to-SQL đều centralized.
- Phát hiện khác: [CoT for DPO](https://aclanthology.org/2025.acl-long.1031/)
  và [ExCoT](https://arxiv.org/abs/2503.19988) (7B-70B) đều là method CoT, và
  báo SQL-only DPO không tăng EX (Qwen2.5-Coder-7B trên BIRD dev: 61.6 xuống
  61.3). [SQLoom](https://arxiv.org/abs/2611.03298) (1.7B) phải gọi GPT-4
  trong lúc train. Ở 1.5B em thấy ngược lại: SQL-only DPO tăng 3.4-3.9 điểm
  EX, không cần CoT hay model ngoài, và CoT còn kém SQL-only.
- DPO của em khác hai bài CoT ở bốn chỗ: kèm loss NLL, sample lại sau mỗi
  round, dùng gold SQL khi không có sample đúng (theo
  [Iterative RPO](https://arxiv.org/abs/2404.19733)), và ghép cặp hai câu SQL
  giống nhau nhất.

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
