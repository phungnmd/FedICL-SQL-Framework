# FedLS-SQL: báo cáo tiến độ (29/10/2026)

Em xin gửi thầy tình hình research hiện tại của dự án.

## 1. Tóm tắt

- **Method:** server distill teacher 7B trên BIRD vào student 1.5B, rồi 3
  round FedAvg trên Spider; mỗi round client replay một ít câu BIRD với
  target top-50 của teacher do server gửi một lần.
- **Framework (Spider test, seed 0):** hơn FedAvg +1.68 (p=.029), hơn train
  tập trung chỉ Spider +2.10 (p=.009), ngang train tập trung Spider + BIRD
  không privacy (-0.61, p=.46).
- **Teacher:** giữ được kiến thức miền public qua các round FL; BIRD dev hơn
  mọi cấu hình không replay target teacher +3.5 đến +7 điểm (p<.001). Trên
  Spider (miền private) phần riêng của teacher nhỏ: +0.56 (seed 0), +1.16
  (seed 1, p=.065).
- **Đang làm:** xác nhận trên 3 seed với Spider test; paper chỉ lấy claim từ
  kết quả 3 seed.

## 2. Method hiện tại

Sau nhiều cấu hình federated đã thử với student Qwen2.5-Coder-1.5B (mục 6),
em chọn `mixkd50_k2aaa`:

1. **Server warm-start:** distill teacher Qwen2.5-Coder-7B (frozen) trên BIRD
   public, 0.5 gold CE + 0.5 KL (Hinton KD, T=2), 2 epoch.
2. **3 round FedAvg trên Spider với client replay:** mỗi round, client trộn
   thêm câu BIRD (20% số câu private) với target top-50 token của teacher do
   server gửi một lần (khoảng 33 MB mỗi client). Teacher không chạy ở client;
   client chỉ gửi LoRA adapter (73.9 MB fp32 mỗi round).

Lý do chọn: trên dev, method cao nhất trên Spider trong các cấu hình
federated và giữ được BIRD. Không có replay thì phần BIRD học từ teacher mất
ngay ở round đầu (43.61 xuống 36.77); có replay thì BIRD giữ và tăng (41.92
rồi 44.78).

## 3. Số EX hiện tại (seed 0)

| Arm                                       | Spider dev |  BIRD dev | Spider test |
| ----------------------------------------- | ---------: | --------: | ----------: |
| Base 1.5B (zero-shot)                     |      59.19 |     21.32 |       57.94 |
| Train một mình (trung bình 5 client)      |      65.49 |     22.96 |       67.27 |
| FedAvg                                    |      67.60 |     25.68 |       71.50 |
| FedNTD                                    |      67.79 |     24.32 |       69.68 |
| Server gold CE warm-start + FedAvg        |      70.41 |     40.03 |       73.03 |
| Pipeline giống method nhưng không teacher |      71.57 |     41.26 |       72.61 |
| Server KD warm-start + FedAvg             |      72.53 |     38.53 |       73.50 |
| Cùng các câu replay nhưng train ở server  |      73.21 |     37.81 |       73.87 |
| **Method**                                |  **74.08** | **44.78** |       73.17 |
| Centralized Spider                        |      71.37 |     25.75 |       71.08 |
| Centralized Spider + BIRD (không privacy) |      73.21 |     43.68 |       73.78 |
| Teacher 7B (zero-shot)                    |      76.69 |     47.07 |             |

So sánh paired (exact McNemar):

- **Framework:** method - FedAvg: Spider test +1.68 (p=.029), BIRD dev
  +19.10 (p<.001). Method - centralized Spider: Spider test +2.10 (p=.009).
  Method - centralized Spider + BIRD: Spider test -0.61 (p=.46).
- **Phần teacher**, so với các cấu hình cùng data nhưng không có target
  teacher trong các round:

| Method minus | Spider test | BIRD dev |
|---|---:|---:|
| Pipeline giống method nhưng không teacher | +0.56 (p=.43) | +3.52 (p<.001) |
| Server KD warm-start + FedAvg (không replay) | -0.33 (p=.62) | +6.26 (p<.001) |
| Cùng các câu replay nhưng train ở server | -0.70 (p=.27) | +6.98 (p<.001) |

## 4. Seed 1 (đang chạy)

