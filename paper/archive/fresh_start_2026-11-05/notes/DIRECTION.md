# FedLS-SQL: hướng của bài

Cập nhật: 2026-11-05 (bản cuối sau hai lượt review độc lập). Trạng thái:
**đề xuất chốt, chờ owner duyệt mục 4**. Bằng chứng nền:
[RESEARCH_STATE](RESEARCH_STATE.md); literature đã kiểm:
[LITERATURE](LITERATURE.md) mục 3.1 và 5.1. Danh sách ứng viên trước đó và
bản nháp đã phản biện: [archive](../archive/directions_2026-11/DIRECTION_CANDIDATES_2026-11-05.md),
[draft](../archive/directions_2026-11/PROPOSAL_DRAFT_REVIEWED_2026-11-05.md).

## 1. Mục tiêu và ràng buộc

- Thắng baseline trên miền private: Spider EX, báo dev và test cùng nhau.
  BIRD dev là kết quả phụ (owner 2026-11-05).
- Vai trò teacher và vai trò RL đều phải đo được trên Spider. RL không cần
  là cơ chế mới. FL là bối cảnh: `central` - FedAvg -0.42 trên test, +3.77
  trên dev ở cùng số pass.
- Teacher Coder-7B 4-bit chỉ ở server, chỉ trên BIRD; student Coder-1.5B LoRA
  r16; 5 client Spider alpha 0.1; hai A5000; deploy SLM SQL-only, greedy.
- Đã bỏ: teacher tổng hợp dữ liệu mới (BIRD đã đủ, owner 2026-11-05); CoT
  làm trục chính; task ẩn (mục 5).

## 2. Hướng chính P

```text
Server, BIRD:  Hinton KD (0.5 CE + 0.5 T^2 KL, T=2), 2 epoch            [teacher]
Client:        3 round FedAvg SFT trên gold Spider                        [FL]
Client:        r round FedDPO: sinh K=8 SQL, execution check, DPO + NLL
               trên pair đúng/sai; câu toàn sai lấy gold làm chosen; FedAvg  [RL]
Deploy:        SLM, SQL-only, greedy
```

Ba phần K2 và 3 round SFT đã có sẵn: đó là `hinton_k2aaa` A3 (Spider test
73.50). Phần mới là các round FedDPO.

Literature: chưa thấy bài federated + RL/DPO + Text-to-SQL (Zhang et al.
ACL 2023 là federated Text-to-SQL không teacher, không RL). Từng mảnh đã có:
Hinton 2015, FedAvg, FedDPO (OpenFedLLM), DPO + NLL (Iterative RPO), DPO
theo execution (ExCoT). Bài phải nêu đúng như vậy, không claim "first".

### Kỳ vọng thực tế trên Spider test

Cộng các phần đã đo: FedAvg 71.50, dữ liệu public +1.53 (`gold_k2aaa`),
teacher +0.47 (`hinton_k2aaa` - `gold_k2aaa`), RL sau SFT khoảng +1.5-2
(centralized `g3d` - `g2` +1.93 dev; chưa có số test). Tổng khoảng 75. Phần
của teacher là phần nhỏ nhất và là rủi ro chính của bài. Mức 58.80 lên 74.18
của `s1` là "học Spider qua RL", không phải phần RL thêm sau SFT.

### Đặc tả FedDPO phải chốt trước pilot FL

| Lựa chọn | Đề xuất | Lý do |
|---|---|---|
| Reference model | Global model đầu mỗi round | Như P2.58-P2.62 và Iterative RPO |
| Câu toàn sai | Gold làm chosen, một SQL sai làm rejected | Client có gold; retry chỉ cứu 23.83% |
| Local update | 1 epoch trên pair của round, lr 1e-5, beta 0.1, NLL weight 1 | Giữ cấu hình centralized đã đo |
| Aggregation | Theo số pair của client trong round; client không có pair giữ adapter đầu round | alpha 0.1 làm số pair rất lệch giữa client |
| Số câu mỗi round | 1,200 câu chia theo client theo tỉ lệ dữ liệu | Như centralized |

## 3. Biến thể

