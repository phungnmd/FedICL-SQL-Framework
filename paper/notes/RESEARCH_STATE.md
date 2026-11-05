# FedLS-SQL: trạng thái nghiên cứu

Cập nhật: 2026-11-05 (thêm C7; tiêu chí chọn hướng mới ở DIRECTION mục 1). File này trả lời bốn câu: ta hỏi gì,
đã biết gì (kèm mức chắc chắn), còn chưa biết gì, và đang ở giai đoạn nào.
Các hướng đang cân nhắc: [DIRECTION](DIRECTION.md). Số liệu: [LAB_LOG](LAB_LOG.md).
Lệnh chạy: [PIPELINE_NEXT](PIPELINE_NEXT.md). Nguồn tham khảo: [LITERATURE](LITERATURE.md).
Bản trước đợt dọn (F1-F31 đầy đủ, các đoạn cập nhật theo ngày):
[archive](../archive/directions_2026-11/RESEARCH_STATE_2026-11-04.md).

## 1. Câu hỏi

Nhiều client giữ dữ liệu Text-to-SQL riêng (Spider, chia theo domain) và cùng
train một SLM bằng federated learning. Server có một LLM teacher frozen và một
public dataset khác miền (BIRD). Chỉ deploy SLM.

> Tổ hợp nào của teacher KD, CoT, RL và federated learning làm SLM federated
> Text-to-SQL tốt hơn rõ rệt, với phần đóng góp của teacher đo được, và chưa
> bị một paper trước làm trùng?

Owner 2026-11-04: bỏ các hướng cũ (K-chain, replay đã freeze, P2.53), tập trung
vào tổ hợp năm thành phần trên miễn là tổ hợp đủ ý nghĩa. Không bắt buộc dùng
đủ cả năm; CoT chỉ giữ nếu bằng chứng ủng hộ.

Metric: Spider EX là chính, báo Spider dev và Spider test cùng nhau (owner
2026-11-04); Spider test được dùng trong quá trình phát triển nên không gọi là
held-out. BIRD dev là metric phụ, chạy cho arm đã chốt.

## 2. Setup cố định

- Student Qwen2.5-Coder-1.5B-Instruct, LoRA r16. Teacher Qwen2.5-Coder-7B,
  4-bit, frozen, chỉ chạy ở server trên public data.
- 5 client, split domain-cluster Dirichlet alpha 0.1 (`k5`), FedAvg theo số mẫu.
  Client chỉ gửi LoRA adapter.
- Public: BIRD train có evidence (9,428 câu). Private: Spider train (8,659).
- Compute: hai RTX A5000 24 GB; teacher 14B/32B không vừa.
- Không ICL. Greedy khi eval, batch 16.

## 3. Đã biết

Mức: **vững** = lặp lại qua nhiều model hoặc seed; **1 seed** = đáng tin về
chiều, chưa về độ lớn; **thăm dò** = tìm ra sau khi xem dữ liệu.

### 3.1. RL bằng execution feedback (centralized, Spider dev)

| # | Phát hiện | Bằng chứng | Mức |
|---|---|---|---|
| R1 | DPO + NLL với pair đúng/sai theo execution nâng SLM rất mạnh | Từ student chỉ train BIRD: `s1` 58.80 lên 74.18 (+15.38, 184/25); `c1` 60.64 lên 70.89 (+10.25) | 1 seed |
| R2 | RL thẳng từ student BIRD đạt mức Spider SFT, không cần SFT trên gold SQL của Spider | `s1_rl9` - `sql2_e1` +0.58 (p=.71); - `sql_rl9` -1.35 (p=.33) | 1 seed |
| R3 | Sau Spider SFT, RL thêm khoảng 2 điểm | `sql_rl9` 75.53 so với `sql2_e1` 73.60; P2.58 `g3d` - `g2` +1.93 (p=.012) | 1 seed, hai lần chạy |
| R5 | Với SQL-only, gain của DPO đến từ chính preference term, không từ NLL | P2.59 `g3d` - `g3n` (chỉ NLL, cùng chosen) +2.22 (41/18, p=.004); `g3n` 72.24 so với `g2` 72.53. Ngược với Liu et al. (ACL 2025, 6.7-15B, BIRD, DPO không NLL) | 1 seed |
| R4 | Retry trên các câu toàn sai vẫn còn gain, chưa thấy trần ở SQL | `s1` retry +2.03, +1.07; `s1` còn tăng ở round cuối | 1 seed |

### 3.2. CoT

| # | Phát hiện | Bằng chứng | Mức |
|---|---|---|---|
| C1 | Cùng route RL, CoT thua SQL-only | `c1_rl8` - `s1_rl9` -3.29 (73/107, p=.014) trên dev; xuất phát CoT hơn 1.84, kết thúc thua 3.29 | 1 seed, chỉ dev cho SQL |
| C2 | Sau SFT, CoT tự do thua SQL khoảng 10 điểm; CoT template (diễn lại SQL) ngang SQL | P2.58 `t2` - `g2` -10.06; P2.61 `cot2g` - `sql2_e1` -10.15; P2.59 `tp2` - `g2` +0.48 | 1 seed, nhiều lần chạy |
| C3 | CoT khám phá nhiều hơn nhưng chuyển vào greedy kém hơn | Cùng bộ câu: pass@8 CoT 84.9-86.3, SQL 81.1-82.5; pair 5,184 so với 2,781; gain mỗi round nhỏ hơn | thăm dò |
| C4 | Stage public của teacher CoT không thua SQL | `cot1_e4` - `sql1_e2` +1.84 (p=.27) với 1,266 câu so với 9,428 | 1 seed |
| C5 | CoT tốn hơn nhiều | Token p50 khoảng 200 so với 25; một round RL 2.5-4 GPU-h so với 1.2 | đo trực tiếp |
| C7 | Khi khám phá, CoT và SQL bổ sung nhau trên câu khó | Cùng bộ câu và round: `c1` có SQL đúng ở 508/1,200 câu `s1` sai hết (42.3%); `s1` tự retry từ checkpoint tốt hơn chỉ cứu 23.83%. Hai model khác nhau, chưa tách khỏi hiệu ứng "có thêm model" | thăm dò, CPU trên file đã publish |
| C6 | Spider test của CoT tốt nhất | `c1_rl8` 69.12 (dev 70.89); chưa có số test của route SQL để so | 1 seed |

