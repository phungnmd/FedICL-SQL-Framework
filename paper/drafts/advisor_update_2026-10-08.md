## FedLS-SQL: tiến độ 08/10/2026

**Setup:** student Qwen2.5-Coder-0.5B, teacher Qwen2.5-Coder-7B (frozen). Private: Spider, 5 clients non-IID. Public: BIRD train. Seed 0.
**Ký hiệu:** `a` = 1 round FL trên Spider; `k` = 1 epoch server trên BIRD; `k2` = 2 epoch. `gold` = CE; `hinton` = CE + KL teacher. Mọi arm có 3 lượt Spider; arm có `k` có thêm 2 epoch BIRD.

### 1. Kết quả (EX %, riêng Spider EM là exact match)

| Arm | Spider EX | Spider EM | Realistic | Syn | DK | BIRD |
|---|---:|---:|---:|---:|---:|---:|
| centralized_e3 | 59.38 | 58.12 | 45.87 | 43.42 | 44.30 | 13.62 |
| fl_aaa | 57.54 | 52.03 | 47.24 | 41.49 | 42.80 | 14.34 |
| gold_akaka | 60.15 | 54.64 | 50.98 | 48.16 | 46.54 | 25.75 |
| hinton_akaka | 62.57 | 57.54 | 52.17 | **50.48** | **47.85** | **28.88** |
| gold_akkaa | 61.80 | 55.90 | 52.17 | 48.65 | 46.17 | 26.60 |
| hinton_akkaa | 63.15 | 56.96 | 51.77 | 49.71 | 47.48 | 27.77 |
| gold_k2aaa | 61.90 | 57.35 | **52.76** | 49.23 | 45.05 | 27.25 |
| hinton_k2aaa | **63.93** | **58.61** | 51.97 | 48.26 | 46.92 | 27.71 |

### 2. Hinton so với gold, cùng schedule (điểm EX)

| Schedule | Spider | BIRD |
|---|---:|---:|
| akaka | +2.42 (p=.020) | +3.13 (p<.001) |
| akkaa | +1.35 (p=.19) | +1.17 (p=.19) |
| k2aaa | +2.03 (p=.048) | +0.46 (p=.67) |

Paired trên cùng câu hỏi, exact McNemar.

### 3. Nhận xét

- Pha public luôn có lợi: mọi arm có `k` hơn fl_aaa +2.6 đến +6.4 điểm Spider và +11.4 đến +14.5 điểm BIRD.
- Teacher hơn gold trên Spider ở cả ba schedule; trên BIRD chỉ rõ ở akaka (`k` gần cuối).
- Chưa schedule nào tách được khỏi schedule khác (mọi p > .1).

### 4. Đang làm

- Thêm FedNTD (Lee et al., NeurIPS 2022) vào training của client: giữ kiến thức public trong các round private, không cần gửi output của teacher xuống client. Kết quả ban đầu ở round cuối khả quan; đang mở rộng ra toàn chuỗi.
- Baseline còn thiếu: FedProx, và centralized Spider+BIRD làm mức trần.
