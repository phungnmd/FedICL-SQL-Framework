# FedLS-SQL: báo cáo tiến độ (29/10/2026)

Em xin gửi thầy tình hình research hiện tại của dự án.

## 1. Method hiện tại

Sau nhiều cấu hình federated đã thử với student Qwen2.5-Coder-1.5B (mục 5),
em chọn `method` (`mixkd50_k2aaa`):

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
| `teacher_7b`                  |          76.69 |        47.07 |             |     *71.06* | *63.83* | *62.43* |

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
| `method`            |    1 |                |              |       74.57 |             |         |         |
| `method_no_teacher` |    0 |          71.57 |        41.26 |       72.61 |     *62.01* | *55.13* | *53.83* |
| `method_no_teacher` |    1 |           71.5 |         42.0 |       73.40 |      *60.6* |  *59.0* |  *55.5* |

Nhận xét:

- `method_no_teacher` ở seed 1 gần như seed 0 trên mọi tập (Spider dev 71.5
  so với 71.57, BIRD dev 42.0 so với 41.26).
- `method` seed 1 đạt 74.57 trên Spider test, cao nhất trong mọi run đến
  nay, hơn `method_no_teacher` 1.2 điểm (seed 0: 0.6 điểm). Phần của
  teacher trên Spider test dương ở cả hai seed, seed 1 lớn hơn.
- Đang chạy ở seed 1: `method_no_replay`, `method_replay_at_server`, FedCoLLM-style.

## 4. Robustness theo public pool (SynSQL-2.5M, seed 0)

Cùng recipe, server đổi public pool từ BIRD sang 3,336 câu SynSQL-2.5M (cùng
số token SQL với BIRD pool). Ở setting này server không dùng BIRD, nên BIRD
dev là miền chưa thấy khi train.

| Arm                 | **Spider dev** | **BIRD dev** | Spider test | *Realistic* |   *SYN* |    *DK* |
| ------------------- | -------------: | -----------: | ----------: | ----------: | ------: | ------: |
| `FedAvg`            |          67.60 |        25.68 |       71.50 |     *59.65* | *53.68* | *53.27* |
| `method_no_teacher` |          69.92 |        28.81 |             |     *61.02* | *53.09* | *54.58* |
| **`method`**        |      **70.70** |    **29.79** |       72.99 |     *61.22* | *54.84* | *54.95* |

Nhận xét: `method` vẫn hiệu quả khi đổi public pool. Nó hơn `FedAvg` trên
mọi tập, rõ nhất ở Spider dev (3.1 điểm), BIRD dev (4.1 điểm) và Spider
test (1.5 điểm), và hơn `method_no_teacher` trên cả 5 tập dev (0.2 đến 1.7
điểm).

## 5. Các cách đã thử nhưng không hiệu quả

Số là dev, seed 0; Spider là Spider dev nếu không ghi test.

