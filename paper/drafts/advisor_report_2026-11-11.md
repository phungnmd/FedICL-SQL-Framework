# FedLS-SQL: báo cáo ngày 11/11/2026

**Đề xuất.** Bỏ CoT khỏi method. Method là SQL-only: server stage trên BIRD,
FedAvg 3 round, rồi federated DPO 3 round. Teacher có thể bỏ theo kịch bản A
hoặc B bên dưới.

**Federated DPO.** Mỗi client sample 8 SQL cho từng câu hỏi của mình, chạy
trên database của mình, ghép cặp đúng / sai theo kết quả so với gold, train
DPO + NLL, gộp bằng FedAvg.

## Kết quả (EX, Spider test, 1 seed)

| Cấu hình | EX |
|---|---:|
| Base | 57.89 |
| FedProx / FedAvg, 3 round | 70.42 / 71.26 |
| Centralized Spider + BIRD | 73.96 |
| BIRD gold / Hinton KD, rồi FedAvg (K2AAA) | 73.08 / 73.31 |
| FedAvg + DPO 1 round | 74.29 |
| K2AAA Hinton + DPO round 1 / 2 / 3 / 4 | 75.69 / 76.43 / 76.71 / 76.94 |
| Teacher 7B zero-shot | **77.22** |
| CoT: server, plan của teacher trên BIRD, 5 epoch | 60.64 |
| CoT: + 1 round FedAvg, template plan | 62.69 |
| CoT: + self-taught round 1 / 2 / 3 | 60.08 / 60.64 / 58.69 |
| CoT + DPO 8 round (centralized, kết quả cũ) | 69.12 |

DPO round 3 hơn FedAvg 5.45 điểm trên Spider test, và 5.3-12.0 điểm trên
Spider dev, Realistic, SYN, DK. Round 4 không tăng rõ, nên cố định 3 round.

## Vì sao bỏ CoT

- Thấp hơn SQL-only ở mọi bước: tốt nhất 62.69; kể cả sau 8 round DPO cũng
  chỉ 69.12, dưới FedAvg SQL-only.
- Thiếu kỹ năng SQL, không phải lỗi format: sai format 48 / 2,147 câu,
  nhưng câu hard đạt 43-50 so với 65.4 của FedAvg.
- Tốn hơn: output dài gấp 4, EX lệch 0.5 điểm giữa hai lần eval.
- Liu et al. (ACL 2025, 7B): CoT + DPO chỉ hơn SQL-only SFT 0.5-0.7 điểm
  trên Spider.

## Hai kịch bản bỏ teacher

Trước DPO, Hinton KD hơn gold 0.23 điểm, chưa rõ rệt; sau DPO student đã gần
teacher zero-shot.

- **A, bỏ teacher, giữ BIRD** (nếu gold + DPO ngang Hinton + DPO): SFT gold
  trên BIRD, FedAvg, DPO. Hinton KD thành ablation.
- **B, bỏ cả server stage** (nếu FedAvg + DPO đuổi kịp; hiện kém 1.40 điểm
  sau 1 round): FedAvg, DPO. Đơn giản nhất, novelty mỏng hơn.

Teacher được giữ nếu Hinton + DPO hơn rõ gold + DPO.

## Tiếp theo

Đang chạy, dự kiến xong trong 11/11: DPO từ gold (A), DPO round 2-3 từ
FedAvg (B), hai control của DPO (chỉ NLL; SFT thêm 2 round). Sau đó seed 1.
