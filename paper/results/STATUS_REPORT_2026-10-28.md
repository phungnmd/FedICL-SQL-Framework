# FedLS-SQL: tình hình paper (2026-10-29)

Mục tiêu: paper ứng dụng, journal Q3 (Data & Knowledge Engineering,
International Journal of Data Science and Analytics, Neural Processing
Letters). Working title: *Keeping the Teacher's Knowledge: Server-Side LLM
Distillation with Client-Side Logit Replay for Federated Text-to-SQL*.

## 1. Bài toán

- 5 client giữ dữ liệu Text-to-SQL private (Spider, split Dirichlet theo
  domain, alpha 0.1). Server giữ teacher Qwen2.5-Coder-7B frozen và public
  data khác miền (BIRD, 9,428 câu, có evidence).
- Cùng train một student Qwen2.5-Coder-1.5B + LoRA r16 bằng FedAvg. Chỉ
  deploy student; teacher không bao giờ chạy ở client.
- Metric chính: Spider EX (miền private). BIRD EX là metric phụ, chỉ tính khi
  Spider không giảm.

## 2. Method (`mixkd50_k2aaa`)

1. **Server warm-start (K2):** student học BIRD 2 epoch với 0.5 gold CE +
   0.5 KL tới teacher (Hinton KD, T=2).
2. **3 round FedAvg trên Spider, có client replay:** mỗi round, client trộn
   thêm câu BIRD (20% số câu private, lấy từ subset cố định 2,000 câu) với
   0.5 gold CE + 0.5 KL tới top-50 token của teacher. Server gửi target này
   một lần (khoảng 33 MB mỗi client).

Communication: adapter 73.9 MB (fp32) mỗi client mỗi chiều mỗi round.

## 3. Câu chuyện

1. Public data ở server giúp FL rõ rệt so với FedAvg thuần.
2. Teacher distill ở server, nhưng phần lợi ích trên public domain bị quên
   trong các round FedAvg.
3. Client replay target của teacher giữ lại phần đó, Spider không giảm.
4. Teacher đóng góp đo được trên BIRD; trên Spider phần của teacher nhỏ.

## 4. Kết quả chính (seed 0)

**Spider test (2,147 câu, tập xác nhận):**

| Arm | Spider dev | Spider test | Method minus (test) | p |
|---|---:|---:|---:|---:|
| FedAvg | 67.60 | 71.50 | +1.68 | .029 |
| FedNTD | 67.79 | 69.68 | +3.49 | <.001 |
| Server gold CE warm-start + FedAvg | 70.41 | 73.03 | +0.14 | .89 |
| Matched pipeline không teacher (gold warm-start, gold replay) | 71.57 | 72.61 | +0.56 | .43 |
| Server KD warm-start + FedAvg | 72.53 | 73.50 | -0.33 | .62 |
| Cùng các câu replay nhưng train ở server | 73.21 | 73.87 | -0.70 | .27 |
| **Method** | **74.08** | 73.17 | | |
| *Tham chiếu* | | | | |
| Base (zero-shot) | 59.19 | 57.94 | +15.23 | <.001 |
| Train một mình, client tốt nhất trên test (trung bình 5 client) | 64.60 (65.49) | 70.28 (67.27) | +2.89 | <.001 |
| Centralized Spider | 71.37 | 71.08 | +2.10 | .009 |
| Centralized Spider + BIRD (không privacy) | 73.21 | 73.78 | -0.61 | .46 |

Exact McNemar trên cùng câu hỏi. Từ dev sang test, FedAvg tăng 3.90; các
arm có warm-start tăng 0.66-2.62; method giảm 0.91 (method được chọn trong
17 cấu hình trên dev). Method ngang train tập trung Spider + BIRD không
privacy và hơn train tập trung chỉ Spider. Khoảng cách FL so với
centralized trên dev (+3.77) không thấy trên test (-0.42, p=.66).

**Seed 1 (đang chạy, chưa publish):**

| Spider test | Seed 0 | Seed 1 |
|---|---:|---:|
| Method | 73.17 | 74.57 |
| Pipeline giống method nhưng không teacher | 72.61 | 73.40 |
| Method - pipeline không teacher (W/L, p) | +0.56 (103/91, .43) | +1.16 (97/72, .065) |

Pipeline không teacher seed 1 trên dev: Spider 71.5, BIRD 42.0, Realistic
60.6, SYN 59.0, DK 55.5 (seed 0: 71.57, 41.26, 62.01, 55.13, 53.83).

**Development sets (Spider dev / BIRD dev):**

| Arm | Spider | BIRD |
|---|---:|---:|
| Base (zero-shot) | 59.19 | 21.32 |
| Client tốt nhất train một mình | 67.02 | 23.99 |
| FedAvg | 67.60 | 25.68 |
| Server gold CE warm-start + FedAvg | 70.41 | 40.03 |
| Matched pipeline không teacher | 71.57 | 41.26 |
| Server KD warm-start + FedAvg | 72.53 | 38.53 |
| Replay chỉ với gold CE | 73.21 | 40.74 |
| Cùng các câu replay nhưng train ở server | 73.21 | 37.81 |
| **Method** | **74.08** | **44.78** |
| *Tham chiếu không federated* | | |
| Centralized Spider | 71.37 | 25.75 |
| Centralized Spider + BIRD (không privacy) | 73.21 | 43.68 |
| Teacher 7B zero-shot | 76.69 | 47.07 |

**Forgetting qua các round (Spider dev / BIRD dev):**

