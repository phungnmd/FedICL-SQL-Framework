# FedLS-SQL: các hướng ứng viên

Cập nhật: 2026-11-05. Trạng thái: **owner chưa chọn hướng**. Bản 2026-11-04 có
ba hướng A/B/C; bản này đánh giá lại theo tiêu chí owner đặt ngày 2026-11-05.
Bằng chứng nền: [RESEARCH_STATE](RESEARCH_STATE.md) mục 3; closest work:
[LITERATURE](LITERATURE.md).

## 1. Tiêu chí (owner, 2026-11-05)

- Bài là một framework áp dụng được cho setup federated. FL là bối cảnh, không
  phải vấn đề chính: với split hiện tại, FedAvg và centralized chênh ít (trên
  Spider test, `central` - FedAvg -0.42).
- Mục tiêu tốt nhất: vai trò của teacher và của RL đều rõ.
- Chỉ bỏ CoT hoặc teacher khi bằng chứng cho thấy chúng không có tác dụng.
- Cơ chế RL phải chưa có paper nào làm, và phải cho hiệu quả rõ ở mức đủ cho Q3.

## 2. Đánh giá lại các hướng cũ

| Hướng | Vai trò teacher | RL mới? | Bằng chứng | Kết luận |
|---|---|---|---|---|
| A. Teacher KD làm điểm xuất phát, federated DPO, replay | Nhỏ trên Spider test (khoảng 0.5, K3); phần chính nằm ở BIRD | Không: DPO + NLL theo execution đã có (ExCoT); federated RLVR đã có (FedMOA, PubSwap) | Lý do "RL ít drift hơn" yếu, vì FL penalty vốn nhỏ | Không đủ. Giữ làm baseline |
| B. Federated CoT-DPO (teacher CoT, CoT SFT, DPO) | Teacher viết CoT, chưa tách được | Không | CoT thua SQL -3.29 (C1), tốn compute gấp 3 lần | Không đủ |
| C. Teacher trong RL ở server (on-policy distillation) | Rõ, nhưng chỉ trên public | Một phần: KDRL, SERL-SQL, OPD đã có ở centralized | Gain ở server bị FedAvg bào mòn (K4) | Để làm phần mở rộng |

Lý do chung: cả ba đều không có một cơ chế RL riêng của bài này.

## 3. Hướng D (khuyến nghị): teacher-seeded CoT exploration, deploy SQL-only

### 3.1. Vấn đề

RL bằng execution không học được gì từ những câu mà cả K mẫu đều sai: không có
pair, không có advantage. Ở P2.62, số câu như vậy chiếm khoảng 15-20% mỗi
round, và hai round retry riêng trên chúng vẫn thêm +3.1 điểm (R4).

Các paper giải quyết câu khó đều cần teacher nhìn thấy chính câu đó:

- hint của teacher khi mọi rollout sai (AAPO, ADHint);
- teacher có gold làm privileged context viết reasoning cho câu khó (ReToolSQL);
- teacher chấm lại các action của student (SERL-SQL);
- trộn trace của teacher vào rollout (LUFFY).

Trong FL, teacher chỉ chạy ở server trên public data, nên không dùng được cho
câu private. Đây là chỗ trống cụ thể, sinh ra từ ràng buộc privacy của FL.

### 3.2. Cơ chế

```text
Server, BIRD public:  teacher 7B viết CoT có kiểm execution
                      student học hai mode trong một LoRA: CoT mode (từ teacher) và SQL mode (gold)
Client, mỗi round:    SQL mode sinh K=8 cho mỗi câu private, execution check
                      câu toàn sai -> CoT mode sinh K mẫu (explorer, kiến thức của teacher)
                      SQL đúng tìm bằng CoT -> chosen cho prompt SQL mode; rejected = mẫu SQL sai
                      DPO + NLL trên pair thường + pair cứu được; FedAvg
Deploy:               chỉ SQL mode, greedy, khoảng 25 token
```

- **Teacher:** kiến thức reasoning của teacher đi tới câu private qua CoT mode
  mà student học trên public. Teacher không bao giờ thấy dữ liệu private.
- **CoT:** chỉ làm explorer lúc train. Lúc deploy không có chi phí CoT, nên
  điểm yếu C1 và C5 (CoT greedy kém, tốn token) được tránh.
- **RL:** cross-mode preference: chosen do mode khác tìm ra, đã kiểm execution
  tại client; pair chỉ tập trung vào câu khó.

### 3.3. Bằng chứng có sẵn

Tính trên CPU từ các file đã publish (`p262_rl_from_bird_s0/data/*_rows.json`,
nested `1eeaa6a`). Hai route cùng bộ câu hỏi và cùng round, cả hai chưa thấy
gold Spider:

