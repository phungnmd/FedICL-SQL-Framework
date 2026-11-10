# FedLS-SQL: báo cáo ngày 11/11/2026

**Đề xuất.** (1) Bỏ CoT khỏi method, giữ lại thành một mục phân tích ngắn.
(2) Method là SQL-only: server stage trên BIRD, FedAvg, rồi federated DPO ở
client. (3) Teacher có thể bỏ theo một trong hai kịch bản ở mục 4.

## 1. Hai hướng đã chạy

Setup không đổi: student Qwen2.5-Coder-1.5B, 5 client Spider (alpha 0.1),
teacher Qwen2.5-Coder-7B chỉ chạy ở server trên BIRD.

**Hướng CoT** (output là query plan + SQL)

- Server: SFT trên 4,109 câu BIRD với query plan + SQL của teacher (chỉ giữ
  câu teacher cho kết quả đúng).
- Client, hai cách: FedAvg SFT với plan sinh từ gold SQL bằng template; hoặc
  self-taught, client tự sample 8 output và lấy plan + SQL đúng phổ biến
  nhất làm target.

**Hướng SQL-only** (output chỉ là SQL)

- Server 2 epoch trên BIRD (Hinton KD từ teacher, hoặc SFT gold), rồi FedAvg
  3 round (K2AAA).
- Federated DPO + NLL, 3 round: client sample 8 SQL cho mỗi câu hỏi của
  mình, chạy trên database của mình, so kết quả với gold để ghép cặp đúng /
  sai (không có sample đúng thì dùng gold), train cục bộ, gộp bằng FedAvg.

## 2. Kết quả (EX, Spider test 2,147 câu, 1 seed)

| Hướng | Cấu hình | EX |
|---|---|---:|
| Tham chiếu | Base, chưa train | 57.89 |
| | Teacher 7B zero-shot | **77.22** |
| | Centralized Spider | 70.75 |
| | Centralized Spider + BIRD | 73.96 |
| | FedAvg 3 round | 71.26 |
| CoT | Server, plan của teacher, 5 epoch | 60.64 |
| | + 1 round client, template plan | 62.69 |
| | + self-taught round 1 / 2 / 3 | 60.08 / 60.64 / 58.69 |
| SQL-only | BIRD gold + FedAvg 3 round | 73.08 |
| | BIRD Hinton KD + FedAvg 3 round | 73.31 |
| | FedAvg 3 round + DPO 1 round | 74.29 |
| | BIRD Hinton KD + FedAvg + DPO round 1 / 2 / 3 / 4 | 75.69 / 76.43 / 76.71 / 76.94 |

- DPO 3 round đưa K2AAA từ 73.31 lên 76.71: hơn rõ FedAvg (71.26) và
  centralized Spider + BIRD (73.96), gần bằng teacher zero-shot.
- Round 4 chỉ thêm 0.23 điểm, chưa rõ rệt, nên số round cố định là 3.
- CoT tốt nhất đạt 62.69, thấp hơn FedAvg SQL-only 8.6 điểm.

## 3. Vì sao hướng CoT không ổn

1. **Thiếu kỹ năng SQL, không phải lỗi format.** Output sai format chỉ
   48 / 2,147 (về 0 sau template round), nhưng câu hard chỉ đạt 43-50, so
   với 65.4 của FedAvg SQL-only.
2. **Server stage bão hòa sớm.** EX qua 6 epoch: 52.17, 56.68, 58.55, 59.94,
   60.64, 60.20; câu hard đứng ở 43-44 từ epoch 3.
3. **Round client không kéo lên được.** Template plan chỉ diễn đạt lại SQL
   theo từng mệnh đề (+2.05, nhưng câu extra giảm 6.1 điểm). Self-taught
   đứng yên rồi giảm, vì model chỉ đúng 55-66% trên sample của chính nó.
4. **Chi phí cao hơn.** Output dài gấp 4 (1,024 so với 256 token), row train
   dài tới 7,600 token, và hai lần eval cùng một adapter đã lệch khoảng 0.5
   điểm.
5. **Literature cùng chiều trên Spider.** Liu et al. (ACL 2025, model
   6.7B-15B): CoT SFT thấp hơn SQL-only SFT 0.7-2.6 điểm, CoT + DPO chỉ hơn
   SQL-only SFT 0.5-0.7 điểm (Spider dev). Kết quả trước đây của nhóm cũng
   vậy: cùng số round DPO, CoT lên 70.89, SQL lên 74.18 (Spider dev).

Để ngang method SQL-only, DPO trên CoT phải thêm khoảng 14 điểm từ 62.69.
Template round 2-3 và DPO trên CoT trong setup federated chưa chạy.

## 4. Hai kịch bản bỏ teacher

Trước DPO, Hinton KD hơn gold 0.23 điểm (73.31 so với 73.08), cùng chiều
nhưng chưa rõ rệt. Sau DPO, student đã gần teacher zero-shot, nên teacher
còn ít thứ để truyền trên Spider.

| | A: bỏ teacher, giữ BIRD | B: bỏ teacher và cả server stage |
|---|---|---|
| Xảy ra khi | gold + DPO ngang Hinton + DPO (76.71), cả hai hơn rõ FedAvg + DPO | FedAvg + DPO 3 round đuổi kịp các line có server stage |
| Method | SFT gold trên BIRD, FedAvg, federated DPO | FedAvg, federated DPO |
| Đóng góp | public data ở server + DPO gán nhãn bằng execution ở client | federated DPO gán nhãn bằng execution ở client |
| Phần bị bỏ | Hinton KD thành một dòng ablation | server stage (gold, Hinton) thành ablation |
| Cần cân nhắc | server không cần model 7B; bài không còn là distillation từ LLM | đơn giản nhất, không cần public data; novelty mỏng hơn, dựa hẳn vào control của DPO |

Số hiện có cho B: sau 1 round DPO, line có server stage hơn line FedAvg 1.40
điểm (75.69 so với 74.29), trước DPO là 2.05. Teacher chỉ được giữ nếu
Hinton + DPO hơn rõ gold + DPO.

## 5. Thảo luận

- Liu et al. và ExCoT (model 6.7B-70B) báo cáo SQL-only DPO không tăng
  hoặc làm giảm EX.
  Ở đây SQL-only DPO tăng 3.4 điểm với model 1.5B, nên cần control tách
  phần đóng góp của preference term: một round chỉ có NLL trên cùng các
  cặp, và FedAvg SFT thêm 2 round.
- Bỏ teacher làm bài lệch khỏi khung LLM-to-SLM ban đầu; cần thống nhất
  khung mới trước khi viết.

## 6. Kế hoạch

- Đang chạy, dự kiến xong trong ngày 11/11: hai control của DPO, DPO 3 round từ
  BIRD gold (quyết định A), DPO round 2-3 từ FedAvg (quyết định B), và các
  dòng trên Spider dev, Realistic, SYN, DK, BIRD dev.
- Sau đó: chốt kịch bản, chạy seed 1 với cấu hình đã chốt.
