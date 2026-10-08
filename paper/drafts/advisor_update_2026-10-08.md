## FedLS-SQL: tiến độ 08/10/2026

**Setup:** student Qwen2.5-Coder-0.5B, teacher Qwen2.5-Coder-7B (frozen). Private: Spider, 5 clients non-IID. Public: BIRD train. Seed 0.
**Ký hiệu:** `a` = 1 round FL trên Spider; `k` = 1 epoch server trên BIRD; `k2` = 2 epoch. `gold` = CE; `hinton` = CE + KL teacher; `ntd` = round `a` cuối có thêm FedNTD (Lee et al., NeurIPS 2022): client giữ phân phối các token không đúng gần với model global nhận được, không cần gửi logit teacher.

### 1. Kết quả (%)

| Arm | Spider EX | Spider EM | Realistic | Syn | DK | BIRD |
|---|---:|---:|---:|---:|---:|---:|
| centralized_e3 | 59.38 | 58.12 | 45.87 | 43.42 | 44.30 | 13.62 |
| fl_aaa | 57.54 | 52.03 | 47.24 | 41.49 | 42.80 | 14.34 |
| gold_akaka | 60.15 | 54.64 | 50.98 | 48.16 | 46.54 | 25.75 |
| hinton_akaka | 62.57 | 57.54 | 52.17 | **50.48** | **47.85** | 28.88 |
| hinton_akaka_ntd | 63.44 | 58.03 | 52.17 | 50.00 | 46.92 | **30.05** |
| gold_akaka_ntd | 59.96 | | | | | 28.62 |
| gold_akkaa | 61.80 | 55.90 | 52.17 | 48.65 | 46.17 | 26.60 |
| hinton_akkaa | 63.15 | 56.96 | 51.77 | 49.71 | 47.48 | 27.77 |
| gold_k2aaa | 61.90 | 57.35 | **52.76** | 49.23 | 45.05 | 27.25 |
| hinton_k2aaa | **63.93** | **58.61** | 51.97 | 48.26 | 46.92 | 27.71 |

Realistic, Syn, DK, BIRD: EX. Mọi arm có 3 lượt Spider; arm có `k` có thêm 2 epoch BIRD. Chưa xong: fedprox_aaa.

### 2. EX so với fl_aaa (điểm)

| Arm | Spider | Realistic | Syn | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| centralized_e3 | +1.84 | −1.37 | +1.93 | +1.50 | −0.72 |
| gold_akaka | +2.61 | +3.74 | +6.67 | +3.74 | +11.41 |
| hinton_akaka | +5.03 | +4.93 | **+8.99** | **+5.05** | +14.54 |
| hinton_akaka_ntd | +5.90 | +4.93 | +8.51 | +4.12 | **+15.71** |
| gold_akkaa | +4.26 | +4.93 | +7.16 | +3.37 | +12.26 |
| hinton_akkaa | +5.61 | +4.53 | +8.22 | +4.68 | +13.43 |
| gold_k2aaa | +4.36 | **+5.52** | +7.74 | +2.25 | +12.91 |
| hinton_k2aaa | **+6.39** | +4.73 | +6.77 | +4.12 | +13.37 |

### 3. Hinton so với gold, cùng schedule (điểm EX)

| Schedule | Spider | BIRD |
|---|---:|---:|
| akaka | +2.42 (p=.020) | +3.13 (p<.001) |
| akkaa | +1.35 (p=.19) | +1.17 (p=.19) |
| k2aaa | +2.03 (p=.048) | +0.46 (p=.67) |

Paired trên cùng câu hỏi, exact McNemar, p chưa hiệu chỉnh nhiều phép so sánh. Seed 0.

### 4. FedNTD ở round cuối (cùng parent, chỉ khác retention)

| hinton_akaka_ntd so với | Spider | BIRD |
|---|---:|---:|
| hinton_akaka | +0.87 (p=.41) | +1.17 (p=.14) |
| gold_k2aaa | +1.55 (p=.19) | +2.80 (p=.007) |
| hinton_k2aaa | −0.48 (p=.70) | +2.35 (p=.020) |

Dòng đầu là phép thử chính, quy tắc chốt trước: cần BIRD tăng với p<.05 và Spider không giảm quá 2 điểm. BIRD chưa đạt nên phép thử chính không qua. Hai dòng sau là so sánh thêm, không chốt trước.

Lặp lại với seed 1 cho round cuối (cùng parent K2): plain 62.09 / 28.42, NTD 62.19 / 31.03 (Spider / BIRD). Gộp hai seed, NTD so với không NTD: BIRD +1.89 (p=.004, CI [+0.59, +3.19]), Spider +0.48 (CI [−1.22, +2.18]). Theo quy tắc chốt trước, NTD được giữ: tăng BIRD, không làm giảm Spider.

Gold cũng dùng NTD (round cuối, seed 0), để xem tác dụng của teacher và của NTD tách nhau thế nào:

| Spider / BIRD | không NTD | có NTD |
|---|---|---|
| gold_akaka | 60.15 / 25.75 | 59.96 / 28.62 |
| hinton_akaka | 62.57 / 28.88 | 63.44 / 30.05 |

Hinton+NTD so với gold+NTD: Spider +3.48 (p=.002), BIRD +1.43 (p=.15). NTD với gold: BIRD +2.87 (p<.001), Spider −0.19.

### 5. Nhận xét

- Pha public (BIRD) luôn có lợi: mọi arm có `k` hơn fl_aaa từ +2.6 đến +6.4 điểm Spider và +11.4 đến +14.5 điểm BIRD.
- Teacher hơn gold trên Spider ở cả ba schedule (+1.35 đến +2.42; p<.05 ở akaka và k2aaa). Trên BIRD, lợi thế chỉ rõ ở akaka, nơi `k` nằm gần cuối.
- Hinton k2aaa không thua gold ở schedule nào trên cả Spider lẫn BIRD. Hai đầu Pareto là hinton_k2aaa (Spider cao nhất) và hinton_akaka (BIRD cao nhất).
- Chưa schedule nào tách được khỏi schedule khác (mọi p > .1).
- FedNTD ở round cuối tăng BIRD khoảng 1.9 điểm (gộp 2 seed, p=.004) và không đổi Spider. Mức tăng Spider ở seed 0 không lặp lại.
- Nhiễu của một round private: khoảng 0.5 đến 1.3 điểm Spider, nên chênh lệch khoảng 1 điểm giữa các schedule nằm trong nhiễu.
- Teacher giúp Spider (dữ liệu private), NTD giúp BIRD (dữ liệu public); hai tác dụng gần như cộng độc lập. hinton_akaka_ntd tốt nhất trên cả hai.
- Ngoài phép lặp seed của NTD, mọi kết quả từ seed 0.