### 3.3. Teacher KD (giai đoạn K-chain, federated, Coder-1.5B)

| # | Phát hiện | Bằng chứng | Mức |
|---|---|---|---|
| K1 | Một stage server trên BIRD làm SLM federated tốt hơn trên cả hai miền | `h_plain` - FedAvg Spider dev +4.16, BIRD +14.28 | vững (3 model) |
| K2 | Soft label của teacher hơn gold trên Spider dev, và lợi thế này không phải do smoothing hay do kéo về base model | `hinton_k2aaa` - `gold_k2aaa` A3 +2.13 (p=.020); so với virtual teacher +2.03; so với self-teacher +2.32 | 1 seed, có control |
| K3 | Trên Spider test, phần teacher chỉ khoảng 0.5 điểm | Các arm K2 72.6-73.9, FedAvg 71.50; `hinton_k2aaa` - `gold_k2aaa` +0.47 | 1 seed |
| K4 | Các round FedAvg bào mòn phần BIRD học ở server; replay target của teacher giữ lại, replay gold thì không | BIRD 43.61 (K2) xuống 36.77 (A1); replay teacher +6.25 BIRD dev; teacher - gold replay +4.04 (p<.001) | 1 seed |
| K5 | Teacher 7B zero-shot mạnh hơn mọi student | Spider test 77.22 | đo trực tiếp |

### 3.4. Federated (SQL-only SFT)

| # | Phát hiện | Bằng chứng | Mức |
|---|---|---|---|
| FL1 | FedAvg thuần gần như không hơn client tốt nhất tự train | FedAvg A3 - client tốt nhất +0.58 (p=.69) trên dev | 1 seed |
| FL2 | Khoảng cách FL so với central có trên dev, không còn trên test | Dev +3.77 ở cùng số pass; test `central` - FedAvg -0.42 (p=.66) | 1 seed |
| FL3 | FedProx (mu 0.01) và FedNTD không mạnh hơn FedAvg | FedProx - FedAvg Spider test -1.07 (p=.047) | 1 seed |
| FL4 | Mốc federated SQL-only | FedAvg A3: Spider dev 67.60, test 71.50 | 1 seed |

Các hướng đã đóng vì kết quả âm hoặc quá tốn: plan task và CoT phụ trong SFT
(P2.10-P2.15), retention loss, weight merge, KID, GKD với `full_bf16`, TAID,
ICL, self-consistency, public pool cùng miền, frozen LoRA A, teacher ở client.

## 4. Chưa biết

| # | Câu hỏi | Cần gì |
|---|---|---|
| Q1 | RL bằng execution feedback có chạy được trong federated (5 client, alpha 0.1) không, và có ít bị non-IID hơn SFT không? | FedAvg của local DPO so với FedAvg SFT, cùng điểm xuất phát |
| Q2 | Teacher đóng góp được bao nhiêu khi pipeline có RL? (điểm xuất phát KD, replay làm neo, on-policy distillation, pair của teacher) | RL từ `hinton_k2` so với từ gold K2, trước tiên ở centralized |
| Q3 | Khoảng cách CoT - SQL (C1) có giữ trên Spider test không? | Spider test cho `s1_rl9`, `sql_rl9`, `sql2_e1` |
| Q4 | Các câu client sinh toàn sai (không có pair) ảnh hưởng thế nào khi dữ liệu non-IID? | Đếm theo client trong pilot FL |
| Q5 | Chi phí rollout trong FL có vừa ngân sách không? | Đo trong pilot FL |

## 5. Giai đoạn và luật

Giai đoạn: **chọn hướng mới** (owner, 2026-11-04). Các ứng viên và thí
nghiệm đầu tiên của mỗi hướng ở [DIRECTION](DIRECTION.md). Không có lệnh GPU
nào đang chạy.

Luật cố định (owner, 2026-10-29), đều về trung thực:

- Mọi số trong paper có evidence trail (checkpoint, config, dataset, seed,
  file prediction, Git SHA). Số chỉ có trong chat ghi "not committed".
- Mỗi số ghi rõ tập (dev hay test); số Spider test đã dùng để chọn gì thì
  không gọi là held-out.
- Gộp seed bằng question-clustered test, không cộng discordant pair qua seed.

Còn lại là thực hành: thăm dò tự do, ghi mọi run vào LAB_LOG; chỉ chạy
control khi nó có thể đổi method hoặc reviewer chắc chắn hỏi; chọn trên dev
làm số phồng lên (cái tốt nhất trong 10 biến thể không có tác dụng vẫn thấy
khoảng +1.7 điểm trên dev); chỉ claim điều có comparator tách riêng. Câu
chuyện teacher chỉ là ablation không đạt mục tiêu paper.
