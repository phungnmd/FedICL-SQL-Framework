# FedLS-SQL: hướng của bài

Cập nhật: 2026-11-05 (lần 3, sau review độc lập). Trạng thái: **đề xuất chốt
P, chờ owner duyệt** (mục 6). Bằng chứng nền:
[RESEARCH_STATE](RESEARCH_STATE.md) mục 3; closest work:
[LITERATURE](LITERATURE.md).

## 1. Tiêu chí (owner, 2026-11-05)

- Bài là một framework cho setup federated: teacher KD trên public ở server,
  dữ liệu private ở client. FL là bối cảnh, không phải vấn đề cần giải. Với
  split hiện tại, khoảng cách FedAvg - centralized nhỏ trên Spider test
  (`central` - FedAvg -0.42) nhưng còn trên Spider dev (+3.77 ở cùng số pass).
- RL không cần là cơ chế mới. Áp RL đã có vào framework để EX vượt rõ các
  baseline.
- Vai trò của teacher và của RL đều phải đo được. Chỉ bỏ CoT hoặc teacher
  khi bằng chứng cho thấy chúng không giúp.

## 2. Literature: tổ hợp này đã có ai làm chưa

Theo các đợt search 2026-11-01 và 2026-11-05, cộng một lượt search độc lập
(đọc abstract và trích đoạn, không phải systematic review):

| Tổ hợp | Có chưa | Bài gần nhất |
|---|---|---|
| Federated Text-to-SQL | Có, nhưng không teacher, không RL | Zhang et al., ACL 2023 |
| Federated + RL hoặc DPO + Text-to-SQL | Chưa thấy | |
| Federated DPO (task khác) | Có | FedPDPO, OpenFedLLM (FedDPO), POPri (ICML 2025) |
| Federated RLVR (toán, code, y tế) | Có, không teacher | FedMOA, PubSwap (ICML 2026), Fed-GRPO |
| FL với server LLM KD vào SLM trên public | Có, task chung | FedCoLLM, FedMKT, FedCoT, KnowledgeSG |
| DPO hoặc RL Text-to-SQL, centralized | Nhiều | ExCoT, Liu et al. (ACL 2025), AutoThinkSQL, SLM-SQL, Arctic-R1 |

Tổ hợp "teacher KD ở server trên public, RL bằng execution tại client trên
private, FedAvg, cho Text-to-SQL" chưa thấy bài nào. Theo novelty bar
(AGENTS.md), áp cơ chế đã có vào federated Text-to-SQL kèm adaptation riêng
của task là đủ cho Q3. Diễn đạt phải nêu closest work, không claim "first".
Về thuật toán, phần FL của P là FedDPO (OpenFedLLM) áp vào Text-to-SQL với
pair theo execution; bài phải nói rõ như vậy.

## 3. KD public/private có phải hướng hợp lý không

Có. Đây là mẫu chuẩn của nhóm FedCoLLM và FedMKT, và khớp ràng buộc teacher
chỉ ở server. Cần tách hai phần:

- Stage server trên BIRD làm SLM federated tốt hơn (K1, +4.16 Spider dev).
  Phần này gộp dữ liệu public với teacher: chỉ gold BIRD đã cho `gold_k2aaa`
  - FedAvg +1.53 Spider test.
- Phần riêng của teacher (soft label so với gold): +2.13 Spider dev (K2)
  nhưng +0.47 Spider test (K3), 1 seed. Trên BIRD dev phần riêng của teacher
  lớn và chắc hơn: replay teacher - replay gold +4.04 (p<.001, K4).

Nghĩa là teacher đo được rõ nhất trên BIRD, còn trên Spider thì nhỏ.

## 4. CoT có mặc định tốt với setup này không

Literature chia hai phía:

- **Ủng hộ CoT:** Liu et al. (ACL 2025): trên BIRD, với 10 model 6.7B-15B, DPO
  không có CoT thường không giúp hoặc làm giảm EX; CoT tổng hợp giúp DPO hiệu
  quả. OmniSQL: CoT hơn SQL-only ở 7B. RetrySQL: gain lớn trên BIRD với gold
  schema links.
- **Không ủng hộ:** ExCoT: ở 70B, SFT SQL-only hơn CoT trên cả Spider và BIRD.
  AutoThinkSQL: model nên tự học khi nào cần reasoning.

Kết quả của ta (1.5B, Spider, greedy) nghiêng về phía không ủng hộ. Điều kiện
khác Liu et al. (có NLL, 1.5B, Spider), nên đây không phải mâu thuẫn trực tiếp:

- SQL-only DPO + NLL hiệu quả: `s1` +15.38 dev. Chính preference term tạo
  gain: `g3d` - `g3n` +2.22 (p=.004).
- CoT thua SQL sau SFT (khoảng -10) và sau RL (`c1_rl8` - `s1_rl9` -3.29,
  p=.014, dev). Phép so sau RL chưa tách riêng CoT: hai route xuất phát từ dữ
  liệu khác nhau (1,266 dòng CoT của teacher so với 9,428 dòng gold).

