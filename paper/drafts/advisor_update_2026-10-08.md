## FedLS-SQL: tiến độ 08/10/2026

**Setup:** student Qwen2.5-Coder-0.5B (LoRA r16), teacher Qwen2.5-Coder-7B (frozen). Private: Spider, 5 clients, non-IID α=0.5. Public (server): BIRD train 9,428 câu. Seed 0.
**Ký hiệu:** `a` = 1 round FedAvg trên Spider; `k` = 1 epoch server trên BIRD; `k2` = 2 epoch liên tục. `gold` = CE; `hinton` = CE + KL teacher (T=2).

### 1. Kết quả cuối, EX / EM (%)

| Arm | Spider EX | Spider EM | Realistic EX | Realistic EM | Syn EX | Syn EM | DK EX | DK EM | BIRD EX |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| centralized_e3 | 59.38 | 58.12 | 45.87 | 47.05 | 43.42 | 40.43 | 44.30 | 43.55 | 13.62 |
| fl_aaa | 57.54 | 52.03 | 47.24 | 42.52 | 41.49 | 35.98 | 42.80 | 37.38 | 14.34 |
| gold_akaka | 60.15 | 54.64 | 50.98 | 45.47 | 48.16 | 40.91 | 46.54 | 42.62 | 25.75 |
| hinton_akaka | 62.57 | 57.54 | **52.17** | **49.41** | **50.48** | **43.81** | **47.85** | **44.30** | **28.88** |
| gold_akkaa | 61.80 | 55.90 | **52.17** | 46.46 | 48.65 | 41.30 | 46.17 | 42.43 | 26.60 |
| hinton_akkaa | 63.15 | 56.96 | 51.77 | 46.65 | 49.71 | 42.36 | 47.48 | 43.36 | 27.77 |
| hinton_k2aaa | **63.9*** | **58.6*** | chờ | chờ | chờ | chờ | chờ | chờ | chờ |
| gold_k2aaa | đang chạy | | | | | | | | |
| fedprox_aaa | đang chạy | | | | | | | | |

\* Từ log server, chưa publish. Số câu: Spider 1,034; BIRD dev 1,534 (chỉ EX, metric chính thức của BIRD).

### 2. Chênh lệch so với fl_aaa (điểm %)

| Arm | Spider EX | Spider EM | Realistic EX | Realistic EM | Syn EX | Syn EM | DK EX | DK EM | BIRD EX |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| centralized_e3 | +1.84 | +6.09 | −1.37 | +4.53 | +1.93 | +4.45 | +1.50 | +6.17 | −0.72 |
| gold_akaka | +2.61 | +2.61 | +3.74 | +2.95 | +6.67 | +4.93 | +3.74 | +5.24 | +11.41 |
| hinton_akaka | +5.03 | +5.51 | **+4.93** | **+6.89** | **+8.99** | **+7.83** | **+5.05** | **+6.92** | **+14.54** |
| gold_akkaa | +4.26 | +3.87 | **+4.93** | +3.94 | +7.16 | +5.32 | +3.37 | +5.05 | +12.26 |
| hinton_akkaa | +5.61 | +4.93 | +4.53 | +4.13 | +8.22 | +6.38 | +4.68 | +5.98 | +13.43 |
| hinton_k2aaa | **+6.36*** | **+6.57*** | | | | | | | |

**Đang chạy:** gold_k2aaa, fedprox_aaa, hinton_k2aaa trên các tập khác. **Tiếp theo:** centralized trên cùng data (Spider + BIRD).
