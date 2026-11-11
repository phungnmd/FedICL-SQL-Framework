# FedLS-SQL: báo cáo tiến độ 11/11/2026

Thưa thầy,

Em gửi thầy kết quả mới và phần đánh giá khoảng trống của đề tài.

**Method** gồm 3 bước:

1. Server distill teacher 7B sang student 1.5B trên BIRD (data public).
2. FedAvg 3 round trên data Spider của các client.
3. Federated DPO 3 round: mỗi client sample 8 câu SQL cho mỗi câu hỏi, chạy
   trên database của mình để ghép cặp đúng / sai, train DPO, rồi server gộp
   bằng FedAvg. Client không gửi data ra ngoài.

Bước 3 là đóng góp chính. Bước 1 em đang cân nhắc giữ hay bỏ.

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

- DPO là phần chính: trên Spider test tăng 3.4 điểm khi có bước 1 và 3.9 điểm
  khi không có. Không có bước 1, DPO vẫn tăng 4.6-6.7 điểm trên bốn set còn
  lại. Control (chỉ train trên câu đúng, hoặc SFT thêm round) không tạo ra
  mức tăng này. 3 round là đủ.
- Cả 3 bước hơn FedAvg 5.45 điểm trên Spider test, hơn bản centralized 2.75
  điểm, và gần bằng teacher 7B zero-shot (77.22).
- Bước 1: data BIRD với gold SQL không còn tác dụng sau DPO. Teacher giúp
  thêm 1.5 điểm trên Spider test (chưa rõ rệt), rõ trên Spider dev (+2.7) và
  DK (+6.2); hai set này dùng chung database nên là một bằng chứng.
- CoT ở 1.5B kém SQL-only ở mọi bước (tốt nhất 69.12 với CoT + DPO, dưới
  FedAvg SQL-only), nên em chỉ giữ làm một phân tích ngắn.

**Khoảng trống so với các paper liên quan:**

| Mảng | Paper gần nhất | Đã có | Chưa có |
| --- | --- | --- | --- |
| Federated Text-to-SQL | FL4SP (ACL 2023) | T5-base, exact match, 8 dataset một domain | SLM decoder, Spider, EX |
| Federated DPO | OpenFedLLM (2024), FedBiscuit (ICLR 2025) | DPO ở client rồi gộp LoRA, nhãn preference của người | nhãn từ verifier tự động |
| Federated RL có verifier | PubSwap, Fed-GRPO, FedMOA (preprint 2026) | GRPO federated ở 1.5-4B, trên toán và code | Text-to-SQL, execution trên database của client |
| DPO cho Text-to-SQL | Liu et al. (ACL 2025), ExCoT (2025) | centralized, 7B-70B, cặp đúng / sai theo execution | model dưới 7B, setting federated |

- Khoảng trống: em chưa tìm thấy paper nào làm federated DPO với cặp do
  client tự gán nhãn bằng execution trên database của mình, và chưa có paper
  federated Text-to-SQL nào dùng SLM decoder với EX. Text-to-SQL hợp với
  hướng này vì verifier có sẵn ở client: không cần nhãn của người, không cần
  gửi data.
- Điểm đáng chú ý: Liu et al. và ExCoT báo SQL-only DPO không tăng ở 7B trở
  lên (Qwen2.5-Coder-7B trên BIRD dev: 61.6 xuống 61.3), phải có CoT mới
  tăng. Ở 1.5B kết quả của em ngược lại: SQL-only DPO tăng 3.4-3.9 điểm, còn
  CoT thì kém. Model nhỏ sai nhiều hơn nên có nhiều cặp để học (5,393 cặp ở
  round 1, Liu et al. chỉ có 0.1-0.3k cặp trên Spider train), và mức tăng
  đến từ việc sửa các câu SQL không chạy được.
- Mức mới: cơ chế DPO rồi gộp LoRA đã có. Phần mới là đưa vào federated
  Text-to-SQL với verifier là execution ở client, cùng kết quả ở 1.5B. Em
  đánh giá mức này phù hợp journal Q3.
- Điểm reviewer có thể hỏi: phần federated chỉ là FedAvg, nên cần row DPO
  centralized và DPO ở từng client không gộp để so. SQLoom (preprint 2026)
  đạt 89.2 trên Spider test ở 1.7B, nhưng train centralized và dùng GPT-4 đọc
  data train, khác setting của em.

**Thảo luận:**

- Teacher: sau DPO student đã gần bằng teacher trên Spider test (76.71 so
  với 77.22), nên phần teacher đóng góp nằm ở robustness (DK) hơn là EX trên
  Spider test. Nếu seed thứ hai lặp lại kết quả trên Spider dev và DK, em giữ
  bước 1. Nếu không, method còn bước 2 + 3, không cần teacher và data public.
- Hạn chế: khoảng 20% câu Spider test là SQL chạy được nhưng sai kết quả.
  DPO chủ yếu sửa các câu SQL không chạy được, chưa sửa được nhóm này.

**Tiếp theo:**

1. Seed thứ hai, dự kiến xong sáng 13/11, rồi quyết định giữ hay bỏ bước 1.
2. Hai row tham chiếu: DPO centralized và DPO ở từng client không gộp.
3. Thêm một cách chia data client khác và các baseline còn thiếu.

Em cảm ơn thầy ạ.
