## FedLS-SQL: tiến độ 08/10/2026

**Setup:** student Qwen2.5-Coder-0.5B, teacher Qwen2.5-Coder-7B (frozen). Private: Spider, 5 clients non-IID. Public: BIRD train.



### 1. Kết quả chính
Em thử kết hợp federated và KD theo các thứ tự khác nhau:
- `a`: 1 round train trên các client với Spider private, rồi FedAvg
- `k`: 1 epoch KD trên server với BIRD làm public proxy dataset (`k2` = 2 epoch liên tiếp)

| Arm            | Spider EX | Spider EM | Realistic |       Syn |        DK |      BIRD |
| -------------- | --------: | --------: | --------: | --------: | --------: | --------: |
| centralized_e3 |     59.38 |     58.12 |     45.87 |     43.42 |     44.30 |     13.62 |
| fl_aaa         |     57.54 |     52.03 |     47.24 |     41.49 |     42.80 |     14.34 |
| gold_akaka     |     60.15 |     54.64 |     50.98 |     48.16 |     46.54 |     25.75 |
| hinton_akaka   |     62.57 |     57.54 |     52.17 | **50.48** | **47.85** | **28.88** |
| gold_akkaa     |     61.80 |     55.90 |     52.17 |     48.65 |     46.17 |     26.60 |
| hinton_akkaa   |     63.15 |     56.96 |     51.77 |     49.71 |     47.48 |     27.77 |
| gold_k2aaa     |     61.90 |     57.35 | **52.76** |     49.23 |     45.05 |     27.25 |
| hinton_k2aaa   | **63.93** | **58.61** |     51.97 |     48.26 |     46.92 |     27.71 |

### 2. Hinton so với gold, cùng schedule
Em chạy cùng setup nhưng server chỉ train CE trên gold SQL của BIRD (không dùng teacher), để đo hiệu quả của KD. Bảng là EX của Hinton trừ gold (điểm).

| Schedule | Spider |  BIRD |
| -------- | -----: | ----: |
| akaka    |  +2.42 | +3.13 |
| akkaa    |  +1.35 | +1.17 |
| k2aaa    |  +2.03 | +0.46 |

### 3. Nhận xét

- Pha public luôn có lợi: mọi arm có public (gold ce hoặc kd) hơn fl_aaa +2.6 đến +6.4 điểm Spider và +11.4 đến +14.5 điểm BIRD, và đều vượt cả centralized_e3 (chỉ train Spider). Em đang làm rõ phần vượt centralized này có bao nhiêu là do model được train thêm trên BIRD.
- Hinton KD hơn gold CE trên Spider ở cả ba schedule; trên BIRD chỉ rõ ở akaka (`k` gần cuối). Trong các phương pháp KD em đã thử, Hinton KD tốt nhất so với chỉ train trên gold.
- Về thứ tự schedule, chưa có thứ tự nào tốt hơn hẳn.
- Đánh giá sau mỗi `a` và `k` cho thấy: với FedAvg và KD thuần, mỗi round FedAvg làm model quên một phần kiến thức BIRD, mỗi round KD làm quên một phần kiến thức Spider.
- Các kết quả hiện tại là có gain nhưng phương pháp chưa cho thấy cơ chế rõ của việc kết hợp giữa federated private và KD qua public dataset.

### 4. Đang làm

- Thêm [FedNTD](https://arxiv.org/abs/2106.03097) vào training của client: giữ kiến thức public qua các round private, không cần gửi output của teacher xuống client. Kết quả ban đầu ở round cuối khả quan, em đang áp dụng chạy lại cho toàn bộ pipeline.
- Distill hai chiều: thêm retention tương tự ở server, trong lúc KD trên BIRD thì model vẫn giữ phân phối của model nhận từ FedAvg (theo [Learning without Forgetting](https://arxiv.org/abs/1606.09282)), để giảm việc quên Spider sau mỗi `k`. Khi đó client giữ kiến thức public, server giữ kiến thức private, và chỉ truyền adapter.
- Baseline còn thiếu: FedProx, và centralized Spider+BIRD làm mức trần.
