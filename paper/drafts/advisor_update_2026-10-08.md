## FedLS-SQL: tiến độ 08/10/2026

**Setup:** student Qwen2.5-Coder-0.5B, teacher Qwen2.5-Coder-7B (frozen). Private: Spider, 5 clients non-IID. Public: BIRD train. Seed 0.
**Ký hiệu:** `a` = 1 round FL trên Spider; `k` = 1 epoch server trên BIRD; `k2` = 2 epoch. `gold` = CE; `hinton` = CE + KL teacher.

### 1. Kết quả (%)

| Arm | Spider EX | Spider EM | Realistic | Syn | DK | BIRD |
|---|---:|---:|---:|---:|---:|---:|
| centralized_e3 | 59.38 | 58.12 | 45.87 | 43.42 | 44.30 | 13.62 |
| fl_aaa | 57.54 | 52.03 | 47.24 | 41.49 | 42.80 | 14.34 |
| gold_akaka | 60.15 | 54.64 | 50.98 | 48.16 | 46.54 | 25.75 |
| hinton_akaka | 62.57 | 57.54 | **52.17** | **50.48** | **47.85** | **28.88** |
| gold_akkaa | 61.80 | 55.90 | **52.17** | 48.65 | 46.17 | 26.60 |
| hinton_akkaa | 63.15 | 56.96 | 51.77 | 49.71 | 47.48 | 27.77 |
| hinton_k2aaa | **63.93** | **58.61** | 51.97 | 48.26 | 46.92 | 27.71 |

Realistic, Syn, DK, BIRD: EX. Đang chạy: gold_k2aaa (đã xong a2: Spider 61.61), fedprox_aaa.

### 2. EX so với fl_aaa (điểm)

| Arm | Spider | Realistic | Syn | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| centralized_e3 | +1.84 | −1.37 | +1.93 | +1.50 | −0.72 |
| gold_akaka | +2.61 | +3.74 | +6.67 | +3.74 | +11.41 |
| hinton_akaka | +5.03 | **+4.93** | **+8.99** | **+5.05** | **+14.54** |
| gold_akkaa | +4.26 | **+4.93** | +7.16 | +3.37 | +12.26 |
| hinton_akkaa | +5.61 | +4.53 | +8.22 | +4.68 | +13.43 |
| hinton_k2aaa | **+6.39** | +4.73 | +6.77 | +4.12 | +13.37 |
