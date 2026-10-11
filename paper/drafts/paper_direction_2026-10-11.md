# Hướng paper FedLS-SQL từ 11/10/2026

Hướng đã chốt (owner, 11/10/2026, sau P2.29): **hướng B, miền private là chính**. Paper framework,
xác nhận bằng 3 seed trên Spider test. Luật: R12 trong [LAB_LOG](../notes/LAB_LOG.md) (cùng R7-R11).
Hướng A (co-primary, v1 có NTD làm method) được thay; kết quả theo luật cũ vẫn giữ nguyên trong LAB_LOG.
Lệnh chạy nằm trong [PIPELINE_NEXT](../notes/PIPELINE_NEXT.md).

## 1. Paper nói gì

Teacher LLM frozen ở server, distill trên public pool **khác miền** (BIRD), làm SLM federated tốt hơn
**trên chính miền private của client** (Spider), ngoài việc phục vụ thêm miền public. FL một mình
thiếu ở câu multi-table JOIN (so cùng số pass, 0.5B: thua central 10-12 điểm JOIN); teacher bù đúng
nhóm này (+5 đến +9 JOIN so với gold). Chỉ LoRA adapter rời client; teacher chỉ ở server; chỉ SLM
được deploy.

Tính mới nằm ở thiết kế và phát hiện, không ở một loss mới:

- LLM chỉ ở server, client chỉ chạy SLM, chỉ adapter đi qua lại; public pool khác miền.
- Phát hiện: KD từ teacher trên miền public cải thiện miền private, vượt gold cùng chuỗi.
- Cơ chế: KD làm miền private bị quên ít hơn gold CE trong stage K; gain nằm ở câu JOIN.
- Round private cuối là núm chỉnh Spider-BIRD (plain hay NTD); báo cả đường trade-off.

| | Claim (R12, gộp seed 0-2, Spider test + BIRD dev) | Seed 0, dev (sinh giả thuyết) | Ước lượng |
|---|---|---|---|
| P | Method (`h_plain`) hơn FL `A>A>A` | Spider +4.16 (p=.0002), BIRD +14.28 | khoảng 90% |
| T | Method hơn gold cùng chuỗi (`g_plain`) | chờ P2.36; trước đó: +2.42 (0.5B), +2.03 (1.5B-Instruct), đều p<.05 | 65-75% |
| D | Method hơn K-first kiểu GPT-FL cùng budget (R11) | chưa chạy; 0.5B: không cặp lịch nào p<.1 | 30-40% |

Báo kèm, không claim: nhánh NTD (v1) của cả Hinton lẫn gold, Spider-BIRD plot mọi arm, bộ Spider dev,
R8 (JOIN), R9 (penalty FL theo số pass), `central`, `central_mix`.

Search 10/2026 không thấy công trình federated Text-to-SQL nào có teacher LLM ở server. Tiền lệ
gần nhất là Federated Semantic Parsing (ACL 2023), không có teacher và không có public pool; xem
[RELATED_WORK_NOVELTY_MATRIX](../notes/RELATED_WORK_NOVELTY_MATRIX.md).

## 2. Method

Chuỗi chung theo objective: `A > K > A[ntd] > K`, rồi round private cuối rẽ hai nhánh:

- **plain A** (method, điểm Spider): `h_plain` với Hinton, `g_plain` với gold;
- **A[ntd]** (điểm BIRD): v1 Hinton, gold v1.

K = Hinton KD (0.5 CE + 0.5 forward KL, T=2) từ teacher Coder-7B frozen trên 9,428 câu BIRD train.
Student Qwen2.5-Coder-1.5B-Instruct, 5 client theo split domain-cluster α=0.1. Seed 0, dev: `h_plain`
71.76 / 39.96, v1 69.25 / 43.29 (Spider / BIRD).

## 3. Bằng chứng nền (đã kiểm lại từ predictions đã publish)

P2.27, model cuối (A3), seed 0:

| Arm | Spider | Realistic | Syn | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| base | 59.19 | 46.26 | 45.94 | 47.66 | 21.32 |
| FL A>A>A | 67.60 | 59.65 | 53.68 | 53.27 | 25.68 |
| FedNTD | 67.79 | 57.09 | 53.38 | 51.96 | 24.32 |
| gold v1 | 67.89 | 59.06 | 55.61 | 52.90 | 41.40 |
| Hinton v1 | 69.25 | 60.83 | 56.38 | 57.57 | 43.29 |
| teacher Coder-7B zero-shot | 76.69 | | | | 47.07 |