- Trong 1,200 câu mà `s1` (SQL) sinh 8 mẫu đều sai, `c1` (CoT) có ít nhất một
  SQL đúng ở 508 câu (42.3%).
- Theo chiều ngược lại, `s1` giải được 386 trong 1,078 câu mà `c1` sai hết.
- Để so: khi `s1` tự retry các câu này từ checkpoint tốt hơn, nó chỉ cứu được 23.83%.
- Tổng số câu toàn sai trong các round fresh: CoT khoảng 1,078, SQL khoảng 1,400.

Hai giới hạn của bằng chứng này:

- `c1` và `s1` là hai model khác nhau, nên một phần mức bổ sung cho nhau có thể
  chỉ do có hai model, không phải do CoT. Cần một explorer SQL thứ hai không
  dùng gold để tách. Route SQL của P2.60 không dùng được làm control: nó đã SFT
  trên gold của chính các câu này và cứu 83%.
- Client có gold SQL, nên baseline bắt buộc là "gold làm chosen cho câu toàn
  sai". D chỉ có ý nghĩa nếu chosen tự tìm hơn chosen là gold. Có cơ sở cho
  khả năng này (on-policy quên ít hơn: RL's Razor), và R2 cho thấy SFT trên
  gold không thêm rõ sau RL (`s1_rl9` - `sql_rl9` -1.35, p=.33), nhưng chưa
  được kiểm trực tiếp.

### 3.4. Claim và comparator

| Claim | Comparator |
|---|---|
| D1. Pair cứu bằng CoT nâng EX hơn RL thường | Cùng số round: D so với `s1`-style |
| D2. Hơn cả khi dùng gold cho câu toàn sai | Chosen là gold SQL trên cùng các câu |
| D3. Explorer có kiến thức teacher hơn explorer không teacher | CoT mode học từ teacher so với CoT tự sinh trên BIRD (STaR-style, gold-blind, lọc execution) |
| D4. Hiệu quả không chỉ do có model thứ hai | Explorer là một SQL model khác không dùng gold |
| D5. Framework chạy được dưới FedAvg `k5` | Federated D so với centralized D |

Vai trò RL được chứng minh qua D1 và `s1` so với SFT; vai trò teacher qua D3;
vai trò CoT qua D1 và D4.

### 3.5. Pilot (centralized, dùng adapter có sẵn)

Từ `s1_rl9` (74.18 dev), lấy các câu nó vẫn sinh toàn sai. Cho `c1_rl8` sinh
K=8 bằng CoT trên các câu đó, rồi chạy một round DPO + NLL cho từng arm:

- `d_cot`: chosen là SQL đúng do `c1_rl8` tìm ra.
- `d_gold`: chosen là gold SQL trên cùng các câu.
- `d_self`: một round retry SQL bình thường.

Eval mỗi arm và `s1_rl9` trên Spider dev và test. Khoảng 3-4 GPU-h cho phần
sample CoT, mỗi arm khoảng 1 GPU-h; vừa một GPU trong khoảng nửa ngày.

- Nếu `d_cot` hơn `d_gold` và `d_self`: xây model hai mode và các control D3, D4,
  rồi mới chạy FL.
- Nếu `d_gold` ngang hoặc hơn: cơ chế cứu bằng CoT không có lý do tồn tại, và
  đóng hướng D.

### 3.6. Rủi ro

- **Hai mode trong một LoRA có thể lấn nhau.** Pilot dùng hai adapter riêng.
  Nếu bản một adapter kém hơn thì phải gửi hai adapter, gấp đôi chi phí truyền.
- **Chosen đến từ phân phối khác (off-policy).** NLL trên chosen giúp phần này.
  LUFFY và ExCoT đều dùng off-policy chosen và có kết quả.
- **Gain có thể nhỏ:** pair cứu được khoảng 500 trên 7,000 câu. Ước lượng thô
  theo R4 (khoảng 300-400 pair retry cho +1 đến +2 điểm) là +1 đến +3 điểm.
  Q3 cần gain giữ được trên test và qua 3 seed.

## 4. Hướng C ở vai trò phụ

Nếu D đứng được, on-policy distillation ở server có thể nâng CoT mode trên
public giữa các round. Chỉ làm khi D3 cho thấy chất lượng explorer là điểm
nghẽn.

## 5. Cần owner quyết

1. Chọn D làm hướng chính và chạy pilot 3.5, hay chọn hướng khác.
2. Nếu chọn D: tôi viết runner pilot (CPU test trước), thêm lệnh Spider test
   cho `s1_rl9`, và đưa vào PIPELINE_NEXT.

## 6. Venue

Data & Knowledge Engineering, International Journal of Data Science and
Analytics, Neural Processing Letters, Distributed and Parallel Databases;
stretch: Journal of Intelligent Information Systems.