| # | Biến thể | So với | Trạng thái | Căn cứ |
|---|---|---|---|---|
| V1 | RL từ ba adapter A3 seed 0: `hinton_k2aaa`, `gold_k2aaa`, FedAvg A3 | Ba arm với nhau, cùng số round | **Chạy trước, quyết định** | Đúng lịch deploy; có arm "không stage server" để tách public data, teacher và RL |
| V2 | Lịch: K2 rồi RL ngay (không SFT round) | P | Ablation ở FL, chỉ a=0 so với a=3 | `sql_rl9` - `s1_rl9` +1.35 (p=.33) |
| V3 | Q: một round DPO + NLL trên BIRD ở server, SQL đúng của teacher làm chosen, trên câu student sai hết | Cùng câu, gold làm chosen | **Có điều kiện**: chỉ khi cổng V1 dưới +1 | Owner giữ một hướng teacher-in-RL. Reviewer thứ hai dự đoán chỉ chạm BIRD, vì SQL đúng của teacher tương đương gold và edge ở server bị các round private bào mòn |
| V4 | Teacher xen kẽ (KD lại sau mỗi round, FedCoLLM-style) | P | **Chỉ làm baseline** | Server step làm Spider giảm ngay (71.57 xuống 65.57); FedCoLLM-style seed 1 Spider test 66.88 |
| V6 | D: SQL do mode CoT tìm được làm chosen cho câu toàn sai | Gold làm chosen | **Pilot rẻ rồi đóng hoặc mở** | C7 42.3% so với 23.83%, nhưng hai model khác nhau, không cùng compute, và gold phủ 100% câu |

Pilot V6 (khoảng 6 GPU-h, centralized): một round DPO + NLL từ `s1_rl9`, cùng
rejected, ba arm: chosen là SQL `c1` cứu được trên 508 câu; gold trên đúng
508 câu đó; gold trên cả 1,200 câu. V6 chỉ vào FL nếu thắng arm thứ hai; khi
đó mới thêm SQL explorer cùng compute (K=64 SQL so với K=8 CoT). Đổi format
prompt của explorer chỉ đáng thử sau khi V6 thắng gold-chosen.

### Hai chỗ teacher có cơ hội đo được trên Spider

Không biến thể nào trong ràng buộc này có kỳ vọng teacher hơn +1 Spider test ở
cuối pipeline. Hai chỗ có cơ hội thật, đều đo trong V1:

- **Số round đến mức EX mục tiêu** (ít communication hơn): đứng được kể cả khi
  RL nén khoảng cách ở cuối.
- **Spider-DK**: Hinton - gold +5.98 ở A3 seed 0; phần riêng của teacher so
  với virtual teacher +2.62 (p=.049), phần còn lại là smoothing.

## 4. Thứ tự và cổng

| Bước | Nội dung | GPU-h | Quyết định |
|---|---|---:|---|
| 0 | Spider test `s1_rl9`, `sql_rl9`, `sql2_e1`; BIRD dev `c1_rl8`, `s1_rl9` (BIRD chỉ để thảo luận CoT) | < 8 | Mốc test của route SQL RL |
| 1 | V1 centralized: route RL P2.62 `s1` (DPO + NLL, retry, gold-chosen cho câu toàn sai) từ ba adapter A3 seed 0, số round cố định, báo theo từng round, kèm Spider-DK | ~30 | Cổng bên dưới |
| 1b | Pilot V6 (song song) | ~6 | Đóng hoặc mở V6 |
| 2 | Dựng FedDPO theo mục 2, pilot một round FL | ~8 | Chi phí, số pair theo client |
| 3 | FL seed 0: P-Hinton, P-gold, FedAvg rồi FedDPO, federated rejection-SFT, FedAvg SFT cùng compute, FedCoLLM-style seed 0; V2 | ~60 | Bảng chính seed 0 |
| 4 | Seed 1-2 cho các arm chính (gồm `gold_k2aaa` seed 1-2, FedAvg seed 1-2, FedCoLLM-style seed 2) | ~130 | Claim chính |
| 5 | Eval đầy đủ: Spider dev + test, BIRD dev, Spider-DK/Realistic/SYN | ~20 | |

Tổng khoảng 260 GPU-h. Cổng của bước 1 (Hinton so với gold, ở cùng round
index, không lấy best theo dev):

- Gộp Spider dev và test (3,181 câu) thành một paired test theo câu; dev và test
  riêng lẻ phải cùng dấu.
- d ≥ +1.0: xây FL như mục 2.
- 0.3 ≤ d < 1.0: chạy seed 1 (adapter `hinton_k2aaa` seed 1 đã có, thiếu
  `gold_k2aaa` seed 1, khoảng 9 GPU-h), quyết định bằng question-clustered
  test trên 2 seed; cân nhắc V3.
