# Hướng paper FedLS-SQL từ 11/10/2026

Hướng đã chốt (owner, 11/10/2026): **hướng A, paper framework** trên method v1, xác nhận bằng 3
seed. Không thêm method mới. Screen S1 (ExST) và S2 (execution-gated KD) bỏ khỏi hàng đợi. Proposal
v2 ([method_v2_proposal_2026-10-11.md](method_v2_proposal_2026-10-11.md)) chỉ còn là lịch sử.

Luật đọc kết quả ở file này là bản tóm tắt. Bản gốc, cố định trước khi có kết quả, nằm trong
[LAB_LOG](../notes/LAB_LOG.md) mục 2026-10-11 (R1-R11). Lệnh chạy nằm trong
[PIPELINE_NEXT](../notes/PIPELINE_NEXT.md).

## 1. Paper nói gì

Một SLM 1.5B train federated trên dữ liệu Text-to-SQL private của các client, cộng với teacher
LLM frozen ở server trên public data khác miền, phục vụ được cả miền private (Spider) lẫn miền public
(BIRD). Chỉ LoRA adapter rời client; teacher chỉ ở server; chỉ SLM được deploy.

Novelty nằm ở thiết kế framework cho NL2SQL, không ở một loss mới:

- LLM chỉ ở server, client chỉ chạy SLM, chỉ adapter đi qua lại.
- Public pool khác miền với private (BIRD so với Spider), đánh giá cả hai miền là co-primary bằng EX.
- Lịch xen kẽ round private và stage KD (AKAKA), có phân tích lịch.
- Cơ chế: KD làm miền private bị quên ít hơn gold CE trong stage public.

Search 10/2026 không thấy công trình federated Text-to-SQL nào có teacher LLM ở server. Tiền lệ
gần nhất là Federated Semantic Parsing (ACL 2023), không có teacher và không có public pool. Các
thành phần (FedAvg LoRA, server KD) đều đã có; xem
[RELATED_WORK_NOVELTY_MATRIX](../notes/RELATED_WORK_NOVELTY_MATRIX.md).

| | Đóng góp | Bằng chứng đến 11/10 (seed 0) | Còn thiếu |
|---|---|---|---|
| C1 | Một SLM phục vụ cả hai miền (claim framework), so với FL và baseline K-first (R11) | Hinton v1 − FedNTD: BIRD +18.97 (p<.001), Spider Wald lower −0.89; pass luật `server_kd`. So với FL: BIRD +17.6, Spider +1.65 | Gộp 3 seed (R7) |
| C2 | Teacher hơn public gold | P2.27: BIRD +1.89 (p=.076), Spider +1.35 (ns), DK +4.67 (p<.001). Spider cùng chiều ở P2.17, P2.18, P2.25 (+2.03, +2.42, +3.77) | Gộp 3 seed (R7); tiêu chí cần BIRD p<.05 và Spider non-inferior, nên BIRD là điểm quyết định |
| C3 | Cơ chế: Hinton KD làm miền private bị quên ít hơn gold CE trong stage K | Sau K: Spider +3.48 (K1, p=.002), +3.00 (K2, p=.013); churn A1 ủng hộ | Seed 1, 2 |
| C4 | Phân tích: heterogeneity, scale, loại SQL, chi phí | α=0.1, 0.5B và 1.5B; audit split (mục 3) | α=0.5 ở 1.5B, `central`, `central_mix`, R8, R9, bảng chi phí |

Bốn số Spider của C2 dùng chung test set nên không gộp được như bằng chứng độc lập; chỉ nói được
là hướng hiệu ứng nhất quán. Kiểm định gộp (R7) chỉ dùng 3 seed của P2.27.

Ước lượng của tôi (không phải luật): C1 gần như chắc giữ được; C2 đạt khi gộp 3 seed khoảng
55-65%.

## 2. Method

FedLS-SQL = các round private FedAvg LoRA ở client, xen kẽ stage K ở server: Hinton KD
(0.5 CE + 0.5 forward KL, T=2) từ teacher Coder-7B frozen trên 9,428 câu BIRD train. Schedule
AKAKA. Student Qwen2.5-Coder-1.5B-Instruct, 5 client theo split domain-cluster α=0.1.

