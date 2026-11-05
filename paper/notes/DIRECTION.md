# FedLS-SQL: các hướng ứng viên

Cập nhật: 2026-11-05 (lần 2). Trạng thái: **owner chưa chọn hướng**. Bằng
chứng nền: [RESEARCH_STATE](RESEARCH_STATE.md) mục 3; closest work:
[LITERATURE](LITERATURE.md).

## 1. Tiêu chí (owner, 2026-11-05)

- Bài là một framework cho setup federated: teacher KD trên public ở server,
  dữ liệu private ở client. FL là bối cảnh, không phải vấn đề cần giải; với
  split hiện tại FedAvg và centralized chênh ít (Spider test `central` -
  FedAvg -0.42).
- RL không cần là cơ chế mới. Áp RL đã có vào framework để EX vượt rõ các
  baseline.
- Vai trò của teacher và của RL đều phải đo được. Chỉ bỏ CoT hoặc teacher
  khi bằng chứng cho thấy chúng không giúp.

## 2. Literature: tổ hợp này đã có ai làm chưa

Theo các đợt search 2026-11-01 và 2026-11-05 (đọc abstract và trích đoạn,
không phải systematic review):

| Tổ hợp | Có chưa | Bài gần nhất |
|---|---|---|
| Federated Text-to-SQL | Có, nhưng không teacher, không RL | Zhang et al., ACL 2023 |
| Federated + RL hoặc DPO + Text-to-SQL | Chưa thấy | |
| Federated DPO (task khác) | Có | FedPDPO, OpenFedLLM (FedDPO), POPri (ICML 2025) |
| Federated RLVR (toán, code, y tế) | Có, không teacher | FedMOA, PubSwap (ICML 2026), Fed-GRPO |
| FL với server LLM KD vào SLM trên public | Có, task chung | FedCoLLM, FedMKT, FedCoT, KnowledgeSG |
| DPO hoặc RL Text-to-SQL, centralized | Nhiều | ExCoT, Liu et al. (ACL 2025), AutoThinkSQL, SLM-SQL, Arctic-R1 |

Tổ hợp "teacher KD ở server trên public + RL bằng execution tại client trên
private + FedAvg, cho Text-to-SQL" chưa thấy bài nào. Theo novelty bar
(AGENTS.md), áp cơ chế đã có vào federated Text-to-SQL kèm adaptation riêng
của task là đủ cho Q3. Diễn đạt phải nêu closest work, không claim "first".

## 3. KD public/private có phải hướng hợp lý không

Có. Đây là mẫu chuẩn của nhóm FedCoLLM và FedMKT, và khớp ràng buộc teacher
chỉ ở server. Bằng chứng của ta:

- Stage server trên BIRD làm SLM federated tốt hơn (K1, +4.16 dev).
- Soft label của teacher hơn gold trên dev, không do smoothing hay anchoring (K2).
- Nhưng trên Spider test phần teacher chỉ khoảng 0.5 (K3).

Câu hỏi còn mở là sau RL phần teacher còn bao nhiêu. Chưa đo, và đó là thí
nghiệm quyết định (mục 5).

## 4. CoT có mặc định tốt với setup này không

Literature chia hai phía:

- **Ủng hộ CoT:** Liu et al. (ACL 2025): trên BIRD, với 10 model 6.7B-15B, DPO
  không có CoT thường không giúp hoặc làm giảm EX; CoT tổng hợp giúp DPO hiệu
  quả. OmniSQL: CoT hơn SQL-only ở 7B. RetrySQL: gain lớn trên BIRD với gold
  schema links.
- **Không ủng hộ:** ExCoT: ở 70B, SFT SQL-only hơn CoT trên cả Spider và BIRD.
  AutoThinkSQL: model nên tự học khi nào cần reasoning.

Kết quả của ta (1.5B, Spider, greedy) nghiêng về phía không ủng hộ, và ngược
với Liu et al. ở điều kiện khác:

- SQL-only DPO + NLL hiệu quả: `s1` +15.38. Chính preference term tạo gain:
  `g3d` - `g3n` +2.22 (p=.004).
- CoT thua SQL sau SFT (khoảng -10) và sau RL (-3.29, p=.014).

Vậy CoT không mặc định tốt ở setup này. Một chỗ chưa kiểm: CoT có thể giúp
trên BIRD, nơi các paper ủng hộ CoT báo gain. Các route CoT chưa từng được
eval trên BIRD dev.

## 5. Các hướng

### P (khuyến nghị): teacher KD ở server, rồi federated execution DPO ở client

```text
Server, BIRD public:  teacher 7B Hinton KD (gold CE + KL) -> G0          [teacher]
Mỗi global round:     client sinh K=8 SQL trên câu private, execution check,
                      DPO + NLL local trên pair đúng/sai -> FedAvg       [RL]
Deploy:               SLM, SQL-only, greedy
```

| Phép so | Đo gì |
|---|---|
| P - FedAvg SFT, cùng số round | Vai trò RL trong FL |
| P từ Hinton K2 - P từ gold K2 | Vai trò teacher sau RL |
| P - `hinton_k2aaa` (KD + SFT round) | RL thay cho SFT round |
| P - centralized P | Chi phí FL (dự kiến nhỏ) |
| P - teacher zero-shot, FedProx, FedCoLLM-style, local | Baseline của bảng chính |