| Arm | Warm-start | Round 1 | Round 2 | Round 3 |
|---|---:|---:|---:|---:|
| Server KD warm-start + FedAvg | 62.28 / 43.61 | 71.57 / 36.77 | 71.86 / 38.66 | 72.53 / 38.53 |
| Cùng các câu replay nhưng train ở server | 61.99 / 42.96 | 71.28 / 37.87 | 72.63 / 38.66 | 73.21 / 37.81 |
| Method | 62.28 / 43.61 | 69.73 / 41.92 | 72.82 / 43.74 | 74.08 / 44.78 |

**Đóng góp của teacher (method minus comparator, BIRD dev, p):** so với
matched pipeline không teacher +3.52 (<.001); so với replay gold +4.04
(<.001); so với server KD warm-start + FedAvg +6.26 (<.001); so với train
cùng câu ở server +6.98 (<.001).

## 5. Claim đã chốt và trạng thái hiện tại

Kiểm trên 3 seed gộp (question-clustered test), Spider test là metric chính;
non-inferiority margin 2.0 điểm.

| Claim | Nội dung | Seed 0 | Seed 1 |
|---|---|---|---|
| C1 | Method > matched pipeline không teacher, Spider test | +0.56 (p=.43) | +1.16 (p=.065) |
| C2 | Method > matched pipeline, BIRD, Spider không kém | BIRD +3.52, Spider test +0.56 | Spider test +1.16; BIRD chờ publish |
| C3 | Method > server KD warm-start + FedAvg, BIRD, Spider không kém | BIRD +6.26, Spider test -0.33 | đang chạy |
| C4 | Method > train cùng câu ở server, BIRD, Spider không kém | BIRD +6.98, Spider test -0.70 | đang chạy |
| C5 | Method so với FedCoLLM-style | chưa chạy (bước 5) | đang chạy |
| C6 | Server KD > server gold CE warm-start, Spider test | +0.47 (chưa test paired) | chờ 6b |
| C7 | Method > FedAvg, Spider test | +1.68 (p=.029) | chờ 6b |

## 6. Đánh giá hiện tại

- **Vững:** framework hơn FedAvg trên Spider test (+1.68), chủ yếu nhờ
  public data ở server (gold warm-start - FedAvg +1.54, p=.042). Teacher giữ BIRD
  qua các round (+3.5 đến +7, p<.001 ở mọi so sánh). Trên Spider test
  method ngang train tập trung Spider + BIRD không privacy (-0.61, p=.46)
  và hơn train tập trung chỉ Spider (+2.10, p=.009).
- **Yếu nhưng đang lên:** phần riêng của teacher trên Spider test: C1
  +0.56 (seed 0) và +1.16 (seed 1, p=.065), cùng chiều; C6 +0.47 (seed 0).
  Chỗ trống trên Spider test hẹp: `central_mix` - `gold_k2aaa` chỉ +0.75
  (p=.37) trên test, so với +2.80 (p=.016) trên dev.
- **Robustness theo pool:** đổi public pool sang SynSQL, method vẫn hơn
  FedAvg trên 5/5 tập dev (Spider +3.09, p=.002) và trên Spider test
  (+1.49, p=.028).
- **Sát biên:** C4 (Spider test -0.70 so với margin -2.0).

## 7. Setting phụ (seed 0, thăm dò)

- **Đảo vai** (BIRD private, Spider public): replay giữ Spider (+6.29,
  p<.001) nhưng BIRD private -1.69 (p=.061). Không vào confirmation.
- **Robustness theo public pool: SynSQL-2.5M** thay BIRD (3,336 câu, cùng
  số token SQL với BIRD pool, cùng recipe; nested `76496b4`):

| Tập | Method (SynSQL pool) | FedAvg | Method - FedAvg (W/L, p) | Method (BIRD pool) |
|---|---:|---:|---:|---:|
| Spider dev | 70.70 | 67.60 | +3.09 (67/35, .002) | 74.08 |
| BIRD dev | 29.79 | 25.68 | +4.11 (124/61, <.001) | 44.78 |
| Realistic | 61.22 | 59.65 | +1.57 (32/24, .35) | 63.58 |
| SYN | 54.84 | 53.68 | +1.16 (70/58, .33) | 58.70 |
| DK | 54.95 | 53.27 | +1.68 (31/22, .27) | 57.20 |
| Spider test | 72.99 | 71.50 | +1.49 (116/84, .028) | 73.17 |

  Method hơn FedAvg trên mọi tập, significant trên Spider dev, BIRD dev và
  Spider test.
  Thấp hơn BIRD pool trên dev, ngang trên Spider test. Teacher (method -
  matched pipeline) cùng chiều 5/5 tập dev (+0.2 đến +1.7), không có ý
  nghĩa thống kê.

## 8. Đang chạy và tiếp theo

- GPU 0: seed 1, method và pipeline không teacher xong; đang chạy
  `hinton_k2aaa`, rồi `k2plus_aaa` (khoảng 10 h); sau đó seed 2.
- GPU 1: FedCoLLM-style seed 1 (khoảng 12 h); sau đó FedCoLLM-style seed 0
  và seed 2.
- Còn lại: 6b (FedAvg, gold warm-start seed 1-2), 6c (dev ở A1/A2 seed
  1-2), 6d (teacher zero-shot Spider test), rồi kiểm định 3 seed. Khoảng 45
  h mỗi GPU.
- SynSQL seed 0 và các dòng tham chiếu đã publish. Số Spider test seed 0
  của P2.53 và execution-filtered replay còn trên GPU server, chưa
  publish vào repo code.
