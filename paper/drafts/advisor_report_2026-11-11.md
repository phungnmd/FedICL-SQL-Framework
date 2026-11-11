# FedLS-SQL: báo cáo tiến độ 11/11/2026

Thưa thầy,

Em gửi thầy kết quả mới của đề tài.

**Method đề xuất** gồm 3 bước:

1. Server distill teacher 7B sang student 1.5B trên BIRD (data public).
2. FedAvg 3 round trên data Spider của các client.
3. Federated DPO 3 round: mỗi client sample 8 câu SQL cho mỗi câu hỏi, chạy
   trên database của mình để ghép cặp đúng / sai, train DPO, rồi server gộp
   bằng FedAvg. Client không gửi data ra ngoài.

Bước 3 là đóng góp chính. Bước 1 là phần em đang cân nhắc giữ hay bỏ (mục
Thảo luận).

**Kết quả trên Spider test** (EX):

| Cấu hình | EX |
|---|---:|
| Base 1.5B | 57.89 |
| FedProx / FedAvg | 70.42 / 71.26 |
| Centralized Spider + BIRD (không federated) | 73.96 |
| Bước 1 + 2 (chưa DPO) | 73.31 |
| FedAvg + DPO (bỏ bước 1) | 75.13 |
| Bước 1 không dùng teacher (SFT gold SQL) + 2 + 3 | 75.22 |
| **Method đề xuất** | **76.71** |

**Kết quả trên các set khác** (EX):

| Cấu hình | Spider dev | Realistic | SYN | DK |
|---|---:|---:|---:|---:|
| FedAvg | 67.89 | 58.86 | 53.77 | 52.15 |
| FedAvg + DPO (bỏ bước 1) | 73.11 | 63.58 | 58.32 | 58.88 |
| Bước 1 không dùng teacher + 2 + 3 | 73.79 | **65.35** | 59.86 | 57.94 |
| Method đề xuất | **76.50** | 64.17 | **61.03** | **64.11** |

- DPO là phần đóng góp chính và không phụ thuộc bước 1: chỉ FedAvg + DPO đã
  hơn FedAvg 3.9 điểm trên Spider test và 4.6-6.7 điểm trên bốn set còn lại.
  Em đã chạy control: chỉ train trên câu đúng (không có cặp đúng / sai) hoặc
  train SFT thêm round đều không tạo ra mức tăng này.
- Method đầy đủ hơn FedAvg 5.45 điểm trên Spider test và 5-12 điểm trên các
  set khác, hơn bản centralized 2.75 điểm, và gần bằng teacher 7B zero-shot
  (77.22).
- Data BIRD với gold SQL không còn tác dụng sau DPO: 75.22 so với 75.13 trên
  Spider test, và không khác rõ rệt trên set nào.
- Teacher giúp thêm 1.5 điểm trên Spider test, mức này chưa rõ rệt. Mức tăng
  rõ trên Spider dev (+2.7) và DK (+6.2), không rõ trên Realistic và SYN.
  Spider dev và DK dùng chung 20 database nên em tính đây là một bằng chứng,
  chưa phải hai.
- 3 round DPO là đủ, round 4 không tăng thêm rõ.

**CoT:** ở 1.5B, CoT kém SQL-only ở mọi bước: server distill plan của
teacher đạt 60.64, thêm FedAvg đạt 62.69, kể cả CoT + DPO 8 round
(centralized) cũng chỉ đạt 69.12, vẫn dưới FedAvg SQL-only (71.26). Vì vậy
em bỏ CoT khỏi method và chỉ giữ làm một phân tích ngắn.

**Thảo luận:**

- Vai trò của teacher. Sau DPO, student đã gần bằng teacher trên Spider test
  (76.71 so với 77.22), nên teacher khó giúp thêm về EX ở set này. Phần
  teacher đóng góp nằm ở robustness, rõ nhất khi câu hỏi cần kiến thức domain
  (DK). Nếu seed thứ hai lặp lại kết quả trên Spider dev và DK, em định giữ
  bước 1 và trình bày teacher là bước khởi tạo giúp model bền hơn, không phải
  nguồn tăng EX trên Spider test.
- Nếu bỏ bước 1. Method còn FedAvg + federated DPO, không cần teacher và
  data public, vẫn hơn FedAvg trên cả 5 set. Method gọn hơn, nhưng đóng góp
  dồn vào một cơ chế: cặp đúng / sai do client tự tạo bằng cách chạy SQL
  trên database của mình. Khi đó paper cần thêm hai row tham chiếu cho phần
  federated: DPO trên data gộp (centralized) và DPO ở từng client không gộp,
  để thấy setting federated mất bao nhiêu so với gộp data và được bao nhiêu
  so với train riêng.
- Nhóm câu chưa sửa được. Khoảng 20% câu Spider test là SQL chạy được nhưng
  sai kết quả. DPO chủ yếu sửa các câu SQL không chạy được, chưa sửa được
  nhóm này.

**Tiếp theo:**

1. Seed thứ hai đang chạy, dự kiến xong sáng 13/11. Sau đó em quyết định giữ
   hay bỏ teacher, dựa trên cả Spider test, Spider dev và DK.
2. Chạy hai row tham chiếu: DPO centralized và DPO ở từng client không gộp.
3. Thêm một cách chia data client khác và bổ sung các baseline tham chiếu còn
   thiếu.

Em cảm ơn thầy ạ.
