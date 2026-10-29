# FedLS-SQL: báo cáo tiến độ (29/10/2026)

Em xin gửi thầy tình hình research hiện tại của dự án.

## 1. Method hiện tại
1. **Server warm-start:** distill teacher Qwen2.5-Coder-7B (frozen) trên BIRD
   public, 0.5 gold CE + 0.5 KL (Hinton KD, T=2), 2 epoch.
2. **3 round FedAvg trên Spider với client replay:** mỗi round, client trộn
   thêm câu BIRD (20% số câu private) với target top-50 token của teacher do
   server gửi một lần (khoảng 33 MB mỗi client). Teacher không chạy ở client;
   client chỉ gửi LoRA adapter (73.9 MB fp32 mỗi round).

Lý do chọn: trên dev, `method` cho EX cao nhất đồng thời trên cả hai miền,
private (Spider) và public (BIRD), trong các cấu hình federated ở bảng dưới.

## 2. Số EX hiện tại (seed 0)

| Arm                           | **Spider dev** | **BIRD dev** | Spider test | *Realistic* |       *SYN* |        *DK* |
| ----------------------------- | -------------: | -----------: | ----------: | ----------: | ----------: | ----------: |
| `base`                        |          59.19 |        21.32 |       57.94 |     *46.26* |     *45.94* |     *47.66* |
| `single_client`               |          65.49 |        22.96 |       67.27 |             |             |             |
| `FedAvg`                      |          67.60 |        25.68 |       71.50 |     *59.65* |     *53.68* |     *53.27* |
| `FedNTD`                      |          67.79 |        24.32 |       69.68 |     *57.09* |     *53.38* |     *51.96* |
| `method_no_teacher_no_replay` |          70.41 |        40.03 |       73.03 |     *61.22* |     *56.38* |     *52.34* |
| `method_no_teacher`           |          71.57 |        41.26 |       72.61 |     *62.01* |     *55.13* |     *53.83* |
| `method_no_replay`            |          72.53 |        38.53 |       73.50 |     *61.81* |     *56.38* | ***58.32*** |
| `method_replay_at_server`     |          73.21 |        37.81 |   **73.87** |     *62.01* | ***58.80*** |     *57.57* |
| **`method`**                  |      **74.08** |    **44.78** |       73.17 | ***63.58*** |     *58.70* |     *57.20* |
| *Tham chiếu không federated*  |                |              |             |             |             |             |
| `central_spider`              |          71.37 |        25.75 |       71.08 |     *61.61* |     *56.00* |     *58.50* |
| `central_spider_bird`         |          73.21 |        43.68 |       73.78 |     *62.99* |     *58.90* |     *58.69* |
| `teacher_7b`                  |      **76.69** |    **47.07** |   **77.22** | ***71.06*** | ***63.83*** | ***62.43*** |

BIRD dev qua các round:

| Arm                       | Sau warm-start | Round 1 | Round 2 | Round 3 |
| ------------------------- | -------------: | ------: | ------: | ------: |
| `method_no_replay`        |          43.61 |   36.77 |   38.66 |   38.53 |
| `method_replay_at_server` |          42.96 |   37.87 |   38.66 |   37.81 |
| `method`                  |          43.61 |   41.92 |   43.74 |   44.78 |

Nhận xét:

- **Framework** (`method` so với `FedAvg`): `method` cao nhất trên Spider
  dev và BIRD dev trong các cấu hình federated, hơn `FedAvg` trên cả 6 tập
  (khoảng 6.5 điểm Spider dev, 19 điểm BIRD dev, 1.7 điểm Spider test). So
  với `central_spider_bird` (train gộp dữ liệu, không có privacy), `method`
  nhỉnh hơn trên Spider dev và BIRD dev, ngang trên Spider test.
- **Teacher** (`method` - `method_no_teacher`): dương trên cả 6 tập, khoảng
  2.5 điểm Spider dev và 3.5 điểm BIRD dev, nhỏ hơn trên Spider test
  (khoảng 0.6 điểm).
- **Replay** (`method` so với `method_no_replay` và
  `method_replay_at_server`): không replay, BIRD giảm 5-7 điểm ngay round
  đầu và ở mức đó đến round 3. Có replay target của teacher, `method` giữ
  và còn tăng BIRD, hơn hai arm này khoảng 6-7 điểm BIRD dev; Spider dev
  cũng cao hơn (khoảng 1-1.5 điểm), Spider test ngang.

## 3. Seed 1

| Arm                       | **Spider dev** | **BIRD dev** | Spider test | *Realistic* |       *SYN* |        *DK* |
| ------------------------- | -------------: | -----------: | ----------: | ----------: | ----------: | ----------: |
| `method_no_teacher`       |          71.47 |        42.05 |       73.40 |     *60.63* |     *58.99* |     *55.51* |
| `method_no_replay`        |          72.82 |        36.77 |       74.10 |     *61.81* |     *58.12* | ***58.13*** |
| `method_replay_at_server` |          72.05 |        36.77 |       73.40 | ***63.19*** |     *57.16* |     *56.64* |
| **`method`**              |      **73.21** |    **43.68** |   **74.57** |     *62.99* | ***60.06*** |     *57.38* |