Có giữ FedNTD ở round private hay không do P2.29 quyết (luật R1). Ở 1.5B, FedNTD so với FL
không giúp Spider (+0.19) và làm BIRD giảm (−1.37, p=.044). Nếu bỏ NTD, method là Hinton AKAKA và
FedNTD chỉ còn là baseline.

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
| P2.29 | `h_plain`: từ Hinton v1 K2, một A3 plain | đang chạy GPU1 | R1 |
| P2.27 publish | `central` xong thì publish, đọc R3 và R9 | không GPU | R3, R9 |
| P2.31 | Seed 1, 2 cho FL, FedNTD, gold, Hinton (NTD theo R1), central | khoảng 2 × 25 h wall clock trên 2 GPU | R7, R8 |
| P2.35 | Baseline K-first kiểu GPT-FL: `hinton_k2aaa` (K hai epoch từ base, rồi 3 round FedAvg), seed 0-2 | khoảng 12 h mỗi seed | R11 |
| Spider test | Eval Spider test (2,147 câu) cho model cuối của các arm R7/R11 và `central`, seed 0-2 | khoảng 0.5 h mỗi arm mỗi seed | R10 |
| P2.32 | α=0.5 ở 1.5B: FL, gold, Hinton, central, seed 0 | khoảng 20 h | mô tả |
| P2.33 | `central_mix` (Spider+BIRD) ở 1.5B làm ceiling | khoảng 7-10 h | tham chiếu |
| A2 | Test-suite EX cho Spider (Zhong et al., EMNLP 2020) | CPU | mô tả |
| A3 | Lỗi theo loại SQL, độ khó BIRD | CPU | mô tả |
| A4 | Bảng chi phí: bytes truyền mỗi round, compute client, GPU-h server, so với không FL | CPU | mô tả |

Thứ tự GPU: P2.29 và `central` đang chạy; sau đó P2.31 trên cả hai GPU, rồi P2.35, P2.32 và
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

## 6. Cách đọc khác và điều có thể làm hướng A sai

- **Student 1.5B đã gần trần của teacher và pool này** (Hinton − FL Spider +1.65, ns): paper đặt
  trọng tâm vào BIRD và robustness, không hứa Spider gain.
- **Gộp 3 seed, BIRD teacher − gold không đạt p<.05:** C2 thu hẹp còn DK và C3; paper đứng trên
  C1. Khi đó chữ "Novel" trong tiêu đề hơi mạnh so với bằng chứng; đổi tên là quyết định của owner.
- **R8 không ủng hộ JOIN:** bỏ phân tích JOIN khỏi claim, chỉ giữ như mô tả seed 0.
- **Reviewer nói train trên BIRD thì BIRD tăng:** đúng, gold public cũng cho +15.7. Vì vậy C1
  luôn đi cùng gold control và `central_mix`; phần riêng của teacher là C2/C3.
- **Lịch xen kẽ AKAKA chưa từng được chứng minh tốt hơn K-first** (grid 0.5B, không cặp nào
  p<.1). R11 kiểm tra ở 1.5B; nếu không qua, AKAKA chỉ là lựa chọn thiết kế.
- **Reviewer nói phần federated là phụ:** trả lời bằng R9 (penalty ở cùng số pass) và nói rõ
  setting cross-silo; không claim synergy với federation.
- **Chỉ có họ Qwen:** ghi là limitation.

## 7. Việc cần làm

1. Đợi P2.29 xong: đọc R1, cố định method.
2. Sau `central`: publish P2.27, đọc R3 và R9.
3. Viết runner P2.31 (có eval Spider test) theo kết quả R1, eval Spider test cho seed 0, và runner
   P2.35; đưa lệnh vào PIPELINE_NEXT.
4. A2, A3, A4 (CPU) bất cứ lúc nào.
5. Sau P2.31: đọc R7 và R8, viết bảng chính của paper.

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
