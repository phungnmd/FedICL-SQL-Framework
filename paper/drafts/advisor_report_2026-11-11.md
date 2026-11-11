# FedLS-SQL: báo cáo ngày 11/11/2026

**Đề xuất.** Bỏ CoT khỏi method. Method là SQL-only: server stage Hinton KD
trên BIRD, FedAvg 3 round, rồi federated DPO 3 round. Server stage chỉ có ích
khi có teacher: nếu bỏ teacher thì bỏ luôn server stage.

**Federated DPO.** Mỗi client sample 8 SQL cho từng câu hỏi của mình, chạy
trên database của mình, ghép cặp đúng / sai theo kết quả so với gold, train
DPO + NLL, gộp bằng FedAvg.

## Kết quả (EX, Spider test, 1 seed)

Baseline:

| Cấu hình | EX |
|---|---:|
| Base | 57.89 |
| FedProx / FedAvg, 3 round | 70.42 / 71.26 |
| Centralized Spider + BIRD | 73.96 |
| Teacher 7B zero-shot | **77.22** |

DPO từ ba điểm xuất phát:

| Điểm xuất phát | Trước DPO | DPO round 1 | Round 2 | Round 3 |
|---|---:|---:|---:|---:|
| FedAvg 3 round, không server stage | 71.26 | 74.29 | 75.17 | 75.13 |
| BIRD gold SFT, rồi FedAvg (K2AAA) | 73.08 | 74.34 | 75.13 | 75.22 |
| BIRD Hinton KD, rồi FedAvg (K2AAA) | **73.31** | **75.69** | **76.43** | **76.71** |

- Method (Hinton + DPO round 3) hơn FedAvg 5.45 điểm, rõ rệt. Round 4
  (76.94) không tăng rõ so với round 3, nên cố định 3 round cho mọi line.
- DPO tăng rõ từ cả ba điểm xuất phát (+2.1 đến +3.9 điểm).
- Gain chủ yếu từ việc bỏ lỗi thực thi: từ FedAvg đến method, số câu lỗi
  thực thi giảm từ 211 xuống 58.

Control, cùng xuất phát từ Hinton K2AAA:

| Bước thêm | EX |
|---|---:|
| Không | 73.31 |
| 1 round chỉ NLL, cùng cặp và cùng lịch train | 73.50 |
| 1 / 2 round FedAvg SFT thêm | 74.15 / 72.99 |
| 1 round DPO + NLL | 75.69 |
| 1 round focused DPO (trọng số cao hơn trên đoạn SQL khác nhau giữa hai mẫu) | **76.20** |

- Gain của DPO đến từ preference term: chỉ NLL gần như không đổi, SFT thêm
  tăng ít rồi giảm. Method hơn control SFT tốt nhất 2.56 điểm, rõ rệt.
- Focused DPO hơn DPO thường 0.51 điểm sau 1 round, chưa rõ rệt. Method giữ
  DPO thường; focused DPO là ablation.

Các set khác (round 3; không có lựa chọn nào dựa trên các set này):

| Cấu hình | Spider test | Spider dev | Realistic | SYN | DK | BIRD dev |
|---|---:|---:|---:|---:|---:|---:|
| FedAvg 3 round | 71.26 | 67.89 | 58.86 | 53.77 | 52.15 | 25.55 |
| FedAvg + DPO | 75.13 | 73.11 | 63.58 | 58.32 | 58.88 | 29.66 |
| Gold K2AAA + DPO | 75.22 | 73.79 | **65.35** | 59.86 | 57.94 | 40.87 |
| Hinton K2AAA + DPO (method) | **76.71** | **76.50** | 64.17 | **61.03** | **64.11** | **41.20** |

- Method hơn FedAvg trên mọi set Spider, từ 5.3 (Realistic) đến 12.0 (DK)
  điểm.
- DPO trên data Spider của client không làm giảm EX trên BIRD dev: cả ba
  line đều tăng.

## Server stage và teacher

- BIRD với gold SQL không còn tác dụng sau DPO: gold + DPO ngang FedAvg +
  DPO ở mọi round trên Spider test (75.22 so với 75.13 ở round 3), và không
  khác rõ trên các set Spider khác. Vì vậy kịch bản bỏ teacher nhưng giữ
  BIRD không còn lý do; nếu bỏ teacher thì method là FedAvg + DPO.
- Teacher giữ được lợi thế sau DPO: Hinton + DPO hơn gold + DPO 1.3-1.5
  điểm ở mọi round, trên cùng câu hỏi BIRD. Trên Spider test mức này ở sát
  ngưỡng; rõ rệt trên Spider dev (+2.71) và DK (+6.17), cùng chiều chưa rõ
  trên SYN, ngược chiều chưa rõ trên Realistic (-1.18).
- So với không có server stage, method hơn FedAvg + DPO 1.58 điểm trên
  Spider test (sát ngưỡng), rõ rệt trên Spider dev, SYN và DK.
- Trên BIRD dev, teacher không giúp: trước DPO gold hơn Hinton 1.69 điểm,
  sau DPO hai line ngang nhau.

## Vì sao bỏ CoT

| Cấu hình CoT | EX |
|---|---:|
| Server, plan của teacher trên BIRD, 5 epoch | 60.64 |
| + 1 round FedAvg, template plan | **62.69** |
| + self-taught round 1 / 2 / 3 | 60.08 / 60.64 / 58.69 |
| CoT + DPO 8 round (centralized, kết quả cũ) | 69.12 |

- Thấp hơn SQL-only ở mọi bước: tốt nhất 62.69; kể cả sau 8 round DPO cũng
  chỉ 69.12, dưới FedAvg SQL-only.
- Thiếu kỹ năng SQL, không phải lỗi format: sai format 48 / 2,147 câu,
  nhưng câu hard đạt 43-50 so với 65.4 của FedAvg.
- Tốn hơn: output dài gấp 4, EX lệch 0.5 điểm giữa hai lần eval.
- Liu et al. (ACL 2025, 7B): CoT + DPO chỉ hơn SQL-only SFT 0.5-0.7 điểm
  trên Spider.

## Thảo luận

- Khoảng 20% câu Spider test (khoảng 440 câu) là SQL chạy được nhưng sai
  kết quả. Con số này gần như không đổi từ base model đến DPO round 4, kể cả
  với focused DPO (439 so với 440). DPO sửa lỗi thực thi, chưa sửa được sai
  logic; đây là phần giới hạn EX ở quanh 77, gần teacher zero-shot.
- Gain của DPO (3-5 điểm) lớn hơn nhiều so với lợi thế của teacher
  (1.3-1.6 điểm): phần đóng góp chính của method là federated DPO với cặp
  được gán nhãn bằng execution trên database của client.

## Tiếp theo

- Đang chạy: seed 1 cho ba line DPO (từ Hinton K2AAA, từ FedAvg, từ gold
  K2AAA), 3 round, kèm các set khác ở round 3. Dự kiến xong sáng 13/11.
- Sau seed 1: quyết định giữ hay bỏ teacher, gộp hai seed theo từng câu
  hỏi.
- Sau đó: các dòng tham chiếu cho setting federated (DPO trên data gộp của
  các client, DPO ở từng client không aggregation) và FedProx, FedNTD, local
  client trên cùng engine eval.