`method` trừ từng arm, seed 0 và seed 1:

| Method vs                 | Seed | Spider test | Spider dev | BIRD dev |
| ------------------------- | ---: | ----------: | ---------: | -------: |
| `method_no_teacher`       |    0 |       +0.56 |      +2.51 |    +3.52 |
| `method_no_teacher`       |    1 |       +1.16 |      +1.74 |    +1.63 |
| `method_no_replay`        |    0 |       -0.33 |      +1.55 |    +6.26 |
| `method_no_replay`        |    1 |       +0.47 |      +0.39 |    +6.91 |
| `method_replay_at_server` |    0 |       -0.70 |      +0.87 |    +6.97 |
| `method_replay_at_server` |    1 |       +1.16 |      +1.16 |    +6.91 |

Nhận xét:

- **Teacher** (`method` - `method_no_teacher`): dương trên cả 6 tập ở cả
  hai seed, nhưng trên Spider test chưa thể hiện rõ.
- **Replay** (`method` so với `method_no_replay` và
  `method_replay_at_server`): BIRD dev hơn khoảng 7 điểm ở cả hai seed.
  Trên Spider dev `method` cũng hơn cả hai ở cả hai seed, còn trên Spider
  test thì lúc thấp hơn, lúc cao hơn một chút, tức là không giảm.
- Ở seed 1, `method` cao nhất trên Spider test (74.57, cao nhất trong các
  student đến nay), Spider dev và BIRD dev.

## 4. Đổi public dataset sang SynSQL-2.5M (seed 0)

Cùng recipe, server đổi public dataset từ BIRD sang 3,336 câu SynSQL-2.5M.

| Arm                 | **Spider dev** | **BIRD dev** | Spider test | *Realistic* |   *SYN* |    *DK* |
| ------------------- | -------------: | -----------: | ----------: | ----------: | ------: | ------: |
| `FedAvg`            |          67.60 |        25.68 |       71.50 |     *59.65* | *53.68* | *53.27* |
| `method_no_teacher` |          69.92 |        28.81 |       72.05 |     *61.02* | *53.09* | *54.58* |
| **`method`**        |      **70.70** |    **29.79** |       72.99 |     *61.22* | *54.84* | *54.95* |

Nhận xét: `method` vẫn hiệu quả khi đổi public dataset. Nó hơn `FedAvg` trên
mọi tập (Spider test khoảng 1.5 điểm) và hơn `method_no_teacher` trên cả 6
tập, nhưng phần hơn `method_no_teacher` nhỏ.

## 5. Thảo luận

1. **Spider test tăng ít hơn Spider dev.** `method` hơn `FedAvg` khoảng 6.5
   điểm trên Spider dev nhưng 1.7 điểm trên Spider test. Trên test, `FedAvg`
   đã ngang `central_spider`, nên FL penalty thấy trên dev (khoảng 3.8 điểm)
   gần như không còn.
2. **Phần teacher trên Spider nhỏ và khó tăng thêm.** So với
   `method_no_teacher`, teacher thêm khoảng 2.5 và 1.7 điểm Spider dev,
   0.6 và 1.2 điểm Spider test (seed 0 và 1). Khoảng trống hẹp: `method`
   đã ngang `central_spider_bird`, còn teacher 7B chỉ hơn bản này khoảng
   3.5 điểm. Client đã có đủ gold Spider, còn teacher chỉ truyền qua BIRD,
   nơi target của teacher gần trùng gold (top-1 trùng khoảng 95% token).
3. **Đóng góp rõ nhất của teacher nằm ở BIRD, metric phụ.** Replay target
   của teacher giữ BIRD hơn khoảng 6-7 điểm so với không replay ở cả hai
   seed, nhưng chỉ hơn replay gold (`method_no_teacher`) 3.5 rồi 1.6 điểm.
   Reviewer có thể hỏi phần lợi đến từ target của teacher hay chỉ từ việc
   replay public data.
4. **Đổi public dataset sang SynSQL không làm phần teacher lớn hơn:** vẫn
   cùng chiều trên cả 6 tập nhưng nhỏ, dưới 1 điểm trên Spider dev và
   Spider test.

## 6. Kế hoạch

1. Seed 2 cho method và các comparator; FedCoLLM-style ở cả 3 seed;
   `FedAvg` và `method_no_teacher_no_replay` ở seed 1-2 (khoảng 2 ngày GPU).
2. Kiểm định gộp 3 seed (question-clustered test).
3. Student 0.5B, 3 seed: `method`, `method_no_teacher`, `method_no_replay`,
   `FedAvg` (thêm khoảng 2 ngày GPU).
4. Viết bản thảo song song.

## 7. Em xin ý kiến thầy

1. Em nhờ thầy review giúp: với kết quả hiện tại, method đã đủ mạnh để chốt
   và viết bài theo hướng thầy đã góp ý chưa?
2. Phần đóng góp của teacher chưa cao, nhất là trên Spider. Em nên tiếp tục
   research để tăng khả năng của method, hay bắt đầu viết bài?