| Hướng                                                                                                                                    | Đã thử                                 | Kết quả chính                                                                                                                                                                                               | Kết luận                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Lịch server và FL**                                                                                                                    |                                        |                                                                                                                                                                                                             |                                                                    |
| Vị trí stage K                                                                                                                           | K2AAA, AK2AA, AKAKA cùng budget (0.5B) | Spider 63.93 / 63.15 / 62.57: K muộn không tăng Spider; BIRD 27.71 / 27.77 / 28.88                                                                                                                          | Chọn K2 ở đầu                                                      |
| KD xen kẽ các round (AKAKA)<br>(FedCoLLM, Fan et al., arXiv 2024)                                                                        | Coder-1.5B, round cuối plain           | Spider 71.76, thấp hơn K2 ở đầu cùng budget (72.53); teacher - gold Spider +0.39, BIRD -0.39                                                                                                                | Edge của teacher mất ở round cuối; giữ làm baseline FedCoLLM-style |
| Server học lại giữa các round (S>A>S>A)<br>(FSL, Mai et al., IEEE TAI 2024)                                                              | Coder-1.5B                             | Spider 73.21, không khác `method_no_replay` (+0.68) và client replay (-0.77); mỗi bước server giảm Spider 3.8-6.0 điểm; BIRD lên 45.18 ở bước server rồi còn 39.77 sau round tiếp, thua client replay -4.95 | Spider không hơn, không giữ được BIRD                              |
| Train thêm các câu replay ở server rồi FedAvg (`method_replay_at_server`)                                                                | Coder-1.5B                             | Spider 73.21, không khác `method_no_replay` (+0.68) và `method` (-0.87); BIRD 42.96 sau server, 37.81 sau round 3 (`method` 44.78)                                                                          | Spider không hơn, không giữ được BIRD; giữ làm comparator          |
| **Thuật toán FL và chống quên**                                                                                                          |                                        |                                                                                                                                                                                                             |                                                                    |
| FedNTD<br>(Lee et al., NeurIPS 2022)                                                                                                     | Coder-1.5B                             | So với FedAvg: Spider +0.19, Spider test 69.68 so với 71.50 (-1.82); BIRD -1.37                                                                                                                             | Không hơn FedAvg                                                   |
| FedProx<br>(Li et al., MLSys 2020)                                                                                                       | 0.5B, μ=0.01                           | So với FedAvg: Spider -1.45, BIRD -0.65                                                                                                                                                                     | Bỏ                                                                 |
| NTD ở round private<br>(Lee et al., NeurIPS 2022)                                                                                        | 0.5B, Coder-1.5B                       | 0.5B: Spider không đổi (+0.48 gộp 2 seed), BIRD +1.89; NTD ở round giữa không đổi kết quả. Coder-1.5B, round cuối: Spider -2.51, BIRD +3.32 so với round plain                                              | Bỏ: ở Coder-1.5B đổi Spider lấy BIRD                               |
| Retention loss ở client (λ=1.0)<br>(LwF, Li & Hoiem, ECCV 2016; FedGKD, Yao et al., IEEE TPDS 2023)                                      | 1.5B-Instruct                          | Spider -3.38 so với round plain, các biến thể Spider giảm tới -6.9; BIRD +1.9                                                                                                                               | Bỏ                                                                 |
| Đóng băng LoRA A ở client<br>(FFA-LoRA, Sun et al., ICLR 2024)                                                                           | Coder-1.5B, 1 round                    | Spider -1.55; BIRD vẫn rơi (37.61, so với 36.77 khi train cả A), khoảng 88% phần quên đi qua LoRA B                                                                                                         | Bỏ                                                                 |
| Merge trọng số không train<br>(WiSE-FT, Wortsman et al., CVPR 2022; task arithmetic, Ilharco et al., ICLR 2023)                          | 1.5B-Instruct                          | Mọi merge làm Spider thấp hơn bản không merge 1.1 đến 10.0 điểm; BIRD tăng tới +6.0                                                                                                                         | Bỏ                                                                 |
| **Cách distill ở server**                                                                                                                |                                        |                                                                                                                                                                                                             |                                                                    |
| SeqKD (CE trên SQL teacher sinh)<br>(Kim & Rush, EMNLP 2016)                                                                             | 1.5B-Instruct                          | So với gold trên cùng 5,319 câu: Spider +1.64 ngay sau server, còn -0.10 sau round private; BIRD +3.00 rồi +0.91                                                                                            | Spider không hơn gold; đổi sang Hinton KD                          |
| KID, GKD<br>(KID, Zhong et al., Findings EMNLP 2024; GKD, Agarwal et al., ICLR 2024)                                                     | 1.5B-Instruct                          | KID so với SeqKD sau round private: Spider 65.47 so với 64.99 (không khác), BIRD 28.94 so với 28.42; tốn khoảng 21 GPU-h. GKD dừng vì chi phí, chưa có số                                                   | Bỏ                                                                 |
| TAID thay Hinton KD<br>(Shing et al., ICLR 2025)                                                                                         | Coder-1.5B                             | So với Hinton: Spider -1.84, DK -4.11, BIRD +1.04                                                                                                                                                           | Bỏ                                                                 |
| Plan task, CoT của teacher<br>(Distilling Step-by-Step, Hsieh et al., Findings ACL 2023; Struct-SQL, Thaker & Bresler, Canadian AI 2026) | 1.5B-Instruct                          | Plan + gold so với gold: Spider -0.97, BIRD +1.24; plan thay SQL: Spider -0.97, BIRD -3.91                                                                                                                  | Bỏ                                                                 |
| **Biến thể replay**                                                                                                                      |                                        |                                                                                                                                                                                                             |                                                                    |
| Replay chỉ với gold, không target teacher<br>(ER, so với DER của Buzzega et al., NeurIPS 2020)                                           | Coder-1.5B                             | So với replay target teacher: Spider -0.87, BIRD -4.04                                                                                                                                                      | Target teacher là cần                                              |
| Replay chỉ các câu teacher đúng (lọc theo execution)<br>(Struct-SQL, Thaker & Bresler, Canadian AI 2026)                                 | Coder-1.5B                             | So với replay không lọc: Spider -1.06, BIRD -0.52                                                                                                                                                           | Giữ replay không lọc                                               |
| **Khác**                                                                                                                                 |                                        |                                                                                                                                                                                                             |                                                                    |
| ICL (hướng FedICL ban đầu)<br>(chọn demo theo DAIL-SQL, Gao et al., VLDB 2024)                                                           | giai đoạn đầu                          | Spider: train với demo -2.90; demo lúc inference -3.87; tốn 2.35 lần thời gian train                                                                                                                        | Bỏ, không dùng ICL                                                 |

