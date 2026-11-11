# FedLS-SQL: báo cáo tiến độ 11/11/2026

Thưa thầy,

Em gửi thầy kết quả mới của đề tài.

**Method đề xuất** gồm 3 bước:

1. Server distill teacher 7B sang student 1.5B trên BIRD (data public).
2. FedAvg 3 round trên data Spider của các client.
3. Federated DPO 3 round: mỗi client sample 8 câu SQL cho mỗi câu hỏi, chạy
   trên database của mình để ghép cặp đúng / sai, train DPO, rồi server gộp
   bằng FedAvg. Client không gửi data ra ngoài.

**Kết quả** (EX trên Spider test):

| Cấu hình | EX |
|---|---:|
| Base 1.5B | 57.89 |
| FedProx / FedAvg | 70.42 / 71.26 |
| Centralized Spider + BIRD (không federated) | 73.96 |
| Bước 1 + 2 (chưa DPO) | 73.31 |
| FedAvg + DPO (bỏ bước 1) | 75.13 |
| Bước 1 không dùng teacher (SFT gold SQL) + 2 + 3 | 75.22 |
| **Method đề xuất** | **76.71** |

- Method hơn FedAvg 5.45 điểm, hơn cả bản centralized 2.75 điểm, và gần
  bằng teacher 7B zero-shot (77.22). Trên các set khác (Spider dev,
  Realistic, SYN, DK) method cũng hơn FedAvg 5-12 điểm.
- DPO là phần đóng góp chính, khoảng +3.4 điểm. Em đã chạy control: chỉ
  train trên câu đúng (không có cặp đúng / sai) hoặc train SFT thêm round
  đều không tạo ra mức tăng này.
- Teacher giúp thêm khoảng 1.5 điểm sau DPO. Trên Spider test mức này chưa
  rõ rệt, nhưng rõ trên Spider dev và DK. Nếu bỏ teacher thì nên bỏ luôn
  bước 1, vì train trên BIRD với gold SQL không còn tác dụng sau DPO.
- 3 round DPO là đủ, round 4 không tăng thêm rõ.

**CoT:** ở 1.5B, CoT kém SQL-only ở mọi bước: server distill plan của
teacher đạt 60.64, thêm FedAvg đạt 62.69, kể cả CoT + DPO 8 round
(centralized) cũng chỉ đạt 69.12, vẫn dưới FedAvg SQL-only (71.26). Vì vậy
em bỏ CoT khỏi method và chỉ giữ làm một phân tích ngắn.

**Điểm hạn chế:** khoảng 20% câu Spider test là SQL chạy được nhưng sai kết
quả. DPO chủ yếu sửa các câu SQL không chạy được, chưa sửa được nhóm này.

**Tiếp theo:** em đang chạy seed thứ hai, dự kiến xong sáng 13/11. Sau đó em
sẽ quyết định giữ hay bỏ teacher, rồi bổ sung các baseline tham chiếu còn
thiếu.

Em cảm ơn thầy ạ.
