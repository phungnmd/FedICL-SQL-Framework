# FedLS-SQL: báo cáo tiến độ (29/10/2026)

Em xin gửi thầy tình hình research hiện tại của dự án.

## 1. Method hiện tại

Sau nhiều cấu hình federated đã thử với student Qwen2.5-Coder-1.5B (file
"Các phương pháp đã thực nghiệm" gửi kèm), em chọn `method` (`mixkd50_k2aaa`):

1. **Server warm-start:** distill teacher Qwen2.5-Coder-7B (frozen) trên BIRD
   public, 0.5 gold CE + 0.5 KL (Hinton KD, T=2), 2 epoch.
2. **3 round FedAvg trên Spider với client replay:** mỗi round, client trộn
   thêm câu BIRD (20% số câu private) với target top-50 token của teacher do
   server gửi một lần (khoảng 33 MB mỗi client). Teacher không chạy ở client;
   client chỉ gửi LoRA adapter (73.9 MB fp32 mỗi round).

Lý do chọn: trên dev, `method` cho EX cao nhất đồng thời trên cả hai miền,
private (Spider) và public (BIRD), trong các cấu hình federated ở bảng dưới.

## 2. Số EX hiện tại (seed 0)

| Arm                           | **Spider dev** | **BIRD dev** | Spider test | *Realistic* |   *SYN* |    *DK* |
| ----------------------------- | -------------: | -----------: | ----------: | ----------: | ------: | ------: |
| `base`                        |          59.19 |        21.32 |       57.94 |     *46.26* | *45.94* | *47.66* |
| `single_client`               |          65.49 |        22.96 |       67.27 |             |         |         |
| `FedAvg`                      |          67.60 |        25.68 |       71.50 |     *59.65* | *53.68* | *53.27* |
| `FedNTD`                      |          67.79 |        24.32 |       69.68 |     *57.09* | *53.38* | *51.96* |
| `method_no_teacher_no_replay` |          70.41 |        40.03 |       73.03 |     *61.22* | *56.38* | *52.34* |
| `method_no_teacher`           |          71.57 |        41.26 |       72.61 |     *62.01* | *55.13* | *53.83* |
| `method_no_replay`            |          72.53 |        38.53 |       73.50 |     *61.81* | *56.38* | *58.32* |
| `method_replay_at_server`     |          73.21 |        37.81 |       73.87 |     *62.01* | *58.80* | *57.57* |
| **`method`**                  |      **74.08** |    **44.78** |       73.17 |     *63.58* | *58.70* | *57.20* |
| *Tham chiếu không federated*  |                |              |             |             |         |         |
| `central_spider`              |          71.37 |        25.75 |       71.08 |     *61.61* | *56.00* | *58.50* |
| `central_spider_bird`         |          73.21 |        43.68 |       73.78 |     *62.99* | *58.90* | *58.69* |
| `teacher_7b`                  |          76.69 |        47.07 |       77.22 |     *71.06* | *63.83* | *62.43* |

BIRD dev qua các round:

| Arm                       | Sau warm-start | Round 1 | Round 2 | Round 3 |
| ------------------------- | -------------: | ------: | ------: | ------: |
| `method_no_replay`        |          43.61 |   36.77 |   38.66 |   38.53 |
| `method_replay_at_server` |          42.96 |   37.87 |   38.66 |   37.81 |
| `method`                  |          43.61 |   41.92 |   43.74 |   44.78 |

Nhận xét:

- **Framework:** `method` cao nhất trên Spider dev và BIRD dev trong các cấu
  hình federated, hơn `FedAvg` 6.5 điểm Spider dev và 19.1 điểm BIRD dev.
  Trên Spider test, `method` hơn `FedAvg` 1.7 điểm và `central_spider` 2.1
  điểm, gần `central_spider_bird` (73.78) dù không gộp dữ liệu.
- **Teacher:** kiến thức BIRD học từ teacher ở warm-start mất ngay ở round
  đầu nếu không replay (43.61 xuống 36.77). Có replay target của teacher,
  `method` giữ và tăng BIRD (44.78), cao hơn các arm cùng data nhưng không
  giữ target teacher qua các round (`method_no_teacher`, `method_no_replay`,
  `method_replay_at_server`: 37.8-41.3). Spider không giảm: mọi arm có server
  warm-start nằm trong 72.6-73.9 trên Spider test.

## 3. Seed 1 (đang chạy)

| Arm                 | Seed | **Spider dev** | **BIRD dev** | Spider test | *Realistic* |   *SYN* |    *DK* |
| ------------------- | ---: | -------------: | -----------: | ----------: | ----------: | ------: | ------: |
| `method`            |    0 |          74.08 |        44.78 |       73.17 |     *63.58* | *58.70* | *57.20* |
| `method`            |    1 |          73.21 |        43.68 |       74.57 |     *62.99* | *60.06* | *57.38* |
| `method_no_teacher` |    0 |          71.57 |        41.26 |       72.61 |     *62.01* | *55.13* | *53.83* |
| `method_no_teacher` |    1 |          71.47 |        42.05 |       73.40 |     *60.63* | *58.99* | *55.51* |
| `method_no_replay`  |    0 |          72.53 |        38.53 |       73.50 |     *61.81* | *56.38* | *58.32* |
| `method_no_replay`  |    1 |          72.82 |        36.77 |       74.10 |     *61.81* | *58.12* | *58.13* |

`method` trừ từng arm:

| Method trừ          | Seed | Spider test | Spider dev | BIRD dev |
| ------------------- | ---: | ----------: | ---------: | -------: |
| `method_no_teacher` |    0 |       +0.56 |      +2.51 |    +3.52 |
| `method_no_teacher` |    1 |       +1.16 |      +1.74 |    +1.63 |
| `method_no_replay`  |    0 |       -0.33 |      +1.55 |    +6.26 |
| `method_no_replay`  |    1 |       +0.47 |      +0.39 |    +6.91 |

Nhận xét:

- **Teacher** (`method` - `method_no_teacher`): dương trên cả 6 tập ở cả
  hai seed. Trên Spider test seed 1 lớn hơn seed 0 (+1.16 so với +0.56).
  Trên BIRD dev seed 1 nhỏ hơn (+1.63 so với +3.52). Từng seed riêng chưa
  significant trên Spider test; kiểm định gộp 3 seed sẽ quyết định.
- **Replay** (`method` - `method_no_replay`): BIRD dev hơn +6.26 và +6.91,
  Spider test không giảm (-0.33 và +0.47).
- `method` seed 1 đạt 74.57 trên Spider test, cao nhất trong mọi run đến
  nay. Spider dev seed 1 thấp hơn seed 0 (73.21 so với 74.08); method được
  chọn trên Spider dev của seed 0, nên số dev seed 1 là ước lượng không bị
  ảnh hưởng bởi việc chọn.
- Chưa có ở seed 1: `method_replay_at_server` (đang chạy round 1),
  FedCoLLM-style (đang chạy), `FedAvg` và `method_no_teacher_no_replay`
  (chưa chạy).

## 4. Đổi public dataset sang SynSQL-2.5M (seed 0)

Cùng recipe, server đổi public dataset từ BIRD sang 3,336 câu SynSQL-2.5M
(cùng số token SQL với BIRD pool). Ở setting này server không dùng BIRD, nên BIRD
dev là miền chưa thấy khi train.

| Arm                 | **Spider dev** | **BIRD dev** | Spider test | *Realistic* |   *SYN* |    *DK* |
| ------------------- | -------------: | -----------: | ----------: | ----------: | ------: | ------: |
| `FedAvg`            |          67.60 |        25.68 |       71.50 |     *59.65* | *53.68* | *53.27* |
| `method_no_teacher` |          69.92 |        28.81 |             |     *61.02* | *53.09* | *54.58* |
| **`method`**        |      **70.70** |    **29.79** |       72.99 |     *61.22* | *54.84* | *54.95* |

Nhận xét: `method` vẫn hiệu quả khi đổi public dataset. Nó hơn `FedAvg` trên
mọi tập, rõ nhất ở Spider dev (3.1 điểm), BIRD dev (4.1 điểm) và Spider
test (1.5 điểm), và hơn `method_no_teacher` trên cả 5 tập dev (0.2 đến 1.7
điểm).

## 5. Vấn đề

1. **EX trên Spider test (tập eval được public sau) không cao như trên dev,
   dù vẫn dương.** `method` hơn `FedAvg` +6.48 trên Spider dev nhưng chỉ
   +1.68 trên Spider test.
2. **Teacher đóng góp nhỏ trên Spider.** Chỉ cần server train gold trên BIRD
   (`method_no_teacher_no_replay`) đã hơn `FedAvg` +1.54 trên Spider test,
   gần bằng `method` (+1.68). Phần thêm vào khi có teacher (`method` so với
   `method_no_teacher`) là +0.56 ở seed 0 và +1.16 ở seed 1, cùng chiều nhưng
   từng seed chưa significant. Khoảng trống để tăng cũng hẹp: train tập
   trung không privacy trên Spider + BIRD (`central_spider_bird`, 73.78)
   chỉ hơn `method_no_teacher_no_replay` (73.03) 0.75 điểm trên Spider test.
   Trong khi đó teacher zero-shot đạt 77.22 trên Spider test, hơn `method`
   +4.05 (seed 0) và +2.65 (seed 1), hơn cả `central_spider_bird` +3.45:
   trên Spider, teacher vẫn cao hơn mọi student đã train.
3. **Đóng góp rõ của teacher nằm ở BIRD (miền public).** Ở seed 0, teacher
   giữ BIRD hơn +3.5 đến +7 điểm ở mọi so sánh (p<.001) mà Spider không
   giảm. Ở seed 1, phần so với `method_no_replay` vẫn lớn (+6.91, p<.001),
   phần so với `method_no_teacher` nhỏ lại (+1.63, p=.12). BIRD là metric
   phụ của bài, nên câu chuyện "teacher đóng góp" đang dựa vào metric phụ.
4. **Setting đổi public dataset sang SynSQL chưa làm rõ thêm phần của
   teacher.** Phần riêng của teacher cùng chiều trên 5/5 tập dev nhưng nhỏ
   (+0.2 đến +1.7), chưa significant.

## 6. Kế hoạch

1. Hết seed 1 và seed 2 cho method và các comparator; FedCoLLM-style ở cả 3
   seed; `FedAvg` và `method_no_teacher_no_replay` ở seed 1-2 (khoảng 2 ngày
   GPU).
2. Kiểm định gộp 3 seed (question-clustered test).
3. Student 0.5B, 3 seed: `method`, `method_no_teacher`, `method_no_replay`,
   `FedAvg` (thêm khoảng 2 ngày GPU).
4. Viết bản thảo song song.

## 7. Em xin ý kiến thầy

1. Em nhờ thầy review giúp: với kết quả hiện tại, method đã đủ mạnh để chốt
   và viết bài theo hướng thầy đã góp ý chưa?
2. Phần đóng góp của teacher chưa cao, nhất là trên Spider. Em nên tiếp tục
   research để tăng khả năng của method, hay bắt đầu viết bài?