Luật P2.27 (cố định 10/10): `server_kd` pass; `teacher` fail (Spider +1.35, p=.23);
`server_kd_spider_gain` fail (p=.26). Ghi đúng như vậy.

**FL có mạnh nhờ cách chia data không** (audit 11/10, LAB_LOG):

- Split α=0.1 lệch domain thật, nhưng là setting nhẹ cho FL: 5 client, đủ người mỗi round,
  1 local epoch, cỡ client chênh tối đa 1.9 lần. Mỗi client vẫn chứa mẫu SQL của 66-78% câu dev.
- So ở cùng số lần đi qua dữ liệu (0.5B, α=0.5), central hơn FL +4.6 (E1-A1) và +4.8 (E2-A2),
  đều p=.001; ở E3-A3 chỉ +1.8 vì central đã overfit. Phần thua nằm ở câu JOIN và extra-hard.
- Nguyên nhân có khả năng nhất: FL có ít optimizer step hiệu dụng hơn, không phải client drift
  (FedNTD, FedProx không giúp).
- Trong paper: báo penalty ở cùng số pass (R9), không chỉ ở checkpoint cuối, và nói rõ setting là
  cross-silo nhẹ. Đây là limitation, không phải điểm yếu cần giấu.

## 4. Kế hoạch thí nghiệm

| ID | Việc | Chi phí ước tính | Luật |
|---|---|---|---|
| P2.29 | `h_plain`: từ Hinton v1 K2, một A3 plain | **xong**: giữ NTD theo R1; thành method branch của B | R1 |
| P2.36 | `g_plain`: từ gold v1 K2, một A3 plain (gold matched của method) | khoảng 2.6 h, GPU1 | R12 (seed 0 mô tả) |
| P2.27 publish | `central` xong thì publish, đọc R3 và R9 | không GPU | R3, R9 |
| P2.31 | Seed 1, 2: FL, chuỗi gold và Hinton `A>K>A[ntd]>K` rẽ 2 nhánh cuối (plain, NTD), central | khoảng 2 × 25 h wall clock trên 2 GPU | R12, R8 |
| P2.35 | Baseline K-first kiểu GPT-FL: `hinton_k2aaa` (K hai epoch từ base, rồi 3 round FedAvg), seed 0-2 | khoảng 12 h mỗi seed | R11, R12 (claim D) |
| Spider test | Eval Spider test (2,147 câu) cho model cuối của mọi arm R12 (cả hai nhánh), `hinton_k2aaa` và `central`, seed 0-2 | khoảng 0.5 h mỗi arm mỗi seed | R10 |
| P2.32 | α=0.5 ở 1.5B: FL, gold, Hinton, central, seed 0 | khoảng 20 h | mô tả |
| P2.33 | `central_mix` (Spider+BIRD) ở 1.5B làm ceiling | khoảng 7-10 h | tham chiếu |
| A2 | Test-suite EX cho Spider dev (Zhong et al., EMNLP 2020) | **seed 0 xong**: mọi contrast giữ dấu và độ lớn; chạy lại khi có seed 1-2 | mô tả |
| A3 | Lỗi theo loại SQL, độ khó BIRD | CPU | mô tả |
| A4 | Bảng chi phí: bytes truyền mỗi round, compute client, GPU-h server, so với không FL | CPU | mô tả |

Thứ tự GPU: `central` (GPU0) và P2.36 (GPU1); sau đó P2.31 trên cả hai GPU, rồi P2.35, P2.32 và
P2.33. Tổng khoảng 155 GPU-h, khoảng 1.5 tuần trên 2 GPU.

**Tập xác nhận (R10):** Spider dev và các bộ sinh từ dev (Realistic, SYN, DK) đã dùng để chọn mọi
thiết kế, nên chỉ là validation. Claim cuối về Spider đọc trên Spider test (2,147 câu, 40 DB riêng,
public từ 02/2024, OmniSQL cũng dùng). BIRD vẫn là BIRD dev vì BIRD test bị ẩn.