Vậy chưa có bằng chứng CoT giúp ở setup này. Chỗ chưa kiểm: BIRD dev, nơi
các paper ủng hộ CoT báo gain.

## 5. Các hướng và review độc lập

Một agent đóng vai reviewer ở các venue mục 7 đã đọc các file notes, không
biết nội dung trao đổi trước đó, và đánh giá từng hướng (2026-11-05). Xác
suất dưới đây là ước lượng thô của reviewer, giả định các thí nghiệm ra như
bằng chứng hiện có gợi ý.

**Một quan sát chung:** RL nén khoảng cách giữa các điểm xuất phát.
`sql2_e1` hơn `sql1_e2` 14.80 điểm, sau RL chỉ còn 1.35 (`sql_rl9` -
`s1_rl9`). `tp1` thua `g1` 2.61, sau RL còn 1.35. Hinton K2 hơn gold K2 khoảng
3.2 dev, nên sau RL phần chênh trên Spider nhiều khả năng dưới 1 điểm.

| Hướng | Nội dung | Reviewer đánh giá | Khả năng Q3 |
|---|---|---|---|
| P | Hinton KD ở server, rồi federated execution DPO + NLL, báo Spider | Major revision; nghiêng reject nếu margin teacher tan, vì teacher chỉ còn là initializer thay được bằng gold | khoảng 35%; 55% nếu Hinton - gold sau RL ≥ +1 Spider test gộp 3 seed; 20-25% nếu < 0.5 |
| **P hai miền** | P, báo Spider và BIRD dev; teacher đo ở BIRD, RL đo ở Spider | Mạnh nhất nếu federated DPO giữ được phần BIRD mà các round SFT bào mòn (K4: 43.61 xuống 36.77) | khoảng 50% |
| Q | Teacher giải câu BIRD student sai hết, làm chosen cho DPO | Đứng riêng: reject hoặc major; SQL đúng của teacher và gold tương đương về ngữ nghĩa | 20%; P+Q khoảng 40% |
| R | CoT làm trục chính | Reject với số hiện có (C1, C2, chi phí 2.5-4 lần) | 10-15%; giữ làm một arm hoặc mục phân tích |
| D | CoT làm explorer cho câu toàn sai, deploy SQL | Ý có cơ chế riêng nhất, nhưng baseline "gold làm chosen" rất mạnh vì client có gold | 25%; P+D 40%, khó xong trong 3-4 tuần |

**Điểm yếu lớn nhất (reviewer):** hai hiệu ứng lớn không cần teacher 7B: RL
(+15 dev) và dữ liệu public (+1.53 test với gold). Phần riêng của teacher
trên Spider là +0.47 test, 1 seed, không có ý nghĩa thống kê, trong khi
teacher zero-shot (77.22 test) hơn mọi student. Con số này làm hỏng bài nếu
headline là teacher trên Spider; không làm hỏng nếu teacher được đo trên
BIRD, nơi nó có tác dụng thật.

**Một điểm reviewer sẽ hỏi ở P hai miền:** BIRD dev cùng phân phối với public
pool, nên gain BIRD có thể bị đọc là "student đã train trên BIRD". Control
replay gold (cùng câu, cùng số bước) trả lời câu này: phần riêng của teacher
là phần vượt gold.

### Baseline và control cần có

Bắt buộc (reviewer chắc chắn hỏi, hoặc có thể đổi method):

1. P xuất phát từ gold K2, cùng lịch: control quyết định cho teacher.
2. Federated rejection-sampling SFT (chỉ NLL trên SQL đúng tự sinh, bản FL
   của `g3n`): tách preference term khỏi việc train thêm.
3. FedAvg SFT với nhiều round hơn, so ở compute tương đương (RL tốn rollout
   K=8).
4. Centralized P (cận trên).
5. FedCoLLM-style KD lặp mỗi round: đã có seed 1 (Spider test 66.88, dev
   63.73, BIRD dev 43.42; nested `ce51178`), cần seed 0 và 2 cho bảng chính.
6. FedAvg, FedProx, teacher 7B zero-shot, base 1.5B; số đã công bố của model
   1.5B mở (OmniSQL, SLM-SQL) kèm ghi chú chênh protocol.
7. Ba seed cho mọi claim chính, gộp bằng question-clustered test.
8. BIRD dev cho mọi arm của bảng chính; Spider-DK, Realistic, SYN cho arm đã
   chốt.
9. Số hiệu quả: dung lượng LoRA r16 mỗi round, GPU-h rollout mỗi client mỗi
   round, chi phí KD một lần ở server, VRAM và latency của 1.5B so với 7B.
10. Một câu vì sao chọn DPO thay vì GRPO (bộ nhớ A5000; Xiong et al. 2025).