| Spider test | Seed 0 | Seed 1 |
|---|---:|---:|
| Method | 73.17 | 74.57 |
| Pipeline giống method nhưng không teacher | 72.61 | 73.40 |
| Method - pipeline không teacher (W/L, p) | +0.56 (103/91, .43) | +1.16 (97/72, .065) |

Phần riêng của teacher trên Spider test cùng chiều ở cả hai seed. Các
comparator còn lại của seed 1 đang chạy.

## 5. Robustness theo public pool (SynSQL-2.5M, seed 0)

Cùng method, server đổi public pool từ BIRD sang 3,336 câu SynSQL-2.5M
(cùng số token SQL):

| Tập | Method (SynSQL pool) | FedAvg | Method - FedAvg (W/L, p) | Method (BIRD pool) |
|---|---:|---:|---:|---:|
| Spider dev | 70.70 | 67.60 | +3.09 (67/35, .002) | 74.08 |
| BIRD dev | 29.79 | 25.68 | +4.11 (124/61, <.001) | 44.78 |
| Realistic | 61.22 | 59.65 | +1.57 (32/24, .35) | 63.58 |
| SYN | 54.84 | 53.68 | +1.16 (70/58, .33) | 58.70 |
| DK | 54.95 | 53.27 | +1.68 (31/22, .27) | 57.20 |
| Spider test | 72.99 | 71.50 | +1.49 (116/84, .028) | 73.17 |

Method vẫn hơn FedAvg trên mọi tập, significant trên Spider dev, BIRD dev
và Spider test; với SynSQL thấp hơn BIRD pool trên dev nhưng ngang trên
Spider test.

## 6. Các cách đã thử nhưng không hiệu quả

Số là dev, seed 0, exact McNemar. "Coder-1.5B" là student hiện tại;
"1.5B-Instruct" (Qwen2.5-1.5B-Instruct) và "0.5B" (Qwen2.5-Coder-0.5B) là
student ở giai đoạn trước.

| Hướng | Đã thử | Kết quả chính | Kết luận |
|---|---|---|---|
| **Lịch server và FL** | | | |
| Vị trí stage K | K2AAA, AK2AA, AKAKA cùng budget (0.5B) | Spider 63.93 / 63.15 / 62.57, không cặp nào p<.1; K muộn giữ BIRD hơn | Chọn K2 ở đầu |
| KD xen kẽ các round (AKAKA) | Coder-1.5B, round cuối plain | Teacher - gold Spider +0.39 (p=.76) | Edge của teacher mất ở round cuối; giữ làm baseline FedCoLLM-style |
| Server học lại giữa các round (FSL-style, S>A>S>A) | Coder-1.5B | BIRD lên ở bước server (45.18) rồi mất ở round sau (39.77); so với client replay BIRD -4.95 (p<.001) | Không giữ được BIRD |
| Train thêm các câu replay ở server rồi FedAvg | Coder-1.5B | BIRD 42.96 sau server, 37.87 sau round 1 | Không giữ được BIRD; giữ làm comparator |
| **Thuật toán FL và chống quên** | | | |
| FedNTD (Lee et al., NeurIPS 2022) | Coder-1.5B | Spider test 69.68 so với FedAvg 71.50; BIRD dev -1.37 | Không hơn FedAvg |
| FedProx | 0.5B | Không hơn FedAvg | Bỏ |
| NTD ở round private | 0.5B, Coder-1.5B | Round giữa: không tác dụng; round cuối: đổi Spider lấy BIRD (Spider -2.51, BIRD +3.32 so với round plain) | Bỏ |
| Retention loss ở client (λ=1.0) | 1.5B-Instruct | BIRD +1.9 nhưng các tập Spider -3.4 đến -6.9 | Bỏ |
| Đóng băng LoRA A ở client (FFA-LoRA, Sun et al., ICLR 2024) | Coder-1.5B | Spider -1.55; BIRD vẫn rơi (37.61), khoảng 88% phần quên đi qua LoRA B | Bỏ |
| Merge trọng số không train (WiSE-FT, task arithmetic) | 1.5B-Instruct | Không qua ngưỡng đặt trước | Bỏ |
| **Cách distill ở server** | | | |
| SeqKD (CE trên SQL teacher sinh) | 1.5B-Instruct | Hơn gold ở server, mất gần hết sau round private cuối | Đổi sang Hinton KD |
| KID, GKD (on-policy KD) | 1.5B-Instruct | KID ngang SeqKD, tốn khoảng 21 GPU-h; GKD dừng vì chi phí | Bỏ |
| TAID (Shing et al., ICLR 2025) thay Hinton KD | Coder-1.5B | Spider -1.84 (p=.050), DK -4.11 (p=.001) so với Hinton | Bỏ |
| Plan task, CoT của teacher (Distilling Step-by-Step, Struct-SQL) | 1.5B-Instruct | Plan + gold so với gold: Spider -0.97 (n.s.); plan thay SQL: BIRD -3.91 | Bỏ |
| **Biến thể replay** | | | |
| Replay chỉ với gold, không target teacher | Coder-1.5B | BIRD -4.04 (p<.001) so với replay target teacher | Target teacher là cần |
| Replay chỉ các câu teacher đúng (lọc theo execution) | Coder-1.5B | Spider -1.06 (p=.071), BIRD -0.52 | Giữ replay không lọc |
| **Khác** | | | |
| ICL (hướng FedICL ban đầu) | giai đoạn đầu | Train với demo: -2.90 (p=.008); demo lúc inference: -3.87 (p=.003); tốn 2.35 lần thời gian train | Bỏ, không dùng ICL |