Tùy chọn cuối, nếu còn GPU: execution voting lúc deploy (P2.28 cho +7 trên câu train). Chỉ là
phần bổ sung lúc inference, không phải đóng góp chính.

## 5. Các hướng đã cân nhắc và không chọn (11/10)

- **ExST (proposal v2):** churn A1 không ủng hộ "round private xóa phần riêng của teacher" (R2),
  nên không thể thành method chính (R5). S1 bỏ khỏi hàng đợi.
- **Execution-gated KD (S2):** không có nguồn trực tiếp, lợi ích dự kiến nhỏ; bỏ.
- **Nghiên cứu method vòng 2** (hai reviewer độc lập, hai vòng, chỉ CPU). Ứng viên tốt nhất: K trên
  BIRD cộng row SQL tổng hợp (SynSQL-2.5M) được chọn theo excess loss của student federated. Ước
  lượng khoảng 18% qua screen central, khoảng 5% đạt đủ tiêu chí synergy, khoảng 53 GPU-h. Owner
  không chọn vì xác suất quá thấp.
- **Bị loại vì bằng chứng:** private-aware KL weighting, schema-perturbation KD, schema-token KD
  (teacher không hơn gold ở chọn bảng), dual adapter, LwF trong K (hiệu ứng retention còn khoảng
  7% sau round private, P2.24).

## 6. Cách đọc khác và điều có thể làm hướng B sai

- **Gain Spider của method so với FL chỉ do thêm bước train** (2 epoch K): claim T (gold cùng
  chuỗi) và D (K-first cùng budget) tách phần teacher và phần lịch khỏi phần compute.
- **T không đạt khi gộp 3 seed:** paper đứng trên P (gain miền private so với FL) cộng DK và cơ chế
  C3; chữ "Novel" khi đó yếu hơn, đổi tên là quyết định của owner.
- **BIRD của method thấp hơn nhánh NTD** (39.96 so với 43.29 ở seed 0): paper báo cả hai nhánh như
  hai điểm làm việc, không giấu nhánh NTD.
- **R8 không ủng hộ JOIN:** bỏ phân tích JOIN khỏi claim, chỉ giữ như mô tả seed 0.
- **Reviewer nói train trên BIRD thì BIRD tăng:** đúng, gold public cũng cho +15.7; vì vậy B đặt
  claim chính vào Spider, BIRD chỉ cần không tệ hơn đối chứng.
- **Lịch xen kẽ AKAKA chưa từng được chứng minh tốt hơn K-first** (grid 0.5B, không cặp nào
  p<.1). R11 kiểm tra ở 1.5B; nếu không qua, AKAKA chỉ là lựa chọn thiết kế.
- **Reviewer nói phần federated là phụ:** trả lời bằng R9 (penalty ở cùng số pass) và nói rõ
  setting cross-silo; không claim synergy với federation.
- **Chỉ có họ Qwen:** ghi là limitation.

## 7. Việc cần làm

1. P2.36 (`g_plain`) trên GPU1; sau `central`: publish P2.27, đọc R3 và R9.
2. Viết runner P2.31 (chuỗi chung, rẽ 2 nhánh cuối, có eval Spider test), eval Spider test cho seed 0,
   và runner P2.35; đưa lệnh vào PIPELINE_NEXT.
3. A2, A3, A4 (CPU) bất cứ lúc nào.
4. Sau P2.31 và P2.35: đọc R12 và R8, viết bảng chính của paper.

Nguồn:
[Federated Semantic Parsing](https://aclanthology.org/2023.acl-long.678/),
[FedNLP](https://arxiv.org/abs/2104.08815),
[Nguyen et al., ICLR 2023](https://arxiv.org/abs/2210.08090),
[test-suite accuracy](https://aclanthology.org/2020.emnlp-main.29/),
[OmniSQL / SynSQL-2.5M](https://arxiv.org/abs/2503.02240),
[GPT-FL](https://arxiv.org/abs/2306.02210),
[Spider (test set release)](https://yale-lily.github.io/spider),
[PubSwap](https://arxiv.org/abs/2604.12160),
[FedMOA](https://arxiv.org/abs/2602.00453).