Mốc để so (seed 0): FedAvg Spider test 71.50; `hinton_k2aaa` 73.50; FedProx
70.42; teacher 7B zero-shot 77.22. Ở centralized, RL từ student BIRD đạt
74.18 dev (`s1_rl9`, chưa có số test). Nếu FL giữ được phần lớn mức này, P hơn
các baseline FL khoảng 2-3 điểm trên test.

**Rủi ro chính:** sau RL, điểm xuất phát Hinton và gold có thể hội tụ về cùng
một mức. Khi đó phần đóng góp của teacher chỉ còn là ablation, không đạt mục
tiêu paper. Phải đo cái này trước khi xây FL:

1. Chạy route `s1` từ adapter K2 của `hinton_k2aaa` (Spider dev 62.28) thay
   cho `sql1_e2` (gần như gold K2: 58.80 so với 59.09). Centralized, một GPU,
   khoảng 10 GPU-h. Đường dẫn adapter cần kiểm trên server.
2. Spider test cho `s1_rl9`, `sql_rl9`, `sql2_e1`.

Nếu Hinton giữ được +1.5 điểm trở lên sau RL (dev, rồi test) thì xây FL. Nếu
không, chuyển sang Q.

**Vị trí KD (đánh giá 2026-11-05):** giữ KD ở đầu (K2 rồi các round RL).

| Lịch | Kết quả cũ | Paper ủng hộ |
|---|---|---|
| KD trước (K2AAA) | Coder-1.5B: teacher - gold +2.13 dev (p=.020), Spider test các arm K2 72.6-73.9; 0.5B: Spider cao nhất (63.93) | Gián tiếp: khởi tạo pretrained trước FL giảm ảnh hưởng của heterogeneity (Nguyen et al. ICLR 2023); public pretraining và distillation từ LLM trước private FL (Wang et al. 2023, arXiv 2305.12132); warm-up trên shared data (Zhao et al. 2018). Distill rồi RL: ExCoT, SLM-SQL; Think2SQL lẫn lộn (3B BIRD: RL 50.0, SFT + RL 48.2). P2.59: SFT rồi RL hơn RL alone +3.00 |
| Một round FedAvg rồi KD (AK2AA) | 0.5B: Spider 63.15, teacher - gold +1.35 (p=.19), yếu nhất trong ba lịch | Không thấy paper nào dùng đúng lịch này |
| KD xen kẽ hoặc sau mỗi FedAvg (AKAKA, server step sau mỗi round) | 0.5B: BIRD edge của teacher chỉ rõ ở đây (+3.13); Coder-1.5B: Spider edge mất khi round cuối plain (+0.39, p=.76); server step sau mỗi round làm Spider giảm ngay (71.57 xuống 65.57) và BIRD mất lại ở round sau | Trực tiếp với teacher trong FL: FedCoLLM, FedMKT (KD lặp mỗi round); FedDF (NeurIPS 2020, ensemble distillation sau mỗi aggregation) |

KD sau mỗi round chỉ có lợi cho BIRD, mà phần đó replay giữ được rẻ hơn. KD
cuối cùng (sau RL) sẽ kéo Spider xuống (F8: K càng muộn Spider càng thấp).
Một ablation lịch đáng làm: K2 rồi A rồi RL, so với K2 rồi RL. Mốc
centralized tương tự: `sql_rl9` - `s1_rl9` +1.35 (p=.33), không có KD.

### Q: teacher làm nguồn pair trên public (bổ sung cho P)

Ở server, teacher giải các câu BIRD mà student sai hết. SQL đúng của teacher
làm chosen, SQL sai của student làm rejected: một round DPO off-policy như
ExCoT. Round này chạy một lần trước FL hoặc xen giữa các round. Phép so là
cùng các câu đó với gold làm chosen. Có sẵn 1,266 lời giải teacher đã kiểm
(P2.60) cộng cache SeqKD 5,319 dòng. Đây là chỗ teacher đóng góp trực tiếp
vào RL. Rủi ro: các lần trước, edge của teacher SQL (SeqKD) mất sau round
private (Q5 cũ).

### R: CoT làm biến thể

Giữ CoT làm một arm của P (teacher CoT trên BIRD, rồi federated DPO trên CoT),
không làm trục chính. Mở lại thành trục chính chỉ khi Spider test hoặc BIRD dev
đảo kết quả C1. Một bước rẻ: eval `c1_rl8` và `s1_rl9` trên BIRD dev.

### D: CoT làm explorer cho câu toàn sai (mở rộng)

CoT mode tìm SQL đúng ở các câu SQL mode sai hết; chỉ deploy SQL. Có tín
hiệu: 42.3% so với 23.83% (C7). Nhưng bắt buộc phải thắng baseline "gold làm
chosen". Dùng khi P cần thêm phần đóng góp của teacher và CoT.

## 6. Cần owner quyết

1. Chọn P làm hướng chính, chạy hai thí nghiệm kiểm ở mục P trước.
2. Có eval BIRD dev cho `c1_rl8` và `s1_rl9` không (quyết định R).

## 7. Venue

Data & Knowledge Engineering, International Journal of Data Science and
Analytics, Neural Processing Letters, Distributed and Parallel Databases;
stretch: Journal of Intelligent Information Systems.