Control đã chạy (không phải method): thay teacher bằng virtual teacher
(Yuan et al., CVPR 2020) hoặc bằng chính base 1.5B. Edge Spider của teacher
ở warm-start không đến từ việc làm mềm label hay kéo model về base (Hinton -
virtual +6.09, Hinton - self +4.26 ở warm-start).

## 7. Vấn đề

1. **Lợi thế trên Spider co lại ở test.** Trên dev method hơn FedAvg +6.48,
   trên test chỉ còn +1.68. Các arm có server warm-start đều nằm trong
   72.6-73.9 trên test, chênh nhau trong mức nhiễu của một seed. Một phần là
   do method được chọn trên chính Spider dev.
2. **Teacher đóng góp nhỏ trên Spider (miền private).** Phần lớn mức tăng
   so với FedAvg đến từ public data ở server (gold warm-start - FedAvg
   +1.54, p=.042). Phần riêng của teacher trên Spider test là +0.56 (seed 0)
   và +1.16 (seed 1, p=.065), cùng chiều nhưng từng seed chưa significant.
   Chỗ trống trên Spider test hẹp: train tập trung Spider + BIRD không
   privacy (73.78) chỉ hơn pipeline FL không teacher (gold warm-start,
   73.03) +0.75 (p=.37), trong khi trên dev khoảng này là +2.80 (p=.016).
3. **Đóng góp rõ của teacher nằm ở BIRD (miền public).** Teacher giữ BIRD hơn
   +3.5 đến +7 điểm ở mọi so sánh (p<.001) mà Spider không giảm. Nhưng BIRD
   là metric phụ của bài, nên câu chuyện "teacher đóng góp" đang dựa vào
   metric phụ.
4. **Setting phụ chưa làm rõ thêm phần của teacher.** Với SynSQL, phần
   riêng của teacher cùng chiều trên 5/5 tập dev nhưng nhỏ (+0.2 đến +1.7),
   chưa significant. Đảo vai (BIRD private, Spider public) thì replay không
   giúp miền private (BIRD -1.69, p=.061), em để ngoài phần xác nhận.

## 8. Kế hoạch

1. Hết seed 1 và seed 2 cho method và các comparator; FedCoLLM-style ở cả 3
   seed; FedAvg và gold warm-start ở seed 1-2; teacher zero-shot trên Spider
   test (khoảng 2 ngày GPU).
2. Kiểm định gộp 3 seed (question-clustered test).
3. Student 0.5B, 3 seed: method, pipeline không teacher, server KD +
   FedAvg, FedAvg (thêm khoảng 2 ngày GPU).
4. Viết bản thảo song song.

## 9. Em xin ý kiến thầy

1. Với kết quả như trên, câu chuyện "framework hơn FedAvg, teacher giữ kiến
   thức public domain qua các round FL mà không giảm miền private" có đủ cho
   một journal Q3 không?
2. Hay em nên tìm một setting mà teacher giúp rõ hơn trên miền private trước
   khi viết?
