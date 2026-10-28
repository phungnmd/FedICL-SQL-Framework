# FedLS-SQL: báo cáo tiến độ (29/10/2026)

Em xin gửi thầy tình hình research hiện tại của dự án
## Method hiện tại

Sau nhiều cấu hình federated đã thử với student Qwen2.5-Coder-1.5B, em chọn
`mixkd50_k2aaa`:

1. **Server warm-start:** distill teacher Qwen2.5-Coder-7B (frozen) trên BIRD
   public, 0.5 gold CE + 0.5 KL (Hinton KD, T=2), 2 epoch.
2. **3 round FedAvg trên Spider với client replay:** mỗi round, client trộn
   thêm câu BIRD (20% số câu private) với target top-50 token của teacher do
   server gửi một lần (khoảng 33 MB mỗi client). Teacher không chạy ở client.

Lý do chọn: trên dev, method cao nhất trên Spider trong các cấu hình
federated và ngang train tập trung Spider + BIRD (không privacy), đồng thời
giữ được BIRD. Không có replay thì phần BIRD học từ teacher mất ngay ở round
đầu (43.61 xuống 36.77); có replay thì BIRD giữ và tăng (41.92 rồi 44.78).

## Số EX hiện tại (seed 0)

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

- Method - FedAvg: Spider test +1.68 (p=.029), BIRD dev +19.10 (p<.001).
- Method - pipeline không teacher: Spider test +0.56 (p=.43), BIRD dev
  +3.52 (p<.001).
- Method - server KD warm-start + FedAvg: Spider test -0.33 (p=.62), BIRD
  dev +6.26 (p<.001).
- Method - centralized Spider: Spider test +2.10 (p=.009).
- Method - centralized Spider + BIRD (không privacy): Spider test -0.61
  (p=.46).

## Seed 1 (đang chạy)

| Spider test | Seed 0 | Seed 1 |
|---|---:|---:|
| Method | 73.17 | 74.57 |
| Pipeline giống method nhưng không teacher | 72.61 | 73.40 |
| Method - pipeline không teacher (W/L, p) | +0.56 (103/91, .43) | +1.16 (97/72, .065) |

Phần riêng của teacher trên Spider test cùng chiều ở cả hai seed. Các
comparator còn lại của seed 1 đang chạy.

## Robustness theo public pool (SynSQL-2.5M, seed 0)

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

Method vẫn hơn FedAvg trên mọi tập, significant trên Spider dev, BIRD
dev và Spider test; với SynSQL thấp hơn BIRD pool trên dev nhưng ngang trên Spider test.

## Vấn đề

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

## Đang chạy

Xác nhận trên 3 seed với Spider test. Seed 1: method và pipeline không
teacher đã xong; server KD warm-start + FedAvg, train ở server và
FedCoLLM-style đang chạy. Sau đó: seed 2, FedAvg và gold warm-start ở seed
1-2, teacher zero-shot trên Spider test; khoảng 2 ngày GPU. Paper sẽ chỉ
lấy claim từ kết quả 3 seed này.

## Em xin ý kiến thầy

1. Với kết quả như trên, câu chuyện "framework hơn FedAvg, teacher giữ kiến
   thức public domain qua các round FL mà không giảm miền private" có đủ cho
   một journal Q3 không?
2. Hay em nên tìm một setting mà teacher giúp rõ hơn trên miền private trước
   khi viết?