Nên có: local-only RL ở từng client; một split khác (alpha 0.5); DPO với gold
làm chosen trên câu toàn sai (client có gold, nên đây vừa là baseline vừa là
một lựa chọn thiết kế của RL).

## 6. Đề xuất chốt (chờ owner duyệt)

Hướng chính: **P hai miền**. Teacher Hinton KD ở server trên BIRD làm điểm
xuất phát, client chạy federated execution DPO + NLL trên Spider private,
deploy SQL-only. Spider EX đo vai trò của RL; BIRD dev đo vai trò của teacher.
Q chỉ thêm vào nếu bước 1 cho thấy teacher không còn phần riêng ở cả hai miền.
CoT giữ làm một arm phân tích (R), không làm trục chính. Đổi metric mang câu
chuyện sang Spider + BIRD là quyết định của owner (AGENTS.md).

Thứ tự thí nghiệm. Mỗi bước có điểm quyết định; GPU-h là ước lượng.

| Bước | Thí nghiệm | GPU-h | Quyết định |
|---|---|---:|---|
| 0 | Spider test cho `s1_rl9`, `sql_rl9`, `sql2_e1`; BIRD dev cho `sql1_e2`, `sql2_e1`, `s1_rl9`, `sql_rl9`, `c1_rl8` | < 8 | RL trên Spider có giữ BIRD không; gain RL có còn trên test không |
| 1 | Centralized: route `s1` từ Hinton K2 và từ đúng adapter gold K2 (không dùng `sql1_e2` làm proxy), hai GPU song song | khoảng 25 | Hinton - gold ≥ +1 Spider (dev và test): P như cũ. Spider < 0.5 nhưng BIRD ≥ +3: P hai miền. Cả hai tan: P không đạt mục tiêu, thử Q một round có control gold-chosen |
| 2 | Pilot FL: một round FedDPO | khoảng 8 | Chi phí rollout (Q5), số pair theo client (Q4) |
| 3 | Các arm FL seed 0: P-Hinton, P-gold, rejection-SFT (FedAvg SFT đã có) | khoảng 50 | Bảng chính seed 0 |
| 4 | Seed 1-2 cho P-Hinton, P-gold, FedAvg, rejection-SFT, gồm K2 còn thiếu | khoảng 130 | Claim chính |
| 5 | Eval đầy đủ các arm đã chốt | khoảng 20 | |
| 6 | Tùy chọn: split alpha 0.5 cho P và FedAvg | khoảng 30 | |

Tổng khoảng 250-300 GPU-h, vừa 3-4 tuần trên hai A5000. Bước 0 không cần
code mới ngoài việc mở rộng script eval; bước 1 cần một runner nhận adapter
xuất phát làm tham số.

## 7. Venue

Data & Knowledge Engineering, International Journal of Data Science and
Analytics, Neural Processing Letters, Distributed and Parallel Databases;
stretch: Journal of Intelligent Information Systems.

## Phụ lục: vị trí KD (đánh giá 2026-11-05)

Giữ KD ở đầu (K2 rồi các round RL).

| Lịch | Kết quả cũ | Paper ủng hộ |
|---|---|---|
| KD trước (K2AAA) | Coder-1.5B: teacher - gold +2.13 dev (p=.020), Spider test các arm K2 72.6-73.9; 0.5B: Spider cao nhất (63.93) | Gián tiếp: khởi tạo pretrained trước FL giảm ảnh hưởng của heterogeneity (Nguyen et al. ICLR 2023); public pretraining và distillation từ LLM trước private FL (Wang et al. 2023, arXiv 2305.12132); warm-up trên shared data (Zhao et al. 2018). Distill rồi RL: ExCoT, SLM-SQL; Think2SQL lẫn lộn (3B BIRD: RL 50.0, SFT + RL 48.2). P2.59: SFT rồi RL hơn RL alone +3.00 |
| Một round FedAvg rồi KD (AK2AA) | 0.5B: Spider 63.15, teacher - gold +1.35 (p=.19), yếu nhất trong ba lịch | Không thấy paper nào dùng đúng lịch này |
| KD xen kẽ hoặc sau mỗi FedAvg (AKAKA, FedCoLLM-style) | 0.5B: BIRD edge của teacher chỉ rõ ở đây (+3.13); Coder-1.5B: Spider edge mất khi round cuối plain (+0.39, p=.76); kết thúc bằng K giữ BIRD nhưng mất khoảng 8 Spider (FedCoLLM-style seed 1: method - nó +7.69 test) | Trực tiếp với teacher trong FL: FedCoLLM, FedMKT (KD lặp mỗi round); FedDF (NeurIPS 2020, ensemble distillation sau mỗi aggregation) |

KD sau mỗi round chỉ có lợi cho BIRD, mà phần đó replay giữ được rẻ hơn.
Một ablation lịch đáng làm: K2 rồi A rồi RL, so với K2 rồi RL.