- d < 0.3 hoặc dev và test ngược dấu: báo owner rằng phần teacher trên Spider
  không có bằng chứng ủng hộ trong ràng buộc hiện tại, kèm đường cong round và
  Spider-DK. Owner quyết.

Lý do: một seed, dev có khoảng 140 discordant pair (SE khoảng 1.1-1.3), test
SE khoảng 0.6-0.8; luật cũ "≥ +1 trên cả dev và test" chỉ qua được khoảng 25%
khi hiệu ứng thật là +1.0. Spider test đã dùng để chọn thì không còn held-out;
Spider-DK, Realistic và SYN là các tập chưa dùng để chọn.

Trước bước 1 cần kiểm trên server: ba adapter A3 seed 0 tồn tại và cùng loss
mode (`target_fp32`).

## 5. Các hướng đã cân nhắc và lý do không chọn

| Hướng | Lý do |
|---|---|
| CoT làm trục chính (teacher CoT SFT, RL CoT ở client) | Trên Spider mọi số đều ngược chiều: C1 -3.29 dev, C2 khoảng -10, AutoThinkSQL CoT DPO 69.14 so với SQL 84.23 (train BIRD, eval Spider, greedy), Liu et al. +0.6-1.1 Spider ở 7B; gain Spider của VCoT-SQL đến từ CoT viết trên Spider train, teacher ở đây không được làm; chi phí 2.5-4 lần |
| CoT kiểu VCoT, teacher thấy gold (pilot cotV, khoảng 30 GPU-h) | Cùng lý do; chỉ giữ BIRD dev của `c1_rl8` ở bước 0 làm mục thảo luận |
| Task ẩn (CoT hoặc plan làm target phụ, inference SQL-only) | Đã đóng vì âm: P2.15 -0.97 trên toàn bộ data; chỉ sửa K2, phần RL nén |
| Teacher tổng hợp dữ liệu mới | Owner bỏ: BIRD đã đủ |
| Teacher xen kẽ làm method | Làm Spider giảm; giữ làm baseline FedCoLLM-style |

## 6. Baseline và control của bảng chính

FedAvg SFT (cùng số round và cùng compute gồm cả rollout), FedProx,
FedCoLLM-style, `hinton_k2aaa` (K2 + SFT, không RL), FedAvg rồi FedDPO (không
stage server), P-gold (không teacher), federated rejection-SFT (NLL trên SQL
đúng tự sinh; centralized `g3r` -0.87 và `g3n` -0.29 so với `g2`), local-only
RL ở từng client, centralized P (cận trên, so ở cùng số pass), local tốt
nhất, teacher 7B zero-shot, base 1.5B. Ba seed, question-clustered test. Số
hiệu quả: dung lượng LoRA r16 mỗi round, GPU-h rollout mỗi client mỗi round,
chi phí KD một lần ở server. Một câu vì sao chọn DPO thay vì GRPO (bộ nhớ
A5000; Xiong et al. 2025).

## 7. Venue

Data & Knowledge Engineering, International Journal of Data Science and
Analytics, Neural Processing Letters, Distributed and Parallel Databases;
stretch: Journal of Intelligent Information Systems.

## Phụ lục: vị trí KD (đánh giá 2026-11-05)

Giữ KD ở đầu.

| Lịch | Kết quả cũ | Paper ủng hộ |
|---|---|---|
| KD trước (K2AAA) | Coder-1.5B: teacher - gold +2.13 dev (p=.020), Spider test các arm K2 72.6-73.9; 0.5B: Spider cao nhất (63.93) | Gián tiếp: khởi tạo pretrained trước FL giảm ảnh hưởng của heterogeneity (Nguyen et al. ICLR 2023); public pretraining và distillation từ LLM trước private FL (Wang et al. 2023, arXiv 2305.12132); warm-up trên shared data (Zhao et al. 2018). Distill rồi RL: ExCoT, SLM-SQL; Think2SQL lẫn lộn (3B BIRD: RL 50.0, SFT + RL 48.2) |
| Một round FedAvg rồi KD (AK2AA) | 0.5B: Spider 63.15, teacher - gold +1.35 (p=.19), yếu nhất trong ba lịch | Không thấy paper nào dùng đúng lịch này |
| KD xen kẽ (AKAKA, FedCoLLM-style) | 0.5B: BIRD edge của teacher chỉ rõ ở đây (+3.13); Coder-1.5B: Spider edge mất khi round cuối plain (+0.39, p=.76); kết thúc bằng K mất khoảng 8 Spider | FedCoLLM, FedMKT (KD lặp mỗi round); FedDF (NeurIPS 2020) |