Control đã chạy (không phải method): thay teacher bằng virtual teacher
(Yuan et al., CVPR 2020) hoặc bằng chính base 1.5B. Edge Spider của teacher
ở warm-start không đến từ việc làm mềm label hay kéo model về base (Hinton -
virtual +6.09, Hinton - self +4.26 ở warm-start).

## 6. Vấn đề

1. **Lợi thế trên Spider co lại ở test.** Trên dev method hơn FedAvg +6.48,
   trên test chỉ còn +1.68. Các arm có server warm-start đều nằm trong
   72.6-73.9 trên test, chênh nhau trong mức nhiễu của một seed. Một phần là
   do method được chọn trên chính Spider dev.
2. **Teacher đóng góp nhỏ trên Spider (miền private).** Phần lớn mức tăng
   so với FedAvg đến từ public data ở server (`method_no_teacher_no_replay` - FedAvg
   +1.54, p=.042). Phần riêng của teacher trên Spider test là +0.56 (seed 0)
   và +1.16 (seed 1, p=.065), cùng chiều nhưng từng seed chưa significant.
   Chỗ trống trên Spider test hẹp: `central_spider_bird` (73.78) chỉ hơn
   `method_no_teacher_no_replay` (73.03) +0.75 (p=.37), trong khi trên dev khoảng này là
   +2.80 (p=.016).
3. **Đóng góp rõ của teacher nằm ở BIRD (miền public).** Teacher giữ BIRD hơn
   +3.5 đến +7 điểm ở mọi so sánh (p<.001) mà Spider không giảm. Nhưng BIRD
   là metric phụ của bài, nên câu chuyện "teacher đóng góp" đang dựa vào
   metric phụ.
4. **Setting phụ chưa làm rõ thêm phần của teacher.** Với SynSQL, phần
   riêng của teacher cùng chiều trên 5/5 tập dev nhưng nhỏ (+0.2 đến +1.7),
   chưa significant. Đảo vai (BIRD private, Spider public) thì replay không
   giúp miền private (BIRD -1.69, p=.061), em để ngoài phần xác nhận.

## 7. Kế hoạch

1. Hết seed 1 và seed 2 cho method và các comparator; FedCoLLM-style ở cả 3
   seed; `FedAvg` và `method_no_teacher_no_replay` ở seed 1-2; `teacher_7b` trên Spider
   test (khoảng 2 ngày GPU).
2. Kiểm định gộp 3 seed (question-clustered test).
3. Student 0.5B, 3 seed: `method`, `method_no_teacher`, `method_no_replay`,
   `FedAvg` (thêm khoảng 2 ngày GPU).
4. Viết bản thảo song song.

## 8. Em xin ý kiến thầy

1. Với kết quả như trên, câu chuyện "framework hơn FedAvg, teacher giữ kiến
   thức public domain qua các round FL mà không giảm miền private" có đủ cho
   một journal Q3 không?
2. Hay em nên tìm một setting mà teacher giúp rõ hơn trên miền private trước
   khi viết?
