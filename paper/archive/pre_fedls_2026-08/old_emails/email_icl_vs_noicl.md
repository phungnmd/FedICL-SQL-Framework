# Email cập nhật kết quả pipeline

**Tiêu đề:** Kết quả pipeline non-ICL: federated nhiều round + server KD

Chào Thầy,

Em xin cập nhật kết quả paper với student Qwen2.5-1.5B-Instruct, teacher
Qwen2.5-Coder-7B-Instruct và greedy decoding. 

## 1. Đề xuất bỏ ICL

Spider dev, 1.034 mẫu. `Train k` là số demo lúc fine-tuning, `Eval k` là số demo
lúc inference.

| Setting            | K clients | Train `k` | Eval `k` |        EX |        EM | Exec. error |
| ------------------ | --------: | --------: | -------: | --------: | --------: | ----------: |
| Base (zero-shot)   |         — |         — |        0 |     50,00 |     21,08 |  **25,92%** |
| Base (zero-shot)   |         — |         — |        3 | **52,22** | **29,30** |      23,98% |
|                    |           |           |          |           |           |             |
| Centralized FT     |         — |         0 |        0 |     62,19 |     57,16 |      20,41% |
| Centralized FT     |         — |         0 |        3 |     61,32 |     56,00 |      21,08% |
| Centralized FT     |         — |         3 |        0 | **64,02** | **58,22** |  **17,79%** |
| Centralized FT     |         — |         3 |        3 |     58,61 |     50,77 |      20,12% |
|                    |           |           |          |           |           |             |
| Federated, round 1 |         5 |         0 |        0 |     63,35 | **31,53** |      12,86% |
| Federated, round 1 |         5 |         0 |        3 |     60,06 |     28,92 |      15,76% |
| Federated, round 1 |         5 |         3 |        0 | **64,02** |     31,04 |  **11,80%** |
| Federated, round 1 |         5 |         3 |        3 |     59,38 |     28,53 |      15,86% |


- Demo lúc inference làm giảm EX ở cả centralized và federated; train/eval cùng.
  `k=3` không khắc phục được suy giảm.
-  ICL chỉ có tác dụng ở base model (đã thử trên vài model khác cho kết quả tương tự)
-  Phương pháp ICL hiện tại đã là tốt nhất từ các phương pháp e đã thử trên nhiều model.


Nên em đề xuất **bỏ ICL khỏi method chính** , mong thầy review chỗ này giúp em.

## 2. Kết quả pipeline non-ICL

Pipeline: `client_ft` → `fedavg` → `server_kd` (CE + reverse KL trên public
pool), lặp qua từng round. Mỗi round cho client đi qua private data đúng 1 pass,
nên round `N` được matched với centralized `N` epoch theo số lượt train trên spider data.

**2.1. Kết quả theo data pass — Spider dev**


| Setting        | Stage                | K clients | Data pass |        EX |        EM | Exec. error |
| -------------- | -------------------- | --------: | --------: | --------: | --------: | ----------: |
| Base           | zero-shot            |         — |         0 |     50,00 |     21,08 |      25,92% |
|                |                      |           |           |           |           |             |
| Federated      | post-FedAvg (pre-KD) |         5 |         1 |     57,35 |     50,58 |      22,82% |
| Federated      | post server KD       |         5 |         1 | **63,35** |     31,53 |  **12,86%** |
| Centralized FT | —                    |         — |         1 |     62,19 | **57,16** |      20,41% |
|                |                      |           |           |           |           |             |
| Federated      | post-FedAvg (pre-KD) |         5 |         2 |     64,02 |     56,96 |      18,38% |
| Federated      | post server KD       |         5 |         2 |     66,15 |     33,56 |  **11,99%** |
| Centralized FT | —                    |         — |         2 | **67,02** | **62,57** |      16,05% |
|                |                      |           |           |           |           |             |
| Federated      | post-FedAvg (pre-KD) |         5 |         3 |     66,05 |     60,15 |      17,21% |
| Federated      | post server KD       |         5 |         3 | **69,54** |     38,59 |   **9,77%** |
| Centralized FT | —                    |         — |         3 |     67,60 | **62,67** |      15,76% |


- Federated tăng **6,19 EX** từ round 1 đến round 3 và có thể tiếp tục tăng ở round sau; centralized gần như dừng sau epoch 2 đã bão hòa
- Ở pass 3, federated đạt 69,54 EX vượt centralized đạt 67,60 EX
- Exec. error của federated giảm còn **9,77%**, so với 15,76% của centralized.
  EM chỉ so sánh trong cùng stage vì server KD thay đổi cách biểu diễn SQL.

**2.2. Robustness và vai trò của fedavg và KD**


| Setting                   | Spider dev |  Realistic |        Syn |         DK |   BIRD dev |
| ------------------------- | ---------: | ---------: | ---------: | ---------: | ---------: |
|                           |  n = 1.034 |        508 |      1.034 |        535 |      1.534 |
| Base                      |      50,00 |      40,35 |      37,04 |      41,68 |      10,89 |
|                           |            |            |            |            |            |
| Federated r1, pre-KD      |      57,35 |      54,92 |      49,32 |      45,23 |      11,15 |
| Federated r1, post-KD     |      63,35 |      52,95 |      49,61 |      47,85 |      19,43 |
| Federated r3, pre-KD      |      66,05 |      58,27 |      55,51 |      50,84 |      17,67 |
| **Federated r3, post-KD** |  **69,54** |  **59,65** |  **55,51** |  **52,71** |  **21,58** |
|                           |            |            |            |            |            |
| Centralized 3 epoch       |      67,60 |      57,87 |      53,19 |      52,52 |      12,91 |
|                           |            |            |            |            |            |
| r3 post-KD − base         | **+19,54** | **+19,30** | **+18,47** | **+11,03** | **+10,69** |

| Đóng góp                           | 3 bộ biến thể Spider                   | BIRD dev                         |
| ---------------------------------- | -------------------------------------- | -------------------------------- |
| Federated thuần (r1 pre-KD − base) | +14,57 / +12,28 / +3,55                | **+0,26**, `p=0,82`              |
| Server KD (post − pre, mọi round)  | 9 cell, **không cell nào significant** | **+8,28** và **+3,91**, `p<1e−6` |

Ý chính:

- Round 3 tăng **+10,69 đến +19,54 EX** so với base và bằng hoặc hơn centralized
  3 epoch trên cả năm bộ;
- Hai component bổ sung nhau: federation mạnh trên các biến thể Spider, server
  KD mạnh trên BIRD và giảm exec. error ở 12/12 cell.
- BIRD dev vì hiện đang chỉ KD từ data mà teacher sinh ra đúng (40%) nên EX thấp.

Em xin ý kiến Thầy về vấn đề bỏ ICL khỏi method chính và nếu bỏ thì chỉ Fed + KD thì bài có đủ value hay cần đổi hướng khác, mong thầy review giúp em.